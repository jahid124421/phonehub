#!/usr/bin/env python3
"""
PhoneHub pipeline — STAGE 2: AI content agent
========================================================================
Reads data/specs.json and generates ORIGINAL editorial for each phone:
pros, cons, a short review, a rating and a popularity score. This is what
makes your site legally yours and safe to rank on Google (no copied text).

Results are cached in data/content.json keyed by phone id, so the LLM only
writes each phone once (saves tokens/cost). Use --force to regenerate.

USAGE:
    python content_agent.py
    python content_agent.py --force
    python content_agent.py --limit 5      # only process N new phones this run

Uses your existing keys (from the env file set in config.json > llm.keys_env_path).
Default provider: groq. Stdlib only.
========================================================================
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

import ph_common as C

# provider -> (endpoint, env key name). All OpenAI-compatible except gemini.
PROVIDERS = {
    "groq":       ("https://api.groq.com/openai/v1/chat/completions", "GROQ_API_KEY"),
    "openrouter": ("https://openrouter.ai/api/v1/chat/completions", "OPENROUTER_API_KEY"),
    "together":   ("https://api.together.xyz/v1/chat/completions", "TOGETHER_API_KEY"),
    "cerebras":   ("https://api.cerebras.ai/v1/chat/completions", "CEREBRAS_API_KEY"),
    "gemini":     ("https://generativelanguage.googleapis.com/v1beta/models", "GEMINI_API_KEY"),
}

SYSTEM = (
    "You are a mobile phone reviewer. Given a phone's specifications, write a "
    "concise, ORIGINAL, factual assessment. Never copy marketing copy or other "
    "reviews. Base everything on the specs provided. Respond ONLY with JSON."
)

USER_TMPL = """Phone: {name}
Brand: {brand}
Key specs:
{specs}

Return JSON with exactly these fields:
{{
  "review": "2-3 original sentences summarizing who this phone is for",
  "pros": ["3 to 5 short pros"],
  "cons": ["2 to 4 short cons"],
  "rating": 4.3,          // number between 3.4 and 4.9, one decimal
  "popularity": 78         // integer 40-99 reflecting mainstream appeal
}}"""


def http_post_json(url, headers, body, retries=3):
    data = json.dumps(body).encode("utf-8")
    last = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:  # show the server's reason
            body = ""
            try:
                body = e.read().decode("utf-8")[:300]
            except Exception:  # noqa
                pass
            last = f"HTTP {e.code}: {body or e.reason}"
            if e.code in (401, 403):  # auth errors won't fix on retry
                break
            time.sleep(2 * (attempt + 1))
        except Exception as e:  # noqa
            last = e
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"POST {url} failed: {last}")


def extract_json(text):
    text = text.strip()
    text = re.sub(r"^```(json)?|```$", "", text, flags=re.MULTILINE).strip()
    m = re.search(r"\{.*\}", text, re.DOTALL)
    return json.loads(m.group(0)) if m else json.loads(text)


def call_llm(provider, model, key, prompt):
    endpoint, _ = PROVIDERS[provider]
    if provider == "gemini":
        url = f"{endpoint}/{model}:generateContent?key={key}"
        body = {
            "contents": [{"parts": [{"text": SYSTEM + "\n\n" + prompt}]}],
            "generationConfig": {"temperature": 0.6, "responseMimeType": "application/json"},
        }
        res = http_post_json(url, {"Content-Type": "application/json"}, body)
        text = res["candidates"][0]["content"]["parts"][0]["text"]
        return extract_json(text)
    # OpenAI-compatible
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
        "temperature": 0.6,
        "response_format": {"type": "json_object"},
    }
    res = http_post_json(url=endpoint, headers=headers, body=body)
    return extract_json(res["choices"][0]["message"]["content"])


def specs_summary(phone):
    q = phone.get("quickSpecs", {})
    lines = [f"- {k}: {v}" for k, v in q.items() if v]
    return "\n".join(lines) or "(specs unavailable)"


def clamp(v, lo, hi, default):
    try:
        v = float(v)
        return max(lo, min(hi, v))
    except Exception:  # noqa
        return default


def main():
    args = sys.argv[1:]
    force = "--force" in args
    limit = None
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])

    cfg = C.load_config()
    llm = cfg.get("llm", {})
    provider = llm.get("provider", "groq").lower()
    model = llm.get("model", "llama-3.3-70b-versatile")
    if provider not in PROVIDERS:
        raise SystemExit(f"Unknown provider '{provider}'. Options: {list(PROVIDERS)}")

    env_path = os.path.join(C.HERE, llm.get("keys_env_path", "../../ai-bots-package/my-keys.env"))
    keys = C.load_env_keys(env_path)
    key_name = PROVIDERS[provider][1]
    key = keys.get(key_name) or os.environ.get(key_name)
    if not key:
        raise SystemExit(f"No {key_name} found in {env_path} or environment.")

    specs = C.read_json("specs.json")
    if not specs:
        raise SystemExit("data/specs.json missing. Run import_specs.py first.")

    cache = C.read_json("content.json", default={})
    phones = specs["phones"]
    todo = [p for p in phones if force or p["id"] not in cache]
    if limit:
        todo = todo[:limit]

    print(f"[content] provider={provider} model={model} | {len(todo)} phones to write "
          f"({len(cache)} cached)")

    done = 0
    for p in todo:
        prompt = USER_TMPL.format(name=p["name"], brand=p.get("brand", ""),
                                  specs=specs_summary(p))
        try:
            out = call_llm(provider, model, key, prompt)
            cache[p["id"]] = {
                "review": str(out.get("review", "")).strip(),
                "pros": [str(x) for x in (out.get("pros") or [])][:5],
                "cons": [str(x) for x in (out.get("cons") or [])][:4],
                "rating": round(clamp(out.get("rating"), 3.4, 4.9, 4.2), 1),
                "popularity": int(clamp(out.get("popularity"), 40, 99, 60)),
            }
            done += 1
            print("  ok " + p["name"].encode("ascii", "replace").decode())
            C.write_json("content.json", cache)  # save incrementally
            time.sleep(0.5)
        except Exception as e:  # noqa
            print(f"  ! {p['name']}: {e}")

    print(f"[content] generated {done}, total cached {len(cache)} -> data/content.json")


if __name__ == "__main__":
    main()

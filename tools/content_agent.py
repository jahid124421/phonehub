#!/usr/bin/env python3
"""
PhoneHub pipeline — STAGE 2: AI content agent
========================================================================
Reads data/specs.json and generates ORIGINAL editorial for each product:
pros, cons, a short review, a rating and a popularity score. This is what
makes your site legally yours and safe to rank on Google (no copied text).

Category-aware: uses different prompts for phones, auto, laptops, TVs, etc.

Results are cached in data/content.json keyed by product id, so the LLM only
writes each product once (saves tokens/cost). Use --force to regenerate.

USAGE:
    python content_agent.py
    python content_agent.py --force
    python content_agent.py --force-category auto     # regenerate only auto products
    python content_agent.py --limit 5      # only process N new products this run

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

# ---------- Category-aware system prompts ----------
CATEGORY_PROMPTS = {
    'phone': "You are an expert mobile phone reviewer. Analyze the specs and provide a concise, insightful review.",
    'auto': "You are an expert automotive reviewer. Analyze the vehicle specs and provide a concise, insightful review about this car/vehicle.",
    'laptop': "You are an expert laptop/computer reviewer. Analyze the specs and provide a concise, insightful review.",
    'tv': "You are an expert TV and display reviewer. Analyze the specs and provide a concise review.",
    'smartwatch': "You are an expert wearable tech reviewer. Analyze the specs and provide a concise review about this smartwatch/wearable.",
    'camera': "You are an expert camera reviewer. Analyze the specs and provide a concise review.",
    'tablet': "You are an expert tablet reviewer. Analyze the specs and provide a concise review.",
    'electronic': "You are an expert electronics reviewer. Analyze the specs and provide a concise review.",
    'appliance': "You are an expert home appliance reviewer. Analyze the specs and provide a concise review.",
    'accessory': "You are an expert tech accessory reviewer. Analyze the specs and provide a concise review.",
    'computer': "You are an expert computer hardware reviewer. Analyze the specs and provide a concise review.",
}
DEFAULT_PROMPT = "You are an expert tech product reviewer. Analyze the specs and provide a concise, insightful review."


def get_system_prompt(category):
    """Return the full system prompt for a given product category."""
    cat = (category or "").lower().strip()
    base = CATEGORY_PROMPTS.get(cat, DEFAULT_PROMPT)
    return (
        f"{base} Given a product's specifications, write a concise, ORIGINAL, "
        "factual assessment. Never copy marketing copy or other reviews. "
        "Base everything on the specs provided. Respond ONLY with JSON."
    )


# ---------- Category-aware spec field hints for the user prompt ----------
CATEGORY_SPEC_HINTS = {
    'phone': 'Focus on: display, processor, RAM, camera, battery, connectivity.',
    'auto': 'Focus on: engine/motor, horsepower, torque, mileage/range, transmission, drivetrain, safety.',
    'laptop': 'Focus on: display, processor, RAM, storage, GPU, battery life, weight.',
    'tv': 'Focus on: screen size, resolution, panel type (OLED/QLED/LED), refresh rate, HDR, smart features.',
    'smartwatch': 'Focus on: display, health sensors, battery life, water resistance, OS compatibility.',
    'camera': 'Focus on: sensor size, megapixels, lens aperture, ISO range, video capabilities.',
    'tablet': 'Focus on: display, processor, RAM, storage, stylus support, battery.',
    'electronic': 'Focus on: key specs, connectivity, battery, build quality.',
    'appliance': 'Focus on: capacity, energy rating, key features, noise level.',
    'accessory': 'Focus on: compatibility, build quality, key features.',
    'computer': 'Focus on: CPU, GPU, RAM, storage, form factor, connectivity.',
}
DEFAULT_SPEC_HINT = 'Focus on the most important specs for this product type.'


USER_TMPL = """Product: {name}
Brand: {brand}
Category: {category}
Key specs:
{specs}

{spec_hint}

Return JSON with exactly these fields:
{{
  "review": "2-3 original sentences summarizing who this product is for and its standout qualities",
  "pros": ["3 to 5 short pros"],
  "cons": ["2 to 4 short cons"],
  "rating": 4.3,          // number between 3.0 and 5.0, one decimal
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


def call_llm(provider, model, key, prompt, system_prompt):
    endpoint, _ = PROVIDERS[provider]
    if provider == "gemini":
        url = f"{endpoint}/{model}:generateContent?key={key}"
        body = {
            "contents": [{"parts": [{"text": system_prompt + "\n\n" + prompt}]}],
            "generationConfig": {"temperature": 0.6, "responseMimeType": "application/json"},
        }
        res = http_post_json(url, {"Content-Type": "application/json"}, body)
        text = res["candidates"][0]["content"]["parts"][0]["text"]
        return extract_json(text)
    # OpenAI-compatible
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system_prompt},
                     {"role": "user", "content": prompt}],
        "temperature": 0.6,
        "response_format": {"type": "json_object"},
    }
    res = http_post_json(url=endpoint, headers=headers, body=body)
    return extract_json(res["choices"][0]["message"]["content"])


def specs_summary(product):
    q = product.get("quickSpecs", {})
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
    force_category = None
    if "--force-category" in args:
        force_category = args[args.index("--force-category") + 1].lower().strip()
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
    keys = C.load_envkeys(env_path)
    key_name = PROVIDERS[provider][1]
    key = keys.get(key_name) or os.environ.get(key_name)
    if not key:
        raise SystemExit(f"No {key_name} found in {env_path} or environment.")

    specs = C.read_json("specs.json")
    if not specs:
        raise SystemExit("data/specs.json missing. Run import_specs.py first.")

    cache = C.read_json("content.json", default={})
    products = specs["phones"]  # key is 'phones' for legacy reasons but contains all categories

    # Filter by category if --force-category is set
    if force_category:
        products = [p for p in products if (p.get("category") or "phone").lower() == force_category]
        todo = [p for p in products if p["id"] not in cache or force]
        print(f"[content] --force-category={force_category}: {len(products)} products found, {len(todo)} to process")
    else:
        todo = [p for p in products if force or p["id"] not in cache]

    if limit:
        todo = todo[:limit]

    # Count by category for logging
    cat_counts = {}
    for p in todo:
        cat = (p.get("category") or "phone").lower()
        cat_counts[cat] = cat_counts.get(cat, 0) + 1
    cat_summary = ", ".join(f"{v} {k}" for k, v in sorted(cat_counts.items()))

    print(f"[content] provider={provider} model={model} | {len(todo)} products to write "
          f"({len(cache)} cached)")
    if cat_summary:
        print(f"[content] categories: {cat_summary}")

    done = 0
    for p in todo:
        category = (p.get("category") or "phone").lower()
        system_prompt = get_system_prompt(category)
        spec_hint = CATEGORY_SPEC_HINTS.get(category, DEFAULT_SPEC_HINT)
        prompt = USER_TMPL.format(
            name=p["name"],
            brand=p.get("brand", ""),
            category=category,
            specs=specs_summary(p),
            spec_hint=spec_hint,
        )
        try:
            out = call_llm(provider, model, key, prompt, system_prompt)
            cache[p["id"]] = {
                "review": str(out.get("review", "")).strip(),
                "pros": [str(x) for x in (out.get("pros") or [])][:5],
                "cons": [str(x) for x in (out.get("cons") or [])][:4],
                "rating": round(clamp(out.get("rating"), 3.0, 5.0, 4.2), 1),
                "popularity": int(clamp(out.get("popularity"), 40, 99, 60)),
            }
            done += 1
            print(f"  ok [{category}] " + p["name"].encode("ascii", "replace").decode())
            C.write_json("content.json", cache)  # save incrementally
            time.sleep(0.5)
        except Exception as e:  # noqa
            print(f"  ! {p['name']}: {e}")

    print(f"[content] generated {done}, total cached {len(cache)} -> data/content.json")


if __name__ == "__main__":
    main()

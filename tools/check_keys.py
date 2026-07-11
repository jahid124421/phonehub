#!/usr/bin/env python3
"""
PhoneHub — LLM key checker
========================================================================
Tests every LLM key in your env file and tells you which ones actually
work, so you know what to put in config.json > llm.provider.

USAGE:
    python check_keys.py
    python check_keys.py --env ../../ai-bots-package/my-keys.env

No specs API needed. Stdlib only.
========================================================================
"""
import json
import sys
import os
import urllib.error
import urllib.request

import ph_common as C

# provider -> (endpoint, env key name, default model)
PROVIDERS = {
    "groq":       ("https://api.groq.com/openai/v1/chat/completions", "GROQ_API_KEY", "llama-3.3-70b-versatile"),
    "openrouter": ("https://openrouter.ai/api/v1/chat/completions", "OPENROUTER_API_KEY", "meta-llama/llama-3.3-70b-instruct"),
    "together":   ("https://api.together.xyz/v1/chat/completions", "TOGETHER_API_KEY", "meta-llama/Llama-3.3-70B-Instruct-Turbo"),
    "cerebras":   ("https://api.cerebras.ai/v1/chat/completions", "CEREBRAS_API_KEY", "llama-3.3-70b"),
    "gemini":     ("https://generativelanguage.googleapis.com/v1beta/models", "GEMINI_API_KEY", "gemini-1.5-flash"),
}


def test_openai_compat(endpoint, key, model):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": "Reply with just: ok"}],
        "max_tokens": 5,
    }).encode("utf-8")
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.loads(r.read().decode("utf-8"))
    return res["choices"][0]["message"]["content"].strip()


def test_gemini(endpoint, key, model):
    url = f"{endpoint}/{model}:generateContent?key={key}"
    body = json.dumps({"contents": [{"parts": [{"text": "Reply with just: ok"}]}]}).encode("utf-8")
    req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.loads(r.read().decode("utf-8"))
    return res["candidates"][0]["content"]["parts"][0]["text"].strip()


def main():
    args = sys.argv[1:]
    env_path = os.path.join(C.HERE, "../../ai-bots-package/my-keys.env")
    if "--env" in args:
        env_path = args[args.index("--env") + 1]
    env_path = os.path.abspath(env_path)

    keys = C.load_env_keys(env_path)
    if not keys:
        print(f"No keys found in {env_path}")
        sys.exit(1)

    print(f"Testing keys from: {env_path}\n")
    working = []
    for provider, (endpoint, key_name, model) in PROVIDERS.items():
        key = keys.get(key_name)
        if not key:
            print(f"  -  {provider:11s} : no {key_name} in env")
            continue
        try:
            if provider == "gemini":
                out = test_gemini(endpoint, key, model)
            else:
                out = test_openai_compat(endpoint, key, model)
            print(f"  OK {provider:11s} : works  (model {model})  ->  \"{out[:40]}\"")
            working.append((provider, model))
        except urllib.error.HTTPError as e:
            reason = ""
            try:
                reason = e.read().decode("utf-8")[:120]
            except Exception:  # noqa
                pass
            print(f"  X  {provider:11s} : HTTP {e.code} {reason}")
        except Exception as e:  # noqa
            print(f"  X  {provider:11s} : {e}")

    print()
    if working:
        p, m = working[0]
        print(f"Use this in config.json:  \"provider\": \"{p}\", \"model\": \"{m}\"")
    else:
        print("No working provider from this machine. If you see HTTP 403 / Cloudflare,")
        print("try a different network, or check that the keys are still valid.")


if __name__ == "__main__":
    main()

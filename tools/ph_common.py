"""Shared helpers for the PhoneHub data pipeline (stdlib only)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(HERE, "data")

BRAND_EMOJI = {
    "apple": "🍎", "samsung": "📱", "google": "🔵", "xiaomi": "🟠",
    "oneplus": "🔴", "nothing": "⚪", "vivo": "🔷", "realme": "🟡",
    "oppo": "🟢", "motorola": "🔶", "asus": "🟣", "sony": "⬛",
}


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def load_config(path=None):
    path = path or os.path.join(HERE, "config.json")
    if not os.path.exists(path):
        raise SystemExit(f"Missing {path}. Copy config.example.json to config.json first.")
    with open(path, "r", encoding="utf-8-sig") as f:
        cfg = json.load(f)
    return {k: v for k, v in cfg.items() if not k.startswith("_")}


def read_json(name, default=None):
    p = os.path.join(DATA_DIR, name)
    if not os.path.exists(p):
        return default
    with open(p, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def write_json(name, obj):
    ensure_data_dir()
    p = os.path.join(DATA_DIR, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    return p


def slugify(text):
    return "".join(c if c.isalnum() else "-" for c in str(text).lower()).strip("-")


# ---------- read data out of js/data.js (JSON or hand-written JS) ----------
def array_text(js_text, var_name):
    """Return the `[ ... ]` substring assigned to window.<var> via bracket matching."""
    idx = js_text.find(f"window.{var_name}")
    if idx == -1:
        return ""
    start = js_text.find("[", idx)
    if start == -1:
        return ""
    depth, i, in_str, esc, quote = 0, start, False, False, ""
    while i < len(js_text):
        ch = js_text[i]
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == quote:
                in_str = False
        else:
            if ch in ('"', "'"):
                in_str, quote = True, ch
            elif ch == "[":
                depth += 1
            elif ch == "]":
                depth -= 1
                if depth == 0:
                    return js_text[start:i + 1]
        i += 1
    return ""


def js_to_json(s):
    """Convert a JS array/object literal (unquoted keys, single quotes) to JSON text."""
    out, i, n = [], 0, len(s)
    while i < n:
        c = s[i]
        if c == '"':
            out.append(c); i += 1
            while i < n:
                out.append(s[i])
                if s[i] == "\\" and i + 1 < n:
                    out.append(s[i + 1]); i += 2; continue
                if s[i] == '"':
                    i += 1; break
                i += 1
            continue
        if c == "'":
            i += 1; buf = []
            while i < n and s[i] != "'":
                if s[i] == "\\" and i + 1 < n:
                    buf.append(s[i + 1]); i += 2; continue
                if s[i] == '"':
                    buf.append('\\"'); i += 1; continue
                buf.append(s[i]); i += 1
            i += 1
            out.append('"' + "".join(buf) + '"')
            continue
        if c.isalpha() or c in "_$":
            j = i
            while j < n and (s[j].isalnum() or s[j] in "_$"):
                j += 1
            word = s[i:j]
            k = j
            while k < n and s[k] in " \t\n\r":
                k += 1
            if k < n and s[k] == ":" and word not in ("true", "false", "null"):
                out.append('"' + word + '"')
            else:
                out.append(word)
            i = j
            continue
        out.append(c); i += 1
    return "".join(out)


def parse_array(js_text, var_name):
    txt = array_text(js_text, var_name)
    if not txt:
        return []
    import json as _json
    return _json.loads(js_to_json(txt))


def load_site_data(datajs_path):
    """Return {'brands':[], 'phones':[], 'news':[]} parsed from a data.js file."""
    with open(datajs_path, "r", encoding="utf-8-sig") as f:
        js = f.read()
    return {
        "brands": parse_array(js, "BRANDS"),
        "phones": parse_array(js, "PHONES"),
        "news": parse_array(js, "NEWS"),
    }


def load_env_keys(env_path):
    """Parse a simple KEY=VALUE .env file into a dict. Ignores comments."""
    keys = {}
    if not env_path or not os.path.exists(env_path):
        return keys
    with open(env_path, "r", encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            keys[k.strip()] = v.strip().strip('"').strip("'")
    return keys

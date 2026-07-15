#!/usr/bin/env python3
"""
PhoneHub pipeline — STAGE 3: prices + affiliate links
========================================================================
Reads data/specs.json and writes data/prices.json:
    { phoneId: { "basePrice": <int|0>, "prices": [ {store, price, url} ] } }

Two modes, automatic:
  1) LINK MODE (default, works immediately, no approval):
     Generates monetized affiliate SEARCH links for each store using your
     partner tag / affiliate id. You earn commission on any resulting sale.
     price is left null -> the site shows "Check price".
  2) PRICE MODE (optional): if Amazon PA-API access+secret keys are present
     in config, fetches the real live price + exact product link via the
     official Product Advertising API (needs an approved Associates account).

USAGE:
    python price_job.py

Stdlib only (PA-API request is signed with hmac/hashlib).
========================================================================
"""
import datetime
import hashlib
import hmac
import json
import sys
import urllib.parse
import urllib.request

import ph_common as C

# Amazon marketplace -> (host, region)
AMZ_HOST = {
    "www.amazon.com": ("webservices.amazon.com", "us-east-1"),
    "www.amazon.in": ("webservices.amazon.in", "eu-west-1"),
    "www.amazon.co.uk": ("webservices.amazon.co.uk", "eu-west-1"),
    "www.amazon.de": ("webservices.amazon.de", "eu-west-1"),
    "www.amazon.ca": ("webservices.amazon.ca", "us-east-1"),
    "www.amazon.com.au": ("webservices.amazon.com.au", "us-west-2"),
}


# ---------------- affiliate link builders (always available) -------------
def amazon_link(name, tag, marketplace):
    q = urllib.parse.quote(name)
    base = "https://" + marketplace.replace("www.", "www.")
    link = f"https://{marketplace}/s?k={q}"
    if tag:
        link += f"&tag={urllib.parse.quote(tag)}"
    return link


def flipkart_link(name, affid):
    q = urllib.parse.quote(name)
    link = f"https://www.flipkart.com/search?q={q}"
    if affid:
        link += f"&affid={urllib.parse.quote(affid)}"
    return link


# ---------------- Amazon PA-API v5 (optional price mode) ----------------
def _sign(key, msg):
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _signature_key(secret, date_stamp, region, service):
    k_date = _sign(("AWS4" + secret).encode("utf-8"), date_stamp)
    k_region = _sign(k_date, region)
    k_service = _sign(k_region, service)
    return _sign(k_service, "aws4_request")


def paapi_search_price(name, cfg_aff):
    """Return (price_int_or_None, url_or_None) using PA-API SearchItems."""
    access = cfg_aff.get("amazon_paapi_access_key")
    secret = cfg_aff.get("amazon_paapi_secret_key")
    tag = cfg_aff.get("amazon_partner_tag")
    marketplace = cfg_aff.get("amazon_marketplace", "www.amazon.in")
    if not (access and secret and tag):
        return None, None

    host, region = AMZ_HOST.get(marketplace, ("webservices.amazon.in", "eu-west-1"))
    service = "ProductAdvertisingAPI"
    uri = "/paapi5/searchitems"
    target = "com.amazon.paapi5.v1.ProductAdvertisingAPIv1.SearchItems"

    payload = json.dumps({
        "Keywords": name,
        "SearchIndex": "Electronics",
        "ItemCount": 1,
        "PartnerTag": tag,
        "PartnerType": "Associates",
        "Marketplace": marketplace,
        "Resources": ["Offers.Listings.Price", "ItemInfo.Title"],
    })

    now = datetime.datetime.utcnow()
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")

    canonical_headers = (
        f"content-encoding:amz-1.0\n"
        f"host:{host}\n"
        f"x-amz-date:{amz_date}\n"
        f"x-amz-target:{target}\n"
    )
    signed_headers = "content-encoding;host;x-amz-date;x-amz-target"
    payload_hash = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = f"POST\n{uri}\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}"

    algorithm = "AWS4-HMAC-SHA256"
    scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = (
        f"{algorithm}\n{amz_date}\n{scope}\n"
        f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    )
    signing_key = _signature_key(secret, date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    auth = (f"{algorithm} Credential={access}/{scope}, "
            f"SignedHeaders={signed_headers}, Signature={signature}")

    headers = {
        "content-encoding": "amz-1.0",
        "content-type": "application/json; charset=utf-8",
        "host": host,
        "x-amz-date": amz_date,
        "x-amz-target": target,
        "Authorization": auth,
    }
    req = urllib.request.Request("https://" + host + uri,
                                 data=payload.encode("utf-8"),
                                 headers=headers, method="POST")
    with urllib.request.urlopen(req, timeout=30) as r:
        res = json.loads(r.read().decode("utf-8"))
    try:
        item = res["SearchResult"]["Items"][0]
        url = item.get("DetailPageURL")
        price = item["Offers"]["Listings"][0]["Price"]["Amount"]
        return int(round(float(price))), url
    except Exception:  # noqa
        return None, None


def main():
    cfg = C.load_config()
    aff = cfg.get("affiliate", {})
    stores = cfg.get("stores", ["Amazon", "Flipkart"])
    tag = aff.get("amazon_partner_tag", "")
    marketplace = aff.get("amazon_marketplace", "www.amazon.in")
    affid = aff.get("flipkart_affiliate_id", "")
    use_paapi = bool(aff.get("amazon_paapi_access_key") and aff.get("amazon_paapi_secret_key"))

    specs = C.read_json("specs.json")
    if not specs:
        raise SystemExit("data/specs.json missing. Run import_specs.py first.")

    print(f"[price] mode={'PA-API + links' if use_paapi else 'affiliate links'} "
          f"| {len(specs['phones'])} phones")

    out = {}
    for p in specs["phones"]:
        name = p["name"]
        rows = []
        amz_price, amz_url = (None, None)
        if use_paapi:
            try:
                amz_price, amz_url = paapi_search_price(name, aff)
            except Exception as e:  # noqa
                print(f"  ! PA-API {name}: {e}")
        if "Amazon" in stores:
            rows.append({"store": "Amazon",
                         "price": amz_price,
                         "url": amz_url or amazon_link(name, tag, marketplace)})
        if "Flipkart" in stores:
            rows.append({"store": "Flipkart", "price": None, "url": flipkart_link(name, affid)})

        prices_known = [r["price"] for r in rows if r["price"]]
        out[p["id"]] = {
            "basePrice": min(prices_known) if prices_known else 0,
            "prices": rows,
        }

    C.write_json("prices.json", out)
    warn = "" if (tag or affid) else "  (no affiliate tag/id set — links won't earn yet!)"
    print(f"[price] wrote data/prices.json for {len(out)} phones{warn}")


if __name__ == "__main__":
    main()

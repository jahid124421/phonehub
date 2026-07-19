#!/usr/bin/env python3
"""Brand logo enricher — fetches logos from free APIs for brands missing valid logo URLs."""

import json
import os
import urllib.request
import urllib.error
import time
import sys

DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')
BRANDS_FILE = os.path.join(DATA_DIR, 'brands.json')

# ─── Free logo sources (no API key needed) ───

# ─── Simple Icons slug overrides (where auto-slug fails) ───
SI_SLUG_OVERRIDES = {
    'hewlett-packard': 'hp', 'mercedes-benz': 'mercedes', 'rolls-royce': 'rollsroyce',
    'citro\u00ebn': 'citroen', 'hispano-suiza': 'hispanosuiza', 'nothing': 'nothing',
    'realme': 'realme', 'honor': 'honor', 'jaguar': 'jaguar', 'dodge': 'dodge',
    'lancia': 'lancia', 'lotus': 'lotus', 'tvr': 'tvr', 'saab': 'saab',
    'stellantis': 'stellantis', 'delorean': 'delorean', 'brabus': 'brabus',
    'rimac': 'rimac', 'byd': 'byd', 'maserati': 'maserati', 'alfa': 'alfaromeo',
    'aston': 'astonmartin', 'mclaren': 'mclaren', 'buick': 'buick',
    'jeep': 'jeep', 'infiniti': 'infiniti', 'pontiac': 'pontiac',
    'datsun': 'datsun', 'isuzu': 'isuzu', 'daihatsu': 'daihatsu',
    'triumph': 'triumph', 'alcatel': 'alcatel', 'suzuki': 'suzuki',
    'proton': 'proton', 'tata': 'tata', 'rover': 'landrover',
    'dacia': 'dacia', 'volvo': 'volvo', 'seat': 'seat',
    'microsoft': 'microsoft', 'logitech': 'logitech',
    'tcl': 'tcl', 'garmin': 'garmin', 'polar': 'polar',
    'suunto': 'suunto', 'withings': 'withings', 'fujifilm': 'fujifilm',
    'pine64': 'pine64', 'ibm': 'ibm', 'toshiba': 'toshiba',
    'acer': 'acer', 'dell': 'dell', 'lenovo': 'lenovo',
    'medion': 'medion', 'sega': 'sega', 'zenith': 'zenith',
    'magnavox': 'magnavox', 'rca': 'rca', 'sharp-s': 'sharp',
    'koninklijke': 'philips',
}


def get_simple_icons_url(brand_name, brand_id=None):
    """Simple Icons CDN — free, no key needed, 2800+ brands.
    Tries override slug first, then auto-generated slug from name, then from id."""
    # 1) Check override map
    if brand_id and brand_id in SI_SLUG_OVERRIDES:
        slug = SI_SLUG_OVERRIDES[brand_id]
        url = f"https://cdn.simpleicons.org/{slug}"
        if check_url(url):
            return url
    # 2) Auto-slug from name
    slug = brand_name.lower().replace(' ', '').replace('-', '').replace('.', '')
    url = f"https://cdn.simpleicons.org/{slug}"
    if check_url(url):
        return url
    # 3) Auto-slug from brand_id
    if brand_id:
        slug2 = brand_id.lower().replace(' ', '').replace('-', '').replace('.', '')
        if slug2 != slug:
            url2 = f"https://cdn.simpleicons.org/{slug2}"
            if check_url(url2):
                return url2
    return None


def get_clearbit_url(domain):
    """Clearbit Logo API — free, no key needed."""
    return f"https://logo.clearbit.com/{domain}"


# ─── Brand-to-domain mapping (all 213 brands) ───
DOMAIN_MAP = {
    # ── Mobiles ──
    'apple': 'apple.com',
    'samsung': 'samsung.com',
    'google': 'google.com',
    'xiaomi': 'xiaomi.com',
    'oneplus': 'oneplus.com',
    'nothing': 'nothing.tech',
    'vivo': 'vivo.com',
    'realme': 'realme.com',
    'oppo': 'oppo.com',
    'motorola': 'motorola.com',
    'sony': 'sony.com',
    'nokia': 'nokia.com',
    'honor': 'honor.com',
    'asus': 'asus.com',
    'huawei': 'huawei.com',
    'tcl': 'tcl.com',
    # ── Laptops ──
    'lenovo': 'lenovo.com',
    'acer': 'acer.com',
    'dell': 'dell.com',
    'hewlett-packard': 'hp.com',
    'microsoft': 'microsoft.com',
    'medion': 'medion.com',
    'toshiba': 'toshiba.com',
    'compaq': 'compaq.com',
    # ── TVs ──
    'lg': 'lg.com',
    'sharp-s': 'sharp.com',
    'koninklijke': 'philips.com',
    'rca': 'rca.com',
    'magnavox': 'magnavox.com',
    # ── Electronics ──
    'garmin': 'garmin.com',
    'withings': 'withings.com',
    'fujifilm': 'fujifilm.com',
    'suunto': 'suunto.com',
    'polar': 'polar.com',
    'sega': 'sega.com',
    'videoton': 'videoton.hu',
    'brionvega': 'brionvega.com',
    # ── Computers ──
    'ibm': 'ibm.com',
    'pine64': 'pine64.org',
    'logitech': 'logitech.com',
    # ── Other (legacy tech / misc) ──
    'zenith': 'zenith.com',
    'tandy': 'radioshack.com',
    'data': 'tata.com',
    'sinclair': 'sinclairzx.com',
    'leaf': 'leafgroup.com',
    'cockerell': 'hoverspeed.com',
    'zato': 'zato.de',
    'rubery': 'ruberyowen.co.uk',
    'frans': 'frans.com',
    # ── Auto brands ──
    'tesla': 'tesla.com',
    'sampo': 'sampocompany.com',
    'renault': 'renault.com',
    'gac': 'gacgroup.com',
    'volkswagen': 'volkswagen.com',
    'rolls-royce': 'rolls-roycemotorcars.com',
    'saipa': 'saipacorp.com',
    'ferrari': 'ferrari.com',
    'chery': 'cheryinternational.com',
    'peugeot': 'peugeot.com',
    'mitsubishi': 'mitsubishi.com',
    'general': 'gm.com',
    'škoda': 'skoda-auto.com',
    'subaru': 'subaru.com',
    'toyota': 'toyota.com',
    'porsche': 'porsche.com',
    'jaguar': 'jaguar.com',
    'alfa': 'alfaromeo.com',
    'mazda': 'mazda.com',
    'hispano-suiza': 'hispano-suizacars.com',
    'honda': 'honda.com',
    'sevel': 'sevel-sud.it',
    'dodge': 'dodge.com',
    'camille': 'lajamaiscontente.com',
    'benz': 'mercedes-benz.com',
    'packard': 'packardmotorcar.com',
    'fiat': 'fiat.com',
    'riley': 'riley.cars',
    'ford': 'ford.com',
    'daihatsu': 'daihatsu.com',
    'audi': 'audi.com',
    'bugatti': 'bugatti.com',
    'de': 'detomaso-automobili.com',
    'british': 'britishmotors.co.uk',
    'nissan': 'nissan.com',
    'bmw': 'bmw.com',
    'opel': 'opel.com',
    'tatra': 'tatra.cz',
    'alan': 'alancars.co.uk',
    'aston': 'astonmartin.com',
    'moskvitch': 'moskvich.ru',
    'matra': 'groupe-matra.com',
    'lancia': 'lancia.com',
    'ac': 'accars.eu',
    'facel': 'facel-vega.com',
    'standard': 'standardmotorcompany.co.uk',
    'mercedes-benz': 'mercedes-benz.com',
    'adam': 'adamcars.com',
    'puch': 'piaggio.com',
    'morgan': 'morgan-motor.com',
    'stellantis': 'stellantis.com',
    'cadillac': 'cadillac.com',
    'delorean': 'delorean.com',
    'uaz': 'uaz.ru',
    'nsu': 'nsu-classic.de',
    'datsun': 'datsun.com',
    'lotus': 'lotuscars.com',
    'volvo': 'volvo.com',
    'bandini': 'bandinicars.com',
    'tvr': 'tvr.co.uk',
    'coda': 'codaautomotive.com',
    'derways': 'derways-auto.ru',
    'seat': 'seat.com',
    'maserati': 'maserati.com',
    'saab': 'saab.com',
    'kia': 'kia.com',
    'mg': 'mg.co.uk',
    'avtovaz': 'lada.ru',
    'lmx': 'lmxregistrostorico.it',
    'hyundai': 'hyundai.com',
    'isuzu': 'isuzu.com',
    'checker': 'checkercab.com',
    'alpina': 'alpina.com',
    'zündapp': 'zuendapp.de',
    'lamborghini': 'lamborghini.com',
    'brabus': 'brabus.com',
    'zastava': 'zastava.rs',
    'piaggio': 'piaggio.com',
    'gm': 'gm.com',
    'great': 'gwm-global.com',
    'byd': 'byd.com',
    'daimler-benz': 'mercedes-benz.com',
    'hanomag': 'hanomag.com',
    'laurin': 'skoda-auto.com',
    'kg': 'kg-mobility.com',
    'bristol': 'bristolcars.com',
    'citroën': 'citroen.com',
    'vector': 'vector-motors.com',
    'dongfeng': 'dongfeng-global.com',
    'zaz': 'zaz.ua',
    'champion': 'championautoparts.com',
    'zil': 'zil.ru',
    'studebaker': 'studebaker.com',
    'mia': 'mia-electric.com',
    'austro-daimler': 'austro-daimler.com',
    'daimler': 'mercedes-benz.com',
    'american': 'theamc.com',
    'automobilwerk': 'awe-museum.de',
    'industrieverband': 'ifa.com',
    'abarth': 'abarth.com',
    'wolseley': 'wolseleycars.com',
    'nash': 'nashmotors.com',
    'mercury': 'mercury.com',
    'panhard': 'panhard.com',
    'carver': 'carver-world.com',
    'isdera': 'isdera.de',
    'alvis': 'thealviscarcompany.co.uk',
    'horch': 'horch.com',
    'asia': 'kia.com',
    'willys': 'jeep.com',
    'mitsuoka': 'mitsuoka-motor.com',
    'steyr-daimler-puch': 'piaggio.com',
    'bitter': 'bittercars.com',
    'bizzarrini': 'bizzarrini.com',
    'melkus': 'melkus.de',
    'air': 'air-car.com',
    'bolwell': 'bolwell.com',
    'rimac': 'rimac.com',
    'brabham': 'brabham.com',
    'tata': 'tata.com',
    'gaz': 'azgaz.ru',
    'geely': 'geely.com',
    'iso': 'isorivolta.com',
    'auto': 'auto-union.com',
    'daewoo': 'daewoomotor.com',
    'k-1': 'k1-attack.com',
    'ss': 'jaguar.com',
    'delage': 'delage.fr',
    'lion-peugeot': 'peugeot.com',
    'suzuki': 'suzuki.com',
    'messerschmitt': 'messerschmitt.com',
    'myers': 'myersmotors.com',
    'rover': 'landrover.com',
    'dacia': 'dacia.com',
    'reliant': 'reliant.co.uk',
    'goggomobil': 'goggomobil.com',
    'land': 'landrover.com',
    'buddy': 'buddy.no',
    'saic': 'saicmotor.com',
    'buick': 'buick.com',
    'alcatel': 'alcatel-mobile.com',
    'proton': 'proton.com',
    'infiniti': 'infiniti.com',
    'innocenti': 'innocenti.com',
    'intermeccanica': 'intermeccanica.com',
    'icml': 'icml.com',
    'stoewer': 'stoewer.com',
    'jensen': 'jensengroup.com',
    'triumph': 'triumphmotorcycles.com',
    'izhavto': 'izhavto.ru',
    'jeep': 'jeep.com',
    'italdesign': 'italdesign.it',
    'monteverdi': 'monteverdi.ch',
    'maḥmīyat': 'mahindra.com',
    'voisin': 'voisin.com',
    'pontiac': 'pontiac.com',
    'mclaren': 'mclaren.com',
    'dome': 'dome.co.jp',
    'simca': 'simca.com',
    'tucker': 'tuckerautomobile.com',
    'rust': 'rust.com',
    'north': 'north.com',
    'saleen': 'saleen.com',
    'wanderer': 'wanderer.com',
}


def check_url(url, timeout=5):
    """Check if a URL returns a valid response (200 status).
    Accepts any 200 response — CDN redirects may change Content-Type."""
    try:
        req = urllib.request.Request(url, method='HEAD')
        req.add_header('User-Agent', 'Mozilla/5.0')
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            if resp.status != 200:
                return False
            final_url = resp.url or url
            ct = resp.headers.get('Content-Type', '')
            # Reject HTML redirects (e.g. Brandfetch docs page)
            if 'text/html' in ct and 'simpleicons.org' not in final_url:
                return False
            return True
    except Exception:
        return False


def enrich_brands():
    """Fetch and update logos for all brands missing valid logo URLs."""
    with open(BRANDS_FILE, 'r', encoding='utf-8-sig') as f:
        brands = json.load(f)

    updated = 0
    skipped = 0
    failed = 0
    failed_list = []

    for brand in brands:
        logo = brand.get('logo', '')
        name = brand.get('name', '')
        brand_id = brand.get('id', '')

        # Skip if logo is a valid HTTP URL that works
        if logo and logo.startswith('http'):
            if check_url(logo):
                skipped += 1
                continue
            print(f"  BROKEN: {name} ({logo})")

        # If logo is emoji or broken, try to fetch
        print(f"  Fetching logo for: {name} (id={brand_id})...")

        # Try Simple Icons first (most reliable, 2800+ brands)
        si_url = get_simple_icons_url(name, brand_id)
        if si_url:
            brand['logo'] = si_url
            updated += 1
            print(f"    \u2713 Simple Icons: {si_url}")
            continue
        
        # Try Clearbit Logo API
        domain = DOMAIN_MAP.get(brand_id)
        if not domain:
            domain = f"{brand_id.replace(' ', '').replace('-', '')}.com"
        cb_url = get_clearbit_url(domain)
        if check_url(cb_url):
            brand['logo'] = cb_url
            updated += 1
            print(f"    \u2713 Clearbit: {cb_url}")
            continue

        failed += 1
        failed_list.append(f"{name} ({brand_id})")
        print(f"    ✗ No logo found for {name}")
        time.sleep(0.1)  # Rate limiting

    # Save updated brands
    with open(BRANDS_FILE, 'w', encoding='utf-8') as f:
        json.dump(brands, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*60}")
    print(f"  RESULTS: {updated} updated, {skipped} already OK, "
          f"{failed} failed out of {len(brands)} total brands")
    if failed_list:
        print(f"\n  Failed brands:")
        for fb in failed_list:
            print(f"    - {fb}")
    print(f"{'='*60}")


if __name__ == '__main__':
    enrich_brands()

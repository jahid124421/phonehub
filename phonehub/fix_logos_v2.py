#!/usr/bin/env python3
"""
Replace brand logos with reliable URLs from clearbit/logoapi services
"""

import re

DATA_FILE = r'c:\Users\96650\OneDrive\Desktop\AI_BA_WORKSPACE\phonehub\js\data.js'

# Use clearbit which is designed for this purpose
# Format: https://logo.clearbit.com/domain.com?size=200
WORKING_LOGOS = {
    "medion": "https://logo.clearbit.com/medion.com?size=200",
    "zenith": "https://logo.clearbit.com/zenith.com?size=200",
    "toshiba": "https://logo.clearbit.com/toshiba.com?size=200",
    "compaq": "https://logo.clearbit.com/compaq.com?size=200",
    "ibm": "https://logo.clearbit.com/ibm.com?size=200",
    "acer": "https://logo.clearbit.com/acer.com?size=200",
    "dell": "https://logo.clearbit.com/dell.com?size=200",
    "garmin": "https://logo.clearbit.com/garmin.com?size=200",
    "withings": "https://logo.clearbit.com/withings.com?size=200",
    "sinclair": "https://logo.clearbit.com/sinclair.com?size=200",
    "magnavox": "https://logo.clearbit.com/magnavox.com?size=200",
    "sega": "https://logo.clearbit.com/sega.com?size=200",
    "rca": "https://logo.clearbit.com/rca.com?size=200",
    "fujifilm": "https://logo.clearbit.com/fujifilm.com?size=200",
    "logitech": "https://logo.clearbit.com/logitech.com?size=200",
    "hewlett-packard": "https://logo.clearbit.com/hp.com?size=200",
    "suunto": "https://logo.clearbit.com/suunto.com?size=200",
    "polar": "https://logo.clearbit.com/polar.com?size=200",
    "tesla": "https://logo.clearbit.com/tesla.com?size=200",
    "renault": "https://logo.clearbit.com/renault.com?size=200",
    "gac": "https://logo.clearbit.com/gac.com?size=200",
    "volkswagen": "https://logo.clearbit.com/volkswagen.com?size=200",
    "rolls-royce": "https://logo.clearbit.com/rolls-royce.com?size=200",
    "ferrari": "https://logo.clearbit.com/ferrari.com?size=200",
    "chery": "https://logo.clearbit.com/chery.com?size=200",
    "peugeot": "https://logo.clearbit.com/peugeot.com?size=200",
    "mitsubishi": "https://logo.clearbit.com/mitsubishi.com?size=200",
    "subaru": "https://logo.clearbit.com/subaru.com?size=200",
    "toyota": "https://logo.clearbit.com/toyota.com?size=200",
    "porsche": "https://logo.clearbit.com/porsche.com?size=200",
    "jaguar": "https://logo.clearbit.com/jaguar.com?size=200",
    "alfa": "https://logo.clearbit.com/alfaromeo.com?size=200",
    "mazda": "https://logo.clearbit.com/mazda.com?size=200",
    "honda": "https://logo.clearbit.com/honda.com?size=200",
    "dodge": "https://logo.clearbit.com/dodge.com?size=200",
    "benz": "https://logo.clearbit.com/mercedes-benz.com?size=200",
    "fiat": "https://logo.clearbit.com/fiat.com?size=200",
    "ford": "https://logo.clearbit.com/ford.com?size=200",
    "daihatsu": "https://logo.clearbit.com/daihatsu.com?size=200",
    "audi": "https://logo.clearbit.com/audi.com?size=200",
    "bugatti": "https://logo.clearbit.com/bugatti.com?size=200",
    "nissan": "https://logo.clearbit.com/nissan.com?size=200",
    "bmw": "https://logo.clearbit.com/bmw.com?size=200",
    "opel": "https://logo.clearbit.com/opel.com?size=200",
    "aston": "https://logo.clearbit.com/astonmartin.com?size=200",
    "lancia": "https://logo.clearbit.com/lancia.com?size=200",
    "mercedes-benz": "https://logo.clearbit.com/mercedes-benz.com?size=200",
    "morgan": "https://logo.clearbit.com/morgan-motor.com?size=200",
    "stellantis": "https://logo.clearbit.com/stellantis.com?size=200",
    "cadillac": "https://logo.clearbit.com/cadillac.com?size=200",
    "datsun": "https://logo.clearbit.com/datsun.com?size=200",
    "lotus": "https://logo.clearbit.com/lotuscars.com?size=200",
    "volvo": "https://logo.clearbit.com/volvo.com?size=200",
    "seat": "https://logo.clearbit.com/seat.com?size=200",
    "maserati": "https://logo.clearbit.com/maserati.com?size=200",
    "saab": "https://logo.clearbit.com/saab.com?size=200",
    "kia": "https://logo.clearbit.com/kia.com?size=200",
    "mg": "https://logo.clearbit.com/mg.com?size=200",
    "hyundai": "https://logo.clearbit.com/hyundai.com?size=200",
    "isuzu": "https://logo.clearbit.com/isuzu.com?size=200",
    "lamborghini": "https://logo.clearbit.com/lamborghini.com?size=200",
    "brabus": "https://logo.clearbit.com/brabus.com?size=200",
    "piaggio": "https://logo.clearbit.com/piaggio.com?size=200",
    "byd": "https://logo.clearbit.com/byd.com?size=200",
    "citroën": "https://logo.clearbit.com/citroen.com?size=200",
    "dongfeng": "https://logo.clearbit.com/dongfeng.com?size=200",
    "abarth": "https://logo.clearbit.com/abarth.com?size=200",
    "škoda": "https://logo.clearbit.com/skoda.com?size=200",
    "microsoft": "https://logo.clearbit.com/microsoft.com?size=200",
    "sony": "https://logo.clearbit.com/sony.com?size=200",
    "lg": "https://logo.clearbit.com/lg.com?size=200",
    "huawei": "https://logo.clearbit.com/huawei.com?size=200",
    "lenovo": "https://logo.clearbit.com/lenovo.com?size=200",
    "tcl": "https://logo.clearbit.com/tcl.com?size=200",
    "pine64": "https://logo.clearbit.com/pine64.org?size=200",
}

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = 0
for brand_id, new_url in WORKING_LOGOS.items():
    # Replace any existing logo URL for this brand
    pattern = r'("id":\s*"' + re.escape(brand_id) + r'"[^}]*?"logo":\s*")[^"]+(")'
    new_content = re.sub(pattern, r'\1' + new_url + r'\2', content)
    if new_content != content:
        content = new_content
        replacements += 1

print(f"Updated {replacements} brand logos with clearbit URLs")

with open(DATA_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
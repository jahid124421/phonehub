#!/usr/bin/env python3
"""
Replace broken brandfetch.io URLs with working logo URLs from Wikipedia/Wikimedia
"""

import re

DATA_FILE = r'c:\Users\96650\OneDrive\Desktop\AI_BA_WORKSPACE\phonehub\js\data.js'

# Working logo URLs from Wikipedia/Wikimedia Commons
WORKING_LOGOS = {
    "medion": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/44/Medion_Logo.svg/200px-Medion_Logo.svg.png",
    "zenith": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Zenith_logo.svg/200px-Zenith_logo.svg.png",
    "toshiba": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Toshiba_logo.svg/200px-Toshiba_logo.svg.png",
    "compaq": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Compaq_logo.svg/200px-Compaq_logo.svg.png",
    "ibm": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/IBM_logo.svg/200px-IBM_logo.svg.png",
    "acer": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Acer_Logo.svg/200px-Acer_Logo.svg.png",
    "dell": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Dell_Logo.svg/200px-Dell_Logo.svg.png",
    "garmin": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Garmin_logo.svg/200px-Garmin_logo.svg.png",
    "withings": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Withings_logo.svg/200px-Withings_logo.svg.png",
    "sinclair": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Sinclair_Research_logo.svg/200px-Sinclair_Research_logo.svg.png",
    "magnavox": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Magnavox_logo.svg/200px-Magnavox_logo.svg.png",
    "sega": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Sega_logo.svg/200px-Sega_logo.svg.png",
    "rca": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/RCA_logo.svg/200px-RCA_logo.svg.png",
    "fujifilm": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Fujifilm_logo.svg/200px-Fujifilm_logo.svg.png",
    "logitech": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Logitech_logo.svg/200px-Logitech_logo.svg.png",
    "hewlett-packard": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/HP_logo_2023.svg/200px-HP_logo_2023.svg.png",
    "suunto": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Suunto_logo.svg/200px-Suunto_logo.svg.png",
    "polar": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/8e/Polar_electro_logo.svg/200px-Polar_electro_logo.svg.png",
    "tesla": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Tesla_Motors.svg/200px-Tesla_Motors.svg.png",
    "renault": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Renault_Logo.svg/200px-Renault_Logo.svg.png",
    "gac": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/GAC_Logo.svg/200px-GAC_Logo.svg.png",
    "volkswagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Volkswagen_logo_2019.svg/200px-Volkswagen_logo_2019.svg.png",
    "rolls-royce": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Rolls-Royce_logo.svg/200px-Rolls-Royce_logo.svg.png",
    "ferrari": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Ferrari_logo.svg/200px-Ferrari_logo.svg.png",
    "chery": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Chery_logo.svg/200px-Chery_logo.svg.png",
    "peugeot": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Peugeot_logo.svg/200px-Peugeot_logo.svg.png",
    "mitsubishi": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mitsubishi_logo.svg/200px-Mitsubishi_logo.svg.png",
    "subaru": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Subaru_logo.svg/200px-Subaru_logo.svg.png",
    "toyota": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Toyota_logo.svg/200px-Toyota_logo.svg.png",
    "porsche": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Porsche_logo.svg/200px-Porsche_logo.svg.png",
    "jaguar": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Jaguar_logo.svg/200px-Jaguar_logo.svg.png",
    "alfa": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Alfa_Romeo_logo.svg/200px-Alfa_Romeo_logo.svg.png",
    "mazda": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mazda_logo.svg/200px-Mazda_logo.svg.png",
    "honda": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Honda_logo.svg/200px-Honda_logo.svg.png",
    "dodge": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Dodge_logo.svg/200px-Dodge_logo.svg.png",
    "benz": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mercedes-Benz_logo.svg/200px-Mercedes-Benz_logo.svg.png",
    "fiat": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Fiat_logo.svg/200px-Fiat_logo.svg.png",
    "ford": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Ford_logo.svg/200px-Ford_logo.svg.png",
    "daihatsu": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Daihatsu_logo.svg/200px-Daihatsu_logo.svg.png",
    "audi": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Audi_logo.svg/200px-Audi_logo.svg.png",
    "bugatti": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Bugatti_logo.svg/200px-Bugatti_logo.svg.png",
    "nissan": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Nissan_logo.svg/200px-Nissan_logo.svg.png",
    "bmw": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/BMW_logo.svg/200px-BMW_logo.svg.png",
    "opel": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Opel_logo.svg/200px-Opel_logo.svg.png",
    "aston": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Aston_Martin_logo.svg/200px-Aston_Martin_logo.svg.png",
    "lancia": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lancia_logo.svg/200px-Lancia_logo.svg.png",
    "mercedes-benz": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mercedes-Benz_logo.svg/200px-Mercedes-Benz_logo.svg.png",
    "morgan": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Morgan_Motor_Company_logo.svg/200px-Morgan_Motor_Company_logo.svg.png",
    "stellantis": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Stellantis_logo.svg/200px-Stellantis_logo.svg.png",
    "cadillac": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Cadillac_logo.svg/200px-Cadillac_logo.svg.png",
    "datsun": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Datsun_logo.svg/200px-Datsun_logo.svg.png",
    "lotus": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lotus_Cars_logo.svg/200px-Lotus_Cars_logo.svg.png",
    "volvo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Volvo_logo.svg/200px-Volvo_logo.svg.png",
    "seat": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/SEAT_logo.svg/200px-SEAT_logo.svg.png",
    "maserati": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Maserati_logo.svg/200px-Maserati_logo.svg.png",
    "saab": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Saab_logo.svg/200px-Saab_logo.svg.png",
    "kia": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Kia_logo.svg/200px-Kia_logo.svg.png",
    "mg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/MG_logo.svg/200px-MG_logo.svg.png",
    "hyundai": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Hyundai_logo.svg/200px-Hyundai_logo.svg.png",
    "isuzu": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Isuzu_logo.svg/200px-Isuzu_logo.svg.png",
    "lamborghini": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lamborghini_logo.svg/200px-Lamborghini_logo.svg.png",
    "brabus": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Brabus_logo.svg/200px-Brabus_logo.svg.png",
    "piaggio": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Piaggio_logo.svg/200px-Piaggio_logo.svg.png",
    "byd": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/BYD_logo.svg/200px-BYD_logo.svg.png",
    "citroën": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Citro%C3%ABn_logo.svg/200px-Citro%C3%ABn_logo.svg.png",
    "dongfeng": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Dongfeng_logo.svg/200px-Dongfeng_logo.svg.png",
    "abarth": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Abarth_logo.svg/200px-Abarth_logo.svg.png",
    "škoda": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/%C5%A0koda_logo.svg/200px-%C5%A0koda_logo.svg.png",
    "microsoft": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Microsoft_logo.svg/200px-Microsoft_logo.svg.png",
    "sony": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Sony_logo.svg/200px-Sony_logo.svg.png",
    "lg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/LG_logo.svg/200px-LG_logo.svg.png",
    "huawei": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Huawei_logo.svg/200px-Huawei_logo.svg.png",
    "lenovo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lenovo_logo.svg/200px-Lenovo_logo.svg.png",
    "tcl": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/TCL_logo.svg/200px-TCL_logo.svg.png",
    "pine64": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/PINE64_logo.svg/200px-PINE64_logo.svg.png",
    "garmin": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Garmin_logo.svg/200px-Garmin_logo.svg.png",
}

with open(DATA_FILE, 'r', encoding='utf-8') as f:
    content = f.read()

replacements = 0
for brand_id, new_url in WORKING_LOGOS.items():
    # Find the brand and replace its logo URL
    pattern = r'("id":\s*"' + re.escape(brand_id) + r'"[^}]*?"logo":\s*")https://cdn\.brandfetch\.io/[^"]+(")'
    new_content = re.sub(pattern, r'\1' + new_url + r'\2', content)
    if new_content != content:
        content = new_content
        replacements += 1

print(f"Replaced {replacements} brandfetch.io URLs with working Wikipedia URLs")

with open(DATA_FILE, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
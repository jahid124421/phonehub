#!/usr/bin/env python3
"""
Download brand logos from Wikipedia/Wikimedia and save locally
"""
import os
import requests
import time

# Brand logos from Wikipedia/Wikimedia Commons (direct image URLs)
BRAND_LOGOS = {
    "acer": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Acer_Logo.svg/200px-Acer_Logo.svg.png",
    "dell": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/48/Dell_Logo.svg/200px-Dell_Logo.svg.png",
    "ibm": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/IBM_logo.svg/200px-IBM_logo.svg.png",
    "toshiba": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Toshiba_logo.svg/200px-Toshiba_logo.svg.png",
    "compaq": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Compaq_logo.svg/200px-Compaq_logo.svg.png",
    "fujifilm": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Fujifilm_logo.svg/200px-Fujifilm_logo.svg.png",
    "logitech": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Logitech_logo.svg/200px-Logitech_logo.svg.png",
    "hewlett-packard": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/HP_logo_2023.svg/200px-HP_logo_2023.svg.png",
    "sony": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Sony_logo.svg/200px-Sony_logo.svg.png",
    "microsoft": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Microsoft_logo.svg/200px-Microsoft_logo.svg.png",
    "lg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/LG_logo.svg/200px-LG_logo.svg.png",
    "huawei": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Huawei_logo.svg/200px-Huawei_logo.svg.png",
    "lenovo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lenovo_logo.svg/200px-Lenovo_logo.svg.png",
    "tcl": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/TCL_logo.svg/200px-TCL_logo.svg.png",
    "garmin": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Garmin_logo.svg/200px-Garmin_logo.svg.png",
    "tesla": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/bd/Tesla_Motors.svg/200px-Tesla_Motors.svg.png",
    "ferrari": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Ferrari_logo.svg/200px-Ferrari_logo.svg.png",
    "bmw": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/BMW_logo.svg/200px-BMW_logo.svg.png",
    "mercedes-benz": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mercedes-Benz_logo.svg/200px-Mercedes-Benz_logo.svg.png",
    "audi": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Audi_logo.svg/200px-Audi_logo.svg.png",
    "toyota": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Toyota_logo.svg/200px-Toyota_logo.svg.png",
    "honda": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Honda_logo.svg/200px-Honda_logo.svg.png",
    "ford": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Ford_logo.svg/200px-Ford_logo.svg.png",
    "volkswagen": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6d/Volkswagen_logo_2019.svg/200px-Volkswagen_logo_2019.svg.png",
    "nissan": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Nissan_logo.svg/200px-Nissan_logo.svg.png",
    "hyundai": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Hyundai_logo.svg/200px-Hyundai_logo.svg.png",
    "kia": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Kia_logo.svg/200px-Kia_logo.svg.png",
    "porsche": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Porsche_logo.svg/200px-Porsche_logo.svg.png",
    "jaguar": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Jaguar_logo.svg/200px-Jaguar_logo.svg.png",
    "land rover": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Land_Rover_logo.svg/200px-Land_Rover_logo.svg.png",
    "renault": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Renault_Logo.svg/200px-Renault_Logo.svg.png",
    "peugeot": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Peugeot_logo.svg/200px-Peugeot_logo.svg.png",
    "citroën": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Citro%C3%ABn_logo.svg/200px-Citro%C3%ABn_logo.svg.png",
    "fiat": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Fiat_logo.svg/200px-Fiat_logo.svg.png",
    "volvo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Volvo_logo.svg/200px-Volvo_logo.svg.png",
    "mazda": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mazda_logo.svg/200px-Mazda_logo.svg.png",
    "subaru": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Subaru_logo.svg/200px-Subaru_logo.svg.png",
    "mitsubishi": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Mitsubishi_logo.svg/200px-Mitsubishi_logo.svg.png",
    "suzuki": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Suzuki_logo.svg/200px-Suzuki_logo.svg.png",
    "isuzu": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Isuzu_logo.svg/200px-Isuzu_logo.svg.png",
    "dodge": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Dodge_logo.svg/200px-Dodge_logo.svg.png",
    "lamborghini": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lamborghini_logo.svg/200px-Lamborghini_logo.svg.png",
    "bugatti": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Bugatti_logo.svg/200px-Bugatti_logo.svg.png",
    "maserati": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Maserati_logo.svg/200px-Maserati_logo.svg.png",
    "alfa romeo": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Alfa_Romeo_logo.svg/200px-Alfa_Romeo_logo.svg.png",
    "lancia": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lancia_logo.svg/200px-Lancia_logo.svg.png",
    "seat": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/SEAT_logo.svg/200px-SEAT_logo.svg.png",
    "škoda": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/%C5%A0koda_logo.svg/200px-%C5%A0koda_logo.svg.png",
    "opel": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Opel_logo.svg/200px-Opel_logo.svg.png",
    "aston martin": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Aston_Martin_logo.svg/200px-Aston_Martin_logo.svg.png",
    "bentley": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Bentley_logo.svg/200px-Bentley_logo.svg.png",
    "rolls-royce": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Rolls-Royce_logo.svg/200px-Rolls-Royce_logo.svg.png",
    "cadillac": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Cadillac_logo.svg/200px-Cadillac_logo.svg.png",
    "lotus": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Lotus_Cars_logo.svg/200px-Lotus_Cars_logo.svg.png",
    "mg": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/MG_logo.svg/200px-MG_logo.svg.png",
    "byd": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/BYD_logo.svg/200px-BYD_logo.svg.png",
    "chery": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Chery_logo.svg/200px-Chery_logo.svg.png",
    "geely": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Geely_logo.svg/200px-Geely_logo.svg.png",
    "great wall": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Great_Wall_Motor_logo.svg/200px-Great_Wall_Motor_logo.svg.png",
    "harley-davidson": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Harley-Davidson_logo.svg/200px-Harley-Davidson_logo.svg.png",
    "ducati": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Ducati_logo.svg/200px-Ducati_logo.svg.png",
    "bmw motorrad": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/BMW_logo.svg/200px-BMW_logo.svg.png",
    "triumph": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Triumph_Motorcycles_logo.svg/200px-Triumph_Motorcycles_logo.svg.png",
    "kawasaki": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Kawasaki_logo.svg/200px-Kawasaki_logo.svg.png",
    "yamaha": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Yamaha_logo.svg/200px-Yamaha_logo.svg.png",
    "honda": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Honda_logo.svg/200px-Honda_logo.svg.png",
    "suzuki": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Suzuki_logo.svg/200px-Suzuki_logo.svg.png",
}

IMG_DIR = r'c:\Users\96650\OneDrive\Desktop\AI_BA_WORKSPACE\phonehub\phonehub\img\brands'
os.makedirs(IMG_DIR, exist_ok=True)

downloaded = 0
failed = []

for brand_id, url in BRAND_LOGOS.items():
    ext = url.split('.')[-1]
    if '?' in ext:
        ext = 'png'
    filename = f"{brand_id.replace(' ', '-')}.{ext}"
    filepath = os.path.join(IMG_DIR, filename)
    
    try:
        if not os.path.exists(filepath):
            print(f"Downloading {brand_id}...")
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(resp.content)
                downloaded += 1
                print(f"  [OK] Saved {filename}")
            else:
                failed.append(brand_id)
                print(f"  [FAIL] Status: {resp.status_code}")
            time.sleep(0.5)  # Be nice to Wikipedia
        else:
            print(f"Skipping {brand_id} (already exists)")
    except Exception as e:
        failed.append(brand_id)
        print(f"  [ERROR] {e}")

print(f"\nDownloaded {downloaded} logos")
if failed:
    print(f"Failed: {', '.join(failed)}")
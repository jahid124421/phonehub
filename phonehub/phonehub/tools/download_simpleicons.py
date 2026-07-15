#!/usr/bin/env python3
"""
Download brand logos from simpleicons.org and save locally
"""
import os
import requests
import time

# All brands from data.js that need logos
BRANDS = [
    "acer", "dell", "ibm", "toshiba", "compaq", "fujifilm", "logitech",
    "hewlett-packard", "sony", "microsoft", "lg", "huawei", "lenovo", "tcl",
    "garmin", "tesla", "ferrari", "bmw", "mercedes-benz", "audi", "toyota",
    "honda", "ford", "volkswagen", "nissan", "hyundai", "kia", "porsche",
    "jaguar", "land-rover", "renault", "peugeot", "citroen", "fiat", "volvo",
    "mazda", "subaru", "mitsubishi", "suzuki", "isuzu", "dodge", "lamborghini",
    "bugatti", "maserati", "alfa-romeo", "lancia", "seat", "skoda", "opel",
    "aston-martin", "bentley", "rolls-royce", "cadillac", "lotus", "mg", "byd",
    "chery", "geely", "great-wall", "harley-davidson", "ducati", "bmw-motorrad",
    "triumph", "kawasaki", "yamaha", "honda", "suzuki", "medion", "zenith",
    "sinclair", "magnavox", "sega", "rca", "suunto", "polar", "pine64",
    "gac", "aston", "brabus", "piaggio", "dongfeng", "abarth", "stellantis",
    "datsun", "saab", "withings", "tcl"
]

IMG_DIR = r'c:\Users\96650\OneDrive\Desktop\AI_BA_WORKSPACE\phonehub\phonehub\img\brands'
os.makedirs(IMG_DIR, exist_ok=True)

headers = {'User-Agent': 'Mozilla/5.0'}

downloaded = 0
failed = []

for brand_id in BRANDS:
    filename = f"{brand_id}.svg"
    filepath = os.path.join(IMG_DIR, filename)
    
    try:
        if not os.path.exists(filepath):
            url = f"https://simpleicons.org/icons/{brand_id}.svg"
            print(f"Downloading {brand_id}...")
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(resp.content)
                downloaded += 1
                print(f"  [OK] Saved {filename} ({len(resp.content)} bytes)")
            else:
                failed.append(brand_id)
                print(f"  [FAIL] Status: {resp.status_code}")
            time.sleep(0.3)  # Be nice
        else:
            print(f"Skipping {brand_id} (already exists)")
    except Exception as e:
        failed.append(brand_id)
        print(f"  [ERROR] {e}")

print(f"\nDownloaded {downloaded} logos")
if failed:
    print(f"Failed: {', '.join(failed)}")
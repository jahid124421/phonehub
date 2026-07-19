#!/usr/bin/env python3
"""
New Product Auto-Detector — Detects new products and adds them to the database.
Local-only mode: no external network calls, uses local data + mock detection.
"""

import json
import os
import re
import hashlib
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')
SEEN_FILE = os.path.join(DATA_DIR, 'seen_products.json')
PRODUCTS_FILE = os.path.join(DATA_DIR, 'products.json')

# Simulated new product announcements (would come from RSS feeds in production)
SIMULATED_FEED = [
    {
        'title': 'Samsung Galaxy S25 Ultra',
        'category': 'phone',
        'specs': {
            'display': '6.9" Dynamic AMOLED 2X, 120Hz',
            'processor': 'Snapdragon 8 Elite',
            'ram': '12GB',
            'storage': '256GB / 512GB / 1TB',
            'camera': '200MP + 50MP + 10MP + 12MP',
            'battery': '5000mAh, 45W charging'
        }
    },
    {
        'title': 'Google Pixel 9 Pro XL',
        'category': 'phone',
        'specs': {
            'display': '6.8" LTPO OLED, 120Hz',
            'processor': 'Google Tensor G4',
            'ram': '16GB',
            'storage': '128GB / 256GB / 512GB / 1TB',
            'camera': '50MP + 48MP + 48MP',
            'battery': '5060mAh, 37W charging'
        }
    },
    {
        'title': 'OnePlus 13',
        'category': 'phone',
        'specs': {
            'display': '6.82" LTPO AMOLED, 120Hz',
            'processor': 'Snapdragon 8 Elite',
            'ram': '12GB / 16GB',
            'storage': '256GB / 512GB',
            'camera': '50MP + 50MP + 50MP',
            'battery': '6000mAh, 100W charging'
        }
    },
    {
        'title': 'Xiaomi 15 Pro',
        'category': 'phone',
        'specs': {
            'display': '6.73" LTPO AMOLED, 120Hz',
            'processor': 'Snapdragon 8 Elite',
            'ram': '12GB / 16GB',
            'storage': '256GB / 512GB',
            'camera': '50MP + 50MP + 50MP Leica',
            'battery': '6100mAh, 90W charging'
        }
    },
    {
        'title': 'Nothing Phone (3)',
        'category': 'phone',
        'specs': {
            'display': '6.55" LTPO OLED, 120Hz',
            'processor': 'Snapdragon 8s Gen 3',
            'ram': '12GB',
            'storage': '256GB',
            'camera': '50MP + 50MP',
            'battery': '4700mAh, 45W charging'
        }
    },
]

KNOWN_BRANDS = [
    'Apple', 'Samsung', 'Google', 'Xiaomi', 'OnePlus', 'Tesla', 'BMW',
    'Sony', 'LG', 'Dell', 'HP', 'Lenovo', 'Asus', 'Acer', 'Microsoft',
    'Motorola', 'Nokia', 'Huawei', 'Oppo', 'Vivo', 'Realme', 'Nothing'
]


def load_seen():
    """Load previously seen product hashes."""
    if os.path.exists(SEEN_FILE):
        with open(SEEN_FILE, encoding='utf-8') as f:
            return json.load(f)
    return {}


def save_seen(seen):
    with open(SEEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(seen, f, indent=2)


def load_products():
    """Load existing products database."""
    if not os.path.exists(PRODUCTS_FILE):
        return []
    with open(PRODUCTS_FILE, encoding='utf-8') as f:
        return json.load(f)


def save_products(products):
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, indent=2)


def extract_brand(title):
    """Extract brand name from product title."""
    for brand in KNOWN_BRANDS:
        if brand.lower() in title.lower():
            return brand.lower()
    return 'unknown'


def make_slug(title):
    """Create a URL-friendly slug from title."""
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')


def detect_new_products():
    """Detect new products from simulated feed."""
    seen = load_seen()
    new_products = []

    for item in SIMULATED_FEED:
        hash_key = hashlib.md5(item['title'].lower().encode()).hexdigest()

        if hash_key not in seen:
            new_products.append(item)
            seen[hash_key] = {
                'title': item['title'],
                'detected_at': datetime.now().isoformat(),
                'category': item['category']
            }
            print(f"    NEW: {item['title']}")

    save_seen(seen)
    return new_products


def add_products_to_database(new_products):
    """Add detected products to products.json."""
    products = load_products()
    added = 0

    for item in new_products:
        slug = make_slug(item['title'])

        # Skip duplicates by slug
        if any(p.get('id') == slug for p in products):
            print(f"    SKIP (exists): {item['title']}")
            continue

        new_product = {
            'id': slug,
            'brand': extract_brand(item['title']),
            'name': item['title'],
            'category': item['category'],
            'image': '',
            'fallbackImg': '',
            'releaseDate': datetime.now().strftime('%Y-%m-%d'),
            'basePrice': 0,
            'popularity': 50,
            'rating': 0,
            'reviewCount': 0,
            'review': '',
            'quickSpecs': item.get('specs', {
                'display': 'TBA',
                'processor': 'TBA',
                'ram': 'TBA',
                'storage': 'TBA',
                'camera': 'TBA',
                'battery': 'TBA'
            }),
            'autoDetected': True,
            'detectedAt': datetime.now().isoformat()
        }

        products.append(new_product)
        added += 1
        print(f"    Added: {item['title']}")

    if added > 0:
        save_products(products)
        print(f"\n  Added {added} new products to database")

    return added


def main():
    print("[+] New Product Detector starting...")

    new_products = detect_new_products()

    if new_products:
        print(f"\n  Found {len(new_products)} new products")
        added = add_products_to_database(new_products)
        print(f"  Added {added} to database")
    else:
        print("  No new products detected")


if __name__ == '__main__':
    main()

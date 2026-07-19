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

# Enhanced brand database with logos, colors, and categories
# Logos from Brandfetch CDN and Simple Icons
BRAND_DATABASE = {
    "apple": {
        "logo": "https://cdn.simpleicons.org/apple",
        "color": "#000000",
        "category": "Mobiles",
        "sub_categories": ["Laptops", "Electronics"]
    },
    "samsung": {
        "logo": "https://cdn.simpleicons.org/samsung",
        "color": "#1428A0",
        "category": "Mobiles",
        "sub_categories": ["Laptops", "TVs", "Appliances", "Electronics"]
    },
    "google": {
        "logo": "https://cdn.simpleicons.org/google",
        "color": "#4285F4",
        "category": "Mobiles",
        "sub_categories": ["Laptops", "Electronics"]
    },
    "xiaomi": {
        "logo": "https://cdn.simpleicons.org/xiaomi",
        "color": "#FF6900",
        "category": "Mobiles",
        "sub_categories": ["Electronics", "Appliances"]
    },
    "oneplus": {
        "logo": "https://cdn.simpleicons.org/oneplus",
        "color": "#EB0028",
        "category": "Mobiles",
        "sub_categories": ["Electronics"]
    },
    "nothing": {
        "logo": "https://cdn.simpleicons.org/nothing/000000",
        "color": "#000000",
        "category": "Mobiles",
        "sub_categories": ["Electronics"]
    },
    "vivo": {
        "logo": "https://cdn.simpleicons.org/vivo",
        "color": "#0C64E8",
        "category": "Mobiles",
        "sub_categories": ["Electronics"]
    },
    "realme": {
        "logo": "https://cdn.simpleicons.org/realme/FFC600",
        "color": "#FFC600",
        "category": "Mobiles",
        "sub_categories": ["Electronics"]
    },
    "oppo": {
        "logo": "https://cdn.simpleicons.org/oppo",
        "color": "#1BA784",
        "category": "Mobiles",
        "sub_categories": ["Electronics"]
    },
    "motorola": {
        "logo": "https://cdn.simpleicons.org/motorola",
        "color": "#5C92FC",
        "category": "Mobiles",
        "sub_categories": ["Electronics"]
    },
    "sony": {
        "logo": "https://cdn.simpleicons.org/sony",
        "color": "#0B0B0B",
        "category": "Electronics",
        "sub_categories": ["Mobiles", "TVs"]
    },
    "nokia": {
        "logo": "https://cdn.simpleicons.org/nokia",
        "color": "#124191",
        "category": "Mobiles",
        "sub_categories": ["Electronics"]
    },
    "honor": {
        "logo": "https://cdn.simpleicons.org/honor/00B0E9",
        "color": "#00B0E9",
        "category": "Mobiles",
        "sub_categories": ["Electronics"]
    },
    "asus": {
        "logo": "https://cdn.simpleicons.org/asus",
        "color": "#000000",
        "category": "Electronics",
        "sub_categories": ["Laptops", "Mobiles"]
    },
    "huawei": {
        "logo": "https://cdn.simpleicons.org/huawei",
        "color": "#C7000B",
        "category": "Mobiles",
        "sub_categories": ["Electronics", "Laptops"]
    },
    "lenovo": {
        "logo": "https://cdn.simpleicons.org/lenovo",
        "color": "#E2231A",
        "category": "Laptops",
        "sub_categories": ["Mobiles", "Computers"]
    },
    "lg": {
        "logo": "https://cdn.simpleicons.org/lg",
        "color": "#A50034",
        "category": "TVs",
        "sub_categories": ["Electronics", "Appliances"]
    },
    "tcl": {
        "logo": "https://cdn.brandfetch.io/tcl.com/w/400/h/400",
        "color": "#0071BC",
        "category": "Mobiles",
        "sub_categories": ["TVs"]
    },
    "microsoft": {
        "logo": "https://cdn.brandfetch.io/microsoft.com/w/400/h/400",
        "color": "#00A4EF",
        "category": "Laptops",
        "sub_categories": ["Laptops"]
    },
    # ---- Other brands (electronics/computing/wearables) ----
    "medion": {
        "logo": "https://cdn.brandfetch.io/medion.com/w/400/h/400",
        "color": "#0066CC",
        "category": "Laptops"
    },
    "toshiba": {
        "logo": "https://cdn.simpleicons.org/toshiba",
        "color": "#FF0000",
        "category": "Laptops",
        "sub_categories": ["TVs", "Computers"]
    },
    "compaq": {
        "logo": "https://cdn.brandfetch.io/compaq.com/w/400/h/400",
        "color": "#0066CC",
        "category": "Laptops"
    },
    "ibm": {
        "logo": "https://cdn.brandfetch.io/ibm.com/w/400/h/400",
        "color": "#006699",
        "category": "Computers"
    },
    "pine64": {
        "logo": "https://cdn.simpleicons.org/pine64/000000",
        "color": "#000000",
        "category": "Computers"
    },
    "acer": {
        "logo": "https://cdn.simpleicons.org/acer",
        "color": "#83B81A",
        "category": "Laptops",
        "sub_categories": ["Electronics"]
    },
    "dell": {
        "logo": "https://cdn.simpleicons.org/dell",
        "color": "#007DB8",
        "category": "Laptops",
        "sub_categories": ["Computers"]
    },
    "garmin": {
        "logo": "https://cdn.simpleicons.org/garmin",
        "color": "#000000",
        "category": "Electronics",
        "sub_categories": ["Electronics"]
    },
    "withings": {
        "logo": "https://cdn.brandfetch.io/withings.com/w/400/h/400",
        "color": "#000000",
        "category": "Electronics"
    },
    "fujifilm": {
        "logo": "https://cdn.simpleicons.org/fujifilm",
        "color": "#ED1C24",
        "category": "Electronics",
        "sub_categories": ["Electronics"]
    },
    "logitech": {
        "logo": "https://cdn.brandfetch.io/logitech.com/w/400/h/400",
        "color": "#00B8FC",
        "category": "Computers",
        "sub_categories": ["Electronics"]
    },
    "hewlett-packard": {
        "logo": "https://cdn.simpleicons.org/hp",
        "color": "#0096D6",
        "category": "Laptops",
        "sub_categories": ["Computers"]
    },
    "suunto": {
        "logo": "https://cdn.brandfetch.io/suunto.com/w/400/h/400",
        "color": "#000000",
        "category": "Electronics"
    },
    "polar": {
        "logo": "https://cdn.brandfetch.io/polar.com/w/400/h/400",
        "color": "#000000",
        "category": "Electronics"
    },
    # ---- Car brands ----
    "renault": {
        "logo": "https://cdn.simpleicons.org/renault",
        "color": "#FFCC00",
        "category": "Auto"
    },
    "volkswagen": {
        "logo": "https://cdn.simpleicons.org/volkswagen",
        "color": "#001E50",
        "category": "Auto"
    },
    "rolls-royce": {
        "logo": "https://cdn.simpleicons.org/rollsroyce",
        "color": "#000000",
        "category": "Auto"
    },
    "ferrari": {
        "logo": "https://cdn.simpleicons.org/ferrari",
        "color": "#FF2800",
        "category": "Auto"
    },
    "peugeot": {
        "logo": "https://cdn.simpleicons.org/peugeot",
        "color": "#000000",
        "category": "Auto"
    },
    "mitsubishi": {
        "logo": "https://cdn.simpleicons.org/mitsubishi",
        "color": "#E2001A",
        "category": "Auto"
    },
    "subaru": {
        "logo": "https://cdn.simpleicons.org/subaru",
        "color": "#013C7A",
        "category": "Auto"
    },
    "toyota": {
        "logo": "https://cdn.simpleicons.org/toyota",
        "color": "#D31017",
        "category": "Auto"
    },
    "porsche": {
        "logo": "https://cdn.simpleicons.org/porsche",
        "color": "#000000",
        "category": "Auto"
    },
    "jaguar": {
        "logo": "https://cdn.brandfetch.io/jaguar.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "mazda": {
        "logo": "https://cdn.simpleicons.org/mazda",
        "color": "#101010",
        "category": "Auto"
    },
    "honda": {
        "logo": "https://cdn.simpleicons.org/honda",
        "color": "#E1001A",
        "category": "Auto"
    },
    "dodge": {
        "logo": "https://cdn.brandfetch.io/dodge.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "fiat": {
        "logo": "https://cdn.simpleicons.org/fiat",
        "color": "#AA001C",
        "category": "Auto"
    },
    "ford": {
        "logo": "https://cdn.simpleicons.org/ford",
        "color": "#003D79",
        "category": "Auto"
    },
    "daihatsu": {
        "logo": "https://cdn.brandfetch.io/daihatsu.com/w/400/h/400",
        "color": "#D50000",
        "category": "Auto"
    },
    "audi": {
        "logo": "https://cdn.simpleicons.org/audi",
        "color": "#000000",
        "category": "Auto"
    },
    "bugatti": {
        "logo": "https://cdn.simpleicons.org/bugatti",
        "color": "#000000",
        "category": "Auto"
    },
    "nissan": {
        "logo": "https://cdn.simpleicons.org/nissan",
        "color": "#C3002F",
        "category": "Auto"
    },
    "bmw": {
        "logo": "https://cdn.simpleicons.org/bmw",
        "color": "#0066B1",
        "category": "Auto"
    },
    "opel": {
        "logo": "https://cdn.simpleicons.org/opel",
        "color": "#000000",
        "category": "Auto"
    },
    "mercedes-benz": {
        "logo": "https://cdn.brandfetch.io/mercedes-benz.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "cadillac": {
        "logo": "https://cdn.simpleicons.org/cadillac",
        "color": "#000000",
        "category": "Auto"
    },
    "delorean": {
        "logo": "https://cdn.brandfetch.io/delorean.com/w/400/h/400",
        "color": "#555555",
        "category": "Auto"
    },
    "lotus": {
        "logo": "https://cdn.brandfetch.io/lotuscars.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "volvo": {
        "logo": "https://cdn.simpleicons.org/volvo",
        "color": "#003057",
        "category": "Auto"
    },
    "maserati": {
        "logo": "https://cdn.simpleicons.org/maserati",
        "color": "#000000",
        "category": "Auto"
    },
    "saab": {
        "logo": "https://cdn.brandfetch.io/saab.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "kia": {
        "logo": "https://cdn.simpleicons.org/kia",
        "color": "#05141F",
        "category": "Auto"
    },
    "mg": {
        "logo": "https://cdn.simpleicons.org/mg",
        "color": "#CC0000",
        "category": "Auto"
    },
    "hyundai": {
        "logo": "https://cdn.simpleicons.org/hyundai",
        "color": "#002C5F",
        "category": "Auto"
    },
    "isuzu": {
        "logo": "https://cdn.brandfetch.io/isuzu.com/w/400/h/400",
        "color": "#E3001B",
        "category": "Auto"
    },
    "lamborghini": {
        "logo": "https://cdn.simpleicons.org/lamborghini",
        "color": "#DDB321",
        "category": "Auto"
    },
    "brabus": {
        "logo": "https://cdn.brandfetch.io/brabus.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "aston": {
        "logo": "https://cdn.simpleicons.org/astonmartin",
        "color": "#00665E",
        "category": "Auto"
    },
    "tata": {
        "logo": "https://cdn.simpleicons.org/tata",
        "color": "#4860A0",
        "category": "Auto"
    },
    "citroën": {
        "logo": "https://cdn.simpleicons.org/citroen",
        "color": "#000000",
        "category": "Auto"
    },
    "seat": {
        "logo": "https://cdn.simpleicons.org/seat",
        "color": "#000000",
        "category": "Auto"
    },
    "byd": {
        "logo": "https://cdn.brandfetch.io/byd.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "rimac": {
        "logo": "https://cdn.brandfetch.io/rimac.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "abarth": {
        "logo": "https://cdn.brandfetch.io/abarth.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "gm": {
        "logo": "https://cdn.brandfetch.io/gm.com/w/400/h/400",
        "color": "#1A1A1A",
        "category": "Auto"
    },
    "daimler-benz": {
        "logo": "https://cdn.brandfetch.io/mercedes-benz.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "daimler": {
        "logo": "https://cdn.brandfetch.io/mercedes-benz.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "piaggio": {
        "logo": "https://cdn.brandfetch.io/piaggio.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    # ---- Retro / legacy tech brands ----
    "zenith": {
        "logo": "https://cdn.brandfetch.io/zenith.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "sega": {
        "logo": "https://cdn.simpleicons.org/sega",
        "color": "#003399",
        "category": "Electronics"
    },
    "tesla": {
        "logo": "https://cdn.simpleicons.org/tesla",
        "color": "#CC0000",
        "category": "Auto"
    },
    "sinclair": {
        "logo": "https://cdn.simpleicons.org/sinclair/000000",
        "color": "#000000",
        "category": "Other"
    },
    "rca": {
        "logo": "https://cdn.brandfetch.io/rca.com/w/400/h/400",
        "color": "#000000",
        "category": "TVs"
    },
    "magnavox": {
        "logo": "https://cdn.simpleicons.org/magnavox/000000",
        "color": "#000000",
        "category": "TVs"
    },
    "sharp-s": {
        "logo": "https://cdn.simpleicons.org/sharp",
        "color": "#000000",
        "category": "TVs",
        "sub_categories": ["Electronics"]
    },
    # ---- Misc brands (keep in Other) ----
    "bristol": {
        "logo": "https://cdn.brandfetch.io/bristolcars.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "alpina": {
        "logo": "https://cdn.brandfetch.io/alpina.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    "stellantis": {
        "logo": "https://cdn.brandfetch.io/stellantis.com/w/400/h/400",
        "color": "#000000",
        "category": "Auto"
    },
    # ---- Additional car brands ----
    "alfa": {"logo": "https://cdn.brandfetch.io/alfaromeo.com/w/400/h/400", "color": "#003D7A", "category": "Auto"},
    "daewoo": {"logo": "https://cdn.brandfetch.io/daewoomotor.com/w/400/h/400", "color": "#0066CC", "category": "Auto"},
    "datsun": {"logo": "https://cdn.brandfetch.io/datsun.com/w/400/h/400", "color": "#003399", "category": "Auto"},
    "lancia": {"logo": "https://cdn.brandfetch.io/lancia.com/w/400/h/400", "color": "#003399", "category": "Auto"},
    "geely": {"logo": "https://cdn.brandfetch.io/geely.com/w/400/h/400", "color": "#003D7A", "category": "Auto"},
    "chery": {"logo": "https://cdn.brandfetch.io/cheryinternational.com/w/400/h/400", "color": "#003D7A", "category": "Auto"},
    "gac": {"logo": "https://cdn.brandfetch.io/gacgroup.com/w/400/h/400", "color": "#003D7A", "category": "Auto"},
    "morgan": {"logo": "https://cdn.brandfetch.io/morgan-motor.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "tvr": {"logo": "https://cdn.brandfetch.io/tvr.co.uk/w/400/h/400", "color": "#007BFF", "category": "Auto"},
    "saipa": {"logo": "https://cdn.brandfetch.io/saipacorp.com/w/400/h/400", "color": "#003D7A", "category": "Auto"},
    "lada": {"logo": "https://cdn.brandfetch.io/lada.ru/w/400/h/400", "color": "#CC0000", "category": "Auto"},
    "dongfeng": {"logo": "https://cdn.brandfetch.io/dongfeng-global.com/w/400/h/400", "color": "#003D7A", "category": "Auto"},
    "gaz": {"logo": "https://cdn.brandfetch.io/azgaz.ru/w/400/h/400", "color": "#003D7A", "category": "Auto"},
    "tatra": {"logo": "https://cdn.brandfetch.io/tatra.cz/w/400/h/400", "color": "#DD0000", "category": "Auto"},
    "\u0161koda": {"logo": "https://cdn.brandfetch.io/skoda-auto.com/w/400/h/400", "color": "#003300", "category": "Auto"},
    "willys": {"logo": "https://cdn.brandfetch.io/jeep.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "avtovaz": {"logo": "https://cdn.brandfetch.io/lada.ru/w/400/h/400", "color": "#CC0000", "category": "Auto"},
    # ---- Vintage/classic car brands ----
    "ac": {"logo": "https://cdn.brandfetch.io/accars.eu/w/400/h/400", "color": "#000000", "category": "Auto"},
    "alvis": {"logo": "https://cdn.brandfetch.io/thealviscarcompany.co.uk/w/400/h/400", "color": "#000000", "category": "Auto"},
    "iso": {"logo": "https://cdn.brandfetch.io/isorivolta.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "panhard": {"logo": "https://cdn.brandfetch.io/panhard.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "studebaker": {"logo": "https://cdn.brandfetch.io/studebaker.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "nash": {"logo": "https://cdn.brandfetch.io/nashmotors.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "mercury": {"logo": "https://cdn.brandfetch.io/mercury.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "packard": {"logo": "https://cdn.brandfetch.io/packardmotorcar.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "zastava": {"logo": "https://cdn.brandfetch.io/zastava.rs/w/400/h/400", "color": "#CC0000", "category": "Auto"},
    "bizzarrini": {"logo": "https://cdn.brandfetch.io/bizzarrini.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "bolwell": {"logo": "https://cdn.brandfetch.io/bolwell.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "brabham": {"logo": "https://cdn.brandfetch.io/brabham.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "champion": {"logo": "https://cdn.brandfetch.io/championautoparts.com/w/400/h/400", "color": "#CC0000", "category": "Auto"},
    "hispano-suiza": {"logo": "https://cdn.brandfetch.io/hispano-suiza.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    # ---- Tech/electronics brands ----
    "brionvega": {"logo": "https://cdn.brandfetch.io/brionvega.com/w/400/h/400", "color": "#000000", "category": "Electronics"},
    "videoton": {"logo": "https://cdn.brandfetch.io/videoton.hu/w/400/h/400", "color": "#003399", "category": "Electronics"},
    "tandy": {"logo": "https://cdn.brandfetch.io/radioshack.com/w/400/h/400", "color": "#CC0000", "category": "Other"},
    "mitsuoka": {"logo": "https://cdn.brandfetch.io/mitsuoka-motor.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "great": {"logo": "https://cdn.brandfetch.io/gwm-global.com/w/400/h/400", "color": "#003D7A", "category": "Auto"},
    "leaf": {"logo": "https://cdn.brandfetch.io/leafgroup.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "general": {"logo": "https://cdn.brandfetch.io/gm.com/w/400/h/400", "color": "#1A1A1A", "category": "Auto"},

    # ---- More obscure car / tech brands ----
    "adam": {"logo": "https://cdn.brandfetch.io/adamcars.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "air": {"logo": "https://cdn.brandfetch.io/air-car.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "alan": {"logo": "https://cdn.brandfetch.io/alancars.co.uk/w/400/h/400", "color": "#000000", "category": "Auto"},
    "american": {"logo": "https://cdn.brandfetch.io/theamc.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "asia": {"logo": "https://cdn.brandfetch.io/kia.com/w/400/h/400", "color": "#05141F", "category": "Auto"},
    "austro-daimler": {"logo": "https://cdn.brandfetch.io/austro-daimler.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "bandini": {"logo": "https://cdn.brandfetch.io/bandinicars.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "benz": {"logo": "https://cdn.brandfetch.io/mercedes-benz.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "bitter": {"logo": "https://cdn.brandfetch.io/bittercars.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "british": {"logo": "https://cdn.brandfetch.io/britishmotors.co.uk/w/400/h/400", "color": "#000000", "category": "Auto"},
    "carver": {"logo": "https://cdn.brandfetch.io/carver-world.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "checker": {"logo": "https://cdn.brandfetch.io/checkercab.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "coda": {"logo": "https://cdn.simpleicons.org/coda", "color": "#000000", "category": "Auto"},
    "data": {"logo": "https://cdn.brandfetch.io/tata.com/w/400/h/400", "color": "#4860A0", "category": "Other"},
    "de": {"logo": "https://cdn.brandfetch.io/detomaso-automobili.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "delage": {"logo": "https://cdn.brandfetch.io/delage.fr/w/400/h/400", "color": "#000000", "category": "Auto"},
    "derways": {"logo": "https://cdn.brandfetch.io/derways-auto.ru/w/400/h/400", "color": "#000000", "category": "Auto"},
    "facel": {"logo": "https://cdn.brandfetch.io/facel-vega.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "hanomag": {"logo": "https://cdn.brandfetch.io/hanomag.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "horch": {"logo": "https://cdn.brandfetch.io/horch.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "isdera": {"logo": "https://cdn.brandfetch.io/isdera.de/w/400/h/400", "color": "#000000", "category": "Auto"},
    "laurin": {"logo": "https://cdn.brandfetch.io/skoda-auto.com/w/400/h/400", "color": "#003300", "category": "Auto"},
    "lion-peugeot": {"logo": "https://cdn.brandfetch.io/peugeot.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "matra": {"logo": "https://cdn.brandfetch.io/groupe-matra.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "melkus": {"logo": "https://cdn.brandfetch.io/melkus.de/w/400/h/400", "color": "#000000", "category": "Auto"},
    "mia": {"logo": "https://cdn.brandfetch.io/mia-electric.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "moskvitch": {"logo": "https://cdn.brandfetch.io/moskvich.ru/w/400/h/400", "color": "#CC0000", "category": "Auto"},
    "nsu": {"logo": "https://cdn.brandfetch.io/nsu-classic.de/w/400/h/400", "color": "#000000", "category": "Auto"},
    "puch": {"logo": "https://cdn.brandfetch.io/piaggio.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "riley": {"logo": "https://cdn.brandfetch.io/riley.cars/w/400/h/400", "color": "#000000", "category": "Auto"},
    "rubery": {"logo": "https://cdn.brandfetch.io/ruberyowen.co.uk/w/400/h/400", "color": "#000000", "category": "Other"},
    "sampo": {"logo": "https://cdn.brandfetch.io/sampo.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "sevel": {"logo": "https://cdn.brandfetch.io/sevel-sud.it/w/400/h/400", "color": "#000000", "category": "Auto"},
    "standard": {"logo": "https://cdn.brandfetch.io/standardmotorcompany.co.uk/w/400/h/400", "color": "#000000", "category": "Auto"},
    "steyr-daimler-puch": {"logo": "https://cdn.brandfetch.io/piaggio.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "uaz": {"logo": "https://cdn.brandfetch.io/uaz.ru/w/400/h/400", "color": "#000000", "category": "Auto"},
    "vector": {"logo": "https://cdn.brandfetch.io/vector-motors.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "wolseley": {"logo": "https://cdn.brandfetch.io/wolseleycars.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "zaz": {"logo": "https://cdn.brandfetch.io/zaz.ua/w/400/h/400", "color": "#000000", "category": "Auto"},
    "zil": {"logo": "https://cdn.brandfetch.io/zil.ru/w/400/h/400", "color": "#000000", "category": "Auto"},
    "zndapp": {"logo": "https://cdn.brandfetch.io/zuendapp.de/w/400/h/400", "color": "#000000", "category": "Auto"},
    "koda": {"logo": "https://cdn.brandfetch.io/skoda-auto.com/w/400/h/400", "color": "#003300", "category": "Auto"},
    "\u0161koda": {"logo": "https://cdn.brandfetch.io/skoda-auto.com/w/400/h/400", "color": "#003300", "category": "Auto"},

    # ---- Final obscure brands (researched on brandfetch) ----
    "auto": {"logo": "https://cdn.brandfetch.io/auto-union.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "automobilwerk": {"logo": "https://cdn.brandfetch.io/awe-museum.de/w/400/h/400", "color": "#000000", "category": "Auto"},
    "camille": {"logo": "https://cdn.brandfetch.io/lajamaiscontente.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "cockerell": {"logo": "https://cdn.brandfetch.io/hoverspeed.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "industrieverband": {"logo": "https://cdn.brandfetch.io/ifa.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "k-1": {"logo": "https://cdn.brandfetch.io/k1-attack.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "kg": {"logo": "https://cdn.brandfetch.io/kg-mobility.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "koninklijke": {"logo": "https://cdn.brandfetch.io/philips.com/w/400/h/400", "color": "#000000", "category": "TVs", "sub_categories": ["Electronics", "Appliances"]},
    "lmx": {"logo": "https://cdn.brandfetch.io/lmxregistrostorico.it/w/400/h/400", "color": "#000000", "category": "Auto"},
    "ss": {"logo": "https://cdn.brandfetch.io/jaguar.com/w/400/h/400", "color": "#000000", "category": "Auto"},
    "zato": {"logo": "https://cdn.brandfetch.io/zato.de/w/400/h/400", "color": "#000000", "category": "Other"},
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

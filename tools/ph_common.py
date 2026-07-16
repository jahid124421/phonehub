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
        "logo": "https://cdn.brandfetch.io/apple.com/w/400/h/400",
        "color": "#000000",
        "category": "Premium"
    },
    "samsung": {
        "logo": "https://cdn.brandfetch.io/samsung.com/w/400/h/400",
        "color": "#1428A0",
        "category": "Premium"
    },
    "google": {
        "logo": "https://cdn.brandfetch.io/google.com/w/400/h/400",
        "color": "#4285F4",
        "category": "Premium"
    },
    "xiaomi": {
        "logo": "https://cdn.brandfetch.io/xiaomi.com/w/400/h/400",
        "color": "#FF6900",
        "category": "Value"
    },
    "oneplus": {
        "logo": "https://cdn.brandfetch.io/oneplus.com/w/400/h/400",
        "color": "#EB0028",
        "category": "Mid-Range"
    },
    "nothing": {
        "logo": "https://cdn.simpleicons.org/nothing/000000",
        "color": "#000000",
        "category": "Mid-Range"
    },
    "vivo": {
        "logo": "https://cdn.brandfetch.io/vivo.com/w/400/h/400",
        "color": "#0C64E8",
        "category": "Value"
    },
    "realme": {
        "logo": "https://cdn.simpleicons.org/realme/FFC600",
        "color": "#FFC600",
        "category": "Budget"
    },
    "oppo": {
        "logo": "https://cdn.brandfetch.io/oppo.com/w/400/h/400",
        "color": "#1BA784",
        "category": "Value"
    },
    "motorola": {
        "logo": "https://cdn.brandfetch.io/motorola.com/w/400/h/400",
        "color": "#5C92FC",
        "category": "Value"
    },
    "sony": {
        "logo": "https://cdn.brandfetch.io/sony.com/w/400/h/400",
        "color": "#0B0B0B",
        "category": "Premium"
    },
    "nokia": {
        "logo": "https://cdn.brandfetch.io/nokia.com/w/400/h/400",
        "color": "#124191",
        "category": "Budget"
    },
    "honor": {
        "logo": "https://cdn.simpleicons.org/honor/00B0E9",
        "color": "#00B0E9",
        "category": "Value"
    },
    "asus": {
        "logo": "https://cdn.brandfetch.io/asus.com/w/400/h/400",
        "color": "#000000",
        "category": "Gaming"
    },
    "huawei": {
        "logo": "https://cdn.brandfetch.io/huawei.com/w/400/h/400",
        "color": "#C7000B",
        "category": "Value"
    },
    "lenovo": {
        "logo": "https://cdn.brandfetch.io/lenovo.com/w/400/h/400",
        "color": "#E2231A",
        "category": "Value"
    },
    "lg": {
        "logo": "https://cdn.brandfetch.io/lg.com/w/400/h/400",
        "color": "#A50034",
        "category": "Value"
    },
    "tcl": {
        "logo": "https://cdn.brandfetch.io/tcl.com/w/400/h/400",
        "color": "#0071BC",
        "category": "Budget"
    },
    "microsoft": {
        "logo": "https://cdn.brandfetch.io/microsoft.com/w/400/h/400",
        "color": "#00A4EF",
        "category": "Premium"
    },
    # ---- Other brands (electronics/computing/wearables) ----
    "medion": {
        "logo": "https://cdn.brandfetch.io/medion.com/w/400/h/400",
        "color": "#0066CC",
        "category": "Budget"
    },
    "toshiba": {
        "logo": "https://cdn.brandfetch.io/toshiba.com/w/400/h/400",
        "color": "#FF0000",
        "category": "Value"
    },
    "compaq": {
        "logo": "https://cdn.brandfetch.io/compaq.com/w/400/h/400",
        "color": "#0066CC",
        "category": "Value"
    },
    "ibm": {
        "logo": "https://cdn.brandfetch.io/ibm.com/w/400/h/400",
        "color": "#006699",
        "category": "Premium"
    },
    "pine64": {
        "logo": "https://cdn.simpleicons.org/pine64/000000",
        "color": "#000000",
        "category": "Budget"
    },
    "acer": {
        "logo": "https://cdn.brandfetch.io/acer.com/w/400/h/400",
        "color": "#83B81A",
        "category": "Value"
    },
    "dell": {
        "logo": "https://cdn.brandfetch.io/dell.com/w/400/h/400",
        "color": "#007DB8",
        "category": "Premium"
    },
    "garmin": {
        "logo": "https://cdn.brandfetch.io/garmin.com/w/400/h/400",
        "color": "#000000",
        "category": "Value"
    },
    "withings": {
        "logo": "https://cdn.brandfetch.io/withings.com/w/400/h/400",
        "color": "#000000",
        "category": "Value"
    },
    "fujifilm": {
        "logo": "https://cdn.brandfetch.io/fujifilm.com/w/400/h/400",
        "color": "#ED1C24",
        "category": "Value"
    },
    "logitech": {
        "logo": "https://cdn.brandfetch.io/logitech.com/w/400/h/400",
        "color": "#00B8FC",
        "category": "Mid-Range"
    },
    "hewlett-packard": {
        "logo": "https://cdn.brandfetch.io/hp.com/w/400/h/400",
        "color": "#0096D6",
        "category": "Value"
    },
    "suunto": {
        "logo": "https://cdn.brandfetch.io/suunto.com/w/400/h/400",
        "color": "#000000",
        "category": "Value"
    },
    "polar": {
        "logo": "https://cdn.brandfetch.io/polar.com/w/400/h/400",
        "color": "#000000",
        "category": "Value"
    },
    # ---- Car brands ----
    "renault": {
        "logo": "https://cdn.brandfetch.io/renault.com/w/400/h/400",
        "color": "#FFCC00",
        "category": "Other"
    },
    "volkswagen": {
        "logo": "https://cdn.brandfetch.io/volkswagen.com/w/400/h/400",
        "color": "#001E50",
        "category": "Other"
    },
    "rolls-royce": {
        "logo": "https://cdn.brandfetch.io/rolls-royce.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "ferrari": {
        "logo": "https://cdn.brandfetch.io/ferrari.com/w/400/h/400",
        "color": "#FF2800",
        "category": "Other"
    },
    "peugeot": {
        "logo": "https://cdn.brandfetch.io/peugeot.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "mitsubishi": {
        "logo": "https://cdn.brandfetch.io/mitsubishi.com/w/400/h/400",
        "color": "#E2001A",
        "category": "Other"
    },
    "subaru": {
        "logo": "https://cdn.brandfetch.io/subaru.com/w/400/h/400",
        "color": "#013C7A",
        "category": "Other"
    },
    "toyota": {
        "logo": "https://cdn.brandfetch.io/toyota.com/w/400/h/400",
        "color": "#D31017",
        "category": "Other"
    },
    "porsche": {
        "logo": "https://cdn.brandfetch.io/porsche.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "jaguar": {
        "logo": "https://cdn.brandfetch.io/jaguar.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "mazda": {
        "logo": "https://cdn.brandfetch.io/mazda.com/w/400/h/400",
        "color": "#101010",
        "category": "Other"
    },
    "honda": {
        "logo": "https://cdn.brandfetch.io/honda.com/w/400/h/400",
        "color": "#E1001A",
        "category": "Other"
    },
    "dodge": {
        "logo": "https://cdn.brandfetch.io/dodge.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "fiat": {
        "logo": "https://cdn.brandfetch.io/fiat.com/w/400/h/400",
        "color": "#AA001C",
        "category": "Other"
    },
    "ford": {
        "logo": "https://cdn.brandfetch.io/ford.com/w/400/h/400",
        "color": "#003D79",
        "category": "Other"
    },
    "daihatsu": {
        "logo": "https://cdn.brandfetch.io/daihatsu.com/w/400/h/400",
        "color": "#D50000",
        "category": "Other"
    },
    "audi": {
        "logo": "https://cdn.brandfetch.io/audi.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "bugatti": {
        "logo": "https://cdn.brandfetch.io/bugatti.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "nissan": {
        "logo": "https://cdn.brandfetch.io/nissan.com/w/400/h/400",
        "color": "#C3002F",
        "category": "Other"
    },
    "bmw": {
        "logo": "https://cdn.brandfetch.io/bmw.com/w/400/h/400",
        "color": "#0066B1",
        "category": "Other"
    },
    "opel": {
        "logo": "https://cdn.brandfetch.io/opel.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "mercedes-benz": {
        "logo": "https://cdn.brandfetch.io/mercedes-benz.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "cadillac": {
        "logo": "https://cdn.brandfetch.io/cadillac.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "delorean": {
        "logo": "https://cdn.brandfetch.io/delorean.com/w/400/h/400",
        "color": "#555555",
        "category": "Other"
    },
    "lotus": {
        "logo": "https://cdn.brandfetch.io/lotuscars.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "volvo": {
        "logo": "https://cdn.brandfetch.io/volvo.com/w/400/h/400",
        "color": "#003057",
        "category": "Other"
    },
    "maserati": {
        "logo": "https://cdn.brandfetch.io/maserati.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "saab": {
        "logo": "https://cdn.brandfetch.io/saab.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "kia": {
        "logo": "https://cdn.brandfetch.io/kia.com/w/400/h/400",
        "color": "#05141F",
        "category": "Other"
    },
    "mg": {
        "logo": "https://cdn.brandfetch.io/mg.co.uk/w/400/h/400",
        "color": "#CC0000",
        "category": "Other"
    },
    "hyundai": {
        "logo": "https://cdn.brandfetch.io/hyundai.com/w/400/h/400",
        "color": "#002C5F",
        "category": "Other"
    },
    "isuzu": {
        "logo": "https://cdn.brandfetch.io/isuzu.com/w/400/h/400",
        "color": "#E3001B",
        "category": "Other"
    },
    "lamborghini": {
        "logo": "https://cdn.brandfetch.io/lamborghini.com/w/400/h/400",
        "color": "#DDB321",
        "category": "Other"
    },
    "brabus": {
        "logo": "https://cdn.brandfetch.io/brabus.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "aston": {
        "logo": "https://cdn.brandfetch.io/astonmartin.com/w/400/h/400",
        "color": "#00665E",
        "category": "Other"
    },
    "tata": {
        "logo": "https://cdn.brandfetch.io/tata.com/w/400/h/400",
        "color": "#4860A0",
        "category": "Other"
    },
    "citroën": {
        "logo": "https://cdn.brandfetch.io/citroen.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "seat": {
        "logo": "https://cdn.brandfetch.io/seat.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "byd": {
        "logo": "https://cdn.brandfetch.io/byd.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "rimac": {
        "logo": "https://cdn.brandfetch.io/rimac.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "abarth": {
        "logo": "https://cdn.brandfetch.io/abarth.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "gm": {
        "logo": "https://cdn.brandfetch.io/gm.com/w/400/h/400",
        "color": "#1A1A1A",
        "category": "Other"
    },
    "daimler-benz": {
        "logo": "https://cdn.brandfetch.io/mercedes-benz.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "daimler": {
        "logo": "https://cdn.brandfetch.io/mercedes-benz.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "piaggio": {
        "logo": "https://cdn.brandfetch.io/piaggio.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    # ---- Retro / legacy tech brands ----
    "zenith": {
        "logo": "https://cdn.brandfetch.io/zenith.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "sega": {
        "logo": "https://cdn.brandfetch.io/sega.com/w/400/h/400",
        "color": "#003399",
        "category": "Other"
    },
    "tesla": {
        "logo": "https://cdn.brandfetch.io/tesla.com/w/400/h/400",
        "color": "#CC0000",
        "category": "Other"
    },
    "sinclair": {
        "logo": "https://cdn.simpleicons.org/sinclair/000000",
        "color": "#000000",
        "category": "Other"
    },
    "rca": {
        "logo": "https://cdn.brandfetch.io/rca.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "magnavox": {
        "logo": "https://cdn.simpleicons.org/magnavox/000000",
        "color": "#000000",
        "category": "Other"
    },
    "sharp-s": {
        "logo": "https://cdn.brandfetch.io/sharp.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    # ---- Misc brands (keep in Other) ----
    "bristol": {
        "logo": "https://cdn.brandfetch.io/bristolcars.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "alpina": {
        "logo": "https://cdn.brandfetch.io/alpina.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    "stellantis": {
        "logo": "https://cdn.brandfetch.io/stellantis.com/w/400/h/400",
        "color": "#000000",
        "category": "Other"
    },
    # ---- Additional car brands ----
    "alfa": {"logo": "https://cdn.brandfetch.io/alfaromeo.com/w/400/h/400", "color": "#003D7A", "category": "Other"},
    "daewoo": {"logo": "https://cdn.brandfetch.io/daewoomotor.com/w/400/h/400", "color": "#0066CC", "category": "Other"},
    "datsun": {"logo": "https://cdn.brandfetch.io/datsun.com/w/400/h/400", "color": "#003399", "category": "Other"},
    "lancia": {"logo": "https://cdn.brandfetch.io/lancia.com/w/400/h/400", "color": "#003399", "category": "Other"},
    "geely": {"logo": "https://cdn.brandfetch.io/geely.com/w/400/h/400", "color": "#003D7A", "category": "Other"},
    "chery": {"logo": "https://cdn.brandfetch.io/cheryinternational.com/w/400/h/400", "color": "#003D7A", "category": "Other"},
    "gac": {"logo": "https://cdn.brandfetch.io/gacgroup.com/w/400/h/400", "color": "#003D7A", "category": "Other"},
    "morgan": {"logo": "https://cdn.brandfetch.io/morgan-motor.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "tvr": {"logo": "https://cdn.brandfetch.io/tvr.co.uk/w/400/h/400", "color": "#007BFF", "category": "Other"},
    "saipa": {"logo": "https://cdn.brandfetch.io/saipacorp.com/w/400/h/400", "color": "#003D7A", "category": "Other"},
    "lada": {"logo": "https://cdn.brandfetch.io/lada.ru/w/400/h/400", "color": "#CC0000", "category": "Other"},
    "dongfeng": {"logo": "https://cdn.brandfetch.io/dongfeng-global.com/w/400/h/400", "color": "#003D7A", "category": "Other"},
    "gaz": {"logo": "https://cdn.brandfetch.io/azgaz.ru/w/400/h/400", "color": "#003D7A", "category": "Other"},
    "tatra": {"logo": "https://cdn.brandfetch.io/tatra.cz/w/400/h/400", "color": "#DD0000", "category": "Other"},
    "\u0161koda": {"logo": "https://cdn.brandfetch.io/skoda-auto.com/w/400/h/400", "color": "#003300", "category": "Other"},
    "willys": {"logo": "https://cdn.brandfetch.io/jeep.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "avtovaz": {"logo": "https://cdn.brandfetch.io/lada.ru/w/400/h/400", "color": "#CC0000", "category": "Other"},
    # ---- Vintage/classic car brands ----
    "ac": {"logo": "https://cdn.brandfetch.io/accars.eu/w/400/h/400", "color": "#000000", "category": "Other"},
    "alvis": {"logo": "https://cdn.brandfetch.io/thealviscarcompany.co.uk/w/400/h/400", "color": "#000000", "category": "Other"},
    "iso": {"logo": "https://cdn.brandfetch.io/isorivolta.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "panhard": {"logo": "https://cdn.brandfetch.io/panhard.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "studebaker": {"logo": "https://cdn.brandfetch.io/studebaker.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "nash": {"logo": "https://cdn.brandfetch.io/nashmotors.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "mercury": {"logo": "https://cdn.brandfetch.io/mercury.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "packard": {"logo": "https://cdn.brandfetch.io/packardmotorcar.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "zastava": {"logo": "https://cdn.brandfetch.io/zastava.rs/w/400/h/400", "color": "#CC0000", "category": "Other"},
    "bizzarrini": {"logo": "https://cdn.brandfetch.io/bizzarrini.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "bolwell": {"logo": "https://cdn.brandfetch.io/bolwell.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "brabham": {"logo": "https://cdn.brandfetch.io/brabham.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "champion": {"logo": "https://cdn.brandfetch.io/championautoparts.com/w/400/h/400", "color": "#CC0000", "category": "Other"},
    "hispano-suiza": {"logo": "https://cdn.brandfetch.io/hispano-suiza.com/w/400/h/400", "color": "#000000", "category": "Other"},
    # ---- Tech/electronics brands ----
    "brionvega": {"logo": "https://cdn.brandfetch.io/brionvega.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "videoton": {"logo": "https://cdn.brandfetch.io/videoton.hu/w/400/h/400", "color": "#003399", "category": "Other"},
    "tandy": {"logo": "https://cdn.brandfetch.io/radioshack.com/w/400/h/400", "color": "#CC0000", "category": "Other"},
    "mitsuoka": {"logo": "https://cdn.brandfetch.io/mitsuoka-motor.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "great": {"logo": "https://cdn.brandfetch.io/gwm-global.com/w/400/h/400", "color": "#003D7A", "category": "Other"},
    "leaf": {"logo": "https://cdn.brandfetch.io/leafgroup.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "general": {"logo": "https://cdn.brandfetch.io/gm.com/w/400/h/400", "color": "#1A1A1A", "category": "Other"},

    # ---- More obscure car / tech brands ----
    "adam": {"logo": "https://cdn.brandfetch.io/adamcars.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "air": {"logo": "https://cdn.brandfetch.io/air-car.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "alan": {"logo": "https://cdn.brandfetch.io/alancars.co.uk/w/400/h/400", "color": "#000000", "category": "Other"},
    "american": {"logo": "https://cdn.brandfetch.io/theamc.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "asia": {"logo": "https://cdn.brandfetch.io/kia.com/w/400/h/400", "color": "#05141F", "category": "Other"},
    "austro-daimler": {"logo": "https://cdn.brandfetch.io/austro-daimler.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "bandini": {"logo": "https://cdn.brandfetch.io/bandinicars.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "benz": {"logo": "https://cdn.brandfetch.io/mercedes-benz.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "bitter": {"logo": "https://cdn.brandfetch.io/bittercars.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "british": {"logo": "https://cdn.brandfetch.io/britishmotors.co.uk/w/400/h/400", "color": "#000000", "category": "Other"},
    "carver": {"logo": "https://cdn.brandfetch.io/carver-world.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "checker": {"logo": "https://cdn.brandfetch.io/checkercab.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "coda": {"logo": "https://cdn.brandfetch.io/codaautomotive.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "data": {"logo": "https://cdn.brandfetch.io/tata.com/w/400/h/400", "color": "#4860A0", "category": "Other"},
    "de": {"logo": "https://cdn.brandfetch.io/detomaso-automobili.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "delage": {"logo": "https://cdn.brandfetch.io/delage.fr/w/400/h/400", "color": "#000000", "category": "Other"},
    "derways": {"logo": "https://cdn.brandfetch.io/derways-auto.ru/w/400/h/400", "color": "#000000", "category": "Other"},
    "facel": {"logo": "https://cdn.brandfetch.io/facel-vega.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "hanomag": {"logo": "https://cdn.brandfetch.io/hanomag.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "horch": {"logo": "https://cdn.brandfetch.io/horch.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "isdera": {"logo": "https://cdn.brandfetch.io/isdera.de/w/400/h/400", "color": "#000000", "category": "Other"},
    "laurin": {"logo": "https://cdn.brandfetch.io/skoda-auto.com/w/400/h/400", "color": "#003300", "category": "Other"},
    "lion-peugeot": {"logo": "https://cdn.brandfetch.io/peugeot.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "matra": {"logo": "https://cdn.brandfetch.io/groupe-matra.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "melkus": {"logo": "https://cdn.brandfetch.io/melkus.de/w/400/h/400", "color": "#000000", "category": "Other"},
    "mia": {"logo": "https://cdn.brandfetch.io/mia-electric.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "moskvitch": {"logo": "https://cdn.brandfetch.io/moskvich.ru/w/400/h/400", "color": "#CC0000", "category": "Other"},
    "nsu": {"logo": "https://cdn.brandfetch.io/nsu-classic.de/w/400/h/400", "color": "#000000", "category": "Other"},
    "puch": {"logo": "https://cdn.brandfetch.io/piaggio.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "riley": {"logo": "https://cdn.brandfetch.io/riley.cars/w/400/h/400", "color": "#000000", "category": "Other"},
    "rubery": {"logo": "https://cdn.brandfetch.io/ruberyowen.co.uk/w/400/h/400", "color": "#000000", "category": "Other"},
    "sampo": {"logo": "https://cdn.brandfetch.io/sampo.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "sevel": {"logo": "https://cdn.brandfetch.io/sevel-sud.it/w/400/h/400", "color": "#000000", "category": "Other"},
    "standard": {"logo": "https://cdn.brandfetch.io/standardmotorcompany.co.uk/w/400/h/400", "color": "#000000", "category": "Other"},
    "steyr-daimler-puch": {"logo": "https://cdn.brandfetch.io/piaggio.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "uaz": {"logo": "https://cdn.brandfetch.io/uaz.ru/w/400/h/400", "color": "#000000", "category": "Other"},
    "vector": {"logo": "https://cdn.brandfetch.io/vector-motors.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "wolseley": {"logo": "https://cdn.brandfetch.io/wolseleycars.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "zaz": {"logo": "https://cdn.brandfetch.io/zaz.ua/w/400/h/400", "color": "#000000", "category": "Other"},
    "zil": {"logo": "https://cdn.brandfetch.io/zil.ru/w/400/h/400", "color": "#000000", "category": "Other"},
    "zndapp": {"logo": "https://cdn.brandfetch.io/zuendapp.de/w/400/h/400", "color": "#000000", "category": "Other"},
    "koda": {"logo": "https://cdn.brandfetch.io/skoda-auto.com/w/400/h/400", "color": "#003300", "category": "Other"},
    "\u0161koda": {"logo": "https://cdn.brandfetch.io/skoda-auto.com/w/400/h/400", "color": "#003300", "category": "Other"},

    # ---- Final obscure brands (researched on brandfetch) ----
    "auto": {"logo": "https://cdn.brandfetch.io/auto-union.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "automobilwerk": {"logo": "https://cdn.brandfetch.io/awe-museum.de/w/400/h/400", "color": "#000000", "category": "Other"},
    "camille": {"logo": "https://cdn.brandfetch.io/lajamaiscontente.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "cockerell": {"logo": "https://cdn.brandfetch.io/hoverspeed.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "industrieverband": {"logo": "https://cdn.brandfetch.io/ifa.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "k-1": {"logo": "https://cdn.brandfetch.io/k1-attack.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "kg": {"logo": "https://cdn.brandfetch.io/kg-mobility.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "koninklijke": {"logo": "https://cdn.brandfetch.io/philips.com/w/400/h/400", "color": "#000000", "category": "Other"},
    "lmx": {"logo": "https://cdn.brandfetch.io/lmxregistrostorico.it/w/400/h/400", "color": "#000000", "category": "Other"},
    "ss": {"logo": "https://cdn.brandfetch.io/jaguar.com/w/400/h/400", "color": "#000000", "category": "Other"},
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

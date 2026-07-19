"""
Firefox Cookie Extractor & OmniRoute Auto-Setup
Extracts cookies from Firefox browser and automatically adds them to OmniRoute
"""

import json
import sqlite3
import os
import sys
from pathlib import Path
import requests
from datetime import datetime

# Firefox profile paths
FIREFOX_PROFILES = {
    'windows': Path(os.getenv('APPDATA')) / 'Mozilla' / 'Firefox' / 'Profiles',
    'linux': Path.home() / '.mozilla' / 'firefox',
    'mac': Path.home() / 'Library' / 'Application Support' / 'Firefox' / 'Profiles'
}

# OmniRoute configuration
OMNIROUTE_URL = 'http://localhost:20128'
ADMIN_PASSWORD = 'CHANGEME'

# Provider to domain mapping
PROVIDER_DOMAINS = {
    'chatgpt-web': {
        'domain': 'chatgpt.com',
        'cookies': ['__Secure-next-auth.session-token.0', '__Secure-next-auth.session-token.1'],
        'name': 'ChatGPT Web'
    },
    'deepseek-web': {
        'domain': 'chat.deepseek.com',
        'cookies': ['ds_session_id'],
        'name': 'DeepSeek Web'
    },
    'dola-web': {
        'domain': 'dola.ai',
        'cookies': ['sessionid'],
        'name': 'Dola AI Web'
    },
    'gemini-web': {
        'domain': 'gemini.google.com',
        'cookies': ['__Secure-1PSID', '__Secure-1PSIDTS'],
        'name': 'Gemini Web'
    },
    'huggingchat': {
        'domain': 'huggingface.co',
        'cookies': ['token'],
        'name': 'HuggingChat'
    },
    'kimi-web': {
        'domain': 'kimi.moonshot.cn',
        'cookies': ['kimi-auth'],
        'name': 'Kimi Web'
    },
    'copilot-web': {
        'domain': 'copilot.microsoft.com',
        'cookies': ['_C_Auth', 'MUID'],
        'name': 'Microsoft Copilot Web'
    },
    'muse-spark-web': {
        'domain': 'meta.ai',
        'cookies': ['ecto_1_sess'],
        'name': 'Meta AI'
    },
    'qwen-web': {
        'domain': 'qwen.alibaba.com',
        'cookies': ['token'],
        'name': 'Qwen Web'
    },
    't3-web': {
        'domain': 't3.gg',
        'cookies': ['wos-session'],
        'name': 'T3.Chat'
    },
    'venice-web': {
        'domain': 'venice.ai',
        'cookies': ['__session'],
        'name': 'Venice AI'
    },
    'zai-web': {
        'domain': 'z.ai',
        'cookies': ['token'],
        'name': 'Z.AI'
    },
    'zenmux-free': {
        'domain': 'zenmux.ai',
        'cookies': ['sessionId'],
        'name': 'Zenmux AI'
    },
    'v0-vercel-web': {
        'domain': 'v0.dev',
        'cookies': ['user_session'],
        'name': 'v0 by Vercel'
    },
    'claude-web': {
        'domain': 'claude.ai',
        'cookies': ['sessionKey'],
        'name': 'Claude Web'
    },
    'perplexity-web': {
        'domain': 'perplexity.ai',
        'cookies': ['__Secure-next-auth.session-token'],
        'name': 'Perplexity Web'
    },
    'grok-web': {
        'domain': 'grok.com',
        'cookies': ['sso', 'sso-rw'],
        'name': 'Grok Web'
    },
    'poe-web': {
        'domain': 'poe.com',
        'cookies': ['p-b'],
        'name': 'Poe Web'
    },
}


def find_firefox_profile():
    """Find the default Firefox profile directory"""
    
    # Determine OS
    if sys.platform == 'win32':
        profile_base = FIREFOX_PROFILES['windows']
    elif sys.platform == 'darwin':
        profile_base = FIREFOX_PROFILES['mac']
    else:
        profile_base = FIREFOX_PROFILES['linux']
    
    if not profile_base.exists():
        print(f"❌ Firefox profile directory not found: {profile_base}")
        return None
    
    # Find default profile
    profiles = list(profile_base.glob('*.default*'))
    if not profiles:
        profiles = list(profile_base.glob('*'))
    
    if not profiles:
        print(f"❌ No Firefox profiles found in {profile_base}")
        return None
    
    # Use the first profile found (usually default)
    profile = profiles[0]
    print(f"✅ Found Firefox profile: {profile.name}")
    return profile


def extract_cookies_from_firefox(profile_dir):
    """Extract cookies from Firefox SQLite database"""
    
    cookies_db = profile_dir / 'cookies.sqlite'
    
    if not cookies_db.exists():
        print(f"❌ Firefox cookies database not found: {cookies_db}")
        return {}
    
    # Copy database to avoid locking issues
    import shutil
    temp_db = Path(__file__).parent / 'temp_cookies.sqlite'
    
    try:
        shutil.copy2(cookies_db, temp_db)
    except Exception as e:
        print(f"❌ Error copying Firefox database: {e}")
        print("💡 Make sure Firefox is closed and try again")
        return {}
    
    extracted_cookies = {}
    
    try:
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        # Query all cookies
        cursor.execute("""
            SELECT host, name, value, path, expiry 
            FROM moz_cookies 
            WHERE expiry > ?
        """, (int(datetime.now().timestamp()),))
        
        for row in cursor.fetchall():
            host, name, value, path, expiry = row
            
            # Match cookies to providers
            for provider_id, config in PROVIDER_DOMAINS.items():
                if config['domain'] in host and name in config['cookies']:
                    if provider_id not in extracted_cookies:
                        extracted_cookies[provider_id] = {}
                    extracted_cookies[provider_id][name] = value
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error reading Firefox cookies: {e}")
        return {}
    finally:
        # Clean up temp file
        if temp_db.exists():
            temp_db.unlink()
    
    return extracted_cookies


def format_cookie_string(cookies_dict):
    """Format cookies dict into cookie header string"""
    return '; '.join([f"{k}={v}" for k, v in cookies_dict.items()])


def login_to_omniroute():
    """Login to OmniRoute dashboard and get auth token"""
    
    try:
        response = requests.post(
            f'{OMNIROUTE_URL}/api/auth/login',
            json={'password': ADMIN_PASSWORD},
            timeout=10
        )
        
        if response.status_code != 200:
            print(f"❌ OmniRoute login failed: {response.status_code}")
            return None
        
        # Extract auth token from cookies
        cookies = response.cookies
        auth_token = cookies.get('auth_token')
        
        if not auth_token:
            print("❌ No auth token received from OmniRoute")
            return None
        
        print("✅ Logged into OmniRoute")
        return auth_token
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to OmniRoute - make sure it's running!")
        print("💡 Start OmniRoute: cd OmniRoute && npm run dev")
        return None
    except Exception as e:
        print(f"❌ Login error: {e}")
        return None


def get_existing_providers(auth_token):
    """Get list of existing providers from OmniRoute"""
    
    try:
        response = requests.get(
            f'{OMNIROUTE_URL}/api/providers',
            cookies={'auth_token': auth_token},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            return set(p['provider'] for p in data.get('providers', []))
        
        return set()
        
    except Exception as e:
        print(f"⚠️  Could not fetch existing providers: {e}")
        return set()


def add_provider_to_omniroute(auth_token, provider_id, cookie_string, provider_name):
    """Add a provider to OmniRoute with cookies"""
    
    try:
        response = requests.post(
            f'{OMNIROUTE_URL}/api/providers',
            json={
                'provider': provider_id,
                'apiKey': cookie_string,
                'name': provider_name,
                'providerSpecificData': {
                    'cookie': cookie_string
                }
            },
            cookies={'auth_token': auth_token},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            return {'success': True, 'data': response.json()}
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else {}
            return {'success': False, 'error': error_data.get('error', f'HTTP {response.status_code}')}
            
    except Exception as e:
        return {'success': False, 'error': str(e)}


def main():
    print("Firefox Cookie Extractor & OmniRoute Auto-Setup\n")
    print("=" * 70)
    
    # Step 1: Find Firefox profile
    print("\n📂 Step 1: Locating Firefox profile...")
    profile = find_firefox_profile()
    
    if not profile:
        print("\n❌ Could not find Firefox profile")
        print("💡 Make sure Firefox is installed")
        return
    
    print("=" * 70)
    
    # Step 2: Extract cookies
    print("\n🍪 Step 2: Extracting cookies from Firefox...")
    print("💡 Make sure Firefox is CLOSED before running this script!\n")
    
    cookies = extract_cookies_from_firefox(profile)
    
    if not cookies:
        print("⚠️  No cookies found for AI providers")
        print("💡 Make sure you're logged into the AI services in Firefox")
        return
    
    print(f"✅ Found cookies for {len(cookies)} providers:")
    for provider_id in cookies.keys():
        provider_name = PROVIDER_DOMAINS[provider_id]['name']
        print(f"   • {provider_name}")
    
    print("\n" + "=" * 70)
    
    # Step 3: Login to OmniRoute
    print("\n🔐 Step 3: Connecting to OmniRoute...")
    auth_token = login_to_omniroute()
    
    if not auth_token:
        return
    
    print("=" * 70)
    
    # Step 4: Get existing providers
    print("\n📊 Step 4: Checking existing providers...")
    existing = get_existing_providers(auth_token)
    print(f"Found {len(existing)} existing providers")
    
    print("\n" + "=" * 70)
    
    # Step 5: Add providers
    print("\n🚀 Step 5: Adding providers to OmniRoute...\n")
    
    results = {
        'added': [],
        'skipped': [],
        'failed': []
    }
    
    for provider_id, provider_cookies in cookies.items():
        config = PROVIDER_DOMAINS[provider_id]
        provider_name = config['name']
        
        print(f"{provider_name}... ", end='', flush=True)
        
        # Skip if already exists
        if provider_id in existing:
            print("ℹ️  Already exists")
            results['skipped'].append(provider_name)
            continue
        
        # Format cookie string
        cookie_string = format_cookie_string(provider_cookies)
        
        # Add provider
        result = add_provider_to_omniroute(auth_token, provider_id, cookie_string, provider_name)
        
        if result['success']:
            print("✅ Added!")
            results['added'].append(provider_name)
        else:
            print(f"❌ Failed: {result['error']}")
            results['failed'].append({'name': provider_name, 'error': result['error']})
    
    # Step 6: Summary
    print("\n" + "=" * 70)
    print("📊 SETUP COMPLETE!\n")
    
    print(f"✅ Successfully Added: {len(results['added'])}")
    for name in results['added']:
        print(f"   • {name}")
    
    if results['skipped']:
        print(f"\n⚠️  Skipped: {len(results['skipped'])}")
        for name in results['skipped']:
            print(f"   • {name}")
    
    if results['failed']:
        print(f"\n❌ Failed: {len(results['failed'])}")
        for item in results['failed']:
            print(f"   • {item['name']}: {item['error']}")
    
    print("\n" + "=" * 70)
    
    if results['added']:
        print(f"\n🎉 SUCCESS! {len(results['added'])} providers added to OmniRoute!")
        print(f"\n🌐 Open dashboard: {OMNIROUTE_URL}")
        print("   View your providers in: Providers → Manage\n")
    
    # Save results
    results_file = Path(__file__).parent / 'firefox_extraction_results.json'
    with open(results_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'omniroute_url': OMNIROUTE_URL,
            'firefox_profile': str(profile),
            'results': results
        }, f, indent=2)
    
    print(f"📄 Results saved to: firefox_extraction_results.json\n")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()

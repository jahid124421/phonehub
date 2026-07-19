/**
 * Automatically Add Cookie Providers to OmniRoute
 * This script logs in and adds all cookie providers automatically
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// OmniRoute API configuration
const OMNIROUTE_BASE_URL = process.env.OMNIROUTE_BASE_URL || 'http://localhost:20128';
const ADMIN_PASSWORD = process.env.INITIAL_PASSWORD || 'CHANGEME';

// Provider configurations - ALL 14 providers from your cookies
const PROVIDERS_TO_ADD = {
  'chatgpt-web': {
    name: 'ChatGPT Web',
    cookieKey: '__Secure-next-auth.session-token',
    providerId: 'chatgpt-web',
  },
  'deepseek-web': {
    name: 'DeepSeek Web', 
    cookieKey: 'ds_session_id',
    providerId: 'deepseek-web',
  },
  'dola-web': {
    name: 'Dola AI Web',
    cookieKey: 'sessionid',
    providerId: 'dola-web',
  },
  'gemini-web': {
    name: 'Gemini Web',
    cookieKey: '__Secure-1PSID',
    providerId: 'gemini-web',
  },
  'huggingchat': {
    name: 'HuggingChat',
    cookieKey: 'token',
    providerId: 'huggingchat',
  },
  'kimi-web': {
    name: 'Kimi Web',
    cookieKey: 'kimi-auth',
    providerId: 'kimi-web',
  },
  'copilot-web': {
    name: 'Microsoft Copilot Web',
    cookieKey: '_C_Auth',
    providerId: 'copilot-web',
  },
  'muse-spark-web': {
    name: 'Meta AI',
    cookieKey: 'ecto_1_sess',
    providerId: 'muse-spark-web',
  },
  'qwen-web': {
    name: 'Qwen Web',
    cookieKey: 'token',
    providerId: 'qwen-web',
  },
  't3-web': {
    name: 'T3.Chat',
    cookieKey: 'wos-session',
    providerId: 't3-web',
  },
  'venice-web': {
    name: 'Venice AI',
    cookieKey: '__session',
    providerId: 'venice-web',
  },
  'zai-web': {
    name: 'Z.AI',
    cookieKey: 'token',
    providerId: 'zai-web',
  },
  'zenmux-free': {
    name: 'Zenmux AI',
    cookieKey: 'sessionId',
    providerId: 'zenmux-free',
  },
  'v0-vercel-web': {
    name: 'v0 by Vercel',
    cookieKey: 'user_session',
    providerId: 'v0-vercel-web',
  },
};

// Read cookies from the markdown file
function loadCookies() {
  try {
    const cookieFile = path.join(__dirname, 'COOKIE_KEYS_FOR_OMNIROUTE.md');
    const content = fs.readFileSync(cookieFile, 'utf8');
    
    const cookies = {};
    const lines = content.split('\n');
    let currentProvider = null;
    let inWhatToPaste = false;
    
    for (let i = 0; i < lines.length; i++) {
      const line = lines[i].trim();
      
      // Detect provider sections
      if (line.startsWith('## ') && line.includes('**')) {
        // Extract provider name from "## 1. **ChatGPT** (chatgpt-web)"
        const match = line.match(/\*\*(.+?)\*\*\s*\((.+?)\)/);
        if (match) {
          currentProvider = match[2]; // Use the ID in parentheses
        }
        inWhatToPaste = false;
      }
      
      // Look for "What to Paste in OmniRoute:" section
      if (line.includes('What to Paste in OmniRoute:')) {
        inWhatToPaste = true;
        continue;
      }
      
      // Extract cookie from code block after "What to Paste"
      if (inWhatToPaste && currentProvider && line.startsWith('```') && i + 1 < lines.length) {
        const nextLine = lines[i + 1].trim();
        if (nextLine && nextLine !== '```' && !nextLine.startsWith('[')) {
          cookies[currentProvider] = nextLine;
          inWhatToPaste = false;
        }
      }
    }
    
    return cookies;
  } catch (error) {
    console.error('❌ Error loading cookies:', error.message);
    return {};
  }
}

// Login to OmniRoute dashboard
async function login() {
  try {
    console.log('🔐 Logging into OmniRoute dashboard...');
    
    const response = await fetch(`${OMNIROUTE_BASE_URL}/api/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        password: ADMIN_PASSWORD,
      }),
    });
    
    if (!response.ok) {
      const error = await response.text();
      throw new Error(`Login failed: ${response.status} - ${error}`);
    }
    
    // Get the auth token from cookies
    const setCookie = response.headers.get('set-cookie');
    if (!setCookie) {
      throw new Error('No auth cookie received');
    }
    
    // Extract auth_token from Set-Cookie header
    const match = setCookie.match(/auth_token=([^;]+)/);
    if (!match) {
      throw new Error('Could not extract auth token');
    }
    
    const authToken = match[1];
    console.log('✅ Successfully logged in!');
    return authToken;
  } catch (error) {
    console.error('❌ Login failed:', error.message);
    return null;
  }
}

// Get existing providers
async function getExistingProviders(authToken) {
  try {
    const response = await fetch(`${OMNIROUTE_BASE_URL}/api/providers`, {
      method: 'GET',
      headers: {
        'Cookie': `auth_token=${authToken}`,
      },
    });
    
    if (!response.ok) {
      throw new Error(`Failed to get providers: ${response.status}`);
    }
    
    const data = await response.json();
    return data.providers || [];
  } catch (error) {
    console.error('⚠️  Could not fetch existing providers:', error.message);
    return [];
  }
}

// Add a provider to OmniRoute
async function addProvider(authToken, providerId, cookieValue, providerName) {
  try {
    const response = await fetch(`${OMNIROUTE_BASE_URL}/api/providers`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Cookie': `auth_token=${authToken}`,
      },
      body: JSON.stringify({
        provider: providerId,
        apiKey: cookieValue,
        name: providerName,
        providerSpecificData: {
          cookie: cookieValue,
        },
      }),
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Unknown error' }));
      throw new Error(error.error || error.message || `HTTP ${response.status}`);
    }
    
    const data = await response.json();
    return { success: true, data };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Validate provider connection
async function validateProvider(authToken, connectionId) {
  try {
    const response = await fetch(`${OMNIROUTE_BASE_URL}/api/providers/${connectionId}/validate`, {
      method: 'POST',
      headers: {
        'Cookie': `auth_token=${authToken}`,
      },
    });
    
    if (!response.ok) {
      const error = await response.json().catch(() => ({ error: 'Validation failed' }));
      return { valid: false, error: error.error || 'Validation failed' };
    }
    
    const data = await response.json();
    return { valid: data.valid, error: data.error };
  } catch (error) {
    return { valid: false, error: error.message };
  }
}

// Main function
async function main() {
  console.log('🚀 OmniRoute Automatic Provider Setup\n');
  console.log('═'.repeat(70));
  
  // Load cookies
  console.log('\n📋 Loading cookies from COOKIE_KEYS_FOR_OMNIROUTE.md...');
  const cookies = loadCookies();
  const cookieCount = Object.keys(cookies).filter(k => cookies[k] && cookies[k] !== '[Cookie value appears here]').length;
  
  if (cookieCount === 0) {
    console.log('❌ No valid cookies found. Please extract cookies first.');
    return;
  }
  
  console.log(`✅ Found ${cookieCount} valid cookies\n`);
  console.log('═'.repeat(70));
  
  // Login
  const authToken = await login();
  if (!authToken) {
    console.log('\n❌ Cannot proceed without authentication');
    console.log('\n💡 Make sure OmniRoute is running: cd OmniRoute && npm run dev');
    return;
  }
  
  console.log('═'.repeat(70));
  
  // Get existing providers
  console.log('\n📊 Checking existing providers...');
  const existingProviders = await getExistingProviders(authToken);
  const existingIds = new Set(existingProviders.map(p => p.provider));
  console.log(`Found ${existingProviders.length} existing providers\n`);
  
  console.log('═'.repeat(70));
  console.log('\n🔧 Adding providers to OmniRoute...\n');
  
  const results = {
    added: [],
    skipped: [],
    failed: [],
    validated: [],
  };
  
  // Add each provider
  for (const [key, config] of Object.entries(PROVIDERS_TO_ADD)) {
    const cookieValue = cookies[key] || cookies[config.cookieKey.toLowerCase()];
    
    process.stdout.write(`${config.name}... `);
    
    // Skip if no cookie
    if (!cookieValue || cookieValue === '[Cookie value appears here]') {
      console.log('⚠️  No cookie (skipped)');
      results.skipped.push(config.name);
      continue;
    }
    
    // Skip if already exists
    if (existingIds.has(config.providerId)) {
      console.log('ℹ️  Already exists (skipped)');
      results.skipped.push(config.name);
      continue;
    }
    
    // Add provider
    const result = await addProvider(authToken, config.providerId, cookieValue, config.name);
    
    if (!result.success) {
      console.log(`❌ Failed: ${result.error}`);
      results.failed.push({ name: config.name, error: result.error });
      continue;
    }
    
    console.log('✅ Added!');
    results.added.push(config.name);
    
    // Validate connection
    if (result.data && result.data.id) {
      process.stdout.write(`   Validating... `);
      const validation = await validateProvider(authToken, result.data.id);
      
      if (validation.valid) {
        console.log('✅ Valid connection!');
        results.validated.push(config.name);
      } else {
        console.log(`⚠️  Validation issue: ${validation.error}`);
      }
    }
    
    // Small delay to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 500));
  }
  
  // Print summary
  console.log('\n' + '═'.repeat(70));
  console.log('📊 SETUP COMPLETE!\n');
  
  console.log(`✅ Successfully Added: ${results.added.length}`);
  if (results.added.length > 0) {
    results.added.forEach(name => {
      const validated = results.validated.includes(name);
      console.log(`   • ${name} ${validated ? '✅ (validated)' : ''}`);
    });
  }
  
  console.log(`\n⚠️  Skipped: ${results.skipped.length}`);
  if (results.skipped.length > 0) {
    results.skipped.forEach(name => {
      console.log(`   • ${name}`);
    });
  }
  
  console.log(`\n❌ Failed: ${results.failed.length}`);
  if (results.failed.length > 0) {
    results.failed.forEach(({ name, error }) => {
      console.log(`   • ${name}: ${error}`);
    });
  }
  
  console.log('\n' + '═'.repeat(70));
  
  if (results.added.length > 0) {
    console.log('\n🎉 SUCCESS! Providers have been added to OmniRoute.');
    console.log(`\n🌐 Open dashboard: ${OMNIROUTE_BASE_URL}`);
    console.log('   View your providers in: Providers → Manage\n');
    
    console.log('💡 You can now use these providers through OmniRoute API:');
    console.log(`   Endpoint: ${OMNIROUTE_BASE_URL}/v1/chat/completions`);
    console.log('   Model format: provider-id/model-name');
    console.log('   Example: chatgpt-web/gpt-4o\n');
  } else {
    console.log('\n⚠️  No new providers were added.');
    console.log('   Check if cookies are valid or if providers already exist.\n');
  }
  
  // Save results
  const reportPath = path.join(__dirname, 'provider_setup_results.json');
  fs.writeFileSync(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    omnirouteUrl: OMNIROUTE_BASE_URL,
    results,
  }, null, 2));
  
  console.log(`📄 Detailed results saved to: provider_setup_results.json\n`);
}

// Run
main().catch(console.error);

/**
 * OmniRoute Cookie Connection Tester
 * Tests web cookie providers with the extracted cookies
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// OmniRoute API configuration
const OMNIROUTE_BASE_URL = process.env.OMNIROUTE_BASE_URL || 'http://localhost:20128';
const OMNIROUTE_API_KEY = process.env.OMNIROUTE_API_KEY || '';

// Provider configurations matching the cookies we extracted
const PROVIDERS_TO_TEST = {
  'chatgpt-web': {
    name: 'ChatGPT Web',
    cookieKey: '__Secure-next-auth.session-token',
    testEndpoint: '/v1/chat/completions',
    testModel: 'gpt-4o',
  },
  'deepseek-web': {
    name: 'DeepSeek Web',
    cookieKey: 'token',
    testEndpoint: '/v1/chat/completions',
    testModel: 'deepseek-chat',
  },
  'gemini-web': {
    name: 'Gemini Web',
    cookieKey: '__Secure-1PSID',
    testEndpoint: '/v1/chat/completions',
    testModel: 'gemini-pro',
  },
  'claude-web': {
    name: 'Claude Web',
    cookieKey: 'sessionKey',
    testEndpoint: '/v1/chat/completions',
    testModel: 'claude-3-sonnet',
  },
  'perplexity-web': {
    name: 'Perplexity Web',
    cookieKey: '__Secure-next-auth.session-token',
    testEndpoint: '/v1/chat/completions',
    testModel: 'sonar',
  },
  'grok-web': {
    name: 'Grok Web',
    cookieKey: 'sso',
    testEndpoint: '/v1/chat/completions',
    testModel: 'grok-2',
  },
  'poe-web': {
    name: 'Poe Web',
    cookieKey: 'p-b',
    testEndpoint: '/v1/chat/completions',
    testModel: 'claude-3-opus',
  },
};

// Read extracted cookies
function loadCookies() {
  try {
    const cookieFile = path.join(__dirname, 'COOKIE_KEYS_FOR_OMNIROUTE.md');
    const content = fs.readFileSync(cookieFile, 'utf8');
    
    const cookies = {};
    const lines = content.split('\n');
    let currentProvider = null;
    
    for (const line of lines) {
      if (line.startsWith('### ')) {
        currentProvider = line.replace('### ', '').trim();
      } else if (line.startsWith('**Cookie Value:**') && currentProvider) {
        const cookieValue = line.split('`')[1] || '';
        const providerKey = currentProvider.toLowerCase().replace(/\s+/g, '-');
        cookies[providerKey] = cookieValue;
      }
    }
    
    return cookies;
  } catch (error) {
    console.error('❌ Error loading cookies:', error.message);
    return {};
  }
}

// Test a simple connection to check if OmniRoute is running
async function testOmniRouteConnection() {
  try {
    const response = await fetch(`${OMNIROUTE_BASE_URL}/api/health`, {
      method: 'GET',
    });
    
    if (response.ok) {
      console.log('✅ OmniRoute is running');
      return true;
    } else {
      console.log('⚠️  OmniRoute responded with status:', response.status);
      return false;
    }
  } catch (error) {
    console.error('❌ Cannot connect to OmniRoute:', error.message);
    console.log(`\n📝 Make sure OmniRoute is running at: ${OMNIROUTE_BASE_URL}`);
    console.log('   Start it with: cd OmniRoute && npm run dev');
    return false;
  }
}

// Test provider connection with a simple chat completion
async function testProviderConnection(providerId, cookieValue) {
  try {
    const headers = {
      'Content-Type': 'application/json',
    };
    
    if (OMNIROUTE_API_KEY) {
      headers['Authorization'] = `Bearer ${OMNIROUTE_API_KEY}`;
    }
    
    const response = await fetch(`${OMNIROUTE_BASE_URL}/v1/chat/completions`, {
      method: 'POST',
      headers,
      body: JSON.stringify({
        model: `${providerId}/${PROVIDERS_TO_TEST[providerId].testModel}`,
        messages: [
          { role: 'user', content: 'Say "OK" if you receive this.' }
        ],
        max_tokens: 10,
        stream: false,
      }),
    });
    
    const data = await response.json();
    
    if (response.ok && data.choices && data.choices[0]) {
      return {
        success: true,
        message: data.choices[0].message.content,
        model: data.model,
      };
    } else {
      return {
        success: false,
        error: data.error?.message || 'Unknown error',
        status: response.status,
      };
    }
  } catch (error) {
    return {
      success: false,
      error: error.message,
    };
  }
}

// Main test function
async function runTests() {
  console.log('🚀 OmniRoute Cookie Connection Tester\n');
  console.log('═'.repeat(60));
  
  // Check OmniRoute connection
  const isOmniRouteRunning = await testOmniRouteConnection();
  if (!isOmniRouteRunning) {
    console.log('\n⚠️  Cannot proceed without OmniRoute running');
    return;
  }
  
  console.log('═'.repeat(60));
  console.log('\n📋 Loading extracted cookies...\n');
  
  const cookies = loadCookies();
  const cookieCount = Object.keys(cookies).length;
  
  console.log(`Found ${cookieCount} cookies in COOKIE_KEYS_FOR_OMNIROUTE.md`);
  
  if (cookieCount === 0) {
    console.log('\n❌ No cookies found. Please run the cookie extractor first.');
    return;
  }
  
  console.log('\n' + '═'.repeat(60));
  console.log('🔍 Testing Provider Connections...\n');
  
  const results = {
    successful: [],
    failed: [],
    notConfigured: [],
  };
  
  for (const [providerId, config] of Object.entries(PROVIDERS_TO_TEST)) {
    const cookieValue = cookies[providerId] || cookies[config.cookieKey.toLowerCase()];
    
    process.stdout.write(`Testing ${config.name}... `);
    
    if (!cookieValue || cookieValue === '[Cookie value appears here]') {
      console.log('⚠️  No cookie configured');
      results.notConfigured.push(config.name);
      continue;
    }
    
    const result = await testProviderConnection(providerId, cookieValue);
    
    if (result.success) {
      console.log('✅ SUCCESS');
      results.successful.push({
        name: config.name,
        model: result.model,
        response: result.message,
      });
    } else {
      console.log(`❌ FAILED: ${result.error}`);
      results.failed.push({
        name: config.name,
        error: result.error,
        status: result.status,
      });
    }
    
    // Small delay to avoid rate limiting
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  // Print summary
  console.log('\n' + '═'.repeat(60));
  console.log('📊 TEST SUMMARY\n');
  
  console.log(`✅ Successful Connections: ${results.successful.length}`);
  if (results.successful.length > 0) {
    results.successful.forEach(r => {
      console.log(`   • ${r.name} (${r.model})`);
    });
  }
  
  console.log(`\n❌ Failed Connections: ${results.failed.length}`);
  if (results.failed.length > 0) {
    results.failed.forEach(r => {
      console.log(`   • ${r.name}: ${r.error}`);
    });
  }
  
  console.log(`\n⚠️  Not Configured: ${results.notConfigured.length}`);
  if (results.notConfigured.length > 0) {
    results.notConfigured.forEach(name => {
      console.log(`   • ${name}`);
    });
  }
  
  console.log('\n' + '═'.repeat(60));
  console.log('\n💡 NEXT STEPS:');
  console.log('\n1. Open OmniRoute Dashboard: ' + OMNIROUTE_BASE_URL);
  console.log('2. Go to Providers → Add Provider');
  console.log('3. Select "Web Cookie" providers');
  console.log('4. Paste the cookie values from COOKIE_KEYS_FOR_OMNIROUTE.md');
  console.log('5. Test each provider in the dashboard\n');
  
  // Save results to file
  const reportPath = path.join(__dirname, 'omniroute_test_results.json');
  fs.writeFileSync(reportPath, JSON.stringify({
    timestamp: new Date().toISOString(),
    omnirouteUrl: OMNIROUTE_BASE_URL,
    results,
  }, null, 2));
  
  console.log(`📄 Full results saved to: omniroute_test_results.json\n`);
}

// Run the tests
runTests().catch(console.error);

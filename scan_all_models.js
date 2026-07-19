/**
 * Scan All Available Models in OmniRoute
 * Lists every working model from all providers
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const OMNIROUTE_URL = process.env.OMNIROUTE_BASE_URL || 'http://localhost:20128';
const ADMIN_PASSWORD = process.env.INITIAL_PASSWORD || 'CHANGEME';

// Model capabilities and power ranking
const MODEL_CAPABILITIES = {
  // Tier 1: Most Powerful (Claude-level)
  'claude-3-opus': { tier: 1, power: 10, capabilities: ['coding', 'analysis', 'creative', 'reasoning'] },
  'claude-3.5-sonnet': { tier: 1, power: 10, capabilities: ['coding', 'analysis', 'creative', 'reasoning'] },
  'claude-3-sonnet': { tier: 1, power: 9, capabilities: ['coding', 'analysis', 'creative'] },
  'gpt-4o': { tier: 1, power: 9, capabilities: ['coding', 'analysis', 'creative', 'vision'] },
  'gpt-4-turbo': { tier: 1, power: 9, capabilities: ['coding', 'analysis', 'creative', 'vision'] },
  'gpt-4': { tier: 1, power: 9, capabilities: ['coding', 'analysis', 'creative'] },
  
  // Tier 2: Strong (Good for most tasks)
  'gemini-1.5-pro': { tier: 2, power: 8, capabilities: ['coding', 'analysis', 'creative', 'vision'] },
  'gemini-pro': { tier: 2, power: 8, capabilities: ['coding', 'analysis', 'creative'] },
  'deepseek-chat': { tier: 2, power: 8, capabilities: ['coding', 'reasoning'] },
  'deepseek-coder': { tier: 2, power: 8, capabilities: ['coding'] },
  'qwen-turbo': { tier: 2, power: 7, capabilities: ['coding', 'analysis'] },
  'qwen-plus': { tier: 2, power: 7, capabilities: ['coding', 'analysis'] },
  
  // Tier 3: Capable (Fast, efficient)
  'claude-3-haiku': { tier: 3, power: 7, capabilities: ['coding', 'analysis'] },
  'gpt-3.5-turbo': { tier: 3, power: 6, capabilities: ['coding', 'chat'] },
  'mixtral': { tier: 3, power: 7, capabilities: ['coding', 'analysis'] },
  'llama-3': { tier: 3, power: 6, capabilities: ['coding', 'chat'] },
  'gemini-flash': { tier: 3, power: 6, capabilities: ['coding', 'fast'] },
  
  // Tier 4: Basic (Good for simple tasks)
  'grok-2': { tier: 4, power: 6, capabilities: ['chat', 'analysis'] },
  'sonar': { tier: 4, power: 5, capabilities: ['search', 'chat'] },
};

async function login() {
  try {
    const response = await fetch(`${OMNIROUTE_URL}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: ADMIN_PASSWORD }),
    });
    
    if (!response.ok) return null;
    
    const setCookie = response.headers.get('set-cookie');
    const match = setCookie?.match(/auth_token=([^;]+)/);
    return match ? match[1] : null;
  } catch (error) {
    return null;
  }
}

async function getProviders(authToken) {
  try {
    const response = await fetch(`${OMNIROUTE_URL}/api/providers`, {
      headers: { 'Cookie': `auth_token=${authToken}` },
    });
    
    if (!response.ok) return [];
    const data = await response.json();
    return data.providers || [];
  } catch (error) {
    return [];
  }
}

async function getModels(authToken) {
  try {
    const response = await fetch(`${OMNIROUTE_URL}/v1/models`, {
      headers: { 'Cookie': `auth_token=${authToken}` },
    });
    
    if (!response.ok) return [];
    const data = await response.json();
    return data.data || [];
  } catch (error) {
    return [];
  }
}

function categorizeModel(modelId) {
  const modelLower = modelId.toLowerCase();
  
  for (const [key, value] of Object.entries(MODEL_CAPABILITIES)) {
    if (modelLower.includes(key.toLowerCase())) {
      return value;
    }
  }
  
  // Default for unknown models
  return { tier: 4, power: 5, capabilities: ['general'] };
}

async function main() {
  console.log('\n' + '═'.repeat(80));
  console.log('🔍 OmniRoute Model Scanner');
  console.log('═'.repeat(80) + '\n');
  
  // Login
  console.log('🔐 Connecting to OmniRoute...');
  const authToken = await login();
  
  if (!authToken) {
    console.log('❌ Cannot connect to OmniRoute');
    console.log('💡 Make sure OmniRoute is running: cd OmniRoute && npm run dev');
    return;
  }
  
  console.log('✅ Connected!\n');
  console.log('═'.repeat(80) + '\n');
  
  // Get providers
  console.log('📊 Scanning providers...');
  const providers = await getProviders(authToken);
  console.log(`Found ${providers.length} providers\n`);
  
  // Get models
  console.log('🎯 Scanning available models...');
  const models = await getModels(authToken);
  console.log(`Found ${models.length} models\n`);
  
  console.log('═'.repeat(80) + '\n');
  
  // Categorize models
  const categorized = {
    tier1: [],
    tier2: [],
    tier3: [],
    tier4: [],
  };
  
  const modelDetails = [];
  
  for (const model of models) {
    const info = categorizeModel(model.id);
    const details = {
      id: model.id,
      ...info,
      provider: model.id.split('/')[0],
      modelName: model.id.split('/')[1] || model.id,
    };
    
    modelDetails.push(details);
    categorized[`tier${info.tier}`].push(details);
  }
  
  // Sort by power within each tier
  for (const tier of Object.keys(categorized)) {
    categorized[tier].sort((a, b) => b.power - a.power);
  }
  
  // Display results
  console.log('📋 AVAILABLE MODELS BY POWER TIER\n');
  
  if (categorized.tier1.length > 0) {
    console.log('🏆 TIER 1: MOST POWERFUL (Claude-level) - Best for Coding & Analysis');
    console.log('─'.repeat(80));
    categorized.tier1.forEach(m => {
      console.log(`  ✨ ${m.id}`);
      console.log(`     Power: ${m.power}/10 | Capabilities: ${m.capabilities.join(', ')}`);
    });
    console.log('');
  }
  
  if (categorized.tier2.length > 0) {
    console.log('🥈 TIER 2: STRONG - Good for Most Tasks');
    console.log('─'.repeat(80));
    categorized.tier2.forEach(m => {
      console.log(`  💪 ${m.id}`);
      console.log(`     Power: ${m.power}/10 | Capabilities: ${m.capabilities.join(', ')}`);
    });
    console.log('');
  }
  
  if (categorized.tier3.length > 0) {
    console.log('🥉 TIER 3: CAPABLE - Fast & Efficient');
    console.log('─'.repeat(80));
    categorized.tier3.forEach(m => {
      console.log(`  ⚡ ${m.id}`);
      console.log(`     Power: ${m.power}/10 | Capabilities: ${m.capabilities.join(', ')}`);
    });
    console.log('');
  }
  
  if (categorized.tier4.length > 0) {
    console.log('🔧 TIER 4: BASIC - Simple Tasks & Chat');
    console.log('─'.repeat(80));
    categorized.tier4.forEach(m => {
      console.log(`  📝 ${m.id}`);
      console.log(`     Power: ${m.power}/10 | Capabilities: ${m.capabilities.join(', ')}`);
    });
    console.log('');
  }
  
  console.log('═'.repeat(80) + '\n');
  
  // Summary by provider
  console.log('📦 MODELS BY PROVIDER\n');
  
  const byProvider = {};
  for (const model of modelDetails) {
    if (!byProvider[model.provider]) {
      byProvider[model.provider] = [];
    }
    byProvider[model.provider].push(model);
  }
  
  for (const [provider, models] of Object.entries(byProvider)) {
    console.log(`${provider}:`);
    models.forEach(m => {
      console.log(`  • ${m.modelName} (Tier ${m.tier}, Power ${m.power}/10)`);
    });
    console.log('');
  }
  
  console.log('═'.repeat(80) + '\n');
  
  // Recommendations
  console.log('💡 RECOMMENDATIONS FOR BEST RESULTS\n');
  
  const bestCoding = modelDetails
    .filter(m => m.capabilities.includes('coding'))
    .sort((a, b) => b.power - a.power)
    .slice(0, 3);
  
  console.log('🎯 Best for Coding:');
  bestCoding.forEach((m, i) => {
    console.log(`  ${i + 1}. ${m.id}`);
  });
  
  const bestAnalysis = modelDetails
    .filter(m => m.capabilities.includes('analysis'))
    .sort((a, b) => b.power - a.power)
    .slice(0, 3);
  
  console.log('\n📊 Best for Business Analysis:');
  bestAnalysis.forEach((m, i) => {
    console.log(`  ${i + 1}. ${m.id}`);
  });
  
  const fastest = modelDetails
    .filter(m => m.capabilities.includes('fast') || m.tier === 3)
    .sort((a, b) => b.power - a.power)
    .slice(0, 3);
  
  console.log('\n⚡ Best for Speed:');
  fastest.forEach((m, i) => {
    console.log(`  ${i + 1}. ${m.id}`);
  });
  
  console.log('\n' + '═'.repeat(80) + '\n');
  
  // Save results
  const results = {
    timestamp: new Date().toISOString(),
    totalModels: models.length,
    totalProviders: providers.length,
    categorized,
    byProvider,
    recommendations: {
      coding: bestCoding.map(m => m.id),
      analysis: bestAnalysis.map(m => m.id),
      speed: fastest.map(m => m.id),
    },
    allModels: modelDetails,
  };
  
  const outputPath = path.join(__dirname, 'omniroute_models_scan.json');
  fs.writeFileSync(outputPath, JSON.stringify(results, null, 2));
  
  console.log('📄 Results saved to: omniroute_models_scan.json\n');
  
  // Statistics
  console.log('📈 STATISTICS\n');
  console.log(`Total Models: ${models.length}`);
  console.log(`Tier 1 (Most Powerful): ${categorized.tier1.length}`);
  console.log(`Tier 2 (Strong): ${categorized.tier2.length}`);
  console.log(`Tier 3 (Capable): ${categorized.tier3.length}`);
  console.log(`Tier 4 (Basic): ${categorized.tier4.length}`);
  console.log(`\nActive Providers: ${providers.length}`);
  console.log('');
}

main().catch(console.error);

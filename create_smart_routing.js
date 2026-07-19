/**
 * Create Smart Model Routing Configuration for OmniRoute
 * Automatically prioritizes powerful models and creates fallback chains
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load scan results
const scanResults = JSON.parse(
  fs.readFileSync(path.join(__dirname, 'omniroute_models_scan.json'), 'utf8')
);

// Smart routing configurations for different use cases
const ROUTING_STRATEGIES = {
  // For heavy coding work - prioritize most powerful models
  CODING_POWERHOUSE: {
    name: 'Coding Powerhouse',
    description: 'Best models for complex coding tasks, prioritizes Claude-level intelligence',
    priority: [
      // Tier 1: Try the absolute best first
      'gh/gpt-4o-2024-11-20',
      'github/gpt-4o-2024-11-20', 
      'openai/gpt-4o',
      'openrouter/openai/gpt-4o',
      
      // Tier 2: Strong coding models
      'deepseek-web/deepseek-chat',
      'openrouter/deepseek/deepseek-chat-v3.1',
      
      // Tier 3: Fast and capable
      'gh/gpt-4o-mini',
      'openai/gpt-4o-mini',
      'openrouter/anthropic/claude-3-haiku',
      'groq/llama-3.3-70b-versatile',
    ],
    fallback: 'gh/gpt-4o-mini', // Always available fast model
  },
  
  // For business analysis - balance power and speed
  BUSINESS_ANALYSIS: {
    name: 'Business Analysis Optimized',
    description: 'Smart models for analysis, documentation, and strategic thinking',
    priority: [
      'gh/gpt-4o-2024-11-20',
      'openai/gpt-4o',
      'gemini-web/gemini-exp-1206',
      'deepseek-web/deepseek-chat',
      'openrouter/google/gemini-pro-latest',
      'gh/gpt-4o-mini',
    ],
    fallback: 'gh/gpt-4o-mini',
  },
  
  // For fast iterations - prioritize speed
  FAST_ITERATION: {
    name: 'Fast Iteration',
    description: 'Quick responses for simple tasks and rapid development',
    priority: [
      'gh/gpt-4o-mini',
      'openai/gpt-4o-mini',
      'groq/llama-3.3-70b-versatile',
      'groq/llama-3.1-70b-versatile',
      'openrouter/anthropic/claude-3-haiku',
      'ddgw/gpt-4o-mini',
    ],
    fallback: 'gh/gpt-4o-mini',
  },
  
  // For creative work - use diverse models
  CREATIVE_MIX: {
    name: 'Creative Mix',
    description: 'Diverse models for creative problem-solving and innovation',
    priority: [
      'openai/gpt-4o',
      'gemini-web/gemini-exp-1206',
      'deepseek-web/deepseek-chat',
      'openrouter/google/gemini-2.0-flash-thinking-exp:free',
      'huggingchat/meta-llama/llama-3.3-70b-instruct',
      'gh/gpt-4o-mini',
    ],
    fallback: 'gh/gpt-4o-mini',
  },
  
  // Maximum power - no compromises
  MAX_POWER: {
    name: 'Maximum Power',
    description: 'Most powerful models only, use for critical tasks',
    priority: [
      'gh/gpt-4o-2024-11-20',
      'github/gpt-4o-2024-11-20',
      'openai/gpt-4o-2024-11-20',
      'openrouter/openai/gpt-4o-2024-11-20',
      't3-web/gpt-4o',
      'openai/gpt-4.1',
    ],
    fallback: 'gh/gpt-4o-2024-11-20',
  },
};

// Generate combos for OmniRoute
function generateCombos() {
  const combos = {};
  
  for (const [key, strategy] of Object.entries(ROUTING_STRATEGIES)) {
    const comboName = key.toLowerCase().replace(/_/g, '-');
    
    combos[comboName] = {
      name: strategy.name,
      description: strategy.description,
      models: strategy.priority,
      fallback: strategy.fallback,
      strategy: 'failover', // Try each model in order until one works
      timeout: 30000, // 30 seconds per model
      retries: 2, // Retry failed models twice
    };
  }
  
  return combos;
}

// Create model lists by category
function categorizeModels() {
  const categories = {
    tier1_powerful: [],
    tier2_strong: [],
    tier3_fast: [],
    coding_specialists: [],
    free_models: [],
    api_key_models: [],
  };
  
  for (const model of scanResults.allModels) {
    // Tier categorization
    if (model.tier === 1) categories.tier1_powerful.push(model.id);
    if (model.tier === 2) categories.tier2_strong.push(model.id);
    if (model.tier === 3) categories.tier3_fast.push(model.id);
    
    // Coding specialists
    if (model.capabilities.includes('coding') && model.power >= 7) {
      categories.coding_specialists.push(model.id);
    }
    
    // Free vs API key
    const freeProviders = ['github', 'gh', 'ddgw', 'groq', 'huggingchat', 'deepseek-web', 'gemini-web', 'zenmux-free'];
    const provider = model.provider.toLowerCase();
    
    if (freeProviders.some(p => provider.includes(p))) {
      categories.free_models.push(model.id);
    } else if (provider.includes('openai') || provider.includes('openrouter')) {
      categories.api_key_models.push(model.id);
    }
  }
  
  return categories;
}

// Generate usage tips
function generateTips(categories) {
  return {
    'Best for Coding': {
      primary: categories.tier1_powerful.slice(0, 3),
      backup: categories.coding_specialists.slice(0, 5),
      tip: 'Use these for complex coding tasks, refactoring, and architecture decisions',
    },
    'Best for BA Work': {
      primary: categories.tier1_powerful.slice(0, 3),
      backup: categories.tier2_strong.slice(0, 5),
      tip: 'Perfect for business analysis, requirements gathering, and documentation',
    },
    'Best for Speed': {
      primary: categories.tier3_fast.slice(0, 5),
      backup: categories.free_models.filter(m => m.includes('mini') || m.includes('groq')).slice(0, 5),
      tip: 'Use these for quick iterations, testing, and simple tasks',
    },
    'Free Models (No API Key)': {
      primary: categories.free_models.slice(0, 10),
      backup: [],
      tip: 'These models don\'t require API keys - use cookies/session auth',
    },
    'API Key Models (Most Reliable)': {
      primary: categories.api_key_models.slice(0, 10),
      backup: [],
      tip: 'Most stable and reliable, but require API keys',
    },
  };
}

// Main execution
function main() {
  console.log('\n' + '═'.repeat(80));
  console.log('🎯 Smart Routing Configuration Generator');
  console.log('═'.repeat(80) + '\n');
  
  console.log(`📊 Processing ${scanResults.totalModels} models...\n`);
  
  // Generate combos
  const combos = generateCombos();
  console.log('✅ Generated Smart Routing Strategies:');
  for (const [key, combo] of Object.entries(combos)) {
    console.log(`   • ${combo.name}: ${combo.models.length} models in priority chain`);
  }
  console.log('');
  
  // Categorize models
  const categories = categorizeModels();
  console.log('✅ Categorized Models:');
  console.log(`   • Tier 1 (Powerful): ${categories.tier1_powerful.length}`);
  console.log(`   • Tier 2 (Strong): ${categories.tier2_strong.length}`);
  console.log(`   • Tier 3 (Fast): ${categories.tier3_fast.length}`);
  console.log(`   • Coding Specialists: ${categories.coding_specialists.length}`);
  console.log(`   • Free Models: ${categories.free_models.length}`);
  console.log(`   • API Key Models: ${categories.api_key_models.length}`);
  console.log('');
  
  // Generate tips
  const tips = generateTips(categories);
  
  // Save everything
  const output = {
    generated: new Date().toISOString(),
    totalModels: scanResults.totalModels,
    
    // Smart routing combos
    combos,
    
    // Model categories
    categories,
    
    // Usage tips
    tips,
    
    // Quick reference
    quickStart: {
      codingCombo: 'coding-powerhouse',
      analysisCombo: 'business-analysis',
      speedCombo: 'fast-iteration',
      bestOverall: combos['coding-powerhouse'].models[0],
    },
  };
  
  fs.writeFileSync(
    path.join(__dirname, 'smart_routing_config.json'),
    JSON.stringify(output, null, 2)
  );
  
  console.log('═'.repeat(80) + '\n');
  console.log('📋 RECOMMENDED ROUTING STRATEGIES\n');
  
  for (const [key, strategy] of Object.entries(ROUTING_STRATEGIES)) {
    console.log(`🎯 ${strategy.name}`);
    console.log(`   ${strategy.description}`);
    console.log(`   Top 3 models:`);
    strategy.priority.slice(0, 3).forEach((model, i) => {
      console.log(`     ${i + 1}. ${model}`);
    });
    console.log(`   Fallback: ${strategy.fallback}`);
    console.log('');
  }
  
  console.log('═'.repeat(80) + '\n');
  console.log('💡 USAGE TIPS\n');
  
  for (const [category, info] of Object.entries(tips)) {
    console.log(`${category}:`);
    console.log(`  💡 ${info.tip}`);
    console.log(`  Primary models:`);
    info.primary.slice(0, 3).forEach(m => console.log(`    • ${m}`));
    console.log('');
  }
  
  console.log('═'.repeat(80) + '\n');
  console.log('📄 Files created:');
  console.log('  • smart_routing_config.json - Complete routing configuration');
  console.log('  • omniroute_models_scan.json - Full model scan results\n');
  
  console.log('🚀 Next Steps:');
  console.log('  1. Use routing combos in your API calls');
  console.log('  2. Configure OmniRoute with these priorities');
  console.log('  3. Test different strategies for your use case\n');
}

main();

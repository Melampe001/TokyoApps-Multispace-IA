import { readFile } from 'fs/promises';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Load Tokyo-specific rules and context
 */
export async function loadTokyoRules() {
  try {
    const rulesPath = join(__dirname, '../../tokyo-rules.json');
    const rulesContent = await readFile(rulesPath, 'utf-8');
    return JSON.parse(rulesContent);
  } catch (error) {
    console.error('Error loading Tokyo rules:', error);
    // Return default rules if file cannot be loaded
    return {
      version: '1.0.0',
      rules: {
        culturalContext: {
          theme: 'Tokyo',
          language: ['Japanese', 'English'],
          style: 'respectful and informative'
        }
      }
    };
  }
}

/**
 * Get specific rule by path
 */
export function getRule(rules, path) {
  return path.split('.').reduce((obj, key) => obj?.[key], rules);
}

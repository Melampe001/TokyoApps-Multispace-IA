import express from 'express';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(express.json());

// Load Tokyo rules
let tokyoRules = {};
try {
  const rulesPath = join(__dirname, 'tokyo-rules.json');
  tokyoRules = JSON.parse(readFileSync(rulesPath, 'utf8'));
  console.log('✓ Tokyo rules loaded successfully');
} catch (error) {
  console.warn('⚠ Warning: Could not load tokyo-rules.json');
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({
    status: 'ok',
    service: 'Tokyo-IA MCP Server',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// MCP endpoint
app.post('/mcp', (req, res) => {
  const { action, context } = req.body;
  
  res.json({
    success: true,
    action: action || 'unknown',
    response: 'MCP server is ready for testing',
    rules: tokyoRules,
    context: context || {}
  });
});

// Get rules endpoint
app.get('/rules', (req, res) => {
  res.json(tokyoRules);
});

// Start server
app.listen(PORT, () => {
  console.log(`🚀 Tokyo-IA MCP Server running on port ${PORT}`);
  console.log(`📍 Health check: http://localhost:${PORT}/health`);
  console.log(`📍 MCP endpoint: http://localhost:${PORT}/mcp`);
});

export default app;

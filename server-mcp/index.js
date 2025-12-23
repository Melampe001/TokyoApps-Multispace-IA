import express from 'express';
import { loadTokyoRules } from './src/context/rules.js';
import { handleAction } from './src/actions/handler.js';

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(express.json());

// Load Tokyo rules
const tokyoRules = await loadTokyoRules();

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: '1.0.0'
  });
});

// MCP endpoint
app.post('/mcp', async (req, res) => {
  try {
    const { action, payload } = req.body;
    
    if (!action) {
      return res.status(400).json({ error: 'Action is required' });
    }

    const result = await handleAction(action, payload, tokyoRules);
    res.json(result);
  } catch (error) {
    console.error('MCP Error:', error);
    res.status(500).json({ error: error.message });
  }
});

// Context endpoint - provides Tokyo-specific context
app.get('/context', (req, res) => {
  res.json({
    rules: tokyoRules,
    capabilities: [
      'text-generation',
      'image-analysis',
      'sentiment-analysis',
      'tokyo-cultural-context'
    ]
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Tokyo-IA MCP Server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});

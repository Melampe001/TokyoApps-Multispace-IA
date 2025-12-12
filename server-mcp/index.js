import express from 'express';
import cors from 'cors';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import fs from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(express.json());

// Load Tokyo rules
let tokyoRules = {};
try {
  const rulesPath = join(__dirname, 'tokyo-rules.json');
  const rulesData = fs.readFileSync(rulesPath, 'utf8');
  tokyoRules = JSON.parse(rulesData);
  console.log('Tokyo rules loaded successfully');
} catch (error) {
  console.warn('Could not load tokyo-rules.json:', error.message);
  tokyoRules = { rules: [], contexts: [] };
}

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'healthy', 
    service: 'tokyo-ia-mcp-server',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// MCP endpoints
app.get('/api/mcp/rules', (req, res) => {
  res.json(tokyoRules);
});

app.post('/api/mcp/process', (req, res) => {
  const { input, context } = req.body;
  
  // Basic processing logic
  const response = {
    processed: true,
    input: input,
    context: context || 'default',
    output: `Processed: ${input}`,
    timestamp: new Date().toISOString(),
    rules_applied: tokyoRules.rules?.length || 0
  };
  
  res.json(response);
});

app.post('/api/mcp/actions/:actionName', (req, res) => {
  const { actionName } = req.params;
  const { payload } = req.body;
  
  // Action handler
  const result = {
    action: actionName,
    status: 'executed',
    payload: payload,
    timestamp: new Date().toISOString()
  };
  
  res.json(result);
});

// Context management
app.get('/api/mcp/context/:contextId', (req, res) => {
  const { contextId } = req.params;
  
  const contextData = {
    id: contextId,
    data: tokyoRules.contexts?.[contextId] || {},
    timestamp: new Date().toISOString()
  };
  
  res.json(contextData);
});

// Error handling
app.use((err, req, res, next) => {
  console.error('Error:', err);
  res.status(500).json({ 
    error: 'Internal server error',
    message: err.message 
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Tokyo-IA MCP Server running on port ${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});

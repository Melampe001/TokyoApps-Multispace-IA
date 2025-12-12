# Tokyo-IA MCP Server

Model Context Protocol server for Tokyo-IA AI features.

## Requirements

- Node.js 18+

## Development

### Install Dependencies
```bash
npm install
```

### Start Server
```bash
npm start
```

### Start with Auto-reload
```bash
npm run dev
```

The server will run on http://localhost:3001

## API Endpoints

### Health Check
```
GET /health
```

### Get Rules
```
GET /api/mcp/rules
```

### Process Input
```
POST /api/mcp/process
Body: { "input": "...", "context": "..." }
```

### Execute Action
```
POST /api/mcp/actions/:actionName
Body: { "payload": {...} }
```

### Get Context
```
GET /api/mcp/context/:contextId
```

## Configuration

Edit `tokyo-rules.json` to configure:
- Processing rules
- Context definitions
- Available actions

## Project Structure

- `index.js` - Main server file
- `tokyo-rules.json` - MCP rules and configuration
- `src/` - Source code
  - `actions/` - Action handlers
  - `context/` - Context management

## Testing

```bash
npm test
```

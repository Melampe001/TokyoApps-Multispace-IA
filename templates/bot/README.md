# Discord/Telegram Bot Template

Production-ready bot template with modular commands, event handling, and AI integration.

## Features

- ✅ Discord.js / node-telegram-bot-api support
- ✅ Modular command system
- ✅ Event handling
- ✅ Slash commands (Discord)
- ✅ Database integration (MongoDB/PostgreSQL)
- ✅ AI integration (OpenAI, Claude)
- ✅ Cooldown system
- ✅ Permission management
- ✅ Error handling
- ✅ Logging
- ✅ Docker support

## Quick Start

```bash
# Install dependencies
npm install

# Configure bot
cp .env.example .env
# Edit .env with your bot token

# Start bot
npm start
```

## Configuration

### Discord Bot

1. Create application at https://discord.com/developers/applications
2. Create bot and copy token
3. Enable necessary intents (Message Content, Guild Members, etc.)
4. Add to `.env`:

```bash
DISCORD_TOKEN=your-bot-token
DISCORD_CLIENT_ID=your-client-id
DISCORD_GUILD_ID=your-test-guild-id
```

### Telegram Bot

1. Create bot with @BotFather
2. Copy token
3. Add to `.env`:

```bash
TELEGRAM_TOKEN=your-bot-token
```

## Commands

### Moderation
- `/kick @user [reason]` - Kick user
- `/ban @user [reason]` - Ban user
- `/mute @user [duration]` - Mute user
- `/warn @user [reason]` - Warn user
- `/clear [amount]` - Clear messages

### Utility
- `/help` - Show help
- `/ping` - Check latency
- `/info` - Server/user info
- `/avatar [@user]` - Get avatar

### Fun
- `/joke` - Random joke
- `/meme` - Random meme
- `/8ball [question]` - Magic 8-ball
- `/roll [dice]` - Roll dice

### AI
- `/ask [question]` - Ask AI
- `/chat [message]` - AI chat
- `/image [prompt]` - Generate image

### Music (Discord)
- `/play [song]` - Play music
- `/skip` - Skip song
- `/queue` - Show queue
- `/pause` - Pause playback
- `/resume` - Resume playback
- `/stop` - Stop and clear queue

## Directory Structure

```
bot-template/
├── src/
│   ├── index.js              # Entry point
│   ├── bot.js                # Bot initialization (see bot.js.txt)
│   ├── commands/             # Command modules
│   │   ├── moderation/
│   │   │   ├── kick.js
│   │   │   ├── ban.js
│   │   │   └── mute.js
│   │   ├── utility/
│   │   │   ├── help.js
│   │   │   ├── ping.js
│   │   │   └── info.js
│   │   ├── fun/
│   │   │   ├── joke.js
│   │   │   └── meme.js
│   │   └── ai/
│   │       ├── ask.js
│   │       └── chat.js
│   ├── events/               # Event handlers
│   │   ├── ready.js
│   │   ├── messageCreate.js
│   │   └── interactionCreate.js
│   ├── utils/                # Utilities
│   │   ├── logger.js
│   │   ├── database.js
│   │   └── permissions.js
│   └── config/               # Configuration
│       └── config.js
├── tests/                    # Tests
├── docs/                     # Documentation
└── package.json
```

> **Note:** See `bot.js.txt` in this directory for a sample implementation.

## Development

```bash
# Run in development mode (with hot reload)
npm run dev

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

## Deployment

### Docker

```bash
# Build image
docker build -t bot-template .

# Run container
docker run -d --env-file .env bot-template
```

### Heroku

```bash
heroku create
heroku config:set DISCORD_TOKEN=your-token
git push heroku main
```

### Railway

```bash
railway init
railway add
railway up
```

## Features in Detail

### Command System

Commands are modular and easy to add:

```javascript
module.exports = {
  name: 'ping',
  description: 'Check bot latency',
  cooldown: 5,
  execute(message, args) {
    message.reply(`Pong! Latency: ${Date.now() - message.createdTimestamp}ms`);
  }
};
```

### Event Handling

Events are handled in separate files:

```javascript
module.exports = {
  name: 'messageCreate',
  once: false,
  execute(message) {
    // Handle message
  }
};
```

### Database Integration

Store user data, settings, etc.:

```javascript
const User = require('./models/User');

// Save user
await User.create({ discordId: user.id, points: 0 });

// Find user
const userData = await User.findOne({ discordId: user.id });
```

### AI Integration

Use OpenAI, Claude, or other LLMs:

```javascript
const response = await openai.chat.completions.create({
  model: 'gpt-4',
  messages: [{ role: 'user', content: prompt }]
});
```

## Error Handling

Comprehensive error handling:

```javascript
try {
  // Command execution
} catch (error) {
  logger.error('Command error:', error);
  message.reply('An error occurred. Please try again.');
}
```

## Logging

Structured logging with Winston:

```javascript
logger.info('Bot started');
logger.error('Error:', error);
logger.debug('Debug info:', data);
```

## Security

- Token stored in environment variables
- Permission checks before command execution
- Rate limiting / cooldown system
- Input validation
- Error messages don't leak sensitive info

## License

MIT License

---

Generated with Tokyo-IA Elite Framework

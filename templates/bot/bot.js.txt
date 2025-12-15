const { Client, GatewayIntentBits, Collection } = require('discord.js');
const fs = require('fs');
const path = require('path');
require('dotenv').config();

// Create client with necessary intents
const client = new Client({
  intents: [
    GatewayIntentBits.Guilds,
    GatewayIntentBits.GuildMessages,
    GatewayIntentBits.MessageContent,
    GatewayIntentBits.GuildMembers,
  ]
});

// Initialize command collection
client.commands = new Collection();

// Load commands
const commandsPath = path.join(__dirname, 'commands');
const commandFolders = fs.readdirSync(commandsPath);

for (const folder of commandFolders) {
  const folderPath = path.join(commandsPath, folder);
  const commandFiles = fs.readdirSync(folderPath).filter(file => file.endsWith('.js'));
  
  for (const file of commandFiles) {
    const filePath = path.join(folderPath, file);
    const command = require(filePath);
    
    if ('name' in command && 'execute' in command) {
      client.commands.set(command.name, command);
      console.log(`✓ Loaded command: ${command.name}`);
    } else {
      console.log(`⚠ Skipping ${file}: missing name or execute`);
    }
  }
}

// Load events
const eventsPath = path.join(__dirname, 'events');
const eventFiles = fs.readdirSync(eventsPath).filter(file => file.endsWith('.js'));

for (const file of eventFiles) {
  const filePath = path.join(eventsPath, file);
  const event = require(filePath);
  
  if (event.once) {
    client.once(event.name, (...args) => event.execute(...args));
  } else {
    client.on(event.name, (...args) => event.execute(...args));
  }
  
  console.log(`✓ Loaded event: ${event.name}`);
}

// Ready event
client.once('ready', () => {
  console.log(`✓ Bot is ready! Logged in as ${client.user.tag}`);
  console.log(`✓ Serving ${client.guilds.cache.size} guilds`);
});

// Message handler
client.on('messageCreate', async message => {
  // Ignore bots
  if (message.author.bot) return;
  
  // Check for command prefix
  const prefix = process.env.BOT_PREFIX || '!';
  if (!message.content.startsWith(prefix)) return;
  
  // Parse command
  const args = message.content.slice(prefix.length).trim().split(/ +/);
  const commandName = args.shift().toLowerCase();
  
  // Get command
  const command = client.commands.get(commandName);
  if (!command) return;
  
  // Execute command
  try {
    await command.execute(message, args);
  } catch (error) {
    console.error(`Error executing ${commandName}:`, error);
    await message.reply('There was an error executing that command.');
  }
});

// Login
client.login(process.env.DISCORD_TOKEN);

module.exports = client;

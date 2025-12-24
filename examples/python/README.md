# Tokyo-IA Python Examples

This directory contains example scripts demonstrating how to use CrewAI with Groq in the Tokyo-IA project.

## 📋 Available Examples

### basic_agent.py
A simple example that creates a Tokyo travel expert agent using CrewAI and Groq LLM.

**Features:**
- Demonstrates basic agent creation
- Shows how to define tasks
- Illustrates crew execution
- Includes error handling and user-friendly output

**Usage:**
```bash
# Set your API key
export GROQ_API_KEY=your_api_key_here

# Run the example
python examples/python/basic_agent.py
```

## 🚀 Getting Started

Before running any examples:

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up your Groq API key:**
   ```bash
   export GROQ_API_KEY=your_api_key_here
   ```
   
   Get your API key from [Groq Console](https://console.groq.com)

3. **Run an example:**
   ```bash
   python examples/python/basic_agent.py
   ```

## 📚 More Information

For detailed setup instructions and usage guides, see [README-python.md](../../README-python.md) in the project root.

## 🤝 Contributing

To add a new example:
1. Create a new Python file in this directory
2. Include a docstring at the top explaining the example
3. Add error handling and helpful output messages
4. Update this README with the new example
5. Test the example thoroughly before submitting

# Tokyo-IA Python Setup Guide

This guide provides instructions for setting up and using Python-based AI agent functionality in Tokyo-IA using CrewAI and Groq.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Basic Usage](#basic-usage)
- [CrewAI Overview](#crewai-overview)
- [Groq Overview](#groq-overview)
- [Example Scripts](#example-scripts)
- [Troubleshooting](#troubleshooting)

## 🔧 Prerequisites

- **Python 3.9 or higher** (Python 3.12+ recommended)
- **pip** (Python package manager)
- **Groq API Key** (obtain from [Groq Console](https://console.groq.com))

To verify your Python installation:
```bash
python3 --version
```

## 📦 Installation

### Step 1: Create a Python Virtual Environment

Using a virtual environment is recommended to avoid dependency conflicts.

```bash
# Navigate to the project root
cd Tokyo-IA

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate
```

### Step 2: Install Dependencies

With the virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

This will install:
- **crewai** - Framework for orchestrating role-playing, autonomous AI agents
- **groq** - Fast inference API for LLMs

### Step 3: Verify Installation

```bash
pip list | grep -E "crewai|groq"
```

You should see both packages listed with their versions.

## 🔑 Environment Configuration

### Required Environment Variables

Create a `.env` file in the project root directory (or set these variables in your environment):

```bash
# Groq API Configuration
GROQ_API_KEY=your_groq_api_key_here

# Optional: Specify a default model (use groq/ prefix format)
GROQ_MODEL=groq/llama-3.1-70b-versatile
```

### Obtaining a Groq API Key

1. Visit the [Groq Console](https://console.groq.com)
2. Sign up or log in to your account
3. Navigate to the API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file

**⚠️ Security Note:** Never commit your `.env` file or API keys to the repository!

## 🚀 Basic Usage

### Using Groq for LLM Inference

Here's a simple example of using Groq to interact with an LLM:

```python
import os
from groq import Groq

# Initialize the Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Create a chat completion
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Explain Tokyo in one sentence.",
        }
    ],
    model="mixtral-8x7b-32768",
)

print(chat_completion.choices[0].message.content)
```

### Using CrewAI with Groq

CrewAI allows you to create AI agents with specific roles and goals. Here's a basic example:

```python
import os
from crewai import Agent, Task, Crew, LLM

# Initialize Groq LLM using CrewAI's native LLM class
llm = LLM(
    model="groq/llama-3.1-70b-versatile"
)

# Create an agent
tokyo_guide = Agent(
    role='Tokyo Travel Expert',
    goal='Provide accurate and helpful information about Tokyo',
    backstory="""You are an experienced travel guide specializing in Tokyo, Japan.
    You have deep knowledge about Tokyo's culture, attractions, food, and transportation.""",
    verbose=True,
    allow_delegation=False,
    llm=llm
)

# Create a task
task = Task(
    description='Recommend 3 must-visit places in Tokyo for first-time visitors',
    agent=tokyo_guide,
    expected_output='A list of 3 places with brief descriptions'
)

# Create a crew and execute
crew = Crew(
    agents=[tokyo_guide],
    tasks=[task],
    verbose=True
)

result = crew.kickoff()
print(result)
```

## 🤖 CrewAI Overview

**CrewAI** is a framework for orchestrating role-playing, autonomous AI agents. Key concepts:

- **Agents**: AI entities with specific roles, goals, and backstories
- **Tasks**: Jobs assigned to agents with expected outputs
- **Crews**: Collections of agents working together
- **Tools**: Custom functions agents can use to perform actions

### Key Features

- 🎭 **Role-Playing Agents**: Agents with distinct personalities and expertise
- 🤝 **Multi-Agent Collaboration**: Agents can delegate and collaborate
- 🔧 **Custom Tools**: Extend agent capabilities with custom functions
- 📊 **Process Management**: Sequential or hierarchical task execution
- 🔄 **Memory**: Agents can maintain context across interactions

### Common Use Cases

- Customer support automation
- Content generation workflows
- Research and analysis tasks
- Data processing pipelines
- Multi-step decision making

## ⚡ Groq Overview

**Groq** provides ultra-fast LLM inference with their custom LPU (Language Processing Unit) technology.

### Supported Models

When using CrewAI's LLM class with Groq, use the `groq/` prefix:

- **groq/llama-3.1-70b-versatile**: Meta's LLaMA 3.1 70B model (recommended)
- **groq/mixtral-8x7b-32768**: Mixtral 8x7B model
- **groq/gemma-7b-it**: Google's Gemma 7B model

See the full list of available models on the [Groq Models page](https://console.groq.com/docs/models).

### Key Features

- ⚡ **Blazing Fast**: 10x+ faster inference than traditional GPU solutions
- 💰 **Cost-Effective**: Competitive pricing for high-throughput applications
- 🌐 **Easy Integration**: Simple REST API and Python SDK
- 🔄 **Streaming Support**: Real-time response streaming
- 📊 **Token Counting**: Accurate token usage tracking

### Rate Limits

Free tier includes:
- 30 requests per minute
- 14,400 tokens per minute

For higher limits, check the [Groq pricing page](https://groq.com/pricing).

## 📚 Example Scripts

See the `examples/python/` directory for complete example scripts:

- `basic_agent.py` - Simple CrewAI agent with Groq

To run an example:

```bash
# Make sure your virtual environment is activated
source venv/bin/activate

# Set your API key
export GROQ_API_KEY=your_api_key_here

# Run an example
python examples/python/basic_agent.py
```

## 🔍 Troubleshooting

### Import Errors

If you encounter import errors:
```bash
# Ensure you're in the virtual environment
which python

# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

### API Key Issues

If you see authentication errors:
- Verify your `GROQ_API_KEY` is set correctly
- Check that the key is valid in the [Groq Console](https://console.groq.com)
- Ensure there are no extra spaces or quotes in your `.env` file

### Rate Limit Errors

If you hit rate limits:
- Add delays between requests using `time.sleep()`
- Implement exponential backoff retry logic
- Consider upgrading your Groq plan for higher limits

### Model Not Found

If you get "model not found" errors:
- Check the [Groq documentation](https://console.groq.com/docs/models) for available models
- Ensure you're using the correct model name
- Some models may require specific API access

## 📖 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com)
- [Groq Documentation](https://console.groq.com/docs)
- [LangChain-Groq Integration](https://python.langchain.com/docs/integrations/chat/groq)

## 🤝 Contributing

When adding new Python functionality:
1. Update `requirements.txt` if adding new dependencies
2. Add example scripts to `examples/python/`
3. Update this README with new usage patterns
4. Follow Python best practices (PEP 8)
5. Test with multiple Python versions (3.9+)

## 📄 License

See the main [LICENSE](LICENSE) file for details.

# AI Agent Template

Production-ready AI Agent template with LangChain, RAG, and multi-agent coordination.

## Features

- ✅ LangChain / CrewAI integration
- ✅ RAG (Retrieval Augmented Generation)
- ✅ Vector database (Pinecone/Weaviate/Chroma)
- ✅ Multiple LLM support (OpenAI, Anthropic, Groq)
- ✅ Custom tools
- ✅ Memory management
- ✅ Multi-agent coordination
- ✅ Prompt templates
- ✅ Streaming responses
- ✅ Function calling
- ✅ Web interface (FastAPI/Streamlit)

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys

# Start agent
python src/main.py
```

## Project Structure

```
agent-template/
├── src/
│   ├── main.py               # Entry point (see main.py.txt)
│   ├── agents/               # Agent definitions
│   │   ├── researcher.py
│   │   ├── writer.py
│   │   └── critic.py
│   ├── tools/                # Custom tools
│   │   ├── web_search.py
│   │   ├── calculator.py
│   │   └── file_ops.py
│   ├── prompts/              # Prompt templates
│   │   ├── system.txt
│   │   └── tasks.txt
│   ├── rag/                  # RAG configuration
│   │   ├── loader.py
│   │   ├── embeddings.py
│   │   └── retriever.py
│   ├── memory/               # Memory management
│   │   └── conversation.py
│   └── utils/                # Utilities
│       ├── logger.py
│       └── config.py
├── data/                     # Knowledge base
│   └── documents/
├── tests/                    # Tests
├── docs/                     # Documentation
└── requirements.txt
```

> **Note:** See `main.py.txt` in this directory for a sample implementation.

## Agent Types

### Research Agent

Searches and analyzes information:

```python
from langchain.agents import Tool
from langchain.agents import initialize_agent

research_agent = initialize_agent(
    tools=[search_tool, scrape_tool],
    llm=llm,
    agent="zero-shot-react-description",
    verbose=True
)

result = research_agent.run("Research recent AI developments")
```

### Writer Agent

Generates content:

```python
writer_agent = Agent(
    role="Content Writer",
    goal="Write engaging articles",
    backstory="Expert writer with 10 years experience",
    tools=[],
    llm=llm
)
```

### Analyst Agent

Analyzes data and provides insights:

```python
analyst_agent = Agent(
    role="Data Analyst",
    goal="Analyze data and provide insights",
    tools=[calculator_tool, chart_tool],
    llm=llm
)
```

## RAG Implementation

### Document Loading

```python
from langchain.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load documents
loader = DirectoryLoader('data/documents')
documents = loader.load()

# Split into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
chunks = text_splitter.split_documents(documents)
```

### Vector Store

```python
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Pinecone

# Create embeddings
embeddings = OpenAIEmbeddings()

# Store in vector database
vectorstore = Pinecone.from_documents(
    chunks,
    embeddings,
    index_name="agent-knowledge"
)
```

### Retrieval

```python
# Create retriever
retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 4}
)

# Retrieve relevant documents
docs = retriever.get_relevant_documents("What is RAG?")
```

### QA Chain

```python
from langchain.chains import RetrievalQA

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

result = qa_chain({"query": "Explain RAG"})
print(result['result'])
print(result['source_documents'])
```

## Custom Tools

### Web Search Tool

```python
from langchain.tools import Tool

def web_search(query: str) -> str:
    """Search the web for information"""
    # Implement web search
    return results

search_tool = Tool(
    name="WebSearch",
    func=web_search,
    description="Search the web for current information"
)
```

### Calculator Tool

```python
import ast
import re

def safe_calculator(expression: str) -> str:
    """
    Safely calculate mathematical expressions.
    Uses AST parsing to prevent code injection.
    Only allows: +, -, *, /, **, ()
    """
    expression = expression.replace(" ", "")
    
    # Validate characters
    if not re.match(r'^[\d+\-*/().\s**]+$', expression):
        return "Error: Invalid characters"
    
    try:
        tree = ast.parse(expression, mode='eval')
        
        # Validate only safe operations
        for node in ast.walk(tree):
            if not isinstance(node, (
                ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
                ast.USub, ast.UAdd, ast.Num, ast.Constant,
                ast.Expression, ast.Load, ast.BinOp, ast.UnaryOp
            )):
                return "Error: Unsupported operation"
        
        result = eval(compile(tree, filename='', mode='eval'))
        return str(result)
    except Exception as e:
        return f"Error: {e}"

calc_tool = Tool(
    name="Calculator",
    func=safe_calculator,
    description="Calculate mathematical expressions safely"
)
```

## Multi-Agent System

### CrewAI Example

```python
from crewai import Crew, Task

# Define tasks
research_task = Task(
    description="Research topic",
    agent=researcher
)

write_task = Task(
    description="Write article",
    agent=writer
)

review_task = Task(
    description="Review article",
    agent=critic
)

# Create crew
crew = Crew(
    agents=[researcher, writer, critic],
    tasks=[research_task, write_task, review_task],
    verbose=True
)

# Execute
result = crew.kickoff()
```

## Memory Management

### Conversation Buffer

```python
from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)
```

### Vector Store Memory

```python
from langchain.memory import VectorStoreRetrieverMemory

memory = VectorStoreRetrieverMemory(
    retriever=retriever,
    memory_key="history"
)
```

## Prompt Templates

```python
from langchain.prompts import PromptTemplate

template = """
You are an expert {role}.
Your task: {task}
Context: {context}

Question: {question}

Provide a detailed answer:
"""

prompt = PromptTemplate(
    input_variables=["role", "task", "context", "question"],
    template=template
)
```

## Streaming Responses

```python
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

llm = ChatOpenAI(
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)

for chunk in llm.stream("Tell me a story"):
    print(chunk.content, end="", flush=True)
```

## Web Interface

### FastAPI

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
async def ask(query: Query):
    result = agent.run(query.question)
    return {"answer": result}
```

### Streamlit

```python
import streamlit as st

st.title("AI Agent")

question = st.text_input("Ask a question:")
if st.button("Submit"):
    with st.spinner("Thinking..."):
        answer = agent.run(question)
        st.write(answer)
```

## Configuration

```python
# .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
PINECONE_API_KEY=...
PINECONE_ENV=us-west1-gcp
```

## Testing

```bash
# Run tests
pytest tests/

# With coverage
pytest --cov=src tests/
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "src/main.py"]
```

### Railway

```bash
railway init
railway add
railway up
```

## Cost Optimization

- Use cheaper models for simple tasks
- Cache responses
- Batch requests
- Limit token usage
- Use streaming for UX

## Monitoring

- Log all queries and responses
- Track token usage
- Monitor latency
- Error tracking
- User feedback

## License

MIT License

---

Generated with Tokyo-IA Elite Framework

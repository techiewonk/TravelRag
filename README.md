# 💼 AI Platform

[![Python Version](https://img.shields.io/python/required-version-toml?tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Ftechiewonk%2FTravelRag%2Frefs%2Fheads%2Fmain%2Fpyproject.toml)](https://github.com/techiewonk/TravelRag/blob/main/pyproject.toml)
[![GitHub License](https://img.shields.io/github/license/techiewonk/TravelRag)](https://github.com/techiewonk/TravelRag/blob/main/LICENSE)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_red.svg)](https://github.com/techiewonk/TravelRag)

Built with [LangGraph](https://langchain-ai.github.io/langgraph/), [FastAPI](https://fastapi.tiangolo.com/), and [Streamlit](https://streamlit.io/), this platform delivers enterprise-grade financial intelligence through specialized AI agents with comprehensive market data integration.

## 🏗️ **System Architecture Overview**

The TravelRag project is a **full-stack AI agent service toolkit** built with LangGraph, FastAPI, and Streamlit. It provides a complete framework for building, deploying, and interacting with AI agents.

## 📊 **Complete Flow Analysis**

### **User Interaction Flow**

```
User Input → Streamlit App → AgentClient → FastAPI Service → Agent Selection → LangGraph Execution
```

### **Agent Execution Flow**

```
Input → Safety Check (LlamaGuard) → Model Selection → Tool Binding → Graph Execution → Response Streaming
```

### **Memory Management Flow**

```
Thread ID → Checkpointer (Short-term) → Store (Long-term) → Vector DB (RAG) → Response Generation
```

### **Multi-Agent Coordination Flow**

```
Supervisor Agent → Sub-Agent Selection → Task Delegation → Result Aggregation → Response Synthesis
```

## 🎯 **Multi-Agent Architecture Overview**

### **Hierarchical Supervisor System**

- **Main Supervisor Agent** 🎯: Master orchestrator managing entire investment advisory workflow
- **Analysis Team Supervisor** 📊: Specialized coordinator for quantitative analysis and portfolio management

### **Specialized Expert Agents**

- **🔬 Market Research Expert**: Market intelligence, SEC filings, economic indicators, news sentiment analysis
- **📊 Portfolio Expert**: Portfolio management, technical analysis (15+ indicators), securities tracking, performance attribution
- **⚖️ Risk Optimization Expert**: VaR/CVaR calculations, regulatory compliance, stress testing, MPT optimization
- **🧮 Math Expert**: Advanced quantitative analysis, Black-Scholes pricing, statistical modeling, backtesting

## 🚀 **Enterprise Features**

### **Advanced Financial Analysis**

- **Real-Time Market Data**: Yahoo Finance, Alpha Vantage, FRED integration with 5-minute caching
- **Technical Analysis**: 15+ indicators including RSI, MACD, Bollinger Bands, Stochastic, ATR, moving averages
- **Fundamental Analysis**: P/E ratios, ROE, debt ratios, financial health scoring, SEC filings analysis
- **Risk Assessment**: VaR (95%/99%), CVaR, maximum drawdown, volatility modeling, stress testing
- **Portfolio Optimization**: Modern Portfolio Theory, efficient frontier analysis, risk-return optimization

### **Regulatory Compliance & Risk Management**

- **Position Limits**: 10% single position monitoring
- **Sector Concentration**: 25% sector limit compliance
- **Liquidity Requirements**: 5% minimum liquid assets
- **Leverage Monitoring**: 2:1 maximum leverage compliance
- **Derivatives Exposure**: 15% options/derivatives limit
- **Stress Testing**: 5 adverse scenarios (market crash, recession, inflation surge, etc.)

### **Production-Ready Infrastructure**

- **Multi-Provider LLM Support**: OpenAI, Anthropic, Google, Groq, AWS Bedrock, Ollama
- **Advanced Streaming**: Real-time token and message streaming with WebSocket support
- **Memory Persistence**: PostgreSQL, SQLite, MongoDB checkpointers for conversation state
- **Content Safety**: LlamaGuard integration for compliance and content moderation
- **Containerization**: Complete Docker setup with health checks and auto-scaling
- **Observability**: LangSmith, Langfuse integration for monitoring and tracing

### **Data Flow & Coordination**

- **SharedDataCache**: Thread-safe inter-agent communication system
- **AgentDataPacket**: Structured data exchange format with metadata
- **Workflow Coordination**: Pre-defined investment analysis workflows
- **Subscription Model**: Agents subscribe to relevant data types for efficient processing

## 🚀 **Quick Start**

### **Prerequisites**

- Python 3.11+ (3.12 recommended)
- Docker & Docker Compose
- At least one LLM API key (OpenAI, Anthropic, etc.)
- Financial API keys (optional but recommended for full functionality)

### **Installation**

1. **Clone the repository:**

   ```bash
   git clone https://github.com/techiewonk/TravelRag.git
   cd TravelRag
   ```

2. **Set up environment variables:**

   ```bash
   cp .env.example .env
   # Edit .env to add your API keys
   ```

3. **Essential API Keys:**

   ```bash
   # LLM Providers (at least one required)
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key

   # Financial Data APIs (recommended)
   FRED_API_KEY=your_fred_api_key
   ALPHA_VANTAGE_API_KEY=your_alpha_vantage_key
   NEWS_API_KEY=your_news_api_key
   ```

4. **Install dependencies:**

   ```bash
   # Using uv (recommended)
   curl -LsSf https://astral.sh/uv/install.sh | sh
   uv sync --frozen

   # Or using pip
   pip install -e .
   ```

### **Running the Application**

#### **Option 1: Docker (Production-Ready)**

```bash
# Start all services with hot reloading
docker compose watch

# Or start in background
docker compose up -d
```

- **Streamlit App**: http://localhost:8501
- **FastAPI Service**: http://localhost:8080
- **API Documentation**: http://localhost:8080/doc
- **PostgreSQL**: localhost:5432

#### **Option 2: Local Development**

```bash
# Terminal 1: Start the API service
python src/run_service.py

# Terminal 2: Start the Streamlit app
streamlit run src/streamlit_app.py

# Terminal 3: (Optional) Run individual agents via LangGraph
langgraph up supervisor-agent
```

#### **Option 3: LangGraph CLI (Agent Development)**

```bash
# Run individual agents for testing

langgraph up math-agent
```

## 📊 **Comprehensive Data Sources**

### **Market Data Providers**

- **Yahoo Finance**: Real-time stock prices, historical data, market cap, volume
- **Alpha Vantage**: Technical indicators, fundamental data, forex, crypto
- **FRED**: 800,000+ economic time series (GDP, inflation, unemployment, Fed rates)
- **Financial Modeling Prep**: SEC filings, company profiles, financial ratios

### **News & Sentiment**

- **NewsAPI**: Real-time financial news with sentiment analysis
- **Economic Indicators**: Real-time monitoring of economic policy changes
- **Regulatory Updates**: SEC, Federal Reserve, and regulatory body announcements

### **Technical Analysis**

- **15+ Technical Indicators**: RSI, MACD, Bollinger Bands, Stochastic, ATR, OBV, VWAP
- **Chart Pattern Recognition**: Support/resistance levels, trend analysis
- **Volume Analysis**: Trading volume patterns and momentum indicators

## 🏗️ **System Architecture**

### **Agent Communication Flow**

```
Main Supervisor Agent
    ├── Market Research Expert (News, Economics, SEC Filings)
    ├── Analysis Team Supervisor
    │   ├── Portfolio Expert (Technical Analysis, Holdings)
    │   └── Math Expert (Quantitative Analysis, Risk Metrics)
    └── Risk Optimization Expert (Compliance, Optimization)
```

### **Data Flow Architecture**

- **SharedDataCache**: Thread-safe inter-agent communication
- **AgentDataPacket**: Structured data exchange with metadata
- **Workflow Coordination**: Multi-step investment analysis workflows
- **Real-time Synchronization**: Thread-specific data isolation and ordering

### **Production Infrastructure**

- **Microservices**: Containerized FastAPI backend, Streamlit frontend
- **Database Layer**: PostgreSQL with connection pooling, SQLite for development
- **Caching**: 5-minute API response caching for performance
- **Security**: Bearer token authentication, content validation, rate limiting

## 🔄 **Complete System Flow Diagram**

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                USER INTERFACE LAYER                             │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Streamlit App (Port 8501)          │  Direct Client Usage                      │
│  ┌─────────────────────────────┐    │  ┌─────────────────────────────────────┐  │
│  │ • Chat Interface            │    │  │ • AgentClient                       │  │
│  │ • Agent Selection           │    │  │ • Sync/Async Methods                │  │
│  │ • Model Selection           │    │  │ • Streaming Support                 │  │
│  │ • Feedback System           │    │  │ • History Management                │  │
│  │ • Thread Management         │    │  │                                     │  │
│  └─────────────────────────────┘    │  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SERVICE LAYER (FastAPI)                            │
├─────────────────────────────────────────────────────────────────────────────────┤
│  FastAPI Service (Port 8080)                                                    │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │ Endpoints:                                                              │    │
│  │ • /info - Service metadata                                              │    │
│  │ • /{agent_id}/invoke - Non-streaming agent calls                        │    │
│  │ • /{agent_id}/stream - Streaming agent calls                            │    │
│  │ • /feedback - LangSmith feedback recording                              │    │
│  │ • /history - Chat history retrieval                                     │    │
│  │ • /health - Health check                                                │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                                AGENT LAYER                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Agent Registry & Execution                                                     │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │ Available Agents:                                                       │    │
│  │ • research-assistant (default) - Web search + calculator                │    │
│  │ • rag-assistant - ChromaDB knowledge base                               │    │
│  │ • chatbot - Simple conversational agent                                 │    │
│  │ • langgraph-supervisor-agent - Multi-agent coordination                 │    │
│  │ • interrupt-agent - Human-in-the-loop workflows                         │    │
│  │ • github-mcp-agent - GitHub integration via MCP                         │    │
│  │ • bg-task-agent - Background task processing                            │    │
│  │ • knowledge-base-agent - Amazon Bedrock integration                     │    │
│  │ • command-agent - Command execution                                     │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              LANGGRAPH EXECUTION                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│  Agent Graph Processing                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │ 1. Input Validation & Safety Check (LlamaGuard)                         │    │
│  │ 2. Model Selection & Tool Binding                                       │    │
│  │ 3. Graph Node Execution:                                                │    │
│  │    • Model Node - LLM inference                                         │    │
│  │    • Tool Node - Tool execution                                         │    │
│  │    • Conditional Edges - Flow control                                   │    │
│  │ 4. Streaming Response Generation                                        │    │
│  │ 5. Memory Persistence                                                   │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CORE COMPONENTS                                    │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────┐ │
│  │ LLM Providers   │  │ Memory Systems  │  │ Tools & Utils   │  │ Safety      │ │
│  │ • OpenAI        │  │ • SQLite        │  │ • Web Search    │  │ • LlamaGuard│ │
│  │ • Anthropic     │  │ • PostgreSQL    │  │ • Calculator    │  │ • Content   │ │
│  │ • Google        │  │ • MongoDB       │  │ • Weather API   │  │   Moderation│ │
│  │ • Groq          │  │ • Checkpointer  │  │ • Database      │  │             │ │
│  │ • Ollama        │  │ • Store         │  │ • GitHub MCP    │  │             │ │
│  │ • Azure OpenAI  │  │ • Thread Memory │  │ • RAG Search    │  │             │ │
│  │ • AWS Bedrock   │  │ • Long-term     │  │ • File I/O      │  │             │ │
│  │ • Fake Models   │  │   Memory        │  │ • Custom Tools  │  │             │ │
│  └─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────┘ │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA PERSISTENCE                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────────────────────┐    │
│  │ Database Layer (Configurable):                                          │    │
│  │ • SQLite (default) - Local development                                  │    │
│  │ • PostgreSQL - Production with connection pooling                       │    │
│  │ • MongoDB - Document-based storage                                      │    │
│  │                                                                         │    │
│  │ Memory Types:                                                           │    │
│  │ • Checkpointer - Conversation state & thread memory                     │    │
│  │ • Store - Long-term knowledge & cross-conversation data                 │    │
│  │ • Vector Store - RAG embeddings (ChromaDB)                              │    │
│  └─────────────────────────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### **Detailed Flow Process**

#### **1. User Interaction Flow**

```
User Input → Streamlit App → AgentClient → FastAPI Service → Agent Selection → LangGraph Execution
```

#### **2. Agent Execution Flow**

```
Input → Safety Check (LlamaGuard) → Model Selection → Tool Binding → Graph Execution → Response Streaming
```

#### **3. Memory Management Flow**

```
Thread ID → Checkpointer (Short-term) → Store (Long-term) → Vector DB (RAG) → Response Generation
```

#### **4. Multi-Agent Coordination Flow**

```
Supervisor Agent → Sub-Agent Selection → Task Delegation → Result Aggregation → Response Synthesis
```

### **Key Components Breakdown**

#### **Entry Points**

- **`src/run_service.py`** - FastAPI service startup
- **`src/streamlit_app.py`** - Web UI application
- **`src/run_client.py`** - Direct client usage examples

#### **Core Architecture**

- **`src/core/`** - LLM providers, settings, and configuration
- **`src/agents/`** - Agent definitions and implementations
- **`src/service/`** - FastAPI service layer
- **`src/client/`** - HTTP client for service interaction
- **`src/schema/`** - Data models and API schemas
- **`src/memory/`** - Database and persistence layer

#### **Agent Types**

1. **Research Assistant** - Web search + calculator tools
2. **RAG Assistant** - ChromaDB knowledge base integration
3. **Supervisor Agent** - Multi-agent coordination
4. **Interrupt Agent** - Human-in-the-loop workflows
5. **GitHub MCP Agent** - Repository management
6. **Background Task Agent** - Async task processing

#### **Memory Systems**

- **Checkpointer** - Conversation state persistence
- **Store** - Long-term knowledge storage
- **Vector Store** - RAG embeddings (ChromaDB)

#### **Safety & Monitoring**

- **LlamaGuard** - Content moderation
- **LangSmith** - Tracing and feedback
- **Langfuse** - Alternative tracing platform

## 🛠️ **Development Guide**

### **Project Structure**

```
src/
├── agents/                 # AI agent implementations
│   ├── supervisor_agent.py    # Main orchestrator
│   ├── portfolio_agent.py     # Portfolio management specialist
│   ├── market_research_agent.py # Market intelligence expert
│   ├── risk_optimization_agent.py # Risk & compliance specialist
│   ├── math_agent.py          # Quantitative analysis expert
│   ├── shared_data_flow.py    # Inter-agent communication
│   └── tools/                 # Specialized tool implementations
├── core/                   # Core LLM and settings
├── schema/                 # Data models and validation
├── service/                # FastAPI service layer
│   ├── service.py             # Main API endpoints
│   └── portfolio_service.py   # Portfolio data management
├── client/                 # HTTP client for API interaction
├── memory/                 # Database adapters and storage
└── streamlit_app.py       # Web interface
```

### **Adding New Agents**

1. Create agent in `src/agents/your_agent.py`
2. Implement agent creation function and export agent variable
3. Add to `src/agents/agents.py` registry
4. Update `langgraph.json` for LangGraph CLI support
5. Add to Streamlit interface if needed

### **Creating Custom Tools**

```python
from langchain_core.tools import tool

@tool
def your_custom_tool(parameter: str) -> dict:
    """Your tool description for the agent."""
    # Implementation
    return {"result": "your_analysis"}
```

### **Testing & Quality Assurance**

```bash
# Install development dependencies
uv sync --frozen --group dev

# Run comprehensive tests
pytest --cov=src --cov-report=html

# Code quality checks
ruff check src/
mypy src/

# Pre-commit hooks
pre-commit install
pre-commit run --all-files
```

## 🔧 **Configuration**

### **Core Environment Variables**

```bash
# LLM Providers
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
GOOGLE_API_KEY=your-google-key
GROQ_API_KEY=gsk_your-groq-key

# Database Configuration
DATABASE_TYPE=postgres  # sqlite, postgres, mongo
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-secure-password
POSTGRES_DB=investadvisory

# Financial Data APIs
FRED_API_KEY=your-fred-key
ALPHA_VANTAGE_API_KEY=your-alphavantage-key
NEWS_API_KEY=your-newsapi-key
FINANCIAL_MODELING_PREP_API_KEY=your-fmp-key

# Observability
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your-langsmith-key
LANGFUSE_PUBLIC_KEY=your-langfuse-key

# Security
AUTH_SECRET=your-secure-auth-token
```

### **Advanced Configuration**

- **Model Selection**: Support for 10+ LLM providers with fallback strategies
- **Memory Backends**: PostgreSQL, SQLite, MongoDB with automatic migration
- **Caching Strategy**: Configurable TTL, Redis integration for production
- **Rate Limiting**: Per-API provider rate limiting with exponential backoff
- **Content Safety**: Configurable LlamaGuard policies and custom filters

## 📈 **Use Cases & Applications**

## 🚀 **Production Deployment**

### **Docker Production Setup**

```bash
# Production deployment with scaling
docker compose -f docker-compose.prod.yml up -d

# Health checks and monitoring
docker compose ps
docker compose logs -f agent_service
```

### **Kubernetes Deployment**

```yaml
# Example Kubernetes deployment
apiVersion: apps/v1
kind: Deployment
metadata:
  name: investment-advisory
spec:
  replicas: 3
  selector:
    matchLabels:
      app: investment-advisory
  template:
    metadata:
      labels:
        app: investment-advisory
    spec:
      containers:
        - name: agent-service
          image: investment-advisory:latest
          ports:
            - containerPort: 8080
```

### **Performance Metrics**

- **API Response Time**: < 500ms (95th percentile)
- **System Uptime**: 99.9% availability target
- **Concurrent Users**: 1000+ supported
- **Database Performance**: < 100ms query response time
- **Memory Usage**: < 2GB per container instance

## 🤝 **Contributing**

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### **Development Workflow**

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes with tests
4. Run quality checks (`ruff check`, `mypy`, `pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### **Areas for Contribution**

- New financial data providers
- Additional technical indicators
- Enhanced risk models
- UI/UX improvements
- Documentation and tutorials
- Performance optimizations

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 **Author**

**Hemprasad Badgujar**

- Email: hemprasad@badgujar.org
- GitHub: [@techiewonk](https://github.com/techiewonk)
- LinkedIn: [Hemprasad Badgujar](https://www.linkedin.com/in/hemprasad-badgujar/)

## 🙏 **Acknowledgments**

- Built on the foundation of modern AI agent architectures
- Powered by [LangGraph](https://langchain-ai.github.io/langgraph/) and [LangChain](https://langchain.com/)
- Financial data provided by Yahoo Finance, Alpha Vantage, FRED, and NewsAPI
- Technical analysis powered by TA-Lib and pandas-ta
- Risk models based on Modern Portfolio Theory and quantitative finance principles

## 📞 **Support**

For support, please:

1. Check the [documentation](docs/)
2. Search existing [GitHub Issues](https://github.com/techiewonk/TravelRag/issues)
3. Open a new issue with detailed information
4. Contact [hemprasad@badgujar.org](mailto:hemprasad@badgujar.org) for enterprise support

## 🔮 **Roadmap**

---

**⚠️ Important Disclaimer**: This software is for educational and research purposes only. It is not intended to provide financial advice. All investment decisions should be made in consultation with qualified financial professionals. Past performance does not guarantee future results. Always consider your risk tolerance and investment objectives before making investment decisions.

**🔒 Security Notice**: This platform handles sensitive financial data. Always use secure API keys, enable proper authentication, and follow security best practices when deploying in production environments.

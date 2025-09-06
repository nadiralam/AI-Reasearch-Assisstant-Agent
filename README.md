# Research Assistant Agent 🤖

A powerful AI-powered research assistant built with **LangChain** and **LangGraph** that automatically conducts comprehensive research on any topic and generates detailed reports.

## 🌟 Features

- **Intelligent Query Planning**: Automatically generates focused search queries
- **Multi-Source Research**: Searches the web using DuckDuckGo
- **Content Analysis**: Extracts key insights from search results
- **Iterative Research**: Conducts multiple research cycles for comprehensive coverage
- **Report Generation**: Creates structured, professional research reports
- **Conditional Routing**: Smart decision-making for when to continue or complete research

## 🏗️ Architecture

The agent uses LangGraph to orchestrate the research workflow:

```
start → plan_queries → search → analyze → synthesize
           ↑                                  ↓
           └──────── continue ←───────────────┘
                                              ↓
                                         finish
                                              ↓
                                    generate_report → end
```

## 📁 Project Structure

```
research_assistant_agent/
├── README.md
├── requirements.txt
├── .env                        # Your API keys
├── main.py                     # Main entry point
├── agent.py                    # LangGraph workflow
├── nodes.py                    # All node functions
├── prompts.py                  # Prompt templates
├── tools.py                    # Utilities and tools
├── setup_check.py              # Environment verification
├── examples/
│   └── basic_example.py        # Usage examples
└── outputs/
    └── reports/                # Generated reports
```

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <your-repo>
cd research_assistant_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup Environment

Create a `.env` file with your OpenAI API key:

```bash
echo "OPENAI_API_KEY=your_openai_api_key_here" > .env
```

### 4. Verify Setup

```bash
python setup_check.py
```

### 5. Run the Agent

```bash
python main.py
```

## 📖 Usage

### Interactive Mode

```bash
python main.py
```

Then enter any research topic:
- "Impact of artificial intelligence on healthcare"
- "Benefits of renewable energy"
- "Future of quantum computing"

### Programmatic Usage

```python
from agent import research_agent

# Conduct research
result = research_agent.research("Your research topic")

# Get the report
report = research_agent.get_report(result)
print(report)
```

### Example Output

The agent generates comprehensive reports with:
- **Executive Summary**: Key findings overview
- **Main Findings**: Detailed research results
- **Supporting Data**: Statistics and evidence
- **Conclusions**: Implications and takeaways
- **Sources**: Referenced materials with credibility notes

Reports are automatically saved to `outputs/reports/` with timestamps.

## 🧠 How It Works

### 1. Query Planning
- Analyzes the research topic
- Generates 3-5 focused search queries
- Considers different aspects and angles

### 2. Web Search
- Executes searches using DuckDuckGo
- Collects diverse information sources
- Handles search errors gracefully

### 3. Content Analysis
- Extracts key facts and statistics
- Identifies expert opinions
- Assesses source credibility
- Scores relevance and quality

### 4. Synthesis
- Reviews all collected information
- Identifies knowledge gaps
- Decides whether to continue research
- Maximum of 3 research iterations

### 5. Report Generation
- Creates structured, professional reports
- Synthesizes findings from all sources
- Provides actionable insights
- Lists all referenced sources

## ⚙️ Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=your_openai_api_key

# Optional
MODEL_NAME=gpt-4o-mini
TEMPERATURE=0.1
MAX_TOKENS=2000
```

### Customization

You can modify the behavior by editing:

- **prompts.py**: Change how queries are generated and content is analyzed
- **nodes.py**: Modify the research logic and decision-making
- **tools.py**: Add new search tools or change LLM settings

## 📊 Research Quality

The agent automatically evaluates research quality based on:
- **Information Coverage**: Breadth of topics covered
- **Source Diversity**: Variety of information sources
- **Content Depth**: Detailed analysis and insights
- **Confidence Level**: Reliability of findings

Research continues until:
- Quality threshold is met (confidence > 7/10)
- Maximum iterations reached (3 cycles)
- Sufficient information coverage achieved

## 🛠️ Development

### Running Tests

```bash
# Basic functionality test
python examples/basic_example.py

# Environment check
python setup_check.py
```

### Adding New Features

1. **New Search Tools**: Add to `tools.py`
2. **Enhanced Analysis**: Modify prompts in `prompts.py`
3. **Custom Routing**: Update decision logic in `nodes.py`
4. **New Report Formats**: Extend `report_generator` function

## 🔍 Example Research Topics

Try these topics to see the agent in action:

**Technology:**
- "Latest developments in quantum computing"
- "Impact of 5G technology on IoT"
- "Ethical considerations in AI development"

**Business:**
- "Remote work productivity trends 2024"
- "Sustainable business practices ROI"
- "Digital transformation challenges"

**Science:**
- "Climate change mitigation strategies"
- "Breakthrough in renewable energy storage"
- "Advances in cancer immunotherapy"

## 📈 Performance Tips

- **API Costs**: Uses GPT-4o-mini for cost efficiency
- **Rate Limits**: Built-in delays between API calls
- **Caching**: Stores search results to avoid redundant queries
- **Error Handling**: Graceful failure recovery

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Troubleshooting

### Common Issues

**API Key Error:**
```
OpenAIError: The api_key client option must be set
```
→ Check your `.env` file has the correct `OPENAI_API_KEY`

**Import Errors:**
```
ModuleNotFoundError: No module named 'langchain'
```
→ Run `pip install -r requirements.txt`

**No Search Results:**
```
Search failed: connection error
```
→ Check your internet connection

### Getting Help

1. Run `python setup_check.py` to diagnose issues
2. Check the generated logs in `outputs/logs/`
3. Review example usage in `examples/basic_example.py`

## 🎯 Future Enhancements

- [ ] Support for academic paper search
- [ ] Multi-language research capabilities
- [ ] Integration with Google Scholar
- [ ] Visual data charts in reports
- [ ] Research template system
- [ ] Collaborative research features
- [ ] Export to PDF/Word formats

---

**Built with ❤️ using LangChain and LangGraph**

*Happy Researching! 🔍📚*

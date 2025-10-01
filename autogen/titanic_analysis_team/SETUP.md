# Titanic Analysis Team - Setup Guide

## What We've Accomplished

✅ **Wikipedia MCP Integration**: Added Wikipedia agent using MCP server
✅ **Enhanced Data Scientist**: Dr. Data can now generate plots based on team responses
✅ **Report Generator**: Creates comprehensive Jupyter notebook reports
✅ **No Raw Data Policy**: All agents provide insights, never raw database data
✅ **Multi-Agent Collaboration**: Four specialized agents working together

## New Structure

```
titanic_analysis_team/
├── agents/
│   ├── wikipedia_agent.py              # Wikipedia MCP integration
│   ├── report_generator_agent.py       # Jupyter notebook generation
│   ├── enhanced_data_scientist_agent.py # Advanced visualization
│   └── math_reasoning.py               # Mathematical reasoning
├── tools/
│   ├── sqlite_tools.py                 # Database operations
│   ├── visualization_tools.py          # Plot creation
│   ├── math.py                         # Mathematical operations
│   └── tools.py                        # Utility functions
├── data/
│   ├── titanic.db                      # Titanic dataset
│   └── example.db                      # Example database
├── reports/                            # Generated reports (auto-created)
├── config/
│   └── mcp_config.json                # MCP server configuration
├── enhanced_chat.py                    # Main chat interface
├── test_team.py                        # Test suite
├── run_team.py                         # Launcher script
└── README.md                           # Documentation
```

## Team Members

### 🔍 Jarvis - Research Assistant
- Analyzes Titanic data using SQL queries
- Provides insights and findings
- Never shows raw database data
- Suggests visualizations

### 📊 Dr. Data - Enhanced Data Scientist
- Creates visualizations based on team findings
- Automatically analyzes team responses
- Generates custom charts and dashboards
- Can create plots from team analysis

### 🌐 Wikipedia Agent
- Provides historical context via MCP
- Searches Wikipedia for relevant information
- Offers insights about Titanic disaster
- Uses Model Context Protocol

### 📝 Report Generator Agent
- Creates comprehensive Jupyter notebooks
- Consolidates team findings
- Generates professional reports
- Organizes insights in structured format

## Key Features

1. **Wikipedia Integration**: Historical context via MCP server
2. **Automated Visualization**: Plots generated based on team analysis
3. **Report Generation**: Comprehensive Jupyter notebook reports
4. **Enhanced Data Analysis**: Never shows raw data, always provides insights
5. **Multi-Agent Collaboration**: Four specialized agents working together
6. **Organized Structure**: Clean, modular codebase

## How to Use

### 1. Basic Test
```bash
cd /home/mileidy/Documents/study/AI/agents/base/autogen/titanic_analysis_team
python test_team.py
```

### 2. Start the Intelligent Team
```bash
python start_team.py
```

### 3. Direct Chat Interface
```bash
python enhanced_chat.py
```

## Example Queries

- "Analyze the relationship between passenger class and survival rates"
- "What was the demographic breakdown of Titanic passengers?"
- "Create visualizations showing age distribution and survival"
- "Generate a comprehensive report of our analysis"
- "Search Wikipedia for historical context about the Titanic disaster"

## Requirements

- Python 3.8+
- OpenAI API key
- SQLite database with Titanic data
- Wikipedia MCP server (installed)

## Next Steps

1. Set up your OpenAI API key in `.env` file
2. Ensure Titanic data is properly loaded in the database
3. Run the test suite to verify everything works
4. Start using the enhanced chat interface

## Notes

- All agents are designed to provide insights, not raw data
- Dr. Data automatically creates plots based on team responses
- Wikipedia agent provides historical context via MCP
- Report generator creates comprehensive Jupyter notebooks
- The system is fully modular and extensible

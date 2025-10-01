# Titanic Analysis Team

A comprehensive AI agent team for analyzing Titanic passenger data with enhanced capabilities including Wikipedia integration, automated visualization, and report generation.

## Team Members

### 🔍 Jarvis - Research Assistant
- Analyzes Titanic data using SQL queries and statistical tools
- Provides insights and findings from the data
- Never shows raw database data - always provides analysis
- Suggests visualizations when appropriate

### 📊 Dr. Data - Enhanced Data Scientist
- Creates visualizations based on team findings
- Automatically analyzes team responses to determine appropriate plots
- Generates custom charts and comprehensive dashboards
- Ensures all visualizations enhance data understanding

### 🌐 Wikipedia Agent
- Provides additional context when other agents lack information
- Acts as a fallback knowledge base when research is insufficient
- Searches Wikipedia for relevant historical information
- Uses MCP (Model Context Protocol) for Wikipedia access
- Automatically activated when research response is incomplete or unclear

### 📝 Report Generator Agent
- Creates comprehensive Jupyter notebook reports
- Consolidates team findings and visualizations
- Generates professional analysis reports
- Organizes insights in structured format

## Features

- **Multi-Agent Collaboration**: Four specialized agents working together
- **Intelligent Wikipedia Integration**: Wikipedia agent acts as fallback when other agents lack information
- **Database-Independent Reports**: Can generate comprehensive reports using only Wikipedia data
- **Automated Visualization**: Plots generated based on team analysis (when database available)
- **Report Generation**: Comprehensive Jupyter notebook reports with or without database data
- **Enhanced Data Analysis**: Never shows raw data, always provides insights
- **Smart Context Detection**: Automatically determines when additional context is needed
- **Organized Structure**: Clean, modular codebase

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

3. Run the enhanced chat:
```bash
python enhanced_chat.py
```

## Usage

### Start the Intelligent Team
```bash
python start_team.py
```

### Direct Chat Interface
```bash
python enhanced_chat.py
```

### Test Individual Agents
```bash
python enhanced_chat.py test
```

### Example Queries
- "Analyze the relationship between passenger class and survival rates"
- "What was the demographic breakdown of Titanic passengers?"
- "Create visualizations showing age distribution and survival"
- "Generate a comprehensive report of our analysis"
- "Tell me about the Titanic disaster and show me survival data"

## Project Structure

```
titanic_analysis_team/
├── agents/
│   ├── wikipedia_agent.py              # Wikipedia MCP integration
│   ├── report_generator_agent.py       # Jupyter notebook generation
│   └── enhanced_data_scientist_agent.py # Advanced visualization
├── tools/
│   ├── sqlite_tools.py                 # Database operations
│   ├── visualization_tools.py          # Plot creation
│   └── math.py                         # Mathematical operations
├── data/
│   └── titanic.db                      # Titanic dataset
├── reports/                            # Generated reports
├── config/
│   └── mcp_config.json                # MCP server configuration
├── enhanced_chat.py                    # Main chat interface
└── requirements.txt                    # Dependencies
```

## Key Improvements

1. **Better Organization**: Clean folder structure with descriptive names
2. **Wikipedia Integration**: Historical context via MCP server
3. **Enhanced Data Scientist**: Can generate plots based on team responses
4. **Report Generation**: Automatic Jupyter notebook creation
5. **No Raw Data**: All responses provide insights, not raw database data
6. **Comprehensive Analysis**: Multi-agent collaboration for thorough analysis

## MCP Configuration

The system uses Model Context Protocol (MCP) for Wikipedia access:

```json
{
  "mcpServers": {
    "wikipedia": {
      "command": "wikipedia-mcp",
      "args": []
    }
  }
}
```

## Requirements

- Python 3.8+
- OpenAI API key
- SQLite database with Titanic data
- Wikipedia MCP server

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - see LICENSE file for details

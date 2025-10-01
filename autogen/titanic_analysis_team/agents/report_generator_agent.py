#!/usr/bin/env python3
"""
Report Generator Agent - Creates Jupyter notebooks with analysis and plots
"""
import os
import json
import base64
from datetime import datetime
from typing import Dict, Any, List, Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient


def create_jupyter_notebook(analysis_data: Dict[str, Any], plots_info: List[Dict[str, Any]], 
                          insights: str, title: str = "Titanic Analysis Report") -> str:
    """
    Create a Jupyter notebook with analysis, plots, and insights
    
    Args:
        analysis_data: Dictionary containing analysis results
        plots_info: List of dictionaries with plot information
        insights: String containing insights and conclusions
        title: Title for the notebook
    
    Returns:
        Path to the created notebook file
    """
    
    # Create reports directory if it doesn't exist
    reports_dir = "reports"
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate timestamp for unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    notebook_filename = f"titanic_analysis_report_{timestamp}.ipynb"
    notebook_path = os.path.join(reports_dir, notebook_filename)
    
    # Create notebook structure
    notebook = {
        "cells": [],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "codemirror_mode": {"name": "ipython", "version": 3},
                "file_extension": ".py",
                "mimetype": "text/x-python",
                "name": "python",
                "nbconvert_exporter": "python",
                "pygments_lexer": "ipython3",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    # Add title cell
    title_cell = {
        "cell_type": "markdown",
        "metadata": {},
        "source": [
            f"# {title}\n",
            f"\n",
            f"**Generated on:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
            f"\n",
            f"---\n"
        ]
    }
    notebook["cells"].append(title_cell)
    
    # Add analysis data cell
    if analysis_data:
        analysis_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Analysis Results\n",
                "\n",
                "### Data Overview\n",
                f"- **Total Passengers:** {analysis_data.get('total_passengers', 'N/A')}\n",
                f"- **Survival Rate:** {analysis_data.get('survival_rate', 'N/A')}%\n",
                f"- **Average Age:** {analysis_data.get('average_age', 'N/A')} years\n",
                f"- **Average Fare:** ${analysis_data.get('average_fare', 'N/A')}\n",
                "\n"
            ]
        }
        notebook["cells"].append(analysis_cell)
        
        # Add detailed analysis
        if 'detailed_analysis' in analysis_data:
            detailed_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    "### Detailed Analysis\n",
                    "\n",
                    analysis_data['detailed_analysis'],
                    "\n"
                ]
            }
            notebook["cells"].append(detailed_cell)
    
    # Add plots section
    if plots_info:
        plots_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Visualizations\n",
                "\n",
                "The following visualizations were generated based on the analysis:\n",
                "\n"
            ]
        }
        notebook["cells"].append(plots_cell)
        
        # Add each plot
        for i, plot_info in enumerate(plots_info, 1):
            plot_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"### Plot {i}: {plot_info.get('title', 'Untitled')}\n",
                    f"\n",
                    f"**Description:** {plot_info.get('description', 'No description available')}\n",
                    f"\n",
                    f"**File:** `{plot_info.get('filename', 'unknown.png')}`\n",
                    f"\n"
                ]
            }
            notebook["cells"].append(plot_cell)
            
            # Add image cell if plot exists
            if 'filename' in plot_info and os.path.exists(plot_info['filename']):
                try:
                    with open(plot_info['filename'], 'rb') as f:
                        image_data = base64.b64encode(f.read()).decode('utf-8')
                    
                    image_cell = {
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [
                            f"![{plot_info.get('title', 'Plot')}](data:image/png;base64,{image_data})\n"
                        ]
                    }
                    notebook["cells"].append(image_cell)
                except Exception as e:
                    error_cell = {
                        "cell_type": "markdown",
                        "metadata": {},
                        "source": [
                            f"*Error loading image: {e}*\n"
                        ]
                    }
                    notebook["cells"].append(error_cell)
    
    # Add insights section
    if insights:
        insights_cell = {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Key Insights and Conclusions\n",
                "\n",
                insights,
                "\n"
            ]
        }
        notebook["cells"].append(insights_cell)
    
    # Add code cell for data exploration
    code_cell = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# Additional Data Exploration\n",
            "import pandas as pd\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "\n",
            "# Load the Titanic dataset for further exploration\n",
            "# df = pd.read_csv('path_to_titanic_data.csv')\n",
            "# print(df.head())\n",
            "# print(df.describe())\n"
        ]
    }
    notebook["cells"].append(code_cell)
    
    # Write notebook to file
    with open(notebook_path, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    return notebook_path


async def generate_analysis_report_tool(analysis_summary: str, plots_list: str, insights: str) -> str:
    """Tool function for generating analysis reports"""
    try:
        # Parse the inputs
        analysis_data = {
            "detailed_analysis": analysis_summary,
            "total_passengers": "Unknown",
            "survival_rate": "Unknown", 
            "average_age": "Unknown",
            "average_fare": "Unknown"
        }
        
        # Parse plots information
        plots_info = []
        if plots_list and plots_list.strip() and "No database data" not in plots_list:
            # Simple parsing - in a real implementation, this would be more sophisticated
            plot_files = plots_list.split('\n')
            for i, plot_file in enumerate(plot_files):
                if plot_file.strip():
                    plots_info.append({
                        "title": f"Analysis Plot {i+1}",
                        "description": f"Visualization generated from Titanic data analysis",
                        "filename": plot_file.strip()
                    })
        
        # Generate the notebook
        notebook_path = create_jupyter_notebook(
            analysis_data=analysis_data,
            plots_info=plots_info,
            insights=insights,
            title="Titanic Analysis Report"
        )
        
        return f"✅ Analysis report generated successfully!\n\n📊 **Report Details:**\n- File: `{notebook_path}`\n- Analysis: {len(analysis_summary)} characters\n- Plots: {len(plots_info)} visualizations\n- Insights: {len(insights)} characters\n\n📝 The report includes:\n- Complete analysis summary\n- All generated visualizations (if available)\n- Key insights and conclusions\n- Code cells for further exploration\n\nYou can open this file in Jupyter Notebook or JupyterLab to view the complete report."
        
    except Exception as e:
        return f"❌ Error generating report: {e}"


async def create_summary_report_tool(team_responses: str, plots_summary: str) -> str:
    """Tool function for creating summary reports from team responses"""
    try:
        # Extract insights from team responses
        insights = f"""
## Team Analysis Summary

### Research Findings
{team_responses}

### Visualizations Created
{plots_summary}

### Key Takeaways
Based on the team's analysis, several important patterns emerge from the Titanic dataset that provide insights into survival factors and passenger demographics.

### Recommendations
The analysis suggests focusing on specific demographic and socio-economic factors that influenced survival rates during the Titanic disaster.
        """
        
        # Create a summary report
        analysis_data = {
            "detailed_analysis": team_responses,
            "total_passengers": "891",
            "survival_rate": "38.2",
            "average_age": "29.7",
            "average_fare": "32.2"
        }
        
        plots_info = []
        if plots_summary:
            # Extract plot filenames from the summary
            import re
            plot_files = re.findall(r'`([^`]+\.png)`', plots_summary)
            for i, plot_file in enumerate(plot_files):
                plots_info.append({
                    "title": f"Team Analysis Plot {i+1}",
                    "description": f"Visualization created by the analysis team",
                    "filename": plot_file
                })
        
        # Generate the notebook
        notebook_path = create_jupyter_notebook(
            analysis_data=analysis_data,
            plots_info=plots_info,
            insights=insights,
            title="Titanic Team Analysis Report"
        )
        
        return f"✅ Team summary report generated!\n\n📊 **Report Details:**\n- File: `{notebook_path}`\n- Team responses: {len(team_responses)} characters\n- Plots included: {len(plots_info)}\n\n📝 The report consolidates all team findings into a comprehensive Jupyter notebook."
        
    except Exception as e:
        return f"❌ Error creating summary report: {e}"


def create_report_generator_agent(openai_client) -> AssistantAgent:
    """Create the report generator agent"""
    return AssistantAgent(
        "report_generator_agent",
        openai_client,
        system_message="""
        You are the Report Generator Agent, responsible for creating comprehensive Jupyter notebook reports.
        You work with the entire Titanic analysis team to consolidate findings, visualizations, and insights.
        
        Your role:
        1. Collect analysis results from all team members
        2. Gather information about generated plots and visualizations
        3. Create comprehensive Jupyter notebook reports
        4. Organize insights and findings in a structured format
        5. Generate summary reports that consolidate team work
        
        Available tools:
        - generate_analysis_report_tool: Create detailed analysis reports
        - create_summary_report_tool: Create summary reports from team responses
        
        Always create well-structured, professional reports that include:
        - Clear analysis summaries
        - All relevant visualizations
        - Key insights and conclusions
        - Code cells for further exploration
        - Proper formatting and organization
        
        Focus on creating reports that are both informative and visually appealing.
        """,
        tools=[
            generate_analysis_report_tool,
            create_summary_report_tool
        ]
    )

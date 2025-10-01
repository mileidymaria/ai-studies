#!/usr/bin/env python3
"""
Enhanced Chat Interface with Complete Titanic Analysis Team
Includes: Research Assistant, Enhanced Data Scientist, Wikipedia Agent, and Report Generator
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import tools
from tools import math
from tools.sqlite_tools import (
    query_titanic_data, 
    get_survivors_by_age, 
    get_passenger_demographics,
    get_survival_by_class,
    search_passengers,
    get_database_schema
)

# Import agents
from agents.wikipedia_agent import create_wikipedia_agent, wikipedia_client
from agents.report_generator_agent import create_report_generator_agent
from agents.enhanced_data_scientist_agent import create_enhanced_data_scientist_agent

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


class TitanicAnalysisTeam:
    """Complete Titanic Analysis Team with all agents"""
    
    def __init__(self):
        self.openai_client = OpenAIChatCompletionClient(model="gpt-3.5-turbo")
        self.agents = {}
        self.team_responses = []
        self.plots_created = []
        self.current_session_id = None
        self.session_notebook_path = None
        
    def start_new_session(self):
        """Start a new chat session with a new notebook"""
        from datetime import datetime
        import os
        
        # Generate new session ID
        self.current_session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create reports directory if it doesn't exist
        reports_dir = "reports"
        os.makedirs(reports_dir, exist_ok=True)
        
        # Create new notebook file for this session
        self.session_notebook_path = os.path.join(reports_dir, f"titanic_session_{self.current_session_id}.ipynb")
        
        # Initialize empty notebook
        self._initialize_session_notebook()
        
        print(f"📝 New session started: {self.current_session_id}")
        print(f"📊 Session notebook: {self.session_notebook_path}")
    
    def _initialize_session_notebook(self):
        """Initialize an empty notebook for the session"""
        import json
        from datetime import datetime
        
        notebook = {
            "cells": [
                {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        f"# Titanic Analysis Session - {self.current_session_id}\n",
                        f"\n",
                        f"**Session Started:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
                        f"\n",
                        f"---\n"
                    ]
                }
            ],
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
        
        with open(self.session_notebook_path, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    async def initialize_agents(self):
        """Initialize all team agents"""
        print("🚀 Initializing Titanic Analysis Team...")
        
        # Start new session
        self.start_new_session()
        
        # Initialize Wikipedia MCP client
        await wikipedia_client.start_server()
        
        # Create Research Assistant Agent
        self.agents['research_assistant'] = AssistantAgent(
            "research_assistant", 
            self.openai_client,
            system_message="""
            You are Jarvis, a research assistant specialized in Titanic data analysis.
            You work with Dr. Data who creates visualizations, Wikipedia Agent who provides context,
            and Report Generator who creates comprehensive reports.
            
            Your role:
            1. Analyze data using SQL queries and statistical tools
            2. Provide insights and findings from the data
            3. Suggest visualizations when appropriate
            4. Never show raw database data - always provide insights and analysis
            
            Always be helpful, clear, and suggest visualizations when they would enhance understanding.
            """,
            tools=[
                math.add_operation, 
                math.multiply_operation, 
                math.divide_operation, 
                math.subtract_operation,
                query_titanic_data,
                get_survivors_by_age,
                get_passenger_demographics,
                get_survival_by_class,
                search_passengers,
                get_database_schema
            ]
        )
        
        # Create Enhanced Data Scientist Agent
        self.agents['data_scientist'] = create_enhanced_data_scientist_agent(self.openai_client)
        
        # Create Wikipedia Agent
        self.agents['wikipedia_agent'] = create_wikipedia_agent(self.openai_client)
        
        # Create Report Generator Agent
        self.agents['report_generator'] = create_report_generator_agent(self.openai_client)
        
        print("✅ All agents initialized successfully!")
    
    async def coordinate_team_analysis(self, user_input: str) -> str:
        """Coordinate analysis between all team members"""
        print(f"\n👤 User: {user_input}")
        print("=" * 80)
        
        team_responses = []
        plots_info = []
        
        # Step 1: Research Assistant analyzes the data
        print("🔍 Research Assistant (Jarvis) analyzing...")
        print("-" * 50)
        
        research_response = await self.agents['research_assistant'].on_messages(
            [TextMessage(content=user_input, source="user")],
            cancellation_token=CancellationToken(),
        )
        
        research_content = research_response.chat_message.content
        print(f"📊 Jarvis: {research_content}")
        team_responses.append(f"Research Assistant: {research_content}")
        
        # Step 2: Wikipedia Agent provides context
        print("\n🌐 Wikipedia Agent providing context...")
        print("-" * 50)
        
        # Extract key terms for Wikipedia search
        search_terms = self._extract_search_terms(user_input, research_content)
        if search_terms:
            wiki_response = await self.agents['wikipedia_agent'].on_messages(
                [TextMessage(content=f"Search for information about: {', '.join(search_terms)}", source="user")],
                cancellation_token=CancellationToken(),
            )
            wiki_content = wiki_response.chat_message.content
            print(f"📚 Wikipedia Agent: {wiki_content}")
            team_responses.append(f"Wikipedia Agent: {wiki_content}")
        
        # Step 3: Enhanced Data Scientist creates visualizations
        print("\n📈 Enhanced Data Scientist (Dr. Data) creating visualizations...")
        print("-" * 50)
        
        # Create plots based on research findings
        viz_response = await self.agents['data_scientist'].on_messages(
            [TextMessage(content=f"Create visualizations based on this analysis: {research_content}", source="research_assistant")],
            cancellation_token=CancellationToken(),
        )
        
        viz_content = viz_response.chat_message.content
        print(f"📊 Dr. Data: {viz_content}")
        team_responses.append(f"Data Scientist: {viz_content}")
        
        # Extract plot information
        plots_info = self._extract_plot_info(viz_content)
        self.plots_created.extend(plots_info)
        
        # Step 4: Report Generator creates comprehensive report
        print("\n📝 Report Generator creating comprehensive report...")
        print("-" * 50)
        
        # Combine all team responses
        combined_responses = "\n\n".join(team_responses)
        plots_summary = "\n".join([f"- {plot}" for plot in plots_info])
        
        report_response = await self.agents['report_generator'].on_messages(
            [TextMessage(content=f"Create a comprehensive report with these team responses: {combined_responses}\n\nPlots created: {plots_summary}", source="user")],
            cancellation_token=CancellationToken(),
        )
        
        report_content = report_response.chat_message.content
        print(f"📋 Report Generator: {report_content}")
        
        # Store team responses for potential follow-up
        self.team_responses = team_responses
        
        print("=" * 80)
        return f"Team Analysis Complete!\n\n{combined_responses}\n\n{report_content}"
    
    def _extract_search_terms(self, user_input: str, research_content: str) -> list:
        """Extract key terms for Wikipedia search"""
        terms = []
        
        # Common Titanic-related terms
        titanic_terms = ['Titanic', 'RMS Titanic', 'Titanic disaster', 'Titanic sinking', 'Titanic passengers']
        
        # Extract terms from user input
        if any(term in user_input.lower() for term in ['titanic', 'ship', 'disaster', 'sinking']):
            terms.extend(titanic_terms)
        
        # Extract terms from research content
        if 'class' in research_content.lower():
            terms.append('Titanic passenger classes')
        if 'survival' in research_content.lower():
            terms.append('Titanic survival factors')
        if 'age' in research_content.lower():
            terms.append('Titanic passenger demographics')
        
        return list(set(terms))  # Remove duplicates
    
    def _extract_plot_info(self, viz_content: str) -> list:
        """Extract plot information from visualization response"""
        plots = []
        
        # Look for plot filenames in the response
        import re
        plot_files = re.findall(r'([^/\s]+\.png)', viz_content)
        plots.extend(plot_files)
        
        return plots
    
    def _create_conceptual_plots(self, research_content: str) -> list:
        """Create conceptual visualization suggestions when database is not available"""
        import matplotlib.pyplot as plt
        import numpy as np
        from datetime import datetime
        import os
        
        plots = []
        
        try:
            # Create plots directory if it doesn't exist
            plots_dir = "plots"
            os.makedirs(plots_dir, exist_ok=True)
            
            # Extract data from research content
            if "age" in research_content.lower():
                # Create age distribution conceptual plot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                plot_filename = f"plots/conceptual_age_analysis_{timestamp}.png"
                
                # Create conceptual age distribution
                fig, ax = plt.subplots(figsize=(10, 6))
                
                # Sample age data based on typical Titanic demographics
                ages = np.random.normal(29.7, 14.5, 1000)  # Mean 29.7, std 14.5
                ages = np.clip(ages, 0, 80)  # Clip to realistic range
                
                ax.hist(ages, bins=20, alpha=0.7, color='skyblue', edgecolor='black')
                ax.set_xlabel('Age (years)')
                ax.set_ylabel('Number of Passengers')
                ax.set_title('Conceptual Age Distribution of Titanic Passengers')
                ax.grid(True, alpha=0.3)
                
                plt.tight_layout()
                plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
                plt.close()
                
                plots.append(plot_filename)
                print(f"📊 Created conceptual age distribution plot: {plot_filename}")
            
            if "survival" in research_content.lower() or "class" in research_content.lower():
                # Create survival by class conceptual plot
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                plot_filename = f"plots/conceptual_survival_by_class_{timestamp}.png"
                
                # Create conceptual survival by class
                fig, ax = plt.subplots(figsize=(10, 6))
                
                classes = ['1st Class', '2nd Class', '3rd Class']
                survival_rates = [62.96, 47.28, 24.24]  # Typical Titanic survival rates
                
                bars = ax.bar(classes, survival_rates, color=['gold', 'silver', 'brown'], alpha=0.8)
                ax.set_ylabel('Survival Rate (%)')
                ax.set_title('Conceptual Survival Rate by Passenger Class')
                ax.set_ylim(0, 100)
                
                # Add value labels on bars
                for bar, rate in zip(bars, survival_rates):
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height + 1,
                           f'{rate:.1f}%', ha='center', va='bottom')
                
                plt.tight_layout()
                plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
                plt.close()
                
                plots.append(plot_filename)
                print(f"📊 Created conceptual survival by class plot: {plot_filename}")
            
        except Exception as e:
            print(f"❌ Error creating conceptual plots: {e}")
        
        return plots
    
    async def intelligent_team_analysis(self, user_input: str) -> str:
        """Intelligent team analysis that automatically determines what to do"""
        print(f"\n👤 User: {user_input}")
        print("=" * 80)
        
        # Analyze the input to determine what actions to take
        analysis_type = self._analyze_user_intent(user_input)
        
        team_responses = []
        plots_info = []
        needs_wikipedia = False
        
        # Step 1: Research Assistant analyzes the data (if available)
        print("🔍 Research Assistant (Jarvis) analyzing...")
        print("-" * 50)
        
        research_response = await self.agents['research_assistant'].on_messages(
            [TextMessage(content=user_input, source="user")],
            cancellation_token=CancellationToken(),
        )
        
        research_content = research_response.chat_message.content
        print(f"📊 Jarvis: {research_content}")
        team_responses.append(f"Research Assistant: {research_content}")
        
        # Check if we need Wikipedia based on research response quality
        needs_wikipedia = self._should_use_wikipedia(user_input, research_content)
        
        # If database has no data, always use Wikipedia for comprehensive information
        if "no such table" in research_content.lower() or "database" in research_content.lower():
            needs_wikipedia = True
        
        # Step 2: Wikipedia Agent provides additional context (if needed)
        if needs_wikipedia:
            print("\n🌐 Wikipedia Agent providing additional context...")
            print("-" * 50)
            
            search_terms = self._extract_search_terms(user_input, research_content)
            if search_terms:
                wiki_response = await self.agents['wikipedia_agent'].on_messages(
                    [TextMessage(content=f"Search for additional information about: {', '.join(search_terms)}", source="user")],
                    cancellation_token=CancellationToken(),
                )
                wiki_content = wiki_response.chat_message.content
                print(f"📚 Wikipedia Agent: {wiki_content}")
                team_responses.append(f"Wikipedia Agent: {wiki_content}")
        
        # Step 3: Enhanced Data Scientist creates visualizations (if needed)
        if analysis_type['needs_visualization']:
            print("\n📈 Enhanced Data Scientist (Dr. Data) creating visualizations...")
            print("-" * 50)
            
            # Try to create visualizations with available data
            viz_response = await self.agents['data_scientist'].on_messages(
                [TextMessage(content=f"Create visualizations based on this analysis: {research_content}. If database is not available, create conceptual visualizations or explain what visualizations would be useful.", source="research_assistant")],
                cancellation_token=CancellationToken(),
            )
            
            viz_content = viz_response.chat_message.content
            print(f"📊 Dr. Data: {viz_content}")
            team_responses.append(f"Data Scientist: {viz_content}")
            
            # Try to create actual plots if data is available
            if "error" not in viz_content.lower() and "unable to open" not in viz_content.lower():
                plots_info = self._extract_plot_info(viz_content)
                self.plots_created.extend(plots_info)
            else:
                # Create conceptual visualization suggestions
                plots_info = self._create_conceptual_plots(research_content)
                self.plots_created.extend(plots_info)
        
        # Step 4: Always add content to session notebook
        print("\n📝 Adding analysis to session notebook...")
        print("-" * 50)
        
        # Combine all team responses
        combined_responses = "\n\n".join(team_responses)
        plots_summary = "\n".join([f"- {plot}" for plot in plots_info]) if plots_info else "No visualizations available (no database data)"
        
        # Add content to session notebook
        self._add_to_session_notebook(user_input, combined_responses, plots_info)
        
        # If specifically requested, create a comprehensive report
        if analysis_type['needs_report']:
            print("\n📋 Report Generator creating comprehensive report...")
            print("-" * 50)
            
            report_response = await self.agents['report_generator'].on_messages(
                [TextMessage(content=f"Create a comprehensive report with these team responses: {combined_responses}\n\nPlots created: {plots_summary}", source="user")],
                cancellation_token=CancellationToken(),
            )
            
            report_content = report_response.chat_message.content
            print(f"📋 Report Generator: {report_content}")
            team_responses.append(f"Report Generator: {report_content}")
        
        # Store team responses for potential follow-up
        self.team_responses = team_responses
        
        print("=" * 80)
        
        # Return the most relevant response based on analysis type
        if analysis_type['needs_report']:
            return f"Team Analysis Complete with Report!\n\n{team_responses[-1]}"
        elif analysis_type['needs_visualization']:
            return f"Team Analysis Complete with Visualizations!\n\n{team_responses[-1]}"
        else:
            return f"Team Analysis Complete!\n\n{research_content}"
    
    def _should_use_wikipedia(self, user_input: str, research_content: str) -> bool:
        """Determine if Wikipedia should be used based on research response quality"""
        # Check if research response indicates lack of information
        research_lower = research_content.lower()
        
        # Indicators that we need more information
        needs_more_info = any(phrase in research_lower for phrase in [
            "i don't know", "i'm not sure", "i cannot", "i can't", "no data available",
            "insufficient data", "limited information", "not enough data",
            "unable to find", "cannot determine", "no information",
            "error", "failed", "not found", "unknown", "no such table",
            "database", "sqlite", "connection error"
        ])
        
        # Check if the response is too short or generic
        is_too_short = len(research_content.strip()) < 100
        
        # Check if user is asking for historical context or general information
        user_lower = user_input.lower()
        asks_for_context = any(word in user_lower for word in [
            'titanic', 'disaster', 'sinking', 'historical', 'context', 'background',
            'ship', 'passenger', 'survival', 'class', 'demographic', 'what happened',
            'tell me about', 'explain', 'describe', 'history', 'report', 'analysis',
            'comprehensive', 'overview', 'summary'
        ])
        
        # Check if research response doesn't contain specific data
        has_specific_data = any(phrase in research_lower for phrase in [
            "survival rate", "percentage", "statistics", "data shows", "analysis reveals",
            "passengers", "class", "age", "fare", "demographic", "titanic"
        ])
        
        # Always use Wikipedia for general questions or when database fails
        # Use Wikipedia if:
        # 1. Research indicates lack of information, OR
        # 2. User asks for context and research doesn't have specific data, OR
        # 3. Response is too short and user asks for context, OR
        # 4. User asks for reports/analysis without specific data requirements
        return needs_more_info or (asks_for_context and not has_specific_data) or (is_too_short and asks_for_context) or (asks_for_context and 'report' in user_lower)
    
    def _analyze_user_intent(self, user_input: str) -> dict:
        """Analyze user input to determine what actions to take"""
        user_lower = user_input.lower()
        
        # Determine if visualization is needed
        needs_visualization = any(word in user_lower for word in [
            'chart', 'graph', 'plot', 'visualize', 'show', 'create', 'display',
            'analysis', 'data', 'survival', 'class', 'age', 'fare', 'demographic'
        ])
        
        # Determine if report is needed
        needs_report = any(word in user_lower for word in [
            'report', 'summary', 'document', 'notebook', 'comprehensive', 'complete',
            'generate', 'create report', 'full analysis'
        ])
        
        return {
            'needs_visualization': needs_visualization,
            'needs_report': needs_report
        }
    
    def _add_to_session_notebook(self, user_input: str, team_responses: str, plots_info: list):
        """Add analysis content to the current session notebook"""
        import json
        import base64
        from datetime import datetime
        
        if not self.session_notebook_path:
            return
        
        try:
            # Load existing notebook
            with open(self.session_notebook_path, 'r', encoding='utf-8') as f:
                notebook = json.load(f)
            
            # Add new analysis section
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            # Add user question cell
            question_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"## Question ({timestamp})\n",
                    f"\n",
                    f"**User:** {user_input}\n",
                    f"\n"
                ]
            }
            notebook["cells"].append(question_cell)
            
            # Add team analysis cell
            analysis_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"### Team Analysis\n",
                    f"\n",
                    f"{team_responses}\n",
                    f"\n"
                ]
            }
            notebook["cells"].append(analysis_cell)
            
            # Add plots if available
            if plots_info:
                plots_cell = {
                    "cell_type": "markdown",
                    "metadata": {},
                    "source": [
                        f"### Visualizations\n",
                        f"\n"
                    ]
                }
                notebook["cells"].append(plots_cell)
                
                # Add each plot as an image
                for plot_file in plots_info:
                    if os.path.exists(plot_file):
                        try:
                            with open(plot_file, 'rb') as f:
                                image_data = base64.b64encode(f.read()).decode('utf-8')
                            
                            plot_cell = {
                                "cell_type": "markdown",
                                "metadata": {},
                                "source": [
                                    f"![Plot](data:image/png;base64,{image_data})\n"
                                ]
                            }
                            notebook["cells"].append(plot_cell)
                        except Exception as e:
                            error_cell = {
                                "cell_type": "markdown",
                                "metadata": {},
                                "source": [
                                    f"*Error loading plot {plot_file}: {e}*\n"
                                ]
                            }
                            notebook["cells"].append(error_cell)
            
            # Add separator
            separator_cell = {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"---\n"
                ]
            }
            notebook["cells"].append(separator_cell)
            
            # Save updated notebook
            with open(self.session_notebook_path, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Content added to session notebook: {self.session_notebook_path}")
            
        except Exception as e:
            print(f"❌ Error adding to session notebook: {e}")
    
    async def cleanup(self):
        """Cleanup resources"""
        await wikipedia_client.stop_server()


async def enhanced_chat():
    """Enhanced chat interface with complete team"""
    print("🚢 Enhanced Titanic Analysis Team Chat")
    print("=" * 60)
    print("Team Members:")
    print("🔍 Jarvis - Research Assistant")
    print("📊 Dr. Data - Enhanced Data Scientist") 
    print("🌐 Wikipedia Agent - Knowledge Base Provider")
    print("📝 Report Generator - Documentation Creator")
    print("=" * 60)
    print("Ask me anything about the Titanic!")
    print("All analysis will be saved to a session notebook (.ipynb)")
    print("Type 'quit' to exit")
    print("=" * 60)
    
    # Initialize team
    team = TitanicAnalysisTeam()
    await team.initialize_agents()
    
    try:
        while True:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye', 'q']:
                print("👋 Goodbye!")
                if team.session_notebook_path:
                    print(f"📊 Session notebook saved: {team.session_notebook_path}")
                break
            
            if not user_input:
                continue
            
            print("\n🤖 Team working...")
            
            try:
                # The team automatically determines what to do based on the input
                response = await team.intelligent_team_analysis(user_input)
                print(f"\n🎯 Final Response:\n{response}")
            except Exception as e:
                print(f"❌ Error during team analysis: {e}")
    
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    finally:
        await team.cleanup()


async def test_individual_agents():
    """Test each agent individually"""
    print("🧪 Testing Individual Agents")
    print("=" * 50)
    
    team = TitanicAnalysisTeam()
    await team.initialize_agents()
    
    try:
        # Test Research Assistant
        print("\n🔍 Testing Research Assistant...")
        research_response = await team.agents['research_assistant'].on_messages(
            [TextMessage(content="What is the survival rate by passenger class?", source="user")],
            cancellation_token=CancellationToken(),
        )
        print(f"Jarvis: {research_response.chat_message.content}")
        
        # Test Wikipedia Agent
        print("\n🌐 Testing Wikipedia Agent...")
        wiki_response = await team.agents['wikipedia_agent'].on_messages(
            [TextMessage(content="Search for information about Titanic disaster", source="user")],
            cancellation_token=CancellationToken(),
        )
        print(f"Wikipedia Agent: {wiki_response.chat_message.content}")
        
        # Test Data Scientist
        print("\n📈 Testing Data Scientist...")
        viz_response = await team.agents['data_scientist'].on_messages(
            [TextMessage(content="Create a chart showing survival rates by passenger class", source="user")],
            cancellation_token=CancellationToken(),
        )
        print(f"Dr. Data: {viz_response.chat_message.content}")
        
        # Test Report Generator
        print("\n📝 Testing Report Generator...")
        report_response = await team.agents['report_generator'].on_messages(
            [TextMessage(content="Create a summary report of our analysis", source="user")],
            cancellation_token=CancellationToken(),
        )
        print(f"Report Generator: {report_response.chat_message.content}")
        
    finally:
        await team.cleanup()


if __name__ == "__main__":
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found")
        print("Please set your OpenAI API key in the .env file")
    else:
        import sys
        if len(sys.argv) > 1 and sys.argv[1] == "test":
            asyncio.run(test_individual_agents())
        else:
            asyncio.run(enhanced_chat())

#!/usr/bin/env python3
"""
Enhanced Data Scientist Agent - Can generate plots based on team responses
"""
import os
import re
from typing import Dict, Any, List, Optional
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Import existing visualization tools
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.visualization_tools import (
    create_survival_by_class_chart,
    create_age_distribution_chart,
    create_fare_analysis_chart,
    create_demographics_dashboard,
    create_custom_chart,
    list_available_plots
)


async def analyze_team_response_for_plotting(team_response: str) -> str:
    """
    Analyze team response to determine what plots should be created
    """
    try:
        # Extract key data points from team response
        data_points = []
        
        # Look for survival rates
        survival_match = re.search(r'survival rate[s]?\s*:?\s*([0-9.]+%)', team_response, re.IGNORECASE)
        if survival_match:
            data_points.append(f"Survival rate mentioned: {survival_match.group(1)}")
        
        # Look for class information
        class_match = re.search(r'class\s+([123])\s+.*?([0-9.]+%)', team_response, re.IGNORECASE)
        if class_match:
            data_points.append(f"Class {class_match.group(1)} survival: {class_match.group(2)}")
        
        # Look for age information
        age_match = re.search(r'age[s]?\s*:?\s*([0-9.]+)', team_response, re.IGNORECASE)
        if age_match:
            data_points.append(f"Age mentioned: {age_match.group(1)}")
        
        # Look for fare information
        fare_match = re.search(r'fare[s]?\s*:?\s*\$?([0-9.]+)', team_response, re.IGNORECASE)
        if fare_match:
            data_points.append(f"Fare mentioned: ${fare_match.group(1)}")
        
        # Determine appropriate visualizations
        suggestions = []
        
        if any('survival' in point.lower() and 'class' in point.lower() for point in data_points):
            suggestions.append("create_survival_by_class_chart")
        
        if any('age' in point.lower() for point in data_points):
            suggestions.append("create_age_distribution_chart")
        
        if any('fare' in point.lower() for point in data_points):
            suggestions.append("create_fare_analysis_chart")
        
        if len(data_points) > 2:
            suggestions.append("create_demographics_dashboard")
        
        # Create response
        response = f"Based on the team's analysis, I recommend creating the following visualizations:\n\n"
        response += f"**Data points identified:**\n"
        for point in data_points:
            response += f"- {point}\n"
        
        response += f"\n**Recommended plots:**\n"
        for suggestion in suggestions:
            response += f"- {suggestion}\n"
        
        return response
        
    except Exception as e:
        return f"Error analyzing team response: {e}"


async def create_plots_from_team_analysis(team_response: str, analysis_type: str = "comprehensive") -> str:
    """
    Create plots based on team analysis response
    """
    try:
        plots_created = []
        
        # Determine what plots to create based on team response
        if "survival" in team_response.lower() and "class" in team_response.lower():
            print("Creating survival by class chart...")
            result = await create_survival_by_class_chart()
            plots_created.append("Survival by Class Chart")
        
        if "age" in team_response.lower() or "demographic" in team_response.lower():
            print("Creating age distribution chart...")
            result = await create_age_distribution_chart()
            plots_created.append("Age Distribution Chart")
        
        if "fare" in team_response.lower() or "price" in team_response.lower():
            print("Creating fare analysis chart...")
            result = await create_fare_analysis_chart()
            plots_created.append("Fare Analysis Chart")
        
        if analysis_type == "comprehensive" or len(plots_created) > 1:
            print("Creating demographics dashboard...")
            result = await create_demographics_dashboard()
            plots_created.append("Demographics Dashboard")
        
        # List all available plots
        plots_list = await list_available_plots()
        
        response = f"✅ Successfully created {len(plots_created)} visualizations based on team analysis:\n\n"
        for i, plot in enumerate(plots_created, 1):
            response += f"{i}. {plot}\n"
        
        response += f"\n📊 **All available plots:**\n{plots_list}\n"
        
        return response
        
    except Exception as e:
        return f"❌ Error creating plots from team analysis: {e}"


async def create_custom_plot_from_data(data_description: str, plot_type: str = "bar") -> str:
    """
    Create a custom plot based on data description
    """
    try:
        # Create a custom chart based on the description
        result = await create_custom_chart(
            query=f"SELECT * FROM passengers WHERE {data_description}",
            chart_type=plot_type,
            title=f"Custom Analysis: {data_description}"
        )
        
        return f"✅ Created custom {plot_type} chart based on: {data_description}\n\n{result}"
        
    except Exception as e:
        return f"❌ Error creating custom plot: {e}"


def create_enhanced_data_scientist_agent(openai_client) -> AssistantAgent:
    """Create the enhanced data scientist agent"""
    return AssistantAgent(
        "enhanced_data_scientist_agent",
        openai_client,
        system_message="""
        You are Dr. Data, an enhanced data scientist specialized in creating visualizations and analyzing team responses.
        You work with the entire Titanic analysis team to create meaningful visualizations based on their findings.
        
        Your enhanced capabilities:
        1. Analyze team responses to automatically determine what plots to create
        2. Generate visualizations based on specific data points mentioned by team members
        3. Create custom plots based on data descriptions
        4. Provide comprehensive visual analysis
        5. Always ensure plots enhance understanding of the data
        
        Your role:
        1. Listen to team analysis and automatically suggest appropriate visualizations
        2. Create plots that complement and enhance team findings
        3. Generate custom visualizations when needed
        4. Provide visual insights that support the team's conclusions
        5. Ensure all visualizations are properly saved and documented
        
        Available tools:
        - analyze_team_response_for_plotting: Analyze team responses to suggest plots
        - create_plots_from_team_analysis: Create plots based on team analysis
        - create_custom_plot_from_data: Create custom plots from data descriptions
        - create_survival_by_class_chart: Standard survival analysis
        - create_age_distribution_chart: Age distribution analysis
        - create_fare_analysis_chart: Fare vs survival analysis
        - create_demographics_dashboard: Comprehensive dashboard
        - create_custom_chart: Custom charts from SQL queries
        - list_available_plots: List all created plots
        
        Always create meaningful visualizations that enhance understanding of the data.
        Focus on creating plots that directly support and illustrate the team's findings.
        Never show raw database data - always present insights through visualizations.
        """,
        tools=[
            analyze_team_response_for_plotting,
            create_plots_from_team_analysis,
            create_custom_plot_from_data,
            create_survival_by_class_chart,
            create_age_distribution_chart,
            create_fare_analysis_chart,
            create_demographics_dashboard,
            create_custom_chart,
            list_available_plots
        ]
    )

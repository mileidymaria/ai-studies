"""
Visualization Tools for Data Scientist Agent
"""
import json
import sqlite3
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, Any, List, Optional
import os
from datetime import datetime

# Simple tool decorator for compatibility
def Tool(func):
    """Simple tool decorator for compatibility"""
    func._is_tool = True
    return func

# Database path
DB_PATH = "state_db/titanic.db"

def get_db_connection():
    """Get SQLite database connection"""
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def execute_query(query: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Execute SQL query and return results as list of dictionaries"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        
        # Get column names
        columns = [description[0] for description in cursor.description]
        
        # Fetch all results and convert to list of dictionaries
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        
        return results
    except Exception as e:
        return [{"error": str(e)}]
    finally:
        conn.close()

def save_plot(fig, filename: str, description: str = "") -> str:
    """Save plot and return file path"""
    plots_dir = "plots"
    os.makedirs(plots_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    full_filename = f"{plots_dir}/{filename}_{timestamp}.png"
    
    fig.savefig(full_filename, dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    return f"Plot saved as: {full_filename} - {description}"

@Tool
def create_survival_by_class_chart() -> str:
    """
    Create a bar chart showing survival rates by passenger class.
    
    Returns:
        String with file path and description
    """
    query = """
    SELECT 
        pclass,
        COUNT(*) as total_passengers,
        SUM(survived) as survived_passengers,
        ROUND(SUM(survived) * 100.0 / COUNT(*), 2) as survival_rate
    FROM Observation
    GROUP BY pclass
    ORDER BY pclass
    """
    
    results = execute_query(query)
    if results and "error" in results[0]:
        return f"Error: {results[0]['error']}"
    
    # Convert to DataFrame
    df = pd.DataFrame(results)
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Bar chart for survival rates
    bars = ax1.bar(df['pclass'], df['survival_rate'], color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ax1.set_xlabel('Passenger Class')
    ax1.set_ylabel('Survival Rate (%)')
    ax1.set_title('Survival Rate by Passenger Class')
    ax1.set_ylim(0, 100)
    
    # Add value labels on bars
    for bar, rate in zip(bars, df['survival_rate']):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                f'{rate}%', ha='center', va='bottom')
    
    # Stacked bar chart for counts
    ax2.bar(df['pclass'], df['survived_passengers'], label='Survived', color='#2ca02c')
    ax2.bar(df['pclass'], df['total_passengers'] - df['survived_passengers'], 
            bottom=df['survived_passengers'], label='Did not survive', color='#d62728')
    ax2.set_xlabel('Passenger Class')
    ax2.set_ylabel('Number of Passengers')
    ax2.set_title('Passenger Count by Class and Survival')
    ax2.legend()
    
    plt.tight_layout()
    
    return save_plot(fig, "survival_by_class", "Survival analysis by passenger class")

@Tool
def create_age_distribution_chart() -> str:
    """
    Create histograms showing age distribution for survivors vs non-survivors.
    
    Returns:
        String with file path and description
    """
    query = """
    SELECT age, survived
    FROM Observation
    WHERE age IS NOT NULL
    """
    
    results = execute_query(query)
    if results and "error" in results[0]:
        return f"Error: {results[0]['error']}"
    
    df = pd.DataFrame(results)
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Age distribution for survivors
    survivors_age = df[df['survived'] == 1]['age']
    non_survivors_age = df[df['survived'] == 0]['age']
    
    # Histogram comparison
    ax1.hist([survivors_age, non_survivors_age], bins=20, alpha=0.7, 
             label=['Survived', 'Did not survive'], color=['#2ca02c', '#d62728'])
    ax1.set_xlabel('Age')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Age Distribution: Survivors vs Non-Survivors')
    ax1.legend()
    
    # Box plot
    data_to_plot = [survivors_age, non_survivors_age]
    ax2.boxplot(data_to_plot, labels=['Survived', 'Did not survive'])
    ax2.set_ylabel('Age')
    ax2.set_title('Age Distribution Box Plot')
    
    plt.tight_layout()
    
    return save_plot(fig, "age_distribution", "Age distribution analysis for survivors vs non-survivors")

@Tool
def create_fare_analysis_chart() -> str:
    """
    Create scatter plot and box plot showing fare vs survival.
    
    Returns:
        String with file path and description
    """
    query = """
    SELECT fare, survived, pclass
    FROM Observation
    WHERE fare IS NOT NULL AND fare > 0
    """
    
    results = execute_query(query)
    if results and "error" in results[0]:
        return f"Error: {results[0]['error']}"
    
    df = pd.DataFrame(results)
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Scatter plot: Fare vs Survival
    colors = ['#d62728' if x == 0 else '#2ca02c' for x in df['survived']]
    scatter = ax1.scatter(df['fare'], df['survived'], c=colors, alpha=0.6)
    ax1.set_xlabel('Fare')
    ax1.set_ylabel('Survived (0=No, 1=Yes)')
    ax1.set_title('Fare vs Survival')
    ax1.set_ylim(-0.1, 1.1)
    
    # Box plot: Fare by Class and Survival
    survived_fare = df[df['survived'] == 1]['fare']
    not_survived_fare = df[df['survived'] == 0]['fare']
    
    ax2.boxplot([survived_fare, not_survived_fare], 
                labels=['Survived', 'Did not survive'])
    ax2.set_ylabel('Fare')
    ax2.set_title('Fare Distribution by Survival Status')
    
    plt.tight_layout()
    
    return save_plot(fig, "fare_analysis", "Fare analysis and its relationship to survival")

@Tool
def create_demographics_dashboard() -> str:
    """
    Create a comprehensive dashboard with multiple charts.
    
    Returns:
        String with file path and description
    """
    # Get data for multiple analyses
    survival_query = """
    SELECT 
        pclass,
        SUM(survived) as survived,
        COUNT(*) - SUM(survived) as not_survived
    FROM Observation
    GROUP BY pclass
    ORDER BY pclass
    """
    
    age_query = """
    SELECT 
        CASE 
            WHEN age < 18 THEN 'Child'
            WHEN age BETWEEN 18 AND 60 THEN 'Adult'
            WHEN age > 60 THEN 'Senior'
            ELSE 'Unknown'
        END as age_group,
        SUM(survived) as survived,
        COUNT(*) - SUM(survived) as not_survived
    FROM Observation
    GROUP BY age_group
    """
    
    survival_data = execute_query(survival_query)
    age_data = execute_query(age_query)
    
    if (survival_data and "error" in survival_data[0]) or (age_data and "error" in age_data[0]):
        return "Error retrieving data for dashboard"
    
    # Create the dashboard
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Survival by Class (Pie Chart)
    df_survival = pd.DataFrame(survival_data)
    total_survived = df_survival['survived'].sum()
    total_not_survived = df_survival['not_survived'].sum()
    
    ax1.pie([total_survived, total_not_survived], 
            labels=['Survived', 'Did not survive'],
            autopct='%1.1f%%', colors=['#2ca02c', '#d62728'])
    ax1.set_title('Overall Survival Rate')
    
    # 2. Survival by Class (Stacked Bar)
    x = df_survival['pclass']
    width = 0.35
    ax2.bar(x, df_survival['survived'], width, label='Survived', color='#2ca02c')
    ax2.bar(x, df_survival['not_survived'], width, bottom=df_survival['survived'], 
            label='Did not survive', color='#d62728')
    ax2.set_xlabel('Passenger Class')
    ax2.set_ylabel('Number of Passengers')
    ax2.set_title('Survival by Passenger Class')
    ax2.legend()
    
    # 3. Age Group Analysis
    df_age = pd.DataFrame(age_data)
    ax3.bar(df_age['age_group'], df_age['survived'], color='#2ca02c', alpha=0.7, label='Survived')
    ax3.bar(df_age['age_group'], df_age['not_survived'], bottom=df_age['survived'], 
            color='#d62728', alpha=0.7, label='Did not survive')
    ax3.set_xlabel('Age Group')
    ax3.set_ylabel('Number of Passengers')
    ax3.set_title('Survival by Age Group')
    ax3.legend()
    
    # 4. Statistics Summary
    ax4.axis('off')
    stats_text = f"""
    TITANIC SURVIVAL STATISTICS
    
    Total Passengers: {total_survived + total_not_survived}
    Total Survived: {total_survived}
    Overall Survival Rate: {total_survived/(total_survived + total_not_survived)*100:.1f}%
    
    By Class:
    • 1st Class: {df_survival.iloc[0]['survived']}/{df_survival.iloc[0]['survived'] + df_survival.iloc[0]['not_survived']} ({df_survival.iloc[0]['survived']/(df_survival.iloc[0]['survived'] + df_survival.iloc[0]['not_survived'])*100:.1f}%)
    • 2nd Class: {df_survival.iloc[1]['survived']}/{df_survival.iloc[1]['survived'] + df_survival.iloc[1]['not_survived']} ({df_survival.iloc[1]['survived']/(df_survival.iloc[1]['survived'] + df_survival.iloc[1]['not_survived'])*100:.1f}%)
    • 3rd Class: {df_survival.iloc[2]['survived']}/{df_survival.iloc[2]['survived'] + df_survival.iloc[2]['not_survived']} ({df_survival.iloc[2]['survived']/(df_survival.iloc[2]['survived'] + df_survival.iloc[2]['not_survived'])*100:.1f}%)
    """
    ax4.text(0.1, 0.9, stats_text, transform=ax4.transAxes, fontsize=10,
             verticalalignment='top', fontfamily='monospace',
             bbox=dict(boxstyle="round,pad=0.3", facecolor="lightgray", alpha=0.5))
    
    plt.suptitle('Titanic Survival Analysis Dashboard', fontsize=16, fontweight='bold')
    plt.tight_layout()
    
    return save_plot(fig, "demographics_dashboard", "Comprehensive Titanic survival analysis dashboard")

@Tool
def create_custom_chart(query: str, chart_type: str = "bar", title: str = "Custom Chart") -> str:
    """
    Create a custom chart based on SQL query results.
    
    Args:
        query: SQL query to execute
        chart_type: Type of chart (bar, line, pie, scatter)
        title: Chart title
    
    Returns:
        String with file path and description
    """
    results = execute_query(query)
    if results and "error" in results[0]:
        return f"Error: {results[0]['error']}"
    
    df = pd.DataFrame(results)
    
    if df.empty:
        return "No data returned from query"
    
    # Create the plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    if chart_type == "bar":
        if len(df.columns) >= 2:
            x_col = df.columns[0]
            y_col = df.columns[1]
            ax.bar(df[x_col], df[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
        else:
            ax.bar(range(len(df)), df.iloc[:, 0])
    
    elif chart_type == "line":
        if len(df.columns) >= 2:
            x_col = df.columns[0]
            y_col = df.columns[1]
            ax.plot(df[x_col], df[y_col], marker='o')
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
        else:
            ax.plot(df.iloc[:, 0])
    
    elif chart_type == "pie":
        if len(df.columns) >= 2:
            labels = df.iloc[:, 0]
            sizes = df.iloc[:, 1]
            ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        else:
            ax.pie(df.iloc[:, 0], autopct='%1.1f%%')
    
    elif chart_type == "scatter":
        if len(df.columns) >= 2:
            x_col = df.columns[0]
            y_col = df.columns[1]
            ax.scatter(df[x_col], df[y_col])
            ax.set_xlabel(x_col)
            ax.set_ylabel(y_col)
        else:
            return "Scatter plot requires at least 2 columns"
    
    else:
        return f"Unsupported chart type: {chart_type}"
    
    ax.set_title(title)
    plt.tight_layout()
    
    return save_plot(fig, f"custom_{chart_type}", f"Custom {chart_type} chart: {title}")

@Tool
def list_available_plots() -> str:
    """
    List all available plot files in the plots directory.
    
    Returns:
        String with list of available plots
    """
    plots_dir = "plots"
    if not os.path.exists(plots_dir):
        return "No plots directory found. Create some plots first!"
    
    plot_files = [f for f in os.listdir(plots_dir) if f.endswith('.png')]
    
    if not plot_files:
        return "No plot files found in plots directory."
    
    plot_list = "Available plots:\n"
    for i, plot_file in enumerate(sorted(plot_files), 1):
        plot_list += f"{i}. {plot_file}\n"
    
    return plot_list

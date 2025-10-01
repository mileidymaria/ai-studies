#!/usr/bin/env python3
"""
Example usage of the Titanic Analysis Team
Demonstrates how the team automatically understands what to do
"""
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

async def demonstrate_team_intelligence():
    """Demonstrate how the team automatically understands what to do"""
    print("🚢 Titanic Analysis Team - Intelligence Demonstration")
    print("=" * 70)
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found")
        print("Please set your OpenAI API key in the .env file")
        return
    
    from enhanced_chat import TitanicAnalysisTeam
    
    # Initialize team
    team = TitanicAnalysisTeam()
    await team.initialize_agents()
    
    try:
        # Example queries that demonstrate different capabilities
        example_queries = [
            "What is the survival rate by passenger class?",
            "Show me visualizations of age distribution", 
            "Tell me about the Titanic disaster and analyze passenger data",
            "Create a comprehensive report of survival analysis",
            "Analyze the relationship between fare and survival",
            "What happened to the Titanic?",
            "I don't understand the data, can you explain?",
            "Who were the passengers on the Titanic?"
        ]
        
        print("🤖 The team will automatically determine what to do based on each query:")
        print("=" * 70)
        
        for i, query in enumerate(example_queries, 1):
            print(f"\n📝 Example {i}: '{query}'")
            print("-" * 50)
            
            # Analyze what the team will do
            analysis_type = team._analyze_user_intent(query)
            
            # Simulate research response to test Wikipedia logic
            mock_research_response = "Based on the Titanic dataset analysis, I found that..."
            needs_wikipedia = team._should_use_wikipedia(query, mock_research_response)
            
            print("🧠 Team Analysis:")
            print(f"   - Needs Visualization: {analysis_type['needs_visualization']}")
            print(f"   - Needs Report: {analysis_type['needs_report']}")
            print(f"   - Needs Wikipedia: {needs_wikipedia}")
            
            print("🤖 Team Actions:")
            print("   - Jarvis will always analyze the data first")
            if needs_wikipedia:
                print("   - Wikipedia Agent will provide additional context (fallback)")
            if analysis_type['needs_visualization']:
                print("   - Dr. Data will create visualizations")
            if analysis_type['needs_report']:
                print("   - Report Generator will create comprehensive report")
            
            print()
        
        print("=" * 70)
        print("✅ The team automatically understands what to do!")
        print("No need to choose options - just ask your question!")
        
    finally:
        await team.cleanup()

async def main():
    """Main demonstration function"""
    await demonstrate_team_intelligence()

if __name__ == "__main__":
    asyncio.run(main())

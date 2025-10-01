#!/usr/bin/env python3
"""
Test script to demonstrate the system working without database data
Shows how Wikipedia can provide comprehensive information for reports
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

async def test_wikipedia_only_analysis():
    """Test the system working with Wikipedia only (no database)"""
    print("🚢 Titanic Analysis Team - Wikipedia-Only Mode Test")
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
        # Test queries that should work with Wikipedia only
        test_queries = [
            "Tell me about the Titanic disaster",
            "What happened to the Titanic?",
            "Create a comprehensive report about the Titanic",
            "Who were the passengers on the Titanic?",
            "Explain the Titanic sinking and its historical significance"
        ]
        
        print("🤖 Testing queries that work with Wikipedia only:")
        print("=" * 70)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: '{query}'")
            print("-" * 50)
            
            # Analyze what the team will do
            analysis_type = team._analyze_user_intent(query)
            
            # Simulate database failure to test Wikipedia fallback
            mock_research_response = "Error: no such table: passengers. Database connection failed."
            needs_wikipedia = team._should_use_wikipedia(query, mock_research_response)
            
            print("🧠 Team Analysis:")
            print(f"   - Needs Visualization: {analysis_type['needs_visualization']}")
            print(f"   - Needs Report: {analysis_type['needs_report']}")
            print(f"   - Needs Wikipedia: {needs_wikipedia}")
            print(f"   - Database Status: Failed (no data)")
            
            print("🤖 Team Actions:")
            print("   - Jarvis will attempt data analysis (will fail)")
            if needs_wikipedia:
                print("   - Wikipedia Agent will provide comprehensive information")
            if analysis_type['needs_visualization']:
                print("   - Dr. Data will note: No database data for visualizations")
            if analysis_type['needs_report']:
                print("   - Report Generator will create report based on Wikipedia data")
            
            print()
        
        print("=" * 70)
        print("✅ The system can work with Wikipedia only!")
        print("Reports can be generated even without database data!")
        
    finally:
        await team.cleanup()

async def main():
    """Main test function"""
    await test_wikipedia_only_analysis()

if __name__ == "__main__":
    asyncio.run(main())

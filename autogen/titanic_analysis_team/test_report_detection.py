#!/usr/bin/env python3
"""
Test script to verify report detection and generation
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

async def test_report_detection():
    """Test the report detection logic"""
    print("🧪 Testing Report Detection Logic")
    print("=" * 50)
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found")
        return
    
    try:
        from enhanced_chat import TitanicAnalysisTeam
        from autogen_agentchat.messages import TextMessage
        from autogen_core import CancellationToken
        
        # Initialize team
        team = TitanicAnalysisTeam()
        await team.initialize_agents()
        
        # Test queries that should trigger report generation
        test_queries = [
            "Create a comprehensive report about the Titanic",
            "Generate a report of the analysis",
            "I need a complete report",
            "Create a summary document",
            "Generate a notebook with the analysis"
        ]
        
        print("🤖 Testing queries that should trigger report generation:")
        print("=" * 60)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Test {i}: '{query}'")
            print("-" * 40)
            
            # Test the intent analysis
            analysis_type = team._analyze_user_intent(query)
            
            print(f"🧠 Analysis Results:")
            print(f"   - Needs Visualization: {analysis_type['needs_visualization']}")
            print(f"   - Needs Report: {analysis_type['needs_report']}")
            
            if analysis_type['needs_report']:
                print("✅ Report generation will be triggered")
            else:
                print("❌ Report generation will NOT be triggered")
            
            print()
        
        print("=" * 60)
        print("✅ Report detection testing completed!")
        
        # Test actual report generation
        print("\n🧪 Testing actual report generation...")
        print("-" * 40)
        
        # Simulate a team response that should trigger report generation
        mock_team_responses = [
            "Research Assistant: The Titanic was a British passenger liner that sank in 1912.",
            "Wikipedia Agent: The RMS Titanic was a British passenger liner operated by the White Star Line.",
            "Data Scientist: No database data available for visualizations"
        ]
        
        combined_responses = "\n\n".join(mock_team_responses)
        plots_summary = "No visualizations available (no database data)"
        
        # Test the report generator directly
        report_response = await team.agents['report_generator'].on_messages(
            [TextMessage(content=f"Create a comprehensive report with these team responses: {combined_responses}\n\nPlots created: {plots_summary}", source="user")],
            cancellation_token=CancellationToken(),
        )
        
        print(f"📋 Report Generator Response: {report_response.chat_message.content}")
        
        # Check if a report was actually created
        reports_dir = "reports"
        if os.path.exists(reports_dir):
            files = os.listdir(reports_dir)
            print(f"📁 Files in reports directory: {files}")
            if files:
                print("✅ Report files were created!")
            else:
                print("❌ No report files were created")
        else:
            print("❌ Reports directory does not exist")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await team.cleanup()

async def main():
    """Main test function"""
    await test_report_detection()

if __name__ == "__main__":
    asyncio.run(main())

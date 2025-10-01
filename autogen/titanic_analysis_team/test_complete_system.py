#!/usr/bin/env python3
"""
Complete system demonstration - shows the full workflow
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

async def demo_complete_system():
    """Demonstrate the complete system working"""
    print("🚢 Complete Titanic Analysis Team Demo")
    print("=" * 60)
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found")
        return
    
    try:
        from enhanced_chat import TitanicAnalysisTeam
        
        # Initialize team
        team = TitanicAnalysisTeam()
        await team.initialize_agents()
        
        # Demo queries that should generate reports
        demo_queries = [
            "Create a comprehensive report about the Titanic disaster",
            "Generate a complete analysis report with historical context",
            "Tell me about the Titanic and create a detailed report"
        ]
        
        print("🤖 Demonstrating complete system workflow:")
        print("=" * 60)
        
        for i, query in enumerate(demo_queries, 1):
            print(f"\n🎯 Demo {i}: '{query}'")
            print("=" * 50)
            
            try:
                # Run the complete team analysis
                response = await team.intelligent_team_analysis(query)
                print(f"\n📋 Final Response:\n{response}")
                
                # Check if reports were created
                reports_dir = "reports"
                if os.path.exists(reports_dir):
                    files = os.listdir(reports_dir)
                    print(f"\n📁 Reports created: {len(files)} files")
                    for file in files:
                        if file.endswith('.ipynb'):
                            print(f"   - {file}")
                
            except Exception as e:
                print(f"❌ Error in demo {i}: {e}")
            
            print("\n" + "-" * 50)
        
        print("\n🎉 Complete system demonstration finished!")
        print("✅ Reports are being generated in .ipynb format!")
        
    except Exception as e:
        print(f"❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await team.cleanup()

async def main():
    """Main demo function"""
    await demo_complete_system()

if __name__ == "__main__":
    asyncio.run(main())

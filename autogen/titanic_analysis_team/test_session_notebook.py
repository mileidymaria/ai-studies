#!/usr/bin/env python3
"""
Test script to demonstrate session-based notebook generation
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

async def test_session_notebook():
    """Test the session-based notebook generation"""
    print("🧪 Testing Session-Based Notebook Generation")
    print("=" * 60)
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found")
        return
    
    try:
        from enhanced_chat import TitanicAnalysisTeam
        
        # Initialize team (this will create a new session)
        team = TitanicAnalysisTeam()
        await team.initialize_agents()
        
        print(f"📝 Session ID: {team.current_session_id}")
        print(f"📊 Session notebook: {team.session_notebook_path}")
        
        # Test queries
        test_queries = [
            "Tell me about the Titanic disaster",
            "What was the survival rate by class?",
            "Create a visualization of passenger demographics"
        ]
        
        print("\n🤖 Testing multiple queries in one session:")
        print("=" * 60)
        
        for i, query in enumerate(test_queries, 1):
            print(f"\n📝 Query {i}: '{query}'")
            print("-" * 40)
            
            try:
                # Run analysis
                response = await team.intelligent_team_analysis(query)
                print(f"✅ Analysis completed and added to notebook")
                
            except Exception as e:
                print(f"❌ Error in query {i}: {e}")
        
        # Check the session notebook
        print(f"\n📁 Checking session notebook...")
        if os.path.exists(team.session_notebook_path):
            with open(team.session_notebook_path, 'r') as f:
                content = f.read()
                print(f"✅ Session notebook exists: {team.session_notebook_path}")
                print(f"📊 Notebook size: {len(content)} characters")
                
                # Count cells
                import json
                notebook = json.loads(content)
                cell_count = len(notebook.get('cells', []))
                print(f"📝 Number of cells: {cell_count}")
        else:
            print(f"❌ Session notebook not found: {team.session_notebook_path}")
        
        # Test starting a new session
        print(f"\n🔄 Testing new session...")
        team.start_new_session()
        print(f"📝 New Session ID: {team.current_session_id}")
        print(f"📊 New Session notebook: {team.session_notebook_path}")
        
        print("\n🎉 Session-based notebook testing completed!")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await team.cleanup()

async def main():
    """Main test function"""
    await test_session_notebook()

if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Test script for the Titanic Analysis Team
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

async def test_basic_functionality():
    """Test basic functionality of the team"""
    print("🧪 Testing Titanic Analysis Team Basic Functionality")
    print("=" * 60)
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found")
        print("Please set your OpenAI API key in the .env file")
        return
    
    try:
        # Test imports
        print("📦 Testing imports...")
        from tools import math
        from tools.sqlite_tools import query_titanic_data
        from tools.visualization_tools import list_available_plots
        print("✅ All imports successful")
        
        # Test database connection
        print("\n🗄️ Testing database connection...")
        result = query_titanic_data("SELECT COUNT(*) as total FROM passengers")
        print(f"✅ Database connected. Total passengers: {result}")
        
        # Test math tools
        print("\n🧮 Testing math tools...")
        add_result = math.add_operation(5, 3)
        print(f"✅ Math tools working. 5 + 3 = {add_result}")
        
        # Test visualization tools
        print("\n📊 Testing visualization tools...")
        plots = list_available_plots()
        print(f"✅ Visualization tools working. Available plots: {plots}")
        
        print("\n🎉 All basic tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

async def test_agent_creation():
    """Test agent creation"""
    print("\n🤖 Testing Agent Creation")
    print("=" * 40)
    
    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        from agents.wikipedia_agent import create_wikipedia_agent
        from agents.report_generator_agent import create_report_generator_agent
        from agents.enhanced_data_scientist_agent import create_enhanced_data_scientist_agent
        
        openai_client = OpenAIChatCompletionClient(model="gpt-3.5-turbo")
        
        # Test Wikipedia Agent
        print("🌐 Testing Wikipedia Agent creation...")
        wiki_agent = create_wikipedia_agent(openai_client)
        print("✅ Wikipedia Agent created successfully")
        
        # Test Report Generator Agent
        print("📝 Testing Report Generator Agent creation...")
        report_agent = create_report_generator_agent(openai_client)
        print("✅ Report Generator Agent created successfully")
        
        # Test Enhanced Data Scientist Agent
        print("📊 Testing Enhanced Data Scientist Agent creation...")
        data_agent = create_enhanced_data_scientist_agent(openai_client)
        print("✅ Enhanced Data Scientist Agent created successfully")
        
        print("\n🎉 All agent creation tests passed!")
        
    except Exception as e:
        print(f"❌ Agent creation test failed: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    print("🚢 Titanic Analysis Team - Test Suite")
    print("=" * 60)
    
    await test_basic_functionality()
    await test_agent_creation()
    
    print("\n" + "=" * 60)
    print("✅ Test suite completed!")
    print("You can now run: python enhanced_chat.py")

if __name__ == "__main__":
    asyncio.run(main())

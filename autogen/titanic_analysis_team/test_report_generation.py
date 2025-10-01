#!/usr/bin/env python3
"""
Test script to verify report generation functionality
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

async def test_report_generation():
    """Test the report generation functionality"""
    print("🧪 Testing Report Generation")
    print("=" * 50)
    
    if not OPENAI_API_KEY:
        print("❌ Error: OPENAI_API_KEY not found")
        return
    
    try:
        # Test the report generator directly
        from agents.report_generator_agent import create_jupyter_notebook, generate_analysis_report_tool
        
        # Test 1: Create a simple notebook
        print("📝 Test 1: Creating a simple notebook...")
        
        analysis_data = {
            "detailed_analysis": "This is a test analysis of the Titanic disaster. The ship sank on April 15, 1912, after hitting an iceberg.",
            "total_passengers": "2,224",
            "survival_rate": "31.6%",
            "average_age": "29.7 years",
            "average_fare": "$32.20"
        }
        
        plots_info = []
        
        insights = """
        Key Insights:
        1. The Titanic disaster was one of the deadliest peacetime maritime disasters in history
        2. Only about 31.6% of passengers survived
        3. The ship was considered unsinkable but sank on its maiden voyage
        4. The disaster led to significant changes in maritime safety regulations
        """
        
        notebook_path = create_jupyter_notebook(
            analysis_data=analysis_data,
            plots_info=plots_info,
            insights=insights,
            title="Titanic Disaster Analysis Report"
        )
        
        print(f"✅ Notebook created: {notebook_path}")
        
        # Test 2: Test the report generator tool
        print("\n📝 Test 2: Testing report generator tool...")
        
        result = await generate_analysis_report_tool(
            analysis_summary="The Titanic was a British passenger liner that sank in the North Atlantic Ocean in 1912.",
            plots_list="",
            insights="This was a tragic maritime disaster that changed maritime safety forever."
        )
        
        print(f"✅ Report generator result: {result}")
        
        # Check if files were created
        print("\n📁 Checking created files...")
        if os.path.exists(notebook_path):
            print(f"✅ Notebook file exists: {notebook_path}")
            with open(notebook_path, 'r') as f:
                content = f.read()
                print(f"📊 Notebook size: {len(content)} characters")
        else:
            print(f"❌ Notebook file not found: {notebook_path}")
        
        # List all files in reports directory
        reports_dir = "reports"
        if os.path.exists(reports_dir):
            files = os.listdir(reports_dir)
            print(f"📁 Files in reports directory: {files}")
        else:
            print("❌ Reports directory does not exist")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        traceback.print_exc()

async def main():
    """Main test function"""
    await test_report_generation()

if __name__ == "__main__":
    asyncio.run(main())

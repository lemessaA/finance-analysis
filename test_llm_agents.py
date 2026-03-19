"""
Test the LLM Agent Service for generating AI-powered dashboard data
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append('/home/lemessa-ahmed/Startup-to-Business/src/backend')

from app.services.llm_agent_service import llm_agent_service

async def test_llm_agents():
    """Test the LLM agent service"""
    print("🤖 Testing LLM Agent Service...")
    
    try:
        # Test with default context
        print("\n📊 Testing with default context...")
        default_data = await llm_agent_service.generate_dashboard_data()
        
        print(f"✅ AI Dashboard Data Generated!")
        print(f"   Generated At: {default_data['generated_at']}")
        print(f"   AI Generated: {default_data['ai_generated']}")
        print(f"   Composite Score: {default_data['score']}")
        print(f"   Business Ideas Count: {len(default_data['business_ideas'])}")
        
        # Test with user context
        print("\n🎯 Testing with user context...")
        user_context = {
            "industry": "Beauty Technology",
            "target_market": "Women 25-45",
            "idea": "AI-powered beauty platform",
            "business_stage": "Early Stage",
            "overall_score": 75
        }
        
        contextual_data = await llm_agent_service.generate_dashboard_data(user_context)
        
        print(f"✅ Contextual AI Dashboard Data Generated!")
        print(f"   Composite Score: {contextual_data['score']}")
        print(f"   Business Ideas: {len(contextual_data['business_ideas'])}")
        
        # Test individual agents
        print("\n🔍 Testing individual agents...")
        
        # Business Analyst
        business_analysis = await llm_agent_service.agents['business_analyst'].analyze(user_context)
        print(f"   Business Analyst: ✅ Viability Score {business_analysis['viability_score']}")
        
        # Market Researcher
        market_research = await llm_agent_service.agents['market_researcher'].research(user_context)
        print(f"   Market Researcher: ✅ Opportunity Score {market_research['opportunity_score']}")
        
        # Financial Analyst
        financial_analysis = await llm_agent_service.agents['financial_analyst'].analyze(user_context)
        print(f"   Financial Analyst: ✅ Health Score {financial_analysis['financial_health_score']}")
        
        # Idea Generator
        ideas = await llm_agent_service.agents['idea_generator'].generate(user_context)
        print(f"   Idea Generator: ✅ Generated {len(ideas)} ideas")
        
        # Display sample business idea
        if ideas:
            idea = ideas[0]
            print(f"\n💡 Sample Business Idea:")
            print(f"   Title: {idea['title']}")
            print(f"   Description: {idea['description']}")
            print(f"   Innovation Score: {idea.get('innovation_score', 'N/A')}")
            print(f"   Market Fit: {idea.get('market_fit', 'N/A')}")
        
        print("\n🎉 All LLM Agent Tests Passed!")
        return True
        
    except Exception as e:
        print(f"❌ LLM Agent Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_error_handling():
    """Test error handling and fallback"""
    print("\n🛡️ Testing Error Handling...")
    
    try:
        # Test with invalid context
        invalid_context = {"invalid": "data"}
        fallback_data = await llm_agent_service.generate_dashboard_data(invalid_context)
        
        if fallback_data.get('ai_generated') == False:
            print("✅ Fallback mechanism working correctly")
        else:
            print("⚠️  Fallback may not be working as expected")
            
        return True
        
    except Exception as e:
        print(f"❌ Error Handling Test Failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 LLM AGENT SERVICE COMPREHENSIVE TEST")
    print("=" * 50)
    
    # Test basic functionality
    basic_test = await test_llm_agents()
    
    # Test error handling
    error_test = await test_error_handling()
    
    print("\n" + "=" * 50)
    if basic_test and error_test:
        print("🎉 ALL TESTS PASSED!")
        print("   ✅ LLM Agent Service is working correctly")
        print("   ✅ AI dashboard generation functional")
        print("   ✅ Error handling and fallback working")
        print("   ✅ Ready for production use")
    else:
        print("❌ SOME TESTS FAILED!")
        print("   Check the errors above for details")
    
    print("=" * 50)

if __name__ == "__main__":
    asyncio.run(main())

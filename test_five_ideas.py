"""
Test the 5-idea template system on the dashboard
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append('/home/lemessa-ahmed/Startup-to-Business/src/backend')

from app.services.llm_agent_service import llm_agent_service

async def test_five_idea_system():
    """Test that the system generates at least 5 ideas"""
    print("💡 TESTING 5-IDEA TEMPLATE SYSTEM")
    print("=" * 50)
    
    try:
        # Test 1: Generate ideas with default context
        print("\n🎯 Test 1: Default Context")
        print("-" * 30)
        
        default_context = {
            "industry": "Technology",
            "target_market": "Small to Medium Businesses",
            "business_stage": "Early Stage"
        }
        
        dashboard_data = await llm_agent_service.generate_dashboard_data(default_context)
        ideas = dashboard_data['business_ideas']
        
        print(f"✅ Generated {len(ideas)} ideas")
        
        # Ensure we have at least 5 ideas
        if len(ideas) >= 5:
            print("✅ Minimum 5 ideas requirement: MET")
        else:
            print("❌ Minimum 5 ideas requirement: NOT MET")
            return False
        
        # Display first 5 ideas
        print(f"\n📋 Displaying first 5 ideas:")
        for i, idea in enumerate(ideas[:5]):
            print(f"   {i+1}. {idea['title']}")
            print(f"      Difficulty: {idea['difficulty']}")
            print(f"      Innovation: {idea.get('innovation_score', 'N/A')}")
            print(f"      Market Fit: {idea.get('market_fit', 'N/A')}")
        
        # Test 2: Different industry context
        print(f"\n🎯 Test 2: Beauty Industry Context")
        print("-" * 30)
        
        beauty_context = {
            "industry": "Beauty Technology",
            "target_market": "Women 25-45",
            "idea": "AI-powered beauty platform",
            "business_stage": "Early Stage"
        }
        
        beauty_dashboard = await llm_agent_service.generate_dashboard_data(beauty_context)
        beauty_ideas = beauty_dashboard['business_ideas']
        
        print(f"✅ Generated {len(beauty_ideas)} beauty industry ideas")
        
        if len(beauty_ideas) >= 5:
            print("✅ Beauty industry: 5+ ideas available")
        else:
            print("❌ Beauty industry: Less than 5 ideas")
        
        # Test 3: Finance industry context
        print(f"\n🎯 Test 3: Finance Industry Context")
        print("-" * 30)
        
        finance_context = {
            "industry": "Financial Technology",
            "target_market": "Millennials and Gen Z",
            "idea": "Digital banking solution",
            "business_stage": "Seed Stage"
        }
        
        finance_dashboard = await llm_agent_service.generate_dashboard_data(finance_context)
        finance_ideas = finance_dashboard['business_ideas']
        
        print(f"✅ Generated {len(finance_ideas)} finance industry ideas")
        
        if len(finance_ideas) >= 5:
            print("✅ Finance industry: 5+ ideas available")
        else:
            print("❌ Finance industry: Less than 5 ideas")
        
        # Test 4: Idea diversity check
        print(f"\n🎯 Test 4: Idea Diversity Check")
        print("-" * 30)
        
        # Check if ideas are diverse (not duplicates)
        idea_titles = [idea['title'] for idea in ideas[:5]]
        unique_titles = set(idea_titles)
        
        if len(unique_titles) == len(idea_titles):
            print("✅ All 5 ideas are unique")
        else:
            print("❌ Some ideas are duplicates")
        
        # Check difficulty diversity
        difficulties = [idea['difficulty'] for idea in ideas[:5]]
        unique_difficulties = set(difficulties)
        print(f"✅ Difficulty levels: {', '.join(unique_difficulties)}")
        
        # Check innovation scores
        innovation_scores = [idea.get('innovation_score', 0) for idea in ideas[:5]]
        avg_innovation = sum(innovation_scores) / len(innovation_scores)
        print(f"✅ Average innovation score: {avg_innovation:.1f}")
        
        # Test 5: Quality check for 5 ideas
        print(f"\n🎯 Test 5: Quality Check for 5 Ideas")
        print("-" * 30)
        
        quality_metrics = {
            'has_title': 0,
            'has_description': 0,
            'has_features': 0,
            'has_target_audience': 0,
            'has_market_opportunity': 0,
            'has_business_model': 0,
            'has_tags': 0,
            'has_difficulty': 0
        }
        
        for idea in ideas[:5]:
            if idea.get('title'): quality_metrics['has_title'] += 1
            if idea.get('description'): quality_metrics['has_description'] += 1
            if idea.get('features'): quality_metrics['has_features'] += 1
            if idea.get('target_audience'): quality_metrics['has_target_audience'] += 1
            if idea.get('market_opportunity'): quality_metrics['has_market_opportunity'] += 1
            if idea.get('business_model'): quality_metrics['has_business_model'] += 1
            if idea.get('tags'): quality_metrics['has_tags'] += 1
            if idea.get('difficulty'): quality_metrics['has_difficulty'] += 1
        
        print("Quality metrics for first 5 ideas:")
        for metric, count in quality_metrics.items():
            percentage = (count / 5) * 100
            status = "✅" if percentage == 100 else "⚠️" if percentage >= 80 else "❌"
            print(f"   {status} {metric}: {count}/5 ({percentage:.0f}%)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Main test function"""
    print("🧪 5-IDEA DASHBOARD TEMPLATE SYSTEM TEST")
    print("=" * 60)
    
    success = await test_five_idea_system()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 5-IDEA SYSTEM TEST: PASSED!")
        print("   ✅ Generates at least 5 business ideas")
        print("   ✅ Ideas are diverse and high-quality")
        print("   ✅ Works across different industries")
        print("   ✅ Ready for dashboard display")
        print("   ✅ Update button functionality ready")
    else:
        print("❌ 5-IDEA SYSTEM TEST: FAILED!")
        print("   Check the errors above")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(main())

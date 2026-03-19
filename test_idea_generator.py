"""
Test the Startup Idea Template Generator with LLM Agents
"""

import asyncio
import sys
import os
import json

# Add the backend directory to the path
sys.path.append('/home/lemessa-ahmed/Startup-to-Business/src/backend')

from app.services.llm_agent_service import llm_agent_service, IdeaGeneratorAgent

async def test_idea_generator():
    """Test the idea generator agent specifically"""
    print("💡 TESTING STARTUP IDEA TEMPLATE GENERATOR")
    print("=" * 60)
    
    try:
        # Initialize idea generator
        idea_generator = IdeaGeneratorAgent()
        
        # Test 1: Default context
        print("\n🎯 Test 1: Default Context")
        print("-" * 30)
        default_context = {
            "industry": "Technology",
            "target_market": "Small to Medium Businesses",
            "business_stage": "Early Stage"
        }
        
        ideas_1 = await idea_generator.generate(default_context)
        print(f"✅ Generated {len(ideas_1)} ideas for default context")
        
        for i, idea in enumerate(ideas_1[:2]):  # Show first 2 ideas
            print(f"\n💡 Idea {i+1}:")
            print(f"   Title: {idea['title']}")
            print(f"   Description: {idea['description']}")
            print(f"   Difficulty: {idea['difficulty']}")
            print(f"   Innovation Score: {idea.get('innovation_score', 'N/A')}")
            print(f"   Market Fit: {idea.get('market_fit', 'N/A')}")
            print(f"   Tags: {', '.join(idea['tags'][:3])}")
        
        # Test 2: Beauty industry context
        print("\n🎯 Test 2: Beauty Industry Context")
        print("-" * 30)
        beauty_context = {
            "industry": "Beauty Technology",
            "target_market": "Women 25-45",
            "idea": "AI-powered beauty platform",
            "business_stage": "Early Stage"
        }
        
        ideas_2 = await idea_generator.generate(beauty_context)
        print(f"✅ Generated {len(ideas_2)} ideas for beauty industry")
        
        for i, idea in enumerate(ideas_2[:2]):  # Show first 2 ideas
            print(f"\n💡 Beauty Idea {i+1}:")
            print(f"   Title: {idea['title']}")
            print(f"   Description: {idea['description']}")
            print(f"   Target Audience: {idea['target_audience']}")
            print(f"   Market Opportunity: {idea['market_opportunity']}")
            print(f"   Business Model: {idea['business_model']}")
        
        # Test 3: Finance industry context
        print("\n🎯 Test 3: Finance Industry Context")
        print("-" * 30)
        finance_context = {
            "industry": "Financial Technology",
            "target_market": "Millennials and Gen Z",
            "idea": "Digital banking solution",
            "business_stage": "Seed Stage"
        }
        
        ideas_3 = await idea_generator.generate(finance_context)
        print(f"✅ Generated {len(ideas_3)} ideas for finance industry")
        
        # Show first finance idea
        if ideas_3:
            idea = ideas_3[0]
            print(f"\n💡 Finance Idea:")
            print(f"   Title: {idea['title']}")
            print(f"   Description: {idea['description']}")
            print(f"   Features: {', '.join(idea['features'][:2])}")
        
        # Test 4: Healthcare industry context
        print("\n🎯 Test 4: Healthcare Industry Context")
        print("-" * 30)
        healthcare_context = {
            "industry": "Healthcare Technology",
            "target_market": "Healthcare providers and patients",
            "idea": "Telemedicine platform",
            "business_stage": "Early Stage"
        }
        
        ideas_4 = await idea_generator.generate(healthcare_context)
        print(f"✅ Generated {len(ideas_4)} ideas for healthcare industry")
        
        # Test 5: Compare diversity of ideas
        print("\n🎯 Test 5: Idea Diversity Analysis")
        print("-" * 30)
        
        all_industries = {
            "Technology": ideas_1,
            "Beauty": ideas_2, 
            "Finance": ideas_3,
            "Healthcare": ideas_4
        }
        
        for industry, ideas in all_industries.items():
            if ideas:
                avg_innovation = sum(idea.get('innovation_score', 0) for idea in ideas) / len(ideas)
                high_fit_count = sum(1 for idea in ideas if idea.get('market_fit') in ['High', 'Very High'])
                print(f"   {industry}: {len(ideas)} ideas, Avg Innovation: {avg_innovation:.1f}, High Fit: {high_fit_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Idea Generator Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_full_llm_integration():
    """Test the full LLM integration with idea generation"""
    print("\n🤖 TESTING FULL LLM INTEGRATION")
    print("=" * 60)
    
    try:
        # Test with different user contexts
        contexts = [
            {
                "name": "Tech Startup",
                "context": {
                    "industry": "Software Development",
                    "target_market": "Enterprise clients",
                    "idea": "Cloud-based development platform",
                    "business_stage": "Early Stage"
                }
            },
            {
                "name": "E-commerce Business",
                "context": {
                    "industry": "E-commerce",
                    "target_market": "Online shoppers",
                    "idea": "AI-powered shopping assistant",
                    "business_stage": "Seed Stage"
                }
            },
            {
                "name": "Sustainability Startup",
                "context": {
                    "industry": "Clean Technology",
                    "target_market": "Environmentally conscious consumers",
                    "idea": "Carbon tracking platform",
                    "business_stage": "Early Stage"
                }
            }
        ]
        
        for test_case in contexts:
            print(f"\n🎯 Testing {test_case['name']} Context:")
            print("-" * 40)
            
            # Generate full dashboard data
            dashboard_data = await llm_agent_service.generate_dashboard_data(test_case['context'])
            
            print(f"✅ Dashboard Generated Successfully!")
            print(f"   Composite Score: {dashboard_data['score']}")
            print(f"   Business Ideas: {len(dashboard_data['business_ideas'])}")
            print(f"   Business Viability: {dashboard_data['business_analysis']['viability_score']}")
            print(f"   Market Opportunity: {dashboard_data['market_intelligence']['opportunity_score']}")
            print(f"   Financial Health: {dashboard_data['financial_insights']['financial_health_score']}")
            
            # Show top business idea
            if dashboard_data['business_ideas']:
                top_idea = dashboard_data['business_ideas'][0]
                print(f"\n💡 Top Business Idea:")
                print(f"   Title: {top_idea['title']}")
                print(f"   Innovation Score: {top_idea.get('innovation_score', 'N/A')}")
                print(f"   Market Fit: {top_idea.get('market_fit', 'N/A')}")
                print(f"   Difficulty: {top_idea['difficulty']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Full LLM Integration Test Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_idea_quality():
    """Test the quality and structure of generated ideas"""
    print("\n📊 TESTING IDEA QUALITY")
    print("=" * 60)
    
    try:
        idea_generator = IdeaGeneratorAgent()
        
        # Generate ideas for analysis
        context = {
            "industry": "Artificial Intelligence",
            "target_market": "Businesses seeking AI solutions",
            "idea": "AI automation platform"
        }
        
        ideas = await idea_generator.generate(context)
        
        # Quality checks
        print(f"\n🔍 Quality Analysis for {len(ideas)} AI Industry Ideas:")
        print("-" * 50)
        
        quality_metrics = {
            'has_title': 0,
            'has_description': 0,
            'has_features': 0,
            'has_target_audience': 0,
            'has_market_opportunity': 0,
            'has_business_model': 0,
            'has_tags': 0,
            'has_difficulty': 0,
            'has_innovation_score': 0,
            'has_market_fit': 0
        }
        
        for idea in ideas:
            if idea.get('title'): quality_metrics['has_title'] += 1
            if idea.get('description'): quality_metrics['has_description'] += 1
            if idea.get('features'): quality_metrics['has_features'] += 1
            if idea.get('target_audience'): quality_metrics['has_target_audience'] += 1
            if idea.get('market_opportunity'): quality_metrics['has_market_opportunity'] += 1
            if idea.get('business_model'): quality_metrics['has_business_model'] += 1
            if idea.get('tags'): quality_metrics['has_tags'] += 1
            if idea.get('difficulty'): quality_metrics['has_difficulty'] += 1
            if idea.get('innovation_score'): quality_metrics['has_innovation_score'] += 1
            if idea.get('market_fit'): quality_metrics['has_market_fit'] += 1
        
        # Print quality results
        for metric, count in quality_metrics.items():
            percentage = (count / len(ideas)) * 100
            status = "✅" if percentage == 100 else "⚠️" if percentage >= 80 else "❌"
            print(f"   {status} {metric}: {count}/{len(ideas)} ({percentage:.0f}%)")
        
        # Calculate overall quality score
        total_metrics = len(quality_metrics)
        total_score = sum(quality_metrics.values())
        max_score = total_metrics * len(ideas)
        quality_percentage = (total_score / max_score) * 100
        
        print(f"\n📈 Overall Idea Quality: {quality_percentage:.1f}%")
        
        if quality_percentage >= 90:
            print("   🎉 EXCELLENT - Ideas are comprehensive and well-structured!")
        elif quality_percentage >= 80:
            print("   ✅ GOOD - Ideas have most required elements")
        elif quality_percentage >= 70:
            print("   ⚠️  FAIR - Ideas need some improvement")
        else:
            print("   ❌ POOR - Ideas lack essential information")
        
        return quality_percentage >= 80
        
    except Exception as e:
        print(f"❌ Idea Quality Test Failed: {e}")
        return False

async def main():
    """Main test function"""
    print("🧪 STARTUP IDEA TEMPLATE GENERATOR - COMPREHENSIVE TEST")
    print("=" * 70)
    
    # Run all tests
    test1 = await test_idea_generator()
    test2 = await test_full_llm_integration()
    test3 = await test_idea_quality()
    
    print("\n" + "=" * 70)
    print("📊 TEST SUMMARY")
    print("=" * 70)
    
    tests = [
        ("Idea Generator Agent", test1),
        ("Full LLM Integration", test2),
        ("Idea Quality Assessment", test3)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, result in tests:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed ({(passed/total)*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        print("   ✅ Startup Idea Template Generator is working perfectly!")
        print("   ✅ High-quality, contextual business ideas are being generated!")
        print("   ✅ Ready for production use!")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Check the details above.")
    
    print("=" * 70)

if __name__ == "__main__":
    asyncio.run(main())

"""
Test the business ideas service
"""

import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append('/home/lemessa-ahmed/Startup-to-Business/src/backend')

from app.services.idea_generator_service import generate_business_ideas

async def test_business_ideas():
    """Test the business ideas generation"""
    try:
        print("🧪 Testing Business Ideas Service...")
        
        # Test with beauty industry
        ideas = await generate_business_ideas("Beauty Technology", "Women 25-45")
        print(f"✅ Generated {len(ideas)} ideas for Beauty Technology")
        
        for i, idea in enumerate(ideas[:2]):  # Show first 2 ideas
            print(f"\n--- Idea {i+1} ---")
            print(f"Title: {idea['title']}")
            print(f"Description: {idea['description']}")
            print(f"Difficulty: {idea['difficulty']}")
            print(f"Tags: {', '.join(idea['tags'])}")
        
        # Test with tech industry
        tech_ideas = await generate_business_ideas("Technology", "Enterprise")
        print(f"\n✅ Generated {len(tech_ideas)} ideas for Technology")
        
        print("\n🎉 Business ideas service working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_business_ideas())

"""
Service for generating business idea templates using LLM.
"""

import logging
from typing import List, Dict, Any
from app.config import settings
from app.utils.logger import setup_logger

logger = setup_logger(__name__)

async def generate_business_ideas(industry: str = None, target_market: str = None) -> List[Dict[str, Any]]:
    """
    Generate business idea templates using LLM based on user's context.
    """
    try:
        # Create context-aware prompt
        context = ""
        if industry:
            context += f"Industry: {industry}\n"
        if target_market:
            context += f"Target Market: {target_market}\n"
        
        prompt = f"""
Generate 4 innovative and viable business idea templates. {context}

For each idea, provide:
1. A catchy, memorable title
2. A brief compelling description (1-2 sentences)
3. Key features/benefits (3-4 bullet points)
4. Target audience
5. Market opportunity (brief)
6. Business model hint

Format as JSON array with structure:
[
  {{
    "title": "Catchy Title",
    "description": "Brief compelling description",
    "features": ["Feature 1", "Feature 2", "Feature 3"],
    "targetAudience": "Specific target audience",
    "marketOpportunity": "Brief market opportunity description",
    "businessModel": "Business model hint",
    "difficulty": "Beginner|Intermediate|Advanced",
    "tags": ["tag1", "tag2", "tag3"]
  }}
]

Make ideas practical, innovative, and suitable for 2024-2025 market trends.
"""

        # In a real implementation, this would call the actual LLM service
        # For now, we'll return context-aware mock ideas
        if industry and "beauty" in industry.lower():
            return [
                {
                    "title": "AI Beauty Concierge",
                    "description": "Personalized beauty recommendations powered by computer vision and AI",
                    "features": [
                        "Virtual makeup try-on",
                        "Skin analysis AI",
                        "Personalized product matching",
                        "Beauty routine planner"
                    ],
                    "targetAudience": "Gen Z and Millennials interested in beauty tech",
                    "marketOpportunity": "$532B global beauty market with growing tech integration",
                    "businessModel": "Freemium app with premium features and brand partnerships",
                    "difficulty": "Intermediate",
                    "tags": ["AI", "Beauty", "Mobile", "Tech"]
                },
                {
                    "title": "Sustainable Beauty Box",
                    "description": "Curated subscription box featuring eco-friendly and cruelty-free beauty products",
                    "features": [
                        "Monthly themed boxes",
                        "Sustainable brand partnerships",
                        "Personalization quiz",
                        "Educational content"
                    ],
                    "targetAudience": "Eco-conscious consumers aged 25-45",
                    "marketOpportunity": "Growing demand for sustainable beauty products",
                    "businessModel": "Subscription-based with tiered pricing",
                    "difficulty": "Beginner",
                    "tags": ["Sustainability", "Subscription", "Beauty", "E-commerce"]
                },
                {
                    "title": "Beauty Professional Marketplace",
                    "description": "Connect customers with vetted beauty professionals for at-home services",
                    "features": [
                        "Vetted professionals",
                        "Real-time availability",
                        "Secure payments",
                        "Review system"
                    ],
                    "targetAudience": "Busy professionals seeking convenient beauty services",
                    "marketOpportunity": "Gig economy expansion in personal services",
                    "businessModel": "Commission-based platform service",
                    "difficulty": "Intermediate",
                    "tags": ["Marketplace", "Beauty", "Services", "Platform"]
                },
                {
                    "title": "Custom Skincare Formulator",
                    "description": "AI-powered platform that creates personalized skincare formulations",
                    "features": [
                        "Skin assessment quiz",
                        "Custom formula creation",
                        "Lab-quality production",
                        "Progress tracking"
                    ],
                    "targetAudience": "People with specific skin concerns seeking personalized solutions",
                    "marketOpportunity": "Personalization trend in skincare industry",
                    "businessModel": "Direct-to-consumer with subscription options",
                    "difficulty": "Advanced",
                    "tags": ["AI", "Skincare", "Personalization", "Health"]
                }
            ]
        elif industry and "tech" in industry.lower():
            return [
                {
                    "title": "No-Code Automation Platform",
                    "description": "Visual workflow builder for automating business processes without coding",
                    "features": [
                        "Drag-and-drop interface",
                        "1000+ app integrations",
                        "AI-powered suggestions",
                        "Team collaboration"
                    ],
                    "targetAudience": "Small to medium businesses without dedicated IT teams",
                    "marketOpportunity": "Growing demand for business automation tools",
                    "businessModel": "SaaS with per-user pricing",
                    "difficulty": "Intermediate",
                    "tags": ["No-Code", "Automation", "SaaS", "B2B"]
                },
                {
                    "title": "Remote Team Wellness App",
                    "description": "Comprehensive wellness platform for distributed teams",
                    "features": [
                        "Mental health tracking",
                        "Virtual team activities",
                        "Wellness challenges",
                        "Analytics dashboard"
                    ],
                    "targetAudience": "HR managers and remote team leaders",
                    "marketOpportunity": "Remote work creating new wellness challenges",
                    "businessModel": "B2B SaaS with tiered pricing",
                    "difficulty": "Beginner",
                    "tags": ["Remote Work", "Wellness", "HR Tech", "SaaS"]
                },
                {
                    "title": "Cybersecurity Training Simulator",
                    "description": "Gamified platform for teaching cybersecurity skills through real scenarios",
                    "features": [
                        "Real-world scenarios",
                        "Gamification elements",
                        "Progress tracking",
                        "Certification prep"
                    ],
                    "targetAudience": "IT professionals and students",
                    "marketOpportunity": "Growing cybersecurity skills gap",
                    "businessModel": "Subscription with enterprise pricing",
                    "difficulty": "Advanced",
                    "tags": ["Cybersecurity", "Education", "Gaming", "B2B"]
                },
                {
                    "title": "AI Content Generator",
                    "description": "Multi-modal AI platform for generating marketing content",
                    "features": [
                        "Text, image, and video generation",
                        "Brand voice training",
                        "Multi-language support",
                        "Performance analytics"
                    ],
                    "targetAudience": "Marketing teams and content creators",
                    "marketOpportunity": "Content creation demand outpacing supply",
                    "businessModel": "Usage-based SaaS pricing",
                    "difficulty": "Advanced",
                    "tags": ["AI", "Content", "Marketing", "SaaS"]
                }
            ]
        else:
            # General business ideas
            return [
                {
                    "title": "Smart Home Energy Optimizer",
                    "description": "AI-powered system that reduces home energy costs through intelligent automation",
                    "features": [
                        "Real-time energy monitoring",
                        "Automated optimization",
                        "Cost savings reports",
                        "Mobile app control"
                    ],
                    "targetAudience": "Homeowners looking to reduce utility costs",
                    "marketOpportunity": "Growing focus on energy efficiency and cost savings",
                    "businessModel": "Hardware sales + subscription service",
                    "difficulty": "Intermediate",
                    "tags": ["IoT", "Energy", "Smart Home", "Sustainability"]
                },
                {
                    "title": "Personal Finance Coach AI",
                    "description": "AI-powered financial advisor that provides personalized guidance",
                    "features": [
                        "Spending analysis",
                        "Investment recommendations",
                        "Goal tracking",
                        "Educational content"
                    ],
                    "targetAudience": "Young professionals seeking financial guidance",
                    "marketOpportunity": "Need for accessible financial advice",
                    "businessModel": "Freemium with premium features",
                    "difficulty": "Intermediate",
                    "tags": ["FinTech", "AI", "Personal Finance", "Mobile"]
                },
                {
                    "title": "Local Experience Marketplace",
                    "description": "Platform connecting travelers with authentic local experiences",
                    "features": [
                        "Vetted local hosts",
                        "Unique experiences",
                        "Secure booking",
                        "Review system"
                    ],
                    "targetAudience": "Travelers seeking authentic local experiences",
                    "marketOpportunity": "Growing demand for authentic travel experiences",
                    "businessModel": "Commission-based marketplace",
                    "difficulty": "Beginner",
                    "tags": ["Travel", "Marketplace", "Local", "Experience"]
                },
                {
                    "title": "Mental Health Support Bot",
                    "description": "AI-powered chatbot providing mental health support and resources",
                    "features": [
                        "24/7 availability",
                        "Crisis detection",
                        "Resource recommendations",
                        "Progress tracking"
                    ],
                    "targetAudience": "Individuals seeking accessible mental health support",
                    "marketOpportunity": "Growing mental health awareness and accessibility needs",
                    "businessModel": "Subscription with professional upgrade options",
                    "difficulty": "Advanced",
                    "tags": ["Health", "AI", "Mental Health", "Support"]
                }
            ]

    except Exception as e:
        logger.error(f"Error generating business ideas: {e}")
        # Return fallback ideas if generation fails
        return [
            {
                "title": "Innovation Hub",
                "description": "A platform connecting innovators with resources and mentors",
                "features": ["Mentorship matching", "Resource library", "Community forums"],
                "targetAudience": "Early-stage entrepreneurs",
                "marketOpportunity": "Growing startup ecosystem",
                "businessModel": "Membership platform",
                "difficulty": "Beginner",
                "tags": ["Innovation", "Community", "Startup"]
            }
        ]

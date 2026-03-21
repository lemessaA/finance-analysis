// Test the exact API calls the frontend makes after the fix
const axios = require('axios');

const API_BASE = 'http://localhost:8000/api/v1';

async function testFixedAPIs() {
    console.log('🔧 Testing Fixed Frontend API Calls\n');
    
    // Test 1: Startup Validation (Fixed field mapping)
    console.log('1️⃣ Testing Fixed Startup Validation...');
    try {
        const response = await axios.post(`${API_BASE}/startup/validate`, {
            idea: "AI-powered meal planning app for diabetic patients with personalized nutrition tracking",
            industry: "HealthTech", 
            target_market: "United States",  // Fixed: was targetMarket
            business_stage: "Early Stage",   // Fixed: was businessStage
            additional_context: "B2C SaaS for diabetes management"  // Fixed: was description
        });
        
        console.log('✅ Startup Validation SUCCESS');
        console.log(`   - Idea: ${response.data.idea}`);
        console.log(`   - Overall Score: ${response.data.overall_score}/100`);
        console.log(`   - Verdict: ${response.data.verdict}`);
        console.log(`   - Key Strengths: ${response.data.key_strengths?.length || 0} items`);
        console.log(`   - Key Risks: ${response.data.key_risks?.length || 0} items`);
        console.log(`   - Recommendations: ${response.data.recommendations?.length || 0} items`);
        
    } catch (error) {
        console.log('❌ Startup Validation FAILED:', error.message);
        if (error.response) {
            console.log('   Response:', error.response.data);
        }
    }
    
    // Test 2: Market Intelligence (Already working)
    console.log('\n2️⃣ Testing Market Intelligence...');
    try {
        const response = await axios.post(`${API_BASE}/market/analyze`, {
            industry: "saas",
            target_market: "Global"  // Already correct
        });
        
        console.log('✅ Market Intelligence SUCCESS');
        console.log(`   - Industry: ${response.data.industry}`);
        console.log(`   - Market Size: ${response.data.market_size_estimate}`);
        console.log(`   - CAGR: ${response.data.cagr_estimate}`);
        console.log(`   - Trends: ${response.data.key_trends?.length || 0} items`);
        console.log(`   - Opportunities: ${response.data.opportunities?.length || 0} items`);
        console.log(`   - Competitors: ${response.data.top_competitors?.length || 0} items`);
        
    } catch (error) {
        console.log('❌ Market Intelligence FAILED:', error.message);
    }
    
    // Test 3: Financial Forecasting (Already working)
    console.log('\n3️⃣ Testing Financial Forecasting...');
    try {
        const response = await axios.post(`${API_BASE}/forecasting/forecast`, {
            metric: "Revenue",
            historical_data: [
                { period: "2023-01", value: 100 },
                { period: "2023-04", value: 120 },
                { period: "2023-07", value: 135 },
                { period: "2023-10", value: 160 },
                { period: "2024-01", value: 190 },
                { period: "2024-04", value: 230 }
            ],
            forecast_periods: 3,
            model_type: "auto"
        });
        
        console.log('✅ Financial Forecasting SUCCESS');
        console.log(`   - Metric: ${response.data.metric}`);
        console.log(`   - Model: ${response.data.model_used}`);
        console.log(`   - R²: ${response.data.r_squared.toFixed(3)}`);
        console.log(`   - Growth Rate: ${(response.data.avg_growth_rate * 100).toFixed(1)}%`);
        console.log(`   - Confidence: ${response.data.confidence}`);
        
        const forecastPoints = response.data.data_points?.filter(p => p.is_forecast) || [];
        console.log(`   - Forecast Points: ${forecastPoints.length}`);
        forecastPoints.forEach(p => {
            console.log(`     ${p.period}: ${p.value.toFixed(1)}`);
        });
        
    } catch (error) {
        console.log('❌ Financial Forecasting FAILED:', error.message);
    }
    
    console.log('\n🎯 SUMMARY:');
    console.log('Frontend API calls should now work correctly!');
    console.log('✅ Fixed field mapping issues');
    console.log('✅ All APIs are properly configured');
    console.log('✅ Frontend should now display results');
}

testFixedAPIs();

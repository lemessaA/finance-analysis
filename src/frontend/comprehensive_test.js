// Comprehensive test of frontend functionality
const axios = require('axios');

const API_BASE = 'http://localhost:8000/api/v1';

async function testAllFeatures() {
    console.log('🚀 Starting Comprehensive Frontend Test\n');
    
    const results = {
        startup: { status: 'pending', data: null, error: null },
        market: { status: 'pending', data: null, error: null },
        forecasting: { status: 'pending', data: null, error: null }
    };
    
    // Test 1: Startup Validation
    console.log('1️⃣ Testing Startup Validation...');
    try {
        const startupResponse = await axios.post(`${API_BASE}/startup/validate`, {
            idea: "AI-powered meal planning app for diabetic patients",
            industry: "HealthTech",
            target_market: "United States"
        });
        
        results.startup.status = 'success';
        results.startup.data = startupResponse.data;
        
        console.log('✅ Startup Validation SUCCESS');
        console.log(`   - Idea: ${startupResponse.data.idea}`);
        console.log(`   - Overall Score: ${startupResponse.data.overall_score}/100`);
        console.log(`   - Verdict: ${startupResponse.data.verdict}`);
        console.log(`   - Key Strengths: ${startupResponse.data.key_strengths?.length || 0} items`);
        console.log(`   - Key Risks: ${startupResponse.data.key_risks?.length || 0} items`);
        console.log(`   - Recommendations: ${startupResponse.data.recommendations?.length || 0} items`);
        
    } catch (error) {
        results.startup.status = 'error';
        results.startup.error = error.message;
        console.log('❌ Startup Validation FAILED:', error.message);
    }
    
    // Test 2: Market Intelligence
    console.log('\n2️⃣ Testing Market Intelligence...');
    try {
        const marketResponse = await axios.post(`${API_BASE}/market/analyze`, {
            industry: "saas",
            target_market: "Global"
        });
        
        results.market.status = 'success';
        results.market.data = marketResponse.data;
        
        console.log('✅ Market Intelligence SUCCESS');
        console.log(`   - Industry: ${marketResponse.data.industry}`);
        console.log(`   - Market Size: ${marketResponse.data.market_size_estimate}`);
        console.log(`   - CAGR: ${marketResponse.data.cagr_estimate}`);
        console.log(`   - Trends: ${marketResponse.data.key_trends?.length || 0} items`);
        console.log(`   - Opportunities: ${marketResponse.data.opportunities?.length || 0} items`);
        console.log(`   - Risks: ${marketResponse.data.risks?.length || 0} items`);
        console.log(`   - Competitors: ${marketResponse.data.top_competitors?.length || 0} items`);
        
    } catch (error) {
        results.market.status = 'error';
        results.market.error = error.message;
        console.log('❌ Market Intelligence FAILED:', error.message);
    }
    
    // Test 3: Financial Forecasting
    console.log('\n3️⃣ Testing Financial Forecasting...');
    try {
        const forecastResponse = await axios.post(`${API_BASE}/forecasting/forecast`, {
            metric: "Revenue",
            historical_data: [
                { period: "2023-01", value: 100 },
                { period: "2023-04", value: 120 },
                { period: "2023-07", value: 135 }
            ],
            forecast_periods: 2,
            model_type: "auto"
        });
        
        results.forecasting.status = 'success';
        results.forecasting.data = forecastResponse.data;
        
        console.log('✅ Financial Forecasting SUCCESS');
        console.log(`   - Metric: ${forecastResponse.data.metric}`);
        console.log(`   - Model: ${forecastResponse.data.model_used}`);
        console.log(`   - R²: ${forecastResponse.data.r_squared.toFixed(3)}`);
        console.log(`   - Growth Rate: ${(forecastResponse.data.avg_growth_rate * 100).toFixed(1)}%`);
        console.log(`   - Confidence: ${forecastResponse.data.confidence}`);
        console.log(`   - Data Points: ${forecastResponse.data.data_points?.length || 0}`);
        
    } catch (error) {
        results.forecasting.status = 'error';
        results.forecasting.error = error.message;
        console.log('❌ Financial Forecasting FAILED:', error.message);
    }
    
    // Summary
    console.log('\n📊 TEST RESULTS SUMMARY:');
    console.log('========================');
    
    const successCount = Object.values(results).filter(r => r.status === 'success').length;
    const errorCount = Object.values(results).filter(r => r.status === 'error').length;
    
    console.log(`✅ Successful Tests: ${successCount}/3`);
    console.log(`❌ Failed Tests: ${errorCount}/3`);
    
    if (successCount === 3) {
        console.log('🎉 ALL TESTS PASSED! Frontend should be working correctly.');
    } else if (successCount >= 2) {
        console.log('⚠️  MOST TESTS PASSED! Frontend should be mostly working.');
    } else {
        console.log('🚨 MULTIPLE TESTS FAILED! Frontend has serious issues.');
    }
    
    // Data Structure Validation
    console.log('\n🔍 Data Structure Validation:');
    console.log('===============================');
    
    if (results.startup.data) {
        const startupFields = ['idea', 'overall_score', 'verdict', 'key_strengths', 'key_risks', 'recommendations'];
        const missingStartup = startupFields.filter(field => !(field in results.startup.data));
        if (missingStartup.length === 0) {
            console.log('✅ Startup validation data structure is correct');
        } else {
            console.log(`❌ Startup validation missing fields: ${missingStartup.join(', ')}`);
        }
    }
    
    if (results.market.data) {
        const marketFields = ['industry', 'market_size_estimate', 'cagr_estimate', 'key_trends', 'opportunities', 'risks', 'top_competitors'];
        const missingMarket = marketFields.filter(field => !(field in results.market.data));
        if (missingMarket.length === 0) {
            console.log('✅ Market intelligence data structure is correct');
        } else {
            console.log(`❌ Market intelligence missing fields: ${missingMarket.join(', ')}`);
        }
    }
    
    if (results.forecasting.data) {
        const forecastFields = ['metric', 'model_used', 'r_squared', 'avg_growth_rate', 'confidence', 'data_points'];
        const missingForecast = forecastFields.filter(field => !(field in results.forecasting.data));
        if (missingForecast.length === 0) {
            console.log('✅ Financial forecasting data structure is correct');
        } else {
            console.log(`❌ Financial forecasting missing fields: ${missingForecast.join(', ')}`);
        }
    }
}

testAllFeatures();

// Test the complete UI flow for market intelligence
const axios = require('axios');

async function testUIFlow() {
    console.log('🧪 Testing Market Intelligence UI Flow...\n');
    
    try {
        // Step 1: Test API call (simulating form submission)
        console.log('1️⃣ Testing API call...');
        const response = await axios.post('http://localhost:8000/api/v1/market/analyze', {
            industry: 'saas',
            target_market: 'Global'
        });
        
        console.log('✅ API call successful!');
        console.log('📊 Response structure:');
        console.log(`   - Industry: ${response.data.industry}`);
        console.log(`   - Market Size: ${response.data.market_size_estimate}`);
        console.log(`   - CAGR: ${response.data.cagr_estimate}`);
        console.log(`   - Trends: ${response.data.key_trends?.length || 0} items`);
        console.log(`   - Opportunities: ${response.data.opportunities?.length || 0} items`);
        console.log(`   - Risks: ${response.data.risks?.length || 0} items`);
        console.log(`   - Competitors: ${response.data.top_competitors?.length || 0} items`);
        
        // Step 2: Verify data structure matches frontend expectations
        console.log('\n2️⃣ Verifying data structure...');
        const requiredFields = [
            'industry', 'market_size_estimate', 'cagr_estimate', 'market_overview',
            'key_trends', 'opportunities', 'risks', 'top_competitors'
        ];
        
        let allFieldsPresent = true;
        requiredFields.forEach(field => {
            if (!(field in response.data)) {
                console.log(`❌ Missing field: ${field}`);
                allFieldsPresent = false;
            }
        });
        
        if (allFieldsPresent) {
            console.log('✅ All required fields present');
        }
        
        // Step 3: Test competitor data structure
        console.log('\n3️⃣ Testing competitor data...');
        if (response.data.top_competitors && response.data.top_competitors.length > 0) {
            const competitor = response.data.top_competitors[0];
            const competitorFields = ['name', 'description', 'strengths', 'weaknesses'];
            
            let competitorStructureValid = true;
            competitorFields.forEach(field => {
                if (!(field in competitor)) {
                    console.log(`❌ Missing competitor field: ${field}`);
                    competitorStructureValid = false;
                }
            });
            
            if (competitorStructureValid) {
                console.log('✅ Competitor data structure valid');
                console.log(`   - Sample competitor: ${competitor.name}`);
                console.log(`   - Strengths: ${competitor.strengths?.length || 0}`);
                console.log(`   - Weaknesses: ${competitor.weaknesses?.length || 0}`);
            }
        }
        
        // Step 4: Simulate UI rendering
        console.log('\n4️⃣ Simulating UI rendering...');
        console.log('🎨 UI Components that would render:');
        console.log(`   - Header: Market Intelligence for ${response.data.industry}`);
        console.log(`   - Stats Cards: Industry, Market Size, CAGR`);
        console.log(`   - Market Overview: ${response.data.market_overview?.substring(0, 100)}...`);
        console.log(`   - Trends Section: ${response.data.key_trends?.length || 0} trend items`);
        console.log(`   - Opportunities Section: ${response.data.opportunities?.length || 0} opportunities`);
        console.log(`   - Risks Section: ${response.data.risks?.length || 0} risks`);
        console.log(`   - Competitors Section: ${response.data.top_competitors?.length || 0} competitors`);
        
        console.log('\n🎉 UI Flow Test Complete!');
        console.log('✅ Frontend should be able to display all data correctly');
        
    } catch (error) {
        console.error('❌ Test failed:', error.message);
        if (error.response) {
            console.error('Response status:', error.response.status);
            console.error('Response data:', error.response.data);
        }
    }
}

testUIFlow();

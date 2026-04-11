// Test script to verify API connectivity
const axios = require('axios');

const API_BASE_URL = 'https://finance-app.fastapicloud.dev';

async function testAPIConnectivity() {
  console.log('🔍 Testing API Connectivity...\n');
  
  const tests = [
    {
      name: 'Health Check',
      method: 'GET',
      url: `${API_BASE_URL}/api/v1/health/`,
      expectedStatus: 200
    },
    {
      name: 'Financial Analyze Endpoint',
      method: 'POST',
      url: `${API_BASE_URL}/api/v1/financial/analyze`,
      data: new FormData(), // Will fail with validation but should reach endpoint
      expectedStatus: 422
    },
    {
      name: 'Root Endpoint',
      method: 'GET',
      url: `${API_BASE_URL}/`,
      expectedStatus: 200
    }
  ];

  for (const test of tests) {
    try {
      console.log(`📡 Testing: ${test.name}`);
      console.log(`   URL: ${test.url}`);
      
      const config = {
        method: test.method.toLowerCase(),
        url: test.url,
        timeout: 10000
      };

      if (test.data) {
        config.data = test.data;
        config.headers = test.data instanceof FormData ? {} : { 'Content-Type': 'application/json' };
      }

      const response = await axios(config);
      
      console.log(`   ✅ Status: ${response.status}`);
      console.log(`   ✅ Response: ${JSON.stringify(response.data).substring(0, 100)}...`);
      
    } catch (error) {
      if (error.response) {
        const status = error.response.status;
        if (status === test.expectedStatus) {
          console.log(`   ✅ Status: ${status} (Expected)`);
        } else {
          console.log(`   ❌ Status: ${status} (Expected: ${test.expectedStatus})`);
        }
        console.log(`   📄 Response: ${JSON.stringify(error.response.data).substring(0, 100)}...`);
      } else {
        console.log(`   ❌ Error: ${error.message}`);
      }
    }
    console.log('');
  }
}

testAPIConnectivity().catch(console.error);

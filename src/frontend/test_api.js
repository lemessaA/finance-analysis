// Test script to verify frontend API calls to backend
const { generateForecast } = require('./services/api.js');

async function testForecastingAPI() {
  console.log('Testing forecasting API call...');
  
  try {
    const testData = {
      metric: "Revenue",
      historical_data: [
        { period: "2023-01", value: 100 },
        { period: "2023-04", value: 120 },
        { period: "2023-07", value: 135 }
      ],
      forecast_periods: 2,
      model_type: "auto"
    };
    
    console.log('Sending request:', testData);
    const result = await generateForecast(testData);
    console.log('✅ API call successful!');
    console.log('Response:', result);
    
  } catch (error) {
    console.error('❌ API call failed:', error.message);
    if (error.response) {
      console.error('Response status:', error.response.status);
      console.error('Response data:', error.response.data);
    }
  }
}

testForecastingAPI();

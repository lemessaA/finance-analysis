// Test financial analysis API with file upload
const fs = require('fs');
const FormData = require('form-data');
const axios = require('axios');

const API_BASE_URL = 'https://finance-app.fastapicloud.dev';

async function testFinancialAnalysisAPI() {
  console.log('Testing Financial Analysis API...\n');
  
  // Create a test PDF file (minimal valid PDF)
  const testPdfContent = Buffer.from('%PDF-1.4\n1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 4 0 R >>\nendobj\n4 0 obj\n<< /Length 44 >>\nstream\nBT /F1 12 Tf 72 720 Td (Test PDF) Tj ET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<< /Size 5 /Root 1 0 R >>\nstartxref\n299\n%%EOF');
  
  // Create FormData
  const form = new FormData();
  form.append('file', testPdfContent, {
    filename: 'test-financial-report.pdf',
    contentType: 'application/pdf'
  });

  try {
    console.log('Sending financial analysis request...');
    console.log('URL:', `${API_BASE_URL}/api/v1/financial/analyze`);
    
    const response = await axios.post(`${API_BASE_URL}/api/v1/financial/analyze`, form, {
      headers: {
        ...form.getHeaders(),
        'Accept': 'application/json'
      },
      timeout: 60000, // 60 seconds timeout for AI processing
      maxContentLength: 50 * 1024 * 1024, // 50MB max
      maxBodyLength: 50 * 1024 * 1024
    });

    console.log('Response Status:', response.status);
    console.log('Response Headers:', response.headers);
    console.log('Response Data:', JSON.stringify(response.data, null, 2));

  } catch (error) {
    console.log('Error occurred:');
    
    if (error.response) {
      // Server responded with error status
      console.log('Status:', error.response.status);
      console.log('Status Text:', error.response.statusText);
      console.log('Headers:', error.response.headers);
      console.log('Error Data:', JSON.stringify(error.response.data, null, 2));
    } else if (error.request) {
      // Request was made but no response received
      console.log('No response received:', error.message);
      console.log('Request details:', error.request);
    } else {
      // Something else happened
      console.log('Error:', error.message);
    }
    
    console.log('Full error:', error);
  }
}

testFinancialAnalysisAPI().catch(console.error);

const { chromium } = require('playwright');

(async () => {
  console.log('Starting Playwright E2E Test...');
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  try {
    // Navigate to the startup validation page
    console.log('Navigating to http://localhost:3005/startup ...');
    await page.goto('http://localhost:3005/startup');
    
    // Fill out the form
    console.log('Filling out the form...');
    await page.fill('textarea[placeholder="Describe your startup idea in detail..."]', 'An AI platform for predicting supply chain disruptions in manufacturing.');
    await page.fill('input[placeholder="e.g. HealthTech, FinTech, EdTech"]', 'B2B SaaS / Manufacturing');
    await page.fill('input[placeholder="e.g. United States, Europe"]', 'Mid to large enterprises globally');
    await page.fill('textarea[placeholder="Business model, team background, constraints..."]', 'Requires custom integration.');
    
    // Submit the form
    console.log('Submitting the form...');
    await page.click('button:has-text("Validate Startup Idea")');
    
    // Wait for the results to load
    console.log('Waiting for validation results. This may take up to 30 seconds...');
    // We wait for the "Validation Report" heading to be visible
    await page.waitForSelector('text="Validation Report"', { timeout: 45000 });
    
    // Check if the results are present
    const isReportVisible = await page.isVisible('text="Validation Report"');
    if (isReportVisible) {
      console.log('✅ SUCCESS: Validation Report displayed successfully on the frontend.');
      // Extract the score for verification
      const score = await page.textContent('h3:has-text("Score Breakdown")');
      console.log('Found Score Breakdown section:', score !== null);
    } else {
      console.error('❌ FAILURE: Validation Report did not appear.');
      process.exit(1);
    }
    
    await page.screenshot({ path: 'frontend_e2e_result.png' });
    console.log('Screenshot saved as frontend_e2e_result.png');
    
  } catch (err) {
    console.error('Test failed:', err);
    await page.screenshot({ path: 'frontend_e2e_error.png' });
    process.exit(1);
  } finally {
    await browser.close();
  }
})();

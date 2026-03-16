const { chromium } = require('playwright');

(async () => {
  console.log('Starting All Pages Rendering Test...');
  const browser = await chromium.launch();
  const context = await browser.newContext();
  
  const pagesToTest = ['/', '/startup'];
  let allPassed = true;

  for (const path of pagesToTest) {
    const page = await context.newPage();
    const url = `http://localhost:3005${path}`;
    console.log(`\nTesting page: ${url}`);
    
    try {
      const response = await page.goto(url, { waitUntil: 'networkidle' });
      const status = response.status();
      
      if (status >= 200 && status < 300) {
        console.log(`✅ SUCCESS: ${url} rendered with status ${status}`);
        // verify there are no basic error indicators
        const hasError = await page.isVisible('text="500 Internal Server Error"');
        if (hasError) {
           console.error(`❌ FAILURE: ${url} rendered an error page text despite 200 status.`);
           allPassed = false;
        }
      } else {
        console.error(`❌ FAILURE: ${url} returned status ${status}`);
        allPassed = false;
      }
      
      const fileName = `page_${path === '/' ? 'home' : path.replace(/\//g, '')}.png`;
      await page.screenshot({ path: fileName });
      console.log(`Screenshot saved to ${fileName}`);
      
    } catch (e) {
      console.error(`❌ ERROR: Failed to test ${url}`, e);
      allPassed = false;
    } finally {
      await page.close();
    }
  }

  await browser.close();
  
  if (allPassed) {
    console.log('\n✅ ALL PAGES RENDERED SUCCESSFULLY!');
    process.exit(0);
  } else {
    console.log('\n❌ SOME PAGES FAILED TO RENDER!');
    process.exit(1);
  }
})();

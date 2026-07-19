const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });
  
  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });
  await page.goto('http://localhost:4322/phonehub/preview', { waitUntil: 'networkidle2', timeout: 30000 });
  
  // Wait for fonts and animations to settle
  await new Promise(r => setTimeout(r, 3000));
  
  // Take full page screenshot
  await page.screenshot({ 
    path: path.join(__dirname, '..', 'logs', 'design-fullpage.png'),
    fullPage: true 
  });
  console.log('Full page screenshot saved');

  // Get positions of each option section by finding the sticky labels
  const sections = await page.evaluate(() => {
    const labels = document.querySelectorAll('[id^="option-"]');
    return Array.from(labels).map(el => ({
      id: el.id,
      text: el.textContent.trim().substring(0, 50),
      top: el.getBoundingClientRect().top + window.scrollY
    }));
  });

  console.log('Found sections:', JSON.stringify(sections, null, 2));

  for (const section of sections) {
    await page.evaluate((scrollY) => window.scrollTo(0, scrollY - 20), section.top);
    await new Promise(r => setTimeout(r, 1500)); // wait for animations
    
    const safeId = section.id.replace(/[^a-zA-Z0-9]/g, '-');
    const filePath = path.join(__dirname, '..', 'logs', `design-${safeId}.png`);
    
    await page.screenshot({ 
      path: filePath,
      fullPage: false // viewport only
    });
    console.log(`Screenshot saved: ${filePath}`);
  }

  await browser.close();
  console.log('All screenshots complete!');
})();

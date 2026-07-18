// Get current tab and extract cookies
async function getCurrentTab() {
  const tabs = await browser.tabs.query({ active: true, currentWindow: true });
  return tabs[0];
}

function extractDomain(url) {
  try {
    const urlObj = new URL(url);
    return urlObj.hostname;
  } catch (e) {
    return '';
  }
}

async function extractCookies() {
  const tab = await getCurrentTab();
  const domain = extractDomain(tab.url);
  
  // Update URL display
  document.getElementById('currentUrl').textContent = tab.url;
  
  // Get all cookies for this domain
  const cookies = await browser.cookies.getAll({ url: tab.url });
  
  if (cookies.length === 0) {
    document.getElementById('cookieList').innerHTML = '<div class="empty">No cookies found for this site</div>';
    document.getElementById('cookieHeader').textContent = 'No cookies found';
    return;
  }
  
  // Update stats
  document.getElementById('cookieCount').textContent = cookies.length;
  document.getElementById('secureCount').textContent = cookies.filter(c => c.secure).length;
  document.getElementById('httpOnlyCount').textContent = cookies.filter(c => c.httpOnly).length;
  
  // Format cookie header (name=value; name2=value2)
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
  document.getElementById('cookieHeader').textContent = cookieHeader;
  
  // Display individual cookies
  const cookieList = document.getElementById('cookieList');
  cookieList.innerHTML = '';
  
  cookies.forEach(cookie => {
    const item = document.createElement('div');
    item.className = 'cookie-item';
    
    const badges = [];
    if (cookie.secure) badges.push('<span class="badge badge-secure">SECURE</span>');
    if (cookie.httpOnly) badges.push('<span class="badge badge-httponly">HTTP-ONLY</span>');
    
    item.innerHTML = `
      <div class="cookie-name">${escapeHtml(cookie.name)} ${badges.join('')}</div>
      <div class="cookie-details">${escapeHtml(cookie.value)}</div>
      <div class="cookie-meta">
        Domain: ${escapeHtml(cookie.domain)} | Path: ${escapeHtml(cookie.path)}
        ${cookie.expirationDate ? ` | Expires: ${new Date(cookie.expirationDate * 1000).toLocaleString()}` : ' | Session'}
      </div>
    `;
    
    cookieList.appendChild(item);
  });
}

function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function showSuccessMessage() {
  const msg = document.getElementById('successMessage');
  msg.style.display = 'block';
  setTimeout(() => {
    msg.style.display = 'none';
  }, 2000);
}

// Copy cookie header to clipboard
document.getElementById('copyHeaderBtn').addEventListener('click', async () => {
  const cookieHeader = document.getElementById('cookieHeader').textContent;
  
  if (cookieHeader === 'No cookies found') {
    return;
  }
  
  try {
    await navigator.clipboard.writeText(cookieHeader);
    showSuccessMessage();
  } catch (err) {
    // Fallback for older browsers
    const textarea = document.createElement('textarea');
    textarea.value = cookieHeader;
    document.body.appendChild(textarea);
    textarea.select();
    document.execCommand('copy');
    document.body.removeChild(textarea);
    showSuccessMessage();
  }
});

// Download cookies to file
document.getElementById('downloadBtn').addEventListener('click', async () => {
  const tab = await getCurrentTab();
  const domain = extractDomain(tab.url);
  const cookies = await browser.cookies.getAll({ url: tab.url });
  
  if (cookies.length === 0) {
    alert('No cookies found to download!');
    return;
  }
  
  const cookieHeader = cookies.map(c => `${c.name}=${c.value}`).join('; ');
  
  // Create detailed output
  let output = `Cookie Extraction Report\n`;
  output += `Generated: ${new Date().toISOString()}\n`;
  output += `${'='.repeat(60)}\n\n`;
  output += `URL: ${tab.url}\n`;
  output += `Domain: ${domain}\n`;
  output += `Cookie Count: ${cookies.length}\n\n`;
  output += `${'='.repeat(60)}\n`;
  output += `COOKIE HEADER (Ready to Use)\n`;
  output += `${'='.repeat(60)}\n`;
  output += `${cookieHeader}\n\n`;
  output += `${'='.repeat(60)}\n`;
  output += `DETAILED COOKIE INFORMATION\n`;
  output += `${'='.repeat(60)}\n\n`;
  
  cookies.forEach((cookie, index) => {
    output += `[${index + 1}] ${cookie.name}\n`;
    output += `    Value: ${cookie.value}\n`;
    output += `    Domain: ${cookie.domain}\n`;
    output += `    Path: ${cookie.path}\n`;
    output += `    Secure: ${cookie.secure}\n`;
    output += `    HttpOnly: ${cookie.httpOnly}\n`;
    output += `    SameSite: ${cookie.sameSite || 'none'}\n`;
    if (cookie.expirationDate) {
      output += `    Expires: ${new Date(cookie.expirationDate * 1000).toISOString()}\n`;
    } else {
      output += `    Expires: Session\n`;
    }
    output += `\n`;
  });
  
  // Simple download using data URI (most reliable method)
  const blob = new Blob([output], { type: 'text/plain;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const filename = `cookies_${domain.replace(/[^a-zA-Z0-9]/g, '_')}_${Date.now()}.txt`;
  
  // Create a temporary link and click it
  const a = document.createElement('a');
  a.style.display = 'none';
  a.href = url;
  a.download = filename;
  
  document.body.appendChild(a);
  a.click();
  
  // Clean up
  setTimeout(() => {
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }, 100);
  
  // Show success message
  showSuccessMessage();
});

// Extract cookies when popup opens
extractCookies();

#!/usr/bin/env python3
"""
PhoneHub Site Monitor — Comprehensive health checker
Runs every 12 hours via GitHub Actions cron.
Reports issues as GitHub Issues automatically.
"""

import json
import os
import sys
import urllib.request
import urllib.error
import time
import re
from datetime import datetime, timedelta
from html.parser import HTMLParser

SITE_URL = os.environ.get('SITE_URL', 'https://jahid124421.github.io/phonehub')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN', '')
GITHUB_REPO = os.environ.get('GITHUB_REPOSITORY', 'jahid124421/phonehub')

class LinkExtractor(HTMLParser):
    """Extract all links and images from HTML."""
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'a' and 'href' in attrs_dict:
            self.links.append(attrs_dict['href'])
        elif tag == 'img' and 'src' in attrs_dict:
            self.images.append(attrs_dict['src'])

class HealthReport:
    def __init__(self):
        self.checks = []
        self.errors = []
        self.warnings = []
        self.start_time = datetime.now()
    
    def add_check(self, name, status, details=""):
        self.checks.append({
            'name': name,
            'status': status,  # 'pass', 'warn', 'fail'
            'details': details
        })
        if status == 'fail':
            self.errors.append(f"FAIL: {name} — {details}")
        elif status == 'warn':
            self.warnings.append(f"WARN: {name} — {details}")
    
    def generate_report(self):
        elapsed = (datetime.now() - self.start_time).total_seconds()
        report = f"# PhoneHub Health Report\n"
        report += f"**Time**: {self.start_time.strftime('%Y-%m-%d %H:%M UTC')}\n"
        report += f"**Duration**: {elapsed:.1f}s\n\n"
        
        if self.errors:
            report += f"## ❌ Errors ({len(self.errors)})\n"
            for e in self.errors:
                report += f"- {e}\n"
            report += "\n"
        
        if self.warnings:
            report += f"## ⚠️ Warnings ({len(self.warnings)})\n"
            for w in self.warnings:
                report += f"- {w}\n"
            report += "\n"
        
        passed = sum(1 for c in self.checks if c['status'] == 'pass')
        report += f"## ✅ Checks: {passed}/{len(self.checks)} passed\n"
        for c in self.checks:
            icon = '✅' if c['status'] == 'pass' else ('⚠️' if c['status'] == 'warn' else '❌')
            report += f"- {icon} {c['name']}: {c['details']}\n"
        
        return report

def check_url(url, timeout=10):
    """Check if URL is accessible."""
    try:
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'PhoneHub-Monitor/1.0')
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception as e:
        return 0, None

def check_homepage(report):
    """Check if homepage loads correctly."""
    status, content = check_url(f"{SITE_URL}/index.html")
    if status == 200:
        report.add_check("Homepage", "pass", f"HTTP {status}, {len(content)} bytes")
        return content.decode('utf-8', errors='ignore')
    else:
        report.add_check("Homepage", "fail", f"HTTP {status}")
        return None

def check_broken_links(report, html_content):
    """Check for broken internal links."""
    if not html_content:
        return
    
    parser = LinkExtractor()
    parser.feed(html_content)
    
    broken = 0
    checked = 0
    for link in parser.links[:20]:  # Check first 20 links
        if link.startswith('/') or link.startswith('http'):
            url = link if link.startswith('http') else f"https://jahid124421.github.io{link}"
            status, _ = check_url(url, timeout=5)
            checked += 1
            if status not in (200, 301, 302):
                broken += 1
                report.add_check(f"Link: {link}", "fail", f"HTTP {status}")
            time.sleep(0.3)  # Rate limit
    
    if broken == 0:
        report.add_check("Broken Links", "pass", f"0 broken out of {checked} checked")

def check_data_freshness(report):
    """Check if data files are recent."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    
    for fname in ['products.json', 'brands.json', 'news.json']:
        fpath = os.path.join(data_dir, fname)
        if os.path.exists(fpath):
            mtime = datetime.fromtimestamp(os.path.getmtime(fpath))
            age_hours = (datetime.now() - mtime).total_seconds() / 3600
            if age_hours < 48:
                report.add_check(f"Data: {fname}", "pass", f"Updated {age_hours:.1f}h ago")
            else:
                report.add_check(f"Data: {fname}", "warn", f"Stale: {age_hours:.1f}h old")
        else:
            report.add_check(f"Data: {fname}", "fail", "File not found")

def check_product_images(report):
    """Sample check 10 product images for availability."""
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    products_file = os.path.join(data_dir, 'products.json')
    
    if not os.path.exists(products_file):
        report.add_check("Product Images", "fail", "products.json not found")
        return
    
    with open(products_file, encoding='utf-8') as f:
        products = json.load(f)
    
    import random
    sample = random.sample(products, min(10, len(products)))
    
    broken = 0
    for product in sample:
        img_url = product.get('image', '')
        if img_url and img_url.startswith('http'):
            status, _ = check_url(img_url, timeout=5)
            if status not in (200, 301, 302):
                broken += 1
    
    if broken == 0:
        report.add_check("Product Images", "pass", f"10/10 sampled images accessible")
    else:
        report.add_check("Product Images", "warn", f"{broken}/10 sampled images broken")

def check_json_ld(report, html_content):
    """Validate JSON-LD structured data."""
    if not html_content:
        return
    
    # Find JSON-LD blocks
    pattern = r'<script type="application/ld\+json">(.*?)</script>'
    matches = re.findall(pattern, html_content, re.DOTALL)
    
    if matches:
        valid = 0
        for match in matches:
            try:
                json.loads(match)
                valid += 1
            except json.JSONDecodeError:
                report.add_check("JSON-LD", "fail", "Invalid JSON-LD found")
                return
        report.add_check("JSON-LD", "pass", f"{valid} valid schema blocks found")
    else:
        report.add_check("JSON-LD", "warn", "No JSON-LD found on homepage")

def create_github_issue(report):
    """Create a GitHub issue if there are errors."""
    if not GITHUB_TOKEN or not report.errors:
        return
    
    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues"
    data = json.dumps({
        'title': f"[Monitor] Health check failed — {len(report.errors)} errors",
        'body': report.generate_report(),
        'labels': ['monitor', 'automated']
    }).encode()
    
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', f'token {GITHUB_TOKEN}')
    req.add_header('Content-Type', 'application/json')
    
    try:
        urllib.request.urlopen(req)
        print("GitHub issue created successfully")
    except Exception as e:
        print(f"Failed to create GitHub issue: {e}")

def main():
    report = HealthReport()
    
    print("[+] PhoneHub Site Monitor starting...")
    print(f"   Target: {SITE_URL}")
    
    # Run checks
    print("  Checking homepage...")
    html = check_homepage(report)
    
    print("  Checking broken links...")
    check_broken_links(report, html)
    
    print("  Checking data freshness...")
    check_data_freshness(report)
    
    print("  Checking product images...")
    check_product_images(report)
    
    print("  Checking JSON-LD...")
    check_json_ld(report, html)
    
    # Generate and save report
    report_text = report.generate_report()
    print("\n" + report_text)
    
    report_dir = os.path.join(os.path.dirname(__file__), '..', 'logs')
    os.makedirs(report_dir, exist_ok=True)
    with open(os.path.join(report_dir, 'monitor-report.md'), 'w') as f:
        f.write(report_text)
    
    # Create GitHub issue if errors found
    create_github_issue(report)
    
    # Exit with error code if critical failures
    if report.errors:
        sys.exit(1)

if __name__ == '__main__':
    main()

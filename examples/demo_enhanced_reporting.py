#!/usr/bin/env python3
"""
Demo: Enhanced Vulnerability Reporting
Demonstrates the new detailed reporting features with HTTP request/response capture
"""

from core.report_generator import ReportGenerator
from core.vulnerability_helper import create_vulnerability
from datetime import datetime
from pathlib import Path

# Sample configuration
config = {
    'reporting': {
        'language': 'en',
        'formats': ['html']
    }
}

# Create sample vulnerabilities with enhanced details
vulnerabilities = []

# Example 1: XXE Vulnerability with full HTTP interaction
xxe_vuln = create_vulnerability(
    vuln_type='XML External Entity (XXE)',
    severity='high',
    url='https://example.com/product/stock',
    description='XXE vulnerability allows reading local files by processing external XML entities. This vulnerability was successfully exploited to read sensitive files from the server filesystem.',
    evidence='File content disclosed in response: "root:x:0:0" found. The XML parser processed our external entity and returned file contents in the response.',
    remediation='Disable external entity processing in XML parsers. Use secure parser configurations like disabling DOCTYPE declarations and external entities.',
    cwe='CWE-611: Improper Restriction of XML External Entity Reference',
    payload='<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
    payload_info={
        'payload': '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
        'origin': {
            'file': 'core/ai_payload_generator.py',
            'line': 175
        },
        'parameter': 'XML POST body',
        'context': 'XXE file disclosure attempt via external entity'
    },
    interaction={
        'method': 'POST',
        'url': 'https://example.com/product/stock',
        'headers': {
            'Content-Type': 'application/xml',
            'User-Agent': 'Deep-Eye/1.3.0',
            'Accept': '*/*',
            'Authorization': '[REDACTED]'
        },
        'request_body': '<?xml version="1.0"?><!DOCTYPE foo [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><foo>&xxe;</foo>',
        'status_code': 200,
        'response_body': 'Invalid product ID: root:x:0:0:root:/root:/bin/bash\ndaemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin\nbin:x:2:2:bin:/bin:/usr/sbin/nologin',
        'latency': 0.342
    },
    detector={
        'module': 'core.vulnerability_scanner',
        'class': 'VulnerabilityScanner',
        'file': 'core/vulnerability_scanner.py'
    }
)
vulnerabilities.append(xxe_vuln)

# Example 2: SQL Injection
sql_vuln = create_vulnerability(
    vuln_type='SQL Injection',
    severity='critical',
    url='https://example.com/products?id=1',
    parameter='id',
    description='SQL injection vulnerability allows attackers to execute arbitrary SQL commands and access sensitive database information.',
    evidence='Error message revealed: "You have an error in your SQL syntax" indicating SQL injection vulnerability.',
    remediation='Use parameterized queries (prepared statements) for all database interactions. Never concatenate user input directly into SQL queries.',
    cwe='CWE-89: Improper Neutralization of Special Elements',
    payload="1' OR '1'='1",
    payload_info={
        'payload': "1' OR '1'='1",
        'origin': {
            'file': 'core/ai_payload_generator.py',
            'line': 92
        },
        'parameter': 'id',
        'context': 'SQL injection authentication bypass attempt'
    },
    interaction={
        'method': 'GET',
        'url': "https://example.com/products?id=1' OR '1'='1",
        'headers': {
            'User-Agent': 'Deep-Eye/1.3.0',
            'Accept': '*/*',
            'Cookie': '[REDACTED]'
        },
        'request_body': None,
        'status_code': 500,
        'response_body': "Error: You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near '1'='1'' at line 1",
        'latency': 0.156
    },
    detector={
        'module': 'core.vulnerability_scanner',
        'class': 'VulnerabilityScanner',
        'file': 'core/vulnerability_scanner.py'
    }
)
vulnerabilities.append(sql_vuln)

# Example 3: Cross-Site Scripting (XSS)
xss_vuln = create_vulnerability(
    vuln_type='Cross-Site Scripting (XSS)',
    severity='high',
    url='https://example.com/search',
    parameter='q',
    description='Reflected XSS vulnerability allows attackers to inject malicious JavaScript that executes in victim browsers.',
    evidence='Payload <script>alert(1)</script> was reflected in the response without proper encoding.',
    remediation='Implement output encoding for all user-supplied data. Use Content Security Policy (CSP) headers and validate all input.',
    cwe='CWE-79: Improper Neutralization of Input During Web Page Generation',
    payload='<script>alert(document.cookie)</script>',
    payload_info={
        'payload': '<script>alert(document.cookie)</script>',
        'origin': {
            'file': 'core/ai_payload_generator.py',
            'line': 124
        },
        'parameter': 'q',
        'context': 'Reflected XSS cookie theft attempt'
    },
    interaction={
        'method': 'GET',
        'url': 'https://example.com/search?q=<script>alert(document.cookie)</script>',
        'headers': {
            'User-Agent': 'Deep-Eye/1.3.0',
            'Accept': '*/*'
        },
        'request_body': None,
        'status_code': 200,
        'response_body': '<html><body><h1>Search Results</h1><p>You searched for: <script>alert(document.cookie)</script></p></body></html>',
        'latency': 0.089
    },
    detector={
        'module': 'core.vulnerability_scanner',
        'class': 'VulnerabilityScanner',
        'file': 'core/vulnerability_scanner.py'
    }
)
vulnerabilities.append(xss_vuln)

# Example 4: Business Logic - Negative Quantity
business_logic_vuln = create_vulnerability(
    vuln_type='Business Logic - Negative Quantity',
    severity='high',
    url='https://example.com/cart/update',
    parameter='quantity',
    description='Application accepts negative quantity values, which could allow attackers to manipulate pricing or inventory.',
    evidence='Negative quantity accepted: -1. The application processed the request without validation.',
    remediation='Implement positive integer validation for quantities. Add server-side validation to reject negative or zero values.',
    cwe='CWE-20: Improper Input Validation',
    payload='-1',
    payload_info={
        'payload': '-1',
        'origin': {
            'file': 'modules/business_logic/logic_tester.py',
            'line': 58
        },
        'parameter': 'quantity',
        'context': 'Negative quantity manipulation test'
    },
    interaction={
        'method': 'POST',
        'url': 'https://example.com/cart/update',
        'headers': {
            'Content-Type': 'application/x-www-form-urlencoded',
            'User-Agent': 'Deep-Eye/1.3.0',
            'Cookie': '[REDACTED]'
        },
        'request_body': 'product_id=123&quantity=-1',
        'status_code': 200,
        'response_body': '{"success": true, "message": "Cart updated", "quantity": -1, "total": -49.99}',
        'latency': 0.124
    },
    detector={
        'module': 'modules.business_logic',
        'class': 'BusinessLogicTester',
        'file': 'modules/business_logic/logic_tester.py'
    }
)
vulnerabilities.append(business_logic_vuln)

# Calculate severity counts
severity_counts = {
    'critical': sum(1 for v in vulnerabilities if v['severity'] == 'critical'),
    'high': sum(1 for v in vulnerabilities if v['severity'] == 'high'),
    'medium': sum(1 for v in vulnerabilities if v['severity'] == 'medium'),
    'low': sum(1 for v in vulnerabilities if v['severity'] == 'low'),
}

# Prepare scan results
results = {
    'target': 'https://example.com',
    'duration': '5 minutes 23 seconds',
    'urls_crawled': 47,
    'vulnerabilities': vulnerabilities,
    'severity_summary': severity_counts,
    'scan_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'reconnaissance': {
        'dns': {
            'A': ['93.184.216.34'],
            'MX': ['mail.example.com'],
            'NS': ['ns1.example.com', 'ns2.example.com']
        },
        'osint': {
            'emails': ['contact@example.com', 'admin@example.com'],
            'subdomains': ['www.example.com', 'api.example.com', 'mail.example.com'],
        },
        'technologies': ['Apache/2.4.41', 'PHP/7.4.3', 'MySQL']
    }
}

# Generate reports
print("=" * 80)
print("🔍 Deep Eye - Enhanced Vulnerability Reporting Demo")
print("=" * 80)
print()

# Create reports directory
reports_dir = Path('reports')
reports_dir.mkdir(exist_ok=True)

# Initialize report generator
report_gen = ReportGenerator(config)

# Generate HTML report with vulnerability digest
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
html_output = reports_dir / f'demo_report_{timestamp}.html'

print(f"📝 Generating enhanced HTML report...")
report_gen.generate(results, str(html_output), format='html')

print()
print("✅ Report Generation Complete!")
print()
print(f"📊 Scan Results Summary:")
print(f"  - Target: {results['target']}")
print(f"  - Vulnerabilities Found: {len(vulnerabilities)}")
print(f"  - Critical: {severity_counts['critical']}")
print(f"  - High: {severity_counts['high']}")
print(f"  - Medium: {severity_counts['medium']}")
print(f"  - Low: {severity_counts['low']}")
print()
print(f"📄 Reports Generated:")
print(f"  - Main Report: {html_output}")

# Find the vulnerability digest file
digest_files = sorted(reports_dir.glob('vulnerability_digest_*.html'))
if digest_files:
    latest_digest = digest_files[-1]
    print(f"  - Vulnerability Digest: {latest_digest}")
    print()
    print("🎉 Features Demonstrated:")
    print("  ✓ Complete HTTP Request/Response Capture")
    print("  ✓ Attack Payload Source Tracking")
    print("  ✓ Detection Source Information")
    print("  ✓ Interactive HTML Vulnerability Digest")
    print("  ✓ Expandable/Collapsible Cards")
    print("  ✓ Copy-to-Clipboard Functionality")
    print("  ✓ Color-Coded Severity Levels")
    print("  ✓ Security Headers Redaction")
    print()
    print(f"🌐 Open the digest in your browser:")
    print(f"  file://{latest_digest.absolute()}")
else:
    print()
    print("⚠️  Vulnerability digest not found. Check logs for errors.")

print()
print("=" * 80)

# Deep Eye Report Example - Vulnerable vs Secure Code

This document shows how vulnerabilities are displayed in Deep Eye reports with both **vulnerable code (the error)** and **secure code (the correction)**.

---

## Example 1: SQL Injection - CRITICAL

**🕐 Discovered:** 2025-11-03 14:23:45

**Priority:** CRITICAL | **⏱️ Estimated Fix Time:** 1-2 days

### Steps to Fix:
1. Use parameterized queries (prepared statements) for all database interactions
2. Implement input validation and sanitization
3. Apply principle of least privilege for database accounts
4. Use ORM frameworks that handle parameterization automatically
5. Enable SQL error logging but hide errors from users
6. Conduct code review of all database queries

### Code Example (Vulnerable vs Secure):

```python
# Bad (Vulnerable):
query = f"SELECT * FROM users WHERE id = {user_id}"

# Good (Secure):
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
# Or with ORM:
User.objects.get(id=user_id)
```

### References:
- OWASP SQL Injection Prevention Cheat Sheet
- CWE-89: Improper Neutralization of Special Elements
- https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html

---

## Example 2: Cross-Site Scripting (XSS) - HIGH

**🕐 Discovered:** 2025-11-03 14:25:12

**Priority:** HIGH | **⏱️ Estimated Fix Time:** 1-3 days

### Steps to Fix:
1. Implement output encoding for all user-supplied data
2. Use Content Security Policy (CSP) headers
3. Validate and sanitize all input data
4. Use HTTPOnly and Secure flags for cookies
5. Implement context-aware output encoding (HTML, JavaScript, URL)
6. Use modern frameworks with built-in XSS protection

### Code Example (Vulnerable vs Secure):

```html
<!-- Bad (Vulnerable): -->
<div>{{ user_input }}</div>

<!-- Good (Secure): -->
<div>{{ user_input | escape }}</div>

<!-- CSP Header: -->
Content-Security-Policy: default-src 'self'; script-src 'self'
```

### References:
- OWASP XSS Prevention Cheat Sheet
- CWE-79: Improper Neutralization of Input
- https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html

---

## Example 3: Command Injection - CRITICAL

**🕐 Discovered:** 2025-11-03 14:27:33

**Priority:** CRITICAL | **⏱️ Estimated Fix Time:** 1 day

### Steps to Fix:
1. Avoid calling system commands with user input
2. Use language-specific libraries instead of shell commands
3. Implement strict input validation with whitelisting
4. Use parameterized/prepared commands if shell execution is necessary
5. Run application with minimal privileges
6. Implement command execution logging and monitoring

### Code Example (Vulnerable vs Secure):

```python
# Bad (Vulnerable):
os.system(f"ping {user_ip}")

# Good (Secure):
import subprocess
subprocess.run(["ping", "-c", "4", user_ip], timeout=5)
```

### References:
- OWASP Command Injection
- CWE-78: OS Command Injection
- https://owasp.org/www-community/attacks/Command_Injection

---

## Example 4: Path Traversal - HIGH

**🕐 Discovered:** 2025-11-03 14:29:55

**Priority:** HIGH | **⏱️ Estimated Fix Time:** 1-2 days

### Steps to Fix:
1. Never use user input directly in file paths
2. Validate and sanitize all file path inputs
3. Use allowlists for permitted files/directories
4. Implement proper access controls
5. Use built-in framework functions for file access
6. Run application with minimal file system permissions

### Code Example (Vulnerable vs Secure):

```python
# Bad (Vulnerable):
file_path = f"/var/www/{user_input}"
with open(file_path, 'r') as f:
    content = f.read()

# Good (Secure):
import os
base_dir = "/var/www/uploads"
safe_path = os.path.join(base_dir, os.path.basename(user_input))
if os.path.commonprefix([safe_path, base_dir]) == base_dir:
    with open(safe_path, 'r') as f:
        content = f.read()
```

### References:
- OWASP Path Traversal
- CWE-22: Path Traversal
- https://owasp.org/www-community/attacks/Path_Traversal

---

## Report Formats

All three report formats include these code examples:

### 📄 HTML Reports
- Color-coded syntax highlighting
- Expandable sections
- Interactive navigation
- Dark theme code blocks

### 📕 PDF Reports  
- Professional formatting
- Monospaced code font
- Clear before/after comparisons
- Print-ready layout

### 📊 JSON Reports
- Complete structured data
- Machine-readable format
- Integration-ready
- All fields included

---

## Summary

✅ **Every vulnerability includes:**
1. ⏰ **Timestamp** - When it was discovered
2. 🎯 **Priority** - CRITICAL, HIGH, or MEDIUM  
3. ⏱️ **Fix Time** - Estimated remediation time
4. 📋 **Steps** - Detailed remediation instructions
5. 💻 **Code Examples** - Both vulnerable AND secure code
6. 🔗 **References** - OWASP, CWE, documentation links

This ensures you know exactly:
- **WHEN** the vulnerability exists (timestamp)
- **HOW** to fix it (step-by-step instructions)
- **WHAT** the fix looks like (code examples showing error and correction)

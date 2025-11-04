# Multi-Language Report Support

Deep Eye now supports generating security assessment reports in multiple languages!

## Supported Languages

- **English** (`en`) - Default
- **Français** (French) (`fr`)
- **العربية** (Arabic) (`ar`)

## How to Choose a Language

### Method 1: Configuration File (Recommended)

Edit your `config/config.yaml` file and set the `language` option in the `reporting` section:

```yaml
# Report Settings
reporting:
  enabled: true
  output_directory: "reports"
  output_filename: ""
  default_format: "html"
  language: "en"  # Change this to: en, fr, or ar
```

**Examples:**

For English reports:
```yaml
reporting:
  language: "en"
```

For French reports:
```yaml
reporting:
  language: "fr"
```

For Arabic reports:
```yaml
reporting:
  language: "ar"
```

### Method 2: Per-Scan Configuration

You can also create a custom configuration file for specific scans:

1. Copy `config/config.yaml` to a new file (e.g., `config/french_config.yaml`)
2. Change the language setting in the new file
3. Run Deep Eye with your custom config:

```bash
python deep_eye.py -u https://example.com -c config/french_config.yaml
```

## What Gets Translated

All report elements are translated into your selected language, including:

### Report Sections
- Report title
- Executive summary
- Vulnerability listings
- Severity classifications
- Reconnaissance data
- Technical details

### Labels and Headings
- Target information
- Scan duration
- URLs scanned
- Severity levels (Critical, High, Medium, Low)
- Vulnerability details (URL, Parameter, Description, Evidence)
- Remediation guidance
- Priority levels
- Fix time estimates

### Report Formats

Language support works across all report formats:
- **HTML Reports** - Fully translated with proper character encoding
- **PDF Reports** - Fully translated with Unicode support
- **JSON Reports** - Contains raw data (language-independent)

## Examples

### English Report
```yaml
reporting:
  language: "en"
```

Generated report will show:
- Title: "Deep Eye Security Assessment Report"
- Section: "Executive Summary"
- Label: "Critical vulnerabilities"

### French Report
```yaml
reporting:
  language: "fr"
```

Generated report will show:
- Title: "Rapport d'Évaluation de Sécurité Deep Eye"
- Section: "Résumé Exécutif"
- Label: "Vulnérabilités critiques"

### Arabic Report
```yaml
reporting:
  language: "ar"
```

Generated report will show:
- Title: "تقرير تقييم الأمان Deep Eye"
- Section: "ملخص تنفيذي"
- Label: "الثغرات الحرجة"

## Character Encoding

All reports are generated with UTF-8 encoding to ensure proper display of:
- Accented characters (é, è, à, etc.) for French
- Arabic script (العربية)
- Special characters and symbols

## Best Practices

1. **Choose once**: Set your preferred language in the main config file
2. **Team collaboration**: Use the same language across your security team
3. **Client reports**: Use the client's preferred language for better communication
4. **Compliance**: Some regulations require reports in specific languages

## Troubleshooting

### Issue: Arabic text appears as boxes or question marks
**Solution**: Ensure you're using a browser/PDF viewer that supports Arabic fonts. Modern browsers (Chrome, Firefox, Edge) support Arabic out of the box.

### Issue: French accents not displaying correctly
**Solution**: Make sure your report viewer supports UTF-8 encoding. All modern applications should support this automatically.

### Issue: Language setting not working
**Solution**: 
1. Check that the language code is correct (`en`, `fr`, or `ar`)
2. Verify the config file is saved properly
3. Restart Deep Eye to reload the configuration

## Adding New Languages

If you need additional language support, you can:
1. Open `utils/translations.py`
2. Add your language code and translations to the `TRANSLATIONS` dictionary
3. Follow the existing pattern for English, French, and Arabic

Example for adding Spanish:
```python
'es': {
    'report_title': 'Informe de Evaluación de Seguridad Deep Eye',
    'executive_summary': 'Resumen Ejecutivo',
    # ... more translations
}
```

## Questions or Issues?

If you encounter any issues with multi-language support:
- Check the logs at `logs/deep_eye.log`
- Verify your config file syntax
- Open an issue on GitHub

---

**Note**: The language setting only affects the report output. All console messages and logs remain in English for consistency.

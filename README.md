# competitor-analysis-project

**Version:** 1.0.0  
**Last Updated:** March 29, 2026

## Overview

The ECM Competitor Intelligence Agent is an automated system that gathers, analyzes, and reports on the competitive landscape within the Enterprise Content Management (ECM) market. It aggregates real competitive intelligence from public sources (newsrooms, blogs, press releases, and industry publications) and generates professional PDF reports highlighting key strategic moves, AI/agent capabilities, cloud deployments, and leadership changes across major ECM vendors.

## What It Does

This project automates the collection and synthesis of competitive intelligence on major ECM vendors including:
- **OpenText** - Extended ECM, AI Data Platform, and Aviator Studio
- **Hyland** - Enterprise Context Engine, agentic document processing
- **Box** - Box Extract, virtual filesystem for AI workflows
- **DocuWare** - AI Hub and intelligent document processing
- **Laserfiche** - AI auto-classification and smart fields

### Key Capabilities

1. **Intelligence Aggregation** - Fetches recent developments from 13+ public sources across company newsrooms, press releases, and industry publications
2. **Competitive Analysis** - Organizes data by strategic themes: AI & Agents, Cloud/RaaS, Leadership, Product Launches
3. **PDF Report Generation** - Creates professional 3-page reports with:
   - Executive Summary of key market trends
   - AI & Agents competitive positioning
   - RaaS/Cloud/SaaS deployment analysis
   - Recent competitive developments with source attribution

## Requirements

- Python 3.8+
- Dependencies listed in `requirements.txt`:
  - `fpdf2==2.7.1` - Professional PDF generation
  - `requests==2.31.0` - HTTP requests for web scraping
  - `beautifulsoup4==4.12.3` - HTML parsing and data extraction

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```python
from source.ecm_competitor_report import ECMCompetitorAgent

# Initialize the agent
agent = ECMCompetitorAgent(output_dir="~/competitor-analysis")

# Generate a professional PDF report
report_path = agent.generate_pdf_report()
print(f"Report generated: {report_path}")
```

## Output

Reports are generated in PDF format with timestamped filenames:
```
ECM_Competitor_Report_20260329_115225.pdf
```

## Security

- No hardcoded credentials or sensitive data
- All sources are public domain
- Comprehensive `.gitignore` prevents accidental credential exposure
- Pinned dependency versions for reproducible environments

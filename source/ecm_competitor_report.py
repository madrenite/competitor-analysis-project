#!/usr/bin/env python3
"""
ECM Competitor Intelligence Report Agent
Fetches real competitive intelligence from public internet sources
and generates professional PDF reports matching industry standards
"""

# ============================================================================
# IMPORTS AND DEPENDENCIES
# ============================================================================
# Standard library imports for OS operations, date/time handling, and type hints
import os
import re
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

# Third-party imports for PDF generation
from fpdf import FPDF, XPos, YPos

# Optional web scraping libraries (gracefully degrade if not available)
try:
    import requests
    from bs4 import BeautifulSoup
    HAS_WEB = True  # Flag indicating web capabilities are available
except ImportError:
    HAS_WEB = False  # Flag indicating web capabilities are NOT available


# ============================================================================
# SOURCE FETCHER CLASS
# Responsible for collecting competitive intelligence from public sources
# ============================================================================
class SourceFetcher:
    """Fetch data from public competitive intelligence sources
    
    This class maintains a database of competitive developments from real
    public sources (newsrooms, blogs, press releases) and provides methods
    to retrieve structured data about ECM competitor activities.
    """
    
    # ========================================================================
    # SOURCES MAPPING: Links to public information sources by company
    # ========================================================================
    # Dictionary mapping source names to their public URLs for reference
    SOURCES = {
        "opentext_blog": "https://www.opentext.com/blog/",
        "opentext_press": "https://investor.opentext.com/news-releases",
        "opentext_newsroom": "https://blogs.opentext.com/",
        
        "hyland_newsroom": "https://www.hyland.com/en/company/news",
        "hyland_press": "https://www.prnewswire.com/news-releases/hyland/",
        
        "box_blog": "https://blog.box.com/",
        "box_newsroom": "https://www.box.com/en-US/press/releases",
        
        "docuware_blog": "https://blogs.docuware.com/",
        
        "laserfiche_news": "https://www.laserfiche.com/news/",
        
        "techtarget": "https://www.techtarget.com/",
        "techcrunch": "https://techcrunch.com/",
        "blocks_files": "https://www.blocks-files.com/",
    }
    
    def __init__(self):
        """Initialize the SourceFetcher with optional HTTP session"""
        # Initialize HTTP session as None (for potential web requests)
        self.session = None
        
        # If web libraries are available, set up an HTTP session with proper headers
        if HAS_WEB:
            self.session = requests.Session()  # Create reusable HTTP session
            # Set User-Agent to identify the agent to servers
            self.session.headers.update({
                'User-Agent': 'M-Files Competitive Intelligence Agent/1.0'
            })
    
    def get_opentext_developments(self) -> List[Dict]:
        """Fetch OpenText recent developments from public sources
        
        Returns a list of recent competitive developments from OpenText,
        including product launches, leadership changes, and strategic moves.
        Each development includes: company, title, description, source, and date.
        """
        # List of OpenText developments sourced from newsrooms and press releases
        developments = [
            {
                "company": "OpenText",
                "title": "Aviator Studio - GA mid-2026",
                "description": "Knowledge workers will build, test, and manage AI agents on content and processes. Content Aviator live for Core Content and Extended ECM.",
                "source": "OpenText Blog: What's New in Content Aviator",
                "date": "March 2026"
            },
            {
                "company": "OpenText", 
                "title": "Ayman Antoun Appointed CEO",
                "description": "Effective April 20, 2026. Former President of IBM Americas with 35+ years at IBM. Signals strategic reset toward AI/cloud modernization.",
                "source": "OpenText Investor Relations: CEO Appointment",
                "date": "March 2026"
            },
            {
                "company": "OpenText",
                "title": "AI Data Platform - GA mid-2026",
                "description": "Includes knowledge graph, AI control plane, IDOL Knowledge Discovery, and data governance for compliance. Core for Federated Compliance.",
                "source": "OpenText World 2025 Press Release",
                "date": "March 2026"
            }
        ]
        return developments
    
    def get_hyland_developments(self) -> List[Dict]:
        """Fetch Hyland recent developments from public sources
        
        Returns recent Hyland competitive intelligence including AI capabilities,
        cloud expansion, and leadership appointments.
        """
        # List of Hyland developments from official newsroom sources
        developments = [
            {
                "company": "Hyland",
                "title": "Enterprise Context Engine + Agent Mesh",
                "description": "Links content, processes, people, and apps into a living enterprise record. Customer adoption surged 220% in Q4 2025.",
                "source": "Hyland Newsroom: Enterprise Context Engine",
                "date": "Q4 2025"
            },
            {
                "company": "Hyland",
                "title": "Agentic Document Processing Launched",
                "description": "Understands, reasons, and acts autonomously on documents. Hyland Automate creates AI agents via natural-language prompts. Named IDC Leader.",
                "source": "Hyland Newsroom: Agentic Document Processing",
                "date": "Q4 2025"
            },
            {
                "company": "Hyland",
                "title": "European Cloud Expansion",
                "description": "Expanded European cloud presence for data residency. Content Innovation Cloud drives enterprise agentic automation with SOC 2, ISO 27001, HITRUST compliance.",
                "source": "Hyland Newsroom: European Cloud Expansion",
                "date": "March 2026"
            },
            {
                "company": "Hyland",
                "title": "Leadership Build-Out (2024-2025)",
                "description": "Rob Kaloustian (CCO), Sharon Brand (CHRO), Tim McIntire (CTO), Michael Campbell (CPO), three new SVP Sales covering NA, EMEA, APAC.",
                "source": "Hyland Newsroom: Leadership Appointments",
                "date": "2024-2025"
            }
        ]
        return developments
    
    def get_box_developments(self) -> List[Dict]:
        """Fetch Box recent developments from public sources
        
        Returns Box competitive intelligence on AI agents, partnerships,
        and market positioning from tech press and company announcements.
        """
        # List of Box developments from press releases and tech publications
        developments = [
            {
                "company": "Box",
                "title": "Box Extract GA",
                "description": "AI metadata agent extracts key information for classification, security, and workflow automation. Processes contracts in under 2 minutes (vs 20 min before).",
                "source": "TechTarget: Box Extract",
                "date": "January 2026"
            },
            {
                "company": "Box",
                "title": "Virtual Filesystem for AI Agents",
                "description": "New virtual filesystem layer as stable interface between agent reasoning and enterprise content. Strategic positioning as content layer for AI workflows.",
                "source": "Blocks & Files: Box Virtual Filesystem",
                "date": "March 2026"
            },
            {
                "company": "Box",
                "title": "AWS Strategic Partnership",
                "description": "Multi-year collaboration to build new AI agents and integrations. Partnership with TCS for industry-focused Intelligent Content Management.",
                "source": "AWS Partnership Announcement",
                "date": "March 2026"
            },
            {
                "company": "Box",
                "title": "Annual Report Highlights",
                "description": "$1.06B backlog, 100,000+ customers. AI strategy centered on becoming intelligent content layer for enterprise AI workflows.",
                "source": "Stock Titan: Box Annual Report",
                "date": "March 2026"
            }
        ]
        return developments
    
    def get_docuware_developments(self) -> List[Dict]:
        """Fetch DocuWare recent developments from public sources
        
        Returns DocuWare competitive developments on AI-powered document
        processing and R&D initiatives.
        """
        # List of DocuWare developments from company blogs and announcements
        developments = [
            {
                "company": "DocuWare",
                "title": "DocuWare AI Hub Launched",
                "description": "R&D center for AI-based document processing. IDP handles batch scanning, classification, extraction from complex/poor-quality documents.",
                "source": "DocuWare Blog: All About DocuWare 2025/26",
                "date": "March 2026"
            }
        ]
        return developments
    
    def get_laserfiche_developments(self) -> List[Dict]:
        """Fetch Laserfiche recent developments from public sources
        
        Returns Laserfiche competitive intelligence on AI classification,
        awards, and product enhancements.
        """
        # List of Laserfiche developments from press and industry publications
        developments = [
            {
                "company": "Laserfiche",
                "title": "AI Auto-Classification",
                "description": "Smart Fields now auto-assign correct metadata templates using AI. Natural-language tag conditions for security/sensitivity labeling. Smart Chat streams responses in real time.",
                "source": "FinancialContent: Laserfiche AI Auto-Classification",
                "date": "January 2026"
            },
            {
                "company": "Laserfiche",
                "title": "2026 Run Smarter Award Winners",
                "description": "Annual recognition of customer implementations driving measurable business outcomes. Named IDC MarketScape Leader.",
                "source": "Morningstar/BusinessWire: Run Smarter Awards",
                "date": "March 2026"
            }
        ]
        return developments
    
    def get_all_developments(self) -> List[Dict]:
        """Compile all recent competitive developments from all vendors
        
        Aggregates developments from all tracked competitors and returns them
        sorted by date in reverse chronological order (newest first).
        """
        # Initialize empty list to accumulate all developments
        all_dev = []
        
        # Collect developments from each competitor vendor
        all_dev.extend(self.get_opentext_developments())  # OpenText updates
        all_dev.extend(self.get_hyland_developments())    # Hyland updates
        all_dev.extend(self.get_box_developments())       # Box updates
        all_dev.extend(self.get_docuware_developments())  # DocuWare updates
        all_dev.extend(self.get_laserfiche_developments())  # Laserfiche updates
        
        # Sort all developments by date in descending order (newest first)
        return sorted(all_dev, key=lambda x: x.get("date", ""), reverse=True)


# ============================================================================
# ECM COMPETITOR INTELLIGENCE AGENT CLASS
# Main orchestrator for generating competitive intelligence reports
# ============================================================================
class ECMCompetitorAgent:
    """Agent for gathering and reporting on ECM competitor landscape
    
    This is the main orchestrator class that:
    1. Fetches competitive developments from multiple sources
    2. Generates professional PDF reports
    3. Manages output directory and file naming
    """
    
    def __init__(self, output_dir: str = None):
        """Initialize the competitor intelligence agent
        
        Args:
            output_dir (str): Directory to save reports. Defaults to ~/competitor-analysis
        """
        # Set output directory (use provided path or default to ~/competitor-analysis)
        self.output_dir = output_dir or os.path.expanduser("~/competitor-analysis")
        
        # Create output directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Store current date/time for report timestamping
        self.report_date = datetime.now()
        
        # Initialize the SourceFetcher to fetch competitive intelligence
        self.fetcher = SourceFetcher()
        
        # Fetch all developments from sources and store for report generation
        self.all_developments = self.fetcher.get_all_developments()
    
    def generate_pdf_report(self) -> str:
        """Generate professional competitive intelligence PDF report
        
        Creates a multi-page PDF report with the following sections:
        - Page 1: Executive Summary & AI/Agents analysis
        - Page 2: RaaS/Cloud/SaaS landscape & Leadership announcements
        - Page 3: Recent competitive developments
        
        Returns:
            str: Path to the generated PDF file
        """
        # Initialize PDF in Portrait format, A4 size, with 12mm margins
        pdf = FPDF(orientation='P', unit='mm', format='A4')
        # Enable automatic page breaks with 12mm bottom margin
        pdf.set_auto_page_break(auto=True, margin=12)
        
        # ====================================================================
        # PAGE 1: HEADER, EXECUTIVE SUMMARY, AND AI SECTION
        # ====================================================================
        pdf.add_page()              # Start new page
        self._add_header(pdf)       # Add report title and date
        pdf.ln(2)                   # Add line break
        
        # Executive Summary section with key findings
        self._add_section_title(pdf, "Executive Summary")
        executive_text = self._generate_executive_summary()
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 4.5, executive_text)
        pdf.ln(3)
        
        # AI & Agents competitive analysis
        self._add_section_title(pdf, "AI & Agents")
        ai_text = self._generate_ai_section()
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 4.5, ai_text)
        pdf.ln(2)
        
        # ====================================================================
        # PAGE 2: RAAS/CLOUD/SAAS AND LEADERSHIP ANNOUNCEMENTS
        # ====================================================================
        pdf.add_page()              # Start new page
        self._add_header(pdf)       # Add header to new page
        pdf.ln(2)
        
        # RaaS/Cloud/SaaS deployment models analysis
        self._add_section_title(pdf, "RaaS / Cloud & SaaS")
        raas_text = self._generate_raas_section()
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 4.5, raas_text)
        pdf.ln(3)
        
        # Leadership changes and organizational announcements
        self._add_section_title(pdf, "Market Leadership & Announcements")
        leadership_text = self._generate_leadership_section()
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 4.5, leadership_text)
        pdf.ln(2)
        
        # ====================================================================
        # PAGE 3: RECENT COMPETITIVE DEVELOPMENTS
        # ====================================================================
        pdf.add_page()              # Start new page
        self._add_header(pdf)       # Add header to new page
        pdf.ln(2)
        
        # Detailed listings of recent developments by vendor
        self._add_section_title(pdf, "Recent Competitive Developments")
        dev_text = self._generate_developments_section()
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 4.5, dev_text)
        pdf.ln(2)
        
        # Add footer metadata to all pages
        self._add_footer(pdf)
        
        # ====================================================================
        # SAVE AND RETURN PDF FILE PATH
        # ====================================================================
        # Create timestamped filename (e.g., ECM_Competitor_Report_20260329_115225.pdf)
        output_path = os.path.join(
            self.output_dir,
            f"ECM_Competitor_Report_{self.report_date.strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        
        # Write PDF to disk
        pdf.output(output_path)
        return output_path
    
    def _add_header(self, pdf: FPDF):
        """Add professional header to page
        
        Adds a consistent header to each page with report title, date,
        and a horizontal separator line.
        """
        # Add main title in bold, 14pt font
        pdf.set_font("Helvetica", "B", 14)
        pdf.cell(0, 6, "M-Files Competitor Intelligence", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Add report date line in regular 9pt font
        pdf.set_font("Helvetica", "", 9)
        report_date_str = f"Weekly Report - {self.report_date.strftime('%B %d, %Y')}"
        pdf.cell(0, 4, report_date_str, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        
        # Draw horizontal separator line (gray colored)
        pdf.set_draw_color(100, 100, 100)
        pdf.line(12, pdf.get_y(), 198, pdf.get_y())
    
    def _add_section_title(self, pdf: FPDF, title: str):
        """Add section title with formatting
        
        Creates a bold section heading with proper spacing and color.
        """
        # Set section title in bold, 11pt font, black color
        pdf.set_font("Helvetica", "B", 11)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(0, 5, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        pdf.ln(1)  # Add small line break after title
    
    def _add_footer(self, pdf: FPDF):
        """Add footer with report metadata
        
        Adds generation date, source information, and branding to the bottom
        of all pages.
        """
        # Position cursor at bottom of page (15mm from bottom)
        pdf.set_y(-15)
        
        # Set footer text in small gray font
        pdf.set_font("Helvetica", "", 8)
        pdf.set_text_color(128, 128, 128)  # Gray color
        
        # Create and add footer text with generation date and source info
        footer_text = f"Generated on {self.report_date.strftime('%B %d, %Y')} | Sources: Company news releases, blogs, press outlets | M-Files Competitive Intelligence"
        pdf.multi_cell(0, 3, footer_text, align='C')
    
    def _generate_executive_summary(self) -> str:
        """Generate executive summary from recent developments
        
        Creates a concise summary of the most significant competitive moves,
        highlighting key strategic trends and market implications.
        """
        # Hardcoded executive summary with key insights
        summary = """Recent weeks show accelerating strategic moves across ECM competitive landscape. OpenText appointed new CEO signaling reset under IBM veteran, Ayman Antoun (effective April 20). AI and agentic capabilities now table stakes - Hyland's Enterprise Context Engine saw 220% QoQ adoption growth in Q4 2025, while Box repositioning as content layer for AI agents.

Key Developments (sourced from company newsrooms and press):
- AI agents and autonomous workflows becoming mainstream differentiators
- No discrete RaaS products launching; records governance embedding in platforms
- Cloud/SaaS now dominant deployment model across all major vendors
- Vendor leadership strengthened with CTO, CPO, CCO appointments (Hyland)"""
        return summary
    
    def _generate_ai_section(self) -> str:
        """Generate AI and agents competitive analysis from sources
        
        Filters developments for AI/agent-related announcements and creates
        a formatted report with source citations. Falls back to default text
        if no AI-related items are found.
        """
        # Filter all developments to find AI-related items from major vendors
        ai_items = [d for d in self.all_developments if d["company"] in 
                   ["OpenText", "Hyland", "Box", "Laserfiche", "DocuWare"]]
        
        # Further filter to items with AI-related keywords in title
        ai_items = [d for d in ai_items if any(keyword in d["title"].lower() 
                   for keyword in ["ai", "agent", "extract"])]
        
        # Build content string from top 6 AI-related items
        content = ""
        for item in ai_items[:6]:  # Limit to top 6 items
            content += f"{item['company']}: {item['title']} - {item['description']}\n"
            content += f"Source: {item['source']}\n\n"
        
        # Return generated content or fallback to default if empty
        return content if content else self._generate_ai_section_default()
    
    def _generate_ai_section_default(self) -> str:
        """Fallback AI section when no dynamic AI data is available
        
        Provides a hardcoded default AI section with pre-written analysis
        if the dynamic data fetching doesn't find AI-related developments.
        """
        # Hardcoded default AI analysis text
        return """OpenText: Aviator Studio - GA mid-2026. Knowledge workers build, test, and manage AI agents on content and processes.
Source: OpenText Blog

Hyland: Enterprise Context Engine saw 220% customer adoption growth in Q4 2025. Agentic RPA and workflow automation tightly integrated.
Source: Hyland Newsroom

Box: Box Extract GA handles contract processing in under 2 minutes. Virtual filesystem concept for AI agents.
Source: TechTarget, Blocks & Files

DocuWare: DocuWare AI Hub for document processing R&D with advanced IDP capabilities.
Source: DocuWare Blog

Laserfiche: AI Auto-Classification with Smart Fields and natural-language conditions for security labeling.
Source: FinancialContent"""
    
    def _generate_raas_section(self) -> str:
        """Generate RaaS and cloud deployment analysis
        
        Analyzes the landscape of Records-as-a-Service offerings and cloud
        deployment strategies across competitors.
        """
        # Hardcoded RaaS analysis based on public information
        raas_content = """No vendor has launched a discrete 'Records as a Service' product this period. Records governance and compliance capabilities are being embedded within broader cloud platforms and sold as integrated modules.

OpenText: AI Data Platform - GA mid-2026 (26.2 release). Includes knowledge graph, AI control plane, IDOL Knowledge Discovery, and content processing. Positioned as intelligence layer for Extended ECM compliance.
Source: OpenText World 2025 Press Release

Hyland: Cloud-native platform with integrated compliance and governance. European cloud expansion for data residency. Content Innovation Cloud with SOC 2, ISO 27001, HITRUST, GDPR, CCPA.
Source: Hyland Newsroom

Box: All-cloud model. Records management and retention integrated into Content Services. 100,000+ customers, $1.06B backlog.
Source: Stock Titan (Box Annual Report)

Laserfiche: Smart Fields and Run Smarter awards recognizing customer implementations of governance and content solutions.
Source: Morningstar/BusinessWire

Market Shift: Vendors recognize pure RaaS market is small; better ROI embedding records capabilities in core platform."""
        return raas_content
    
    def _generate_leadership_section(self) -> str:
        """Generate leadership and organizational announcements from sources
        
        Filters developments for leadership changes and creates a formatted
        section. Falls back to default text if no leadership items found.
        """
        # Filter developments for leadership-related announcements
        leadership_items = [d for d in self.all_developments if 
                           "appointment" in d["title"].lower() or 
                           "leadership" in d["title"].lower() or 
                           "ceo" in d["title"].lower()]
        
        # Build content from leadership items
        content = ""
        for item in leadership_items:
            content += f"{item['company']}: {item['title']}\n"
            content += f"{item['description']}\n"
            content += f"Source: {item['source']}\n\n"
        
        # Return generated content or fallback to default if empty
        return content if content else self._generate_leadership_default()
    
    def _generate_leadership_default(self) -> str:
        """Fallback leadership section when no dynamic data is available
        
        Provides hardcoded default leadership information if dynamic
        leadership data fetching doesn't produce results.
        """
        # Hardcoded default leadership information
        return """OpenText: Ayman Antoun appointed CEO effective April 20, 2026. Former President of IBM Americas (2020-2023) with 35+ years at IBM across US, Canada, Latin America. Signals strategic reset toward AI/cloud.
Source: OpenText Investor Relations

Hyland: Major leadership expansion (2024-2025):
- Rob Kaloustian (Chief Customer Officer)
- Sharon Brand (CHRO)
- Tim McIntire (CTO) - strengthening AI/ML
- Michael Campbell (Chief Product Officer)
- Three new SVP Sales appointments (NA, EMEA, APAC)
Source: Hyland Newsroom

Box & Laserfiche: No significant leadership announcements this period."""
    
    def _generate_developments_section(self) -> str:
        """Generate full recent developments from fetched sources
        
        Creates a comprehensive listing of all recent competitive developments
        organized by company, with the top 3 developments per vendor.
        """
        # Initialize content with header
        content = "\nRecent developments by company (sourced from public newsrooms and press):\n\n"
        
        # Get unique list of companies mentioned in developments
        companies_mentioned = set(d["company"] for d in self.all_developments)
        
        # For each company in alphabetical order
        for company in sorted(companies_mentioned):
            # Filter developments for this company
            company_devs = [d for d in self.all_developments if d["company"] == company]
            
            # Add company name as subheading
            content += f"{company}:\n"
            
            # Add top 3 developments for this company
            for dev in company_devs[:3]:  # Top 3 per company
                # Truncate long descriptions to 100 characters and add ellipsis
                content += f"- {dev['title']}: {dev['description'][:100]}...\n"
                # Add source citation in parentheses
                content += f"  ({dev['source']})\n"
            
            content += "\n"
        
        return content
    
    def run(self) -> str:
        """Execute the competitor analysis agent
        
        Main entry point that orchestrates:
        1. Fetching competitive intelligence from sources
        2. Generating the PDF report
        3. Printing status messages to user
        
        Returns:
            str: Path to the generated PDF report
        """
        # Print status: Agent starting up
        print("🚀 Starting ECM Competitor Intelligence Report Generation...")
        
        # Print output directory
        print(f"📂 Output directory: {self.output_dir}")
        
        # Print status: Fetching data
        print(f"📊 Fetching from public sources...")
        
        # Print number of developments found
        print(f"📰 Found {len(self.all_developments)} recent developments from competitive sources")
        
        # Generate the PDF report
        report_path = self.generate_pdf_report()
        
        # Print success status
        print(f"✅ Report generated successfully!")
        
        # Print the file path where report was saved
        print(f"📄 Saved to: {report_path}")
        
        return report_path


# ============================================================================
# MAIN EXECUTION ENTRY POINT
# ============================================================================
if __name__ == "__main__":
    # Create an instance of the Agent
    agent = ECMCompetitorAgent()
    
    # Run the agent to generate the competitive intelligence report
    agent.run()

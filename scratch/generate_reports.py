import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

# Ensure matplotlib runs in headless mode
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# ==========================================
# XML STYLING HELPER FUNCTIONS
# ==========================================

def set_cell_background(cell, hex_color):
    """Sets the background color of a cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    """Sets cell padding (in twentieths of a point, dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_horizontal_borders_only(table, color="CBD5E1"):
    """Applies horizontal borders and removes vertical borders for a clean look."""
    tblPr = table._tbl.tblPr
    tblBorders = OxmlElement('w:tblBorders')
    for bdr_name in ['top', 'bottom', 'insideH']:
        border = OxmlElement(f'w:{bdr_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '6') # 3/4 pt
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), color)
        tblBorders.append(border)
    for bdr_name in ['left', 'right', 'insideV']:
        border = OxmlElement(f'w:{bdr_name}')
        border.set(qn('w:val'), 'none')
        tblBorders.append(border)
    tblPr.append(tblBorders)

def add_p_border_bottom(paragraph, hex_color="0284C7", sz="8", space="4"):
    """Adds a nice thick bottom border under headings."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), sz)
    bottom.set(qn('w:space'), space)
    bottom.set(qn('w:color'), hex_color)
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_hyperlink(paragraph, url, text, color="0284C7", underline=True):
    """Adds a clickable hyperlink with blue text color and underline."""
    part = paragraph.part
    # OpenXML relationship for hyperlink
    HYPERLINK_RELATION = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink"
    r_id = part.relate_to(url, HYPERLINK_RELATION, is_external=True)
    
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    if color:
        c = OxmlElement('w:color')
        c.set(qn('w:val'), color)
        rPr.append(c)
    if underline:
        u = OxmlElement('w:u')
        u.set(qn('w:val'), 'single')
        rPr.append(u)
    new_run.append(rPr)
    
    text_node = OxmlElement('w:t')
    text_node.text = text
    new_run.append(text_node)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)
    return hyperlink

# ==========================================
# TYPOGRAPHY HELPER FUNCTIONS
# ==========================================

def apply_text_style(run, name="Segoe UI", size_pt=10.5, color_rgb=(51, 65, 85), bold=False, italic=False):
    """Applies specific font settings to a text run."""
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.font.color.rgb = RGBColor(*color_rgb)
    run.bold = bold
    run.italic = italic

def setup_document_styles(doc):
    """Applies global style settings to the document."""
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Segoe UI'
    font.size = Pt(10.5)
    font.color.rgb = RGBColor(51, 65, 85) # Slate 700

def add_heading_1(doc, text):
    """Adds a primary Heading with blue bottom border line."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(20)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    apply_text_style(run, name="Segoe UI", size_pt=14, color_rgb=(15, 23, 42), bold=True)
    add_p_border_bottom(p, hex_color="0EA5E9", sz="12", space="6")
    return p

def add_heading_2(doc, text):
    """Adds a sub-heading."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    apply_text_style(run, name="Segoe UI", size_pt=12, color_rgb=(2, 132, 199), bold=True)
    return p

def add_bullet_item(doc, bold_prefix, text_body):
    """Adds a bullet list item with a bold leading term."""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        run_bold = p.add_run(bold_prefix)
        apply_text_style(run_bold, name="Segoe UI", size_pt=10.5, color_rgb=(15, 23, 42), bold=True)
    run_body = p.add_run(text_body)
    apply_text_style(run_body, name="Segoe UI", size_pt=10.5, color_rgb=(51, 65, 85))
    return p

def add_callout(doc, text, title=""):
    """Adds a beautiful shaded callout box with a thick left border."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC") # Slate 50
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # Custom border XML: thick left border, no others
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24') # 3pt
    left.set(qn('w:color'), '0EA5E9') # Cyan
    tcBorders.append(left)
    
    for bdr_name in ['top', 'bottom', 'right']:
        border = OxmlElement(f'w:{bdr_name}')
        border.set(qn('w:val'), 'none')
        tcBorders.append(border)
    tcPr.append(tcBorders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    
    if title:
        run_title = p.add_run(title + "\n")
        apply_text_style(run_title, name="Segoe UI", size_pt=10.5, color_rgb=(15, 23, 42), bold=True)
        
    run_body = p.add_run(text)
    apply_text_style(run_body, name="Segoe UI", size_pt=10, color_rgb=(71, 85, 105), italic=True)

# ==========================================
# DIAGRAM GENERATION
# ==========================================

def generate_auth_flow_diagram(output_path):
    """Generates a high-quality authentication flow diagram using matplotlib."""
    fig, ax = plt.subplots(figsize=(9.0, 1.8), dpi=300)
    ax.axis('off')
    
    steps = [
        "User\n(Client View)",
        "Login Form\n(Credentials Input)",
        "Laravel API\n(Validation & DB Check)",
        "JWT / Session Token\n(Issued & Cached)",
        "Dashboard\n(Role-Based View)"
    ]
    
    fc_color = "#F8FAFC"
    ec_color = "#0284C7"
    text_color = "#0F172A"
    
    bbox_props = dict(boxstyle="round,pad=0.5", fc=fc_color, ec=ec_color, lw=2.0)
    
    for i, step in enumerate(steps):
        x = i * 2.3
        y = 0.5
        ax.text(x, y, step, ha='center', va='center', fontsize=7.5, fontweight='bold', color=text_color, bbox=bbox_props, fontname='sans-serif')
        
        if i < len(steps) - 1:
            ax.annotate('', xy=(x + 1.45, y), xytext=(x + 0.85, y),
                        arrowprops=dict(arrowstyle="-|>", color=ec_color, lw=2.0, mutation_scale=10))
            
    ax.set_xlim(-0.8, len(steps) * 2.3 - 1.5)
    ax.set_ylim(0.1, 0.9)
    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', transparent=True)
    plt.close()
    print("Authentication flow diagram generated.")

# ==========================================
# METADATA & TABLE STYLING CORES
# ==========================================

def add_header_block(doc, title, subtitle):
    """Adds a styled title header block to start the document."""
    # Top border element
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run(title)
    apply_text_style(run_title, name="Segoe UI", size_pt=20, color_rgb=(15, 23, 42), bold=True)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    run_sub = p_sub.add_run(subtitle)
    apply_text_style(run_sub, name="Segoe UI", size_pt=12, color_rgb=(2, 132, 199), italic=True)
    add_p_border_bottom(p_sub, hex_color="0F172A", sz="18", space="6")

def add_meta_tables(doc):
    """Adds Course and Team Information tables with professional styling."""
    add_heading_2(doc, "Course Information")
    course_table = doc.add_table(rows=5, cols=2)
    course_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    course_table.autofit = False
    
    course_data = [
        ("Course Code", "CSE 4204"),
        ("Course Title", "Mobile Computing Lab"),
        ("Assignment", "Week 07 – Frontend Development & API Integration"),
        ("Team ID", "CSE4204-8C-T07"),
        ("Section", "8C")
    ]
    
    widths = [Inches(2.0), Inches(4.5)]
    for i, (k, v) in enumerate(course_data):
        row = course_table.rows[i]
        
        cell_k = row.cells[0]
        cell_k.width = widths[0]
        p_k = cell_k.paragraphs[0]
        p_k.paragraph_format.space_after = Pt(0)
        run_k = p_k.add_run(k)
        apply_text_style(run_k, name="Segoe UI", size_pt=10, color_rgb=(15, 23, 42), bold=True)
        set_cell_margins(cell_k, top=100, bottom=100, left=120, right=120)
        set_cell_background(cell_k, "F8FAFC")
        
        cell_v = row.cells[1]
        cell_v.width = widths[1]
        p_v = cell_v.paragraphs[0]
        p_v.paragraph_format.space_after = Pt(0)
        run_v = p_v.add_run(v)
        apply_text_style(run_v, name="Segoe UI", size_pt=10, color_rgb=(51, 65, 85))
        set_cell_margins(cell_v, top=100, bottom=100, left=120, right=120)
        
    set_table_horizontal_borders_only(course_table)
    
    # Team Info Table
    add_heading_2(doc, "Team Members")
    team_table = doc.add_table(rows=4, cols=3)
    team_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    team_table.autofit = False
    
    team_data = [
        ("Name", "Student ID", "Role"),
        ("MD Robayet Hassan Rupom", "11220320979", "Frontend Developer & Team Leader"),
        ("Bushra Monzur Moumi", "11220321048", "AI Integration Lead"),
        ("Aqib Jawwad Nahin", "11220320969", "Backend Developer & Database Manager")
    ]
    
    t_widths = [Inches(2.5), Inches(1.5), Inches(2.5)]
    for r_idx, row_data in enumerate(team_data):
        row = team_table.rows[r_idx]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = t_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if r_idx == 0:
                apply_text_style(run, name="Segoe UI", size_pt=10, color_rgb=(255, 255, 255), bold=True)
                set_cell_background(cell, "0F172A") # Dark Header
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                apply_text_style(run, name="Segoe UI", size_pt=10, color_rgb=(51, 65, 85))
                if r_idx % 2 == 1:
                    set_cell_background(cell, "F8FAFC")
                    
    set_table_horizontal_borders_only(team_table)
    
    # GitHub Repo section
    p_git = doc.add_paragraph()
    p_git.paragraph_format.space_before = Pt(12)
    run_git_label = p_git.add_run("GitHub Repository: ")
    apply_text_style(run_git_label, name="Segoe UI", size_pt=10, color_rgb=(15, 23, 42), bold=True)
    add_hyperlink(p_git, "https://github.com/Rupom090/CSE4204-8C-T07-Humanova", "https://github.com/Rupom090/CSE4204-8C-T07-Humanova")

# ==========================================
# DOCUMENT 1: PROGRESS REPORT GENERATOR
# ==========================================

def generate_progress_report(output_path, auth_diagram_path):
    """Generates the Frontend Progress Report Word Document."""
    doc = Document()
    setup_document_styles(doc)
    
    add_header_block(doc, "Frontend Progress Report", "Humanova: AI Hallucination Detection & Verification System")
    add_meta_tables(doc)
    
    # 1. Project Overview
    add_heading_1(doc, "1. Project Overview")
    p_overview = doc.add_paragraph()
    p_overview.paragraph_format.line_spacing = 1.15
    p_overview.paragraph_format.space_after = Pt(8)
    p_overview.add_run("Humanova is a state-of-the-art, web-based AI Hallucination Detection and Verification System designed to address the critical issue of reliability in AI outputs. The application is built to evaluate large language model (LLM) responses, perform multi-source facts verification, check cross-references and citations, evaluate semantic confidence levels, and generate structured validation reports. This report highlights the frontend development and API integration milestones achieved in Week 07, creating a seamless connection between our Laravel back-end microservices and the Vite-React single-page application (SPA).")
    
    # 2. Frontend Technology Stack
    add_heading_1(doc, "2. Frontend Technology Stack")
    add_heading_2(doc, "Core Framework & Build Tooling")
    add_bullet_item(doc, "React.js: ", "Selected for its declarative components and virtual DOM, facilitating rapid, modular user interface updates.")
    add_bullet_item(doc, "TypeScript: ", "Ensures strict typing, interfaces, and early compile-time bug detection across the entire component tree.")
    add_bullet_item(doc, "Vite: ", "Serves as the high-speed build server and bundler, delivering near-instant Hot Module Replacement (HMR).")
    
    add_heading_2(doc, "Styling & UI Architecture")
    add_bullet_item(doc, "Tailwind CSS: ", "Utilized for utility-first CSS layouts, guaranteeing clean styling, fast styling iteration, and responsive utilities.")
    add_bullet_item(doc, "CSS Modules: ", "Used for encapsulating component-specific style properties to prevent class collision.")
    add_bullet_item(doc, "Lucide React: ", "Integrated for a clean, cohesive set of customizable SVG vector icons.")
    add_bullet_item(doc, "Framer Motion: ", "Employed for fluid interface micro-interactions, page-level transitions, and interactive visual indicators.")
    
    add_heading_2(doc, "State Management & Data Control")
    add_bullet_item(doc, "Zustand: ", "A lightweight, robust state manager representing the single source of truth for global authentication sessions, user settings, and theme configurations.")
    add_bullet_item(doc, "Context API: ", "Used for secondary layout configurations, sidebar toggle states, and localized toast alerts.")
    add_bullet_item(doc, "React Router: ", "Configured for client-side routing, query-params parsing, and managing protective routing middleware.")
    
    add_heading_2(doc, "API Integration & Form Management")
    add_bullet_item(doc, "Axios: ", "Integrated as the primary HTTP client, configured with custom interceptors for attaching bearer tokens and intercepting global API errors.")
    add_bullet_item(doc, "React Hook Form: ", "Optimizes forms by reducing unnecessary component re-renders while registering input fields.")
    add_bullet_item(doc, "Zod: ", "Enforces strict runtime type validation and schema validations on input fields before triggering API submissions.")
    add_bullet_item(doc, "Recharts: ", "Provides interactive charts (area, pie, and bar charts) for system logs and verification dashboards.")

    # 3. Frontend Project Structure
    doc.add_page_break()
    add_heading_1(doc, "3. Frontend Project Structure")
    p_structure_desc = doc.add_paragraph()
    p_structure_desc.add_run("The frontend codebase follows a clean, modular structure optimized for scalability, feature segregation, and separation of concerns:")
    
    # Directory structure block in a callout/code style box
    dir_tree = (
        "frontend/\n"
        "├── public/\n"
        "├── src/\n"
        "│   ├── assets/            # Static media (logos, default graphics)\n"
        "│   ├── components/        # Reusable global UI widgets & shells\n"
        "│   │   ├── layouts/       # Dashboard shell and app structures\n"
        "│   │   └── ui/            # Form elements, buttons, loaders\n"
        "│   ├── app/               # Core application routing config\n"
        "│   │   └── Router.tsx     # Route definitions and guard logic\n"
        "│   ├── pages/             # View components mapped to routing paths\n"
        "│   │   ├── auth/          # Login and registration templates\n"
        "│   │   ├── dashboard/     # Statistics and summary charts\n"
        "│   │   ├── ai-studio/     # AI studio and prompt assistant\n"
        "│   │   ├── verification/  # Text and citation validation controls\n"
        "│   │   ├── analytics/     # Analytics and detailed reporting metrics\n"
        "│   │   ├── community/     # Shared verification history and forum\n"
        "│   │   ├── reports/       # Report history and PDF download views\n"
        "│   │   ├── settings/      # Account and organization parameters\n"
        "│   │   └── Home.tsx       # Landing page wrapper\n"
        "│   ├── services/          # API calling layers (Axios endpoints mapping)\n"
        "│   ├── hooks/             # Custom utility hooks (query wrappers)\n"
        "│   ├── stores/            # Zustand global stores (session states)\n"
        "│   │   └── authStore.ts   # User state context & localStorage sync\n"
        "│   ├── types/             # Shared TypeScript models and interfaces\n"
        "│   ├── utils/             # Local validators, data formatters\n"
        "│   └── App.tsx            # Main App React entry point\n"
        "├── package.json           # Scripts and dependency registry\n"
        "└── vite.config.ts         # Bundler and alias mappings config"
    )
    add_callout(doc, dir_tree, title="Directory Tree Structure (modular architecture)")

    # 4. Completed Pages
    add_heading_1(doc, "4. Completed Pages")
    p_pages_desc = doc.add_paragraph()
    p_pages_desc.add_run("The following table lists the core pages that have been developed and styled according to the approved UI/UX designs:")
    
    pages_table = doc.add_table(rows=14, cols=3)
    pages_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    pages_table.autofit = False
    
    pages_headers = ["Page Name", "Status", "Description & Components Included"]
    p_widths = [Inches(2.0), Inches(1.0), Inches(3.5)]
    
    # Headers
    for c_idx, text in enumerate(pages_headers):
        cell = pages_table.rows[0].cells[c_idx]
        cell.width = p_widths[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        apply_text_style(run, name="Segoe UI", size_pt=10, color_rgb=(255, 255, 255), bold=True)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        
    pages_rows = [
        ("Landing Page", "✅ Completed", "Hero section, service core values, call-to-actions, visual benefits grid, footer."),
        ("Login Page", "✅ Completed", "Secure credentials form, error boundaries, loading locks, navigation links."),
        ("Registration Page", "✅ Completed", "Extended fields validator, onboarding steps integration, backend register sync."),
        ("Dashboard", "✅ Completed", "Verification logs, quick stats layout, active scanners list, sidebar shell integration."),
        ("User Profile Page", "✅ Completed", "Account settings, password modifier, avatar upload interface, session viewer."),
        ("AI Verification Page", "✅ Completed", "Fact evaluation input, confidence scoring logs, claims highlighter."),
        ("Prompt Studio Page", "✅ Completed", "System prompts optimizer, side-by-side enhanced text compare, copying triggers."),
        ("Analytics Dashboard", "✅ Completed", "Recharts charts (line, bar, pie), scanner frequency trends, evaluation rates."),
        ("Community Page", "✅ Completed", "Report explorer feed, voting widgets, user-led validation forums."),
        ("Reports Page", "✅ Completed", "Report history logs, filters, search bar, download-to-PDF triggers."),
        ("Org Management", "✅ Completed", "Organization information editor, team members invite form, roles assign tables."),
        ("Settings Page", "✅ Completed", "General configuration inputs, API keys generator, developer settings tab."),
        ("Admin Dashboard", "✅ Completed", "Admin panels, active users stats, API endpoints load gauges, logs auditor.")
    ]
    
    for r_idx, (name, status, desc) in enumerate(pages_rows, start=1):
        row = pages_table.rows[r_idx]
        data = [name, status, desc]
        for c_idx, val in enumerate(data):
            cell = row.cells[c_idx]
            cell.width = p_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            apply_text_style(run, name="Segoe UI", size_pt=9.5, color_rgb=(51, 65, 85))
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            
            # Shading
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            if c_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
    set_table_horizontal_borders_only(pages_table)

    # 5. Backend APIs Integrated
    add_heading_1(doc, "5. Backend APIs Integrated")
    p_apis_desc = doc.add_paragraph()
    p_apis_desc.add_run("To replace temporary frontend mockups with live data, the application successfully integrates with the Laravel backend API. The following REST routes are mapped:")
    add_bullet_item(doc, "User Authentication & Session: ", "Supports Login, Register, Logout, and Token refreshing routes, maintaining user cookies.")
    add_bullet_item(doc, "User Profile & Security: ", "Fetches profile models, updates name and email fields, and resets passwords.")
    add_bullet_item(doc, "Organization & Member management: ", "Permits creating organizations, listing members, sending invites, and changing roles.")
    add_bullet_item(doc, "AI verification Pipeline: ", "Submits validation forms, polls execution tasks, retrieves facts checks, and saves results.")
    add_bullet_item(doc, "Prompt Enhancement: ", "Submits unoptimized prompts to AI models, retrieving revised, optimized versions.")
    add_bullet_item(doc, "Dashboard & Global Analytics: ", "Retrieves summaries, chart logs, audit reports, and active scanners data.")
    add_bullet_item(doc, "Report Archiver: ", "Queries verification database logs, handles filter requests, and handles PDF export files.")

    # 6. Authentication Flow
    doc.add_page_break()
    add_heading_1(doc, "6. Authentication Flow")
    p_auth_desc = doc.add_paragraph()
    p_auth_desc.add_run("Security routes are protected using client-side middleware. Here is how the authentication lifecycle is structured:")
    add_bullet_item(doc, "1. Credentials Entry: ", "The user enters their details on the Login view. React Hook Form validates the input format, and Zod prevents submission if inputs are invalid.")
    add_bullet_item(doc, "2. Request Transmission: ", "Axios sends a POST request with payload credentials to the Laravel API server.")
    add_bullet_item(doc, "3. Token Dispatch: ", "Upon authentication, the backend generates and returns a secure JWT (JSON Web Token) with user metadata.")
    add_bullet_item(doc, "4. State Cache & Authorization: ", "The frontend stores the JWT in the Zustand state store and synchronization storage (localStorage). It sets the Axios Authorization header default to include the bearer token.")
    add_bullet_item(doc, "5. Navigation: ", "The application updates route states, allowing access to protected dashboard views.")
    
    # Diagram container
    add_heading_2(doc, "Authentication Flow Diagram")
    if os.path.exists(auth_diagram_path):
        # Insert in a centered paragraph
        p_dia = doc.add_paragraph()
        p_dia.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_dia.paragraph_format.space_before = Pt(8)
        p_dia.paragraph_format.space_after = Pt(4)
        run_dia = p_dia.add_run()
        run_dia.add_picture(auth_diagram_path, width=Inches(6.2))
        
        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run_cap = p_caption.add_run("Figure 6.1: Step-by-Step JWT Authentication and Routing Authorization Flow")
        apply_text_style(run_cap, name="Segoe UI", size_pt=9, color_rgb=(100, 116, 139), italic=True)
    else:
        p_dia = doc.add_paragraph()
        p_dia.add_run("[Diagram Auth Flow Image Not Found - Skipped]")
        apply_text_style(p_dia.runs[0], color_rgb=(220, 38, 38))

    # 7. API Integration Summary
    add_heading_1(doc, "7. API Integration Summary")
    p_api_summary = doc.add_paragraph()
    p_api_summary.add_run("All UI content is fetched dynamically from Laravel controllers rather than hardcoded mock variables. To prevent page stalling during API queries, the frontend utilizes:")
    add_bullet_item(doc, "Axios Interceptors: ", "Automatically attach Bearer tokens to all outgoing requests and process 401 Unauthorized codes by routing users to the login screen.")
    add_bullet_item(doc, "Status Indicators: ", "Utilize status properties in state management to trigger skeletons and loading animation spinners, maintaining visual continuity during fetches.")
    add_bullet_item(doc, "Global Error Toast Alerts: ", "Alerts are automatically triggered to show user-friendly messages for network errors or server failures.")

    # 8. Form Validation
    add_heading_1(doc, "8. Form Validation")
    p_val_desc = doc.add_paragraph()
    p_val_desc.add_run("Form fields validate inputs locally before submitting requests to the backend API:")
    add_bullet_item(doc, "Email Validation: ", "Checks formatting (e.g., matching standard user@domain.com regex) and marks empty fields.")
    add_bullet_item(doc, "Password Constraints: ", "Requires a minimum of 8 characters, containing uppercase characters, lowercase characters, numeric digits, and special symbols.")
    add_bullet_item(doc, "Required Parameters: ", "Marks mandatory parameters with a red asterisk and disables submit triggers until criteria are met.")
    add_bullet_item(doc, "Error Indicators: ", "Displays real-time validation error alerts below each input field for instant visual feedback.")

    # 9. Responsive Design
    add_heading_1(doc, "9. Responsive Design")
    p_resp = doc.add_paragraph()
    p_resp.add_run("To ensure readability across all screen sizes, the application leverages Tailwind's mobile-first responsive utility break points:")
    add_bullet_item(doc, "Flexible Grid Layouts: ", "Main panels scale dynamically between 1 column (mobile devices), 2 columns (tablets), and 3-4 columns (desktop resolutions).")
    add_bullet_item(doc, "Navigation Shells: ", "Switches the desktop side panel to an overlay drawer on mobile viewports, triggered via a header menu button.")
    add_bullet_item(doc, "Adaptive Card Elements: ", "Compresses cards and lists into vertical formats on screens below 768px wide.")

    # 10. User Experience Improvements
    add_heading_1(doc, "10. User Experience Improvements")
    p_ux = doc.add_paragraph()
    p_ux.add_run("The application includes visual design enhancements to improve overall user interaction:")
    add_bullet_item(doc, "Skeleton Loading Layouts: ", "Displays mock card wireframes and text lines during data fetches, preventing layout shifts.")
    add_bullet_item(doc, "Operation Feeback: ", "Triggers sliding notifications (toasts) to confirm operations like 'Report Generated' or 'Password Updated'.")
    add_bullet_item(doc, "Modal Overlays: ", "Uses frosted glass overlay sheets to prompt confirmation for critical actions, such as removing members or logging out.")

    # 11. Current Development Progress
    doc.add_page_break()
    add_heading_1(doc, "11. Current Development Progress")
    p_progress_desc = doc.add_paragraph()
    p_progress_desc.add_run("The current state of development for the frontend features is summarized below:")
    
    prog_table = doc.add_table(rows=11, cols=3)
    prog_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    prog_table.autofit = False
    
    prog_widths = [Inches(2.5), Inches(1.5), Inches(2.5)]
    prog_headers = ["Feature Area", "Progress State", "Integration Status"]
    
    for c_idx, text in enumerate(prog_headers):
        cell = prog_table.rows[0].cells[c_idx]
        cell.width = prog_widths[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        apply_text_style(run, name="Segoe UI", size_pt=10, color_rgb=(255, 255, 255), bold=True)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        
    prog_rows = [
        ("Frontend UI & Styles", "✅ Completed", "All pages match design models."),
        ("Responsive Layouts", "✅ Completed", "Tested on mobile, tablet, and desktop."),
        ("Authentication Engine", "✅ Completed", "Zustand auth and route guards configured."),
        ("API Communication Layer", "✅ Completed", "Axios client endpoints and interceptors active."),
        ("Dashboard Statistics", "✅ Completed", "Dynamic charts pulling data from DB."),
        ("User profile Controls", "✅ Completed", "Forms and API integrations functional."),
        ("Verification Module UI", "✅ Completed", "Fact-checking interface completed."),
        ("Analytics Interface", "✅ Completed", "Interactive charts pulling live metrics."),
        ("Reports Archiver UI", "✅ Completed", "Search, filters, and PDF export setup."),
        ("Admin Control Panel", "✅ Completed", "Tenant, system, and logs panels ready.")
    ]
    
    for r_idx, (area, state, status) in enumerate(prog_rows, start=1):
        row = prog_table.rows[r_idx]
        data = [area, state, status]
        for c_idx, val in enumerate(data):
            cell = row.cells[c_idx]
            cell.width = prog_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            apply_text_style(run, name="Segoe UI", size_pt=9.5, color_rgb=(51, 65, 85))
            set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
            if c_idx == 1:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                
    set_table_horizontal_borders_only(prog_table)

    # 12. GitHub Repository Activity
    add_heading_1(doc, "12. GitHub Repository Activity")
    p_git_activity = doc.add_paragraph()
    p_git_activity.add_run("Version control practices are maintained to coordinate code integrations:")
    add_bullet_item(doc, "Frequent Commit Blocks: ", "Developers push daily branches, avoiding large, monolithic merges.")
    add_bullet_item(doc, "Meaningful Commit Messages: ", "Commits document precise features (e.g., 'feat: connect authentication API' or 'fix: resolve hover animation').")
    add_bullet_item(doc, "Standard Repository Layout: ", "Files are structured into frontend, backend, and documentation directories.")

    # 13. Challenges Faced
    add_heading_1(doc, "13. Challenges Faced")
    p_challenges = doc.add_paragraph()
    p_challenges.add_run("During development, several key technical challenges were identified and addressed:")
    add_bullet_item(doc, "API Integration: ", "Addressed authentication state resets on refresh by caching tokens in localStorage and syncing them during initialization.")
    add_bullet_item(doc, "Layout Responsiveness: ", "Optimized large tables and complex charts for mobile viewports using touch-scroll container classes.")
    add_bullet_item(doc, "Cross-Origin Requests (CORS): ", "Configured the Laravel API CORS settings to allow local frontend ports during development.")

    # 14. Future Work
    add_heading_1(doc, "14. Future Work")
    p_future = doc.add_paragraph()
    p_future.add_run("Planned enhancements to refine the platform include:")
    add_bullet_item(doc, "Performance Tuning: ", "Splitting large code blocks using React Lazy Suspense imports to minimize the initial load package size.")
    add_bullet_item(doc, "Real-time Verification Status: ", "Transitioning from polling requests to WebSockets (Laravel Echo) for instant fact-checking updates.")
    add_bullet_item(doc, "Service Workers: ", "Adding offline support (PWA) to allow viewing saved verification reports without network access.")

    # 15. Conclusion
    add_heading_1(doc, "15. Conclusion")
    p_conclusion = doc.add_paragraph()
    p_conclusion.paragraph_format.line_spacing = 1.15
    p_conclusion.paragraph_format.space_after = Pt(8)
    p_conclusion.add_run("The Humanova frontend interface has been successfully developed, styled, and integrated with the backend services. Security routes are protected, forms are validated using Zod, and data visualization elements display live database values. The project meets all Week 07 milestones, laying a solid foundation for upcoming features.")

    # 16. References
    add_heading_1(doc, "References")
    p_ref = doc.add_paragraph()
    p_ref.add_run("1. React Documentation — ")
    add_hyperlink(p_ref, "https://react.dev", "https://react.dev")
    p_ref.add_run("\n2. Tailwind CSS Reference Guide — ")
    add_hyperlink(p_ref, "https://tailwindcss.com/docs", "https://tailwindcss.com/docs")
    p_ref.add_run("\n3. Axios API Guide — ")
    add_hyperlink(p_ref, "https://axios-http.com", "https://axios-http.com")
    p_ref.add_run("\n4. React Router Documentation — ")
    add_hyperlink(p_ref, "https://reactrouter.com", "https://reactrouter.com")
    
    # Save document
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    doc.save(output_path)
    print(f"Progress Report saved to {output_path}")

# ==========================================
# DOCUMENT 2: SCREENSHOT REPORT GENERATOR
# ==========================================

def generate_screenshot_report(output_path, screens_dir):
    """Generates the User Interface Screenshots Report Word Document."""
    doc = Document()
    setup_document_styles(doc)
    
    add_header_block(doc, "User Interface Screenshots Report", "Humanova: AI Hallucination Detection & Verification System")
    add_meta_tables(doc)
    
    # Introduction
    p_intro = doc.add_paragraph()
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(12)
    p_intro.add_run("This document showcases the user interface screens of the Humanova AI Hallucination Detection & Verification system, demonstrating the visual style, layout structure, and design system implementation. These screenshots verify that the frontend components closely align with the approved UI/UX designs and reflect successful integration with the backend APIs.")
    
    # List of screens to display: (Title, filename, purpose, key components, api endpoints)
    screens_list = [
        {
            "id": "Screenshot 01",
            "title": "Screenshot 01 — Landing / Home Page",
            "filename": "landing-page.png",
            "purpose": "Introduces the Humanova system to public visitors, outlines core fact-checking benefits, and provides navigation to authentication gateways.",
            "components": "Responsive Navigation bar, Hero section with interactive call-to-actions, features grid layout, platform stats counter, and footer links.",
            "apis": "Public content, does not require active session tokens."
        },
        {
            "id": "Screenshot 02",
            "title": "Screenshot 02 — Login Page",
            "filename": "login-page.png",
            "purpose": "Permits registered users to authenticate, verify active accounts, and gain access to protected console features.",
            "components": "Email input validation, password secure field, remember-me checkmark, login trigger button, and navigation triggers for registration or password recovery.",
            "apis": "POST /api/auth/login (JWT authentication endpoints)."
        },
        {
            "id": "Screenshot 03",
            "title": "Screenshot 03 — Registration Page",
            "filename": "register-page.png",
            "purpose": "Enables new users to create accounts on the platform.",
            "components": "Full name validation field, corporate email validation, password strength checker, confirm-password field, and links to terms of service.",
            "apis": "POST /api/auth/register (Account onboarding endpoints)."
        },
        {
            "id": "Screenshot 04",
            "title": "Screenshot 04 — Dashboard",
            "filename": "dashboard.png",
            "purpose": "Serves as the central console for authenticated users, displaying system statistics, recent activity lists, and shortcuts.",
            "components": "Verification counters (totals, flagged, verified), live facts check trends (area charts), navigation sidebar shell, and quick action tiles.",
            "apis": "GET /api/dashboard/stats, GET /api/scans/recent."
        },
        {
            "id": "Screenshot 05",
            "title": "Screenshot 05 — Reports Page",
            "filename": "report-page.png",
            "purpose": "Allows users to explore generated verification documents, filter scan database logs, and trigger file exports.",
            "components": "Reports list, document metadata, search parameters, sorting filters, and PDF export buttons.",
            "apis": "GET /api/reports, GET /api/reports/{id}/export (PDF dispatch routing)."
        },
        {
            "id": "Screenshot 06",
            "title": "Screenshot 06 — User Profile Page",
            "filename": "profile-page.png",
            "purpose": "Allows users to review, edit, and update account details, change passwords, and configure profile parameters.",
            "components": "Personal details fields, password edit section, profile picture uploader, and active sessions tracker.",
            "apis": "GET /api/user/profile, PUT /api/user/profile/update."
        },
        {
            "id": "Screenshot 07",
            "title": "Screenshot 07 — Settings & API Key Management Page",
            "filename": "api-key-page.png",
            "purpose": "Allows developers to generate, copy, and revoke API access keys for integration.",
            "components": "Active keys list table, 'Create New Key' modal trigger, token permissions config, and copy-to-clipboard elements.",
            "apis": "GET /api/settings/keys, POST /api/settings/keys/generate."
        },
        {
            "id": "Screenshot 08",
            "title": "Screenshot 08 — Organization Management Page",
            "filename": "organization-page.png",
            "purpose": "Allows workspace administrators to manage organization profiles, invite users, and update member privileges.",
            "components": "Organization details form, members list table, email invite validator, and member role assignment dropdowns.",
            "apis": "GET /api/org/details, POST /api/org/members/invite, PUT /api/org/members/{id}/role."
        },
        {
            "id": "Screenshot 09",
            "title": "Screenshot 09 — Admin Panel",
            "filename": "admin-dashboard.png",
            "purpose": "Allows platform administrators to monitor usage metrics, verify active system states, and audit logs.",
            "components": "Active system load graphs, user count monitors, endpoint frequency gauges, tenant records, and security audit logs table.",
            "apis": "GET /api/admin/metrics, GET /api/admin/users, GET /api/admin/audit-logs."
        }
    ]
    
    # Write each screenshot section
    for idx, item in enumerate(screens_list, start=1):
        doc.add_page_break()
        add_heading_1(doc, item["title"])
        
        # Details table
        table = doc.add_table(rows=3, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        
        widths = [Inches(1.8), Inches(4.7)]
        details = [
            ("Purpose", item["purpose"]),
            ("Key UI Components", item["components"]),
            ("Backend API Mappings", item["apis"])
        ]
        
        for r_idx, (k, v) in enumerate(details):
            row = table.rows[r_idx]
            
            cell_k = row.cells[0]
            cell_k.width = widths[0]
            p_k = cell_k.paragraphs[0]
            p_k.paragraph_format.space_after = Pt(0)
            run_k = p_k.add_run(k)
            apply_text_style(run_k, name="Segoe UI", size_pt=9.5, color_rgb=(15, 23, 42), bold=True)
            set_cell_margins(cell_k, top=80, bottom=80, left=100, right=100)
            set_cell_background(cell_k, "F8FAFC")
            
            cell_v = row.cells[1]
            cell_v.width = widths[1]
            p_v = cell_v.paragraphs[0]
            p_v.paragraph_format.space_after = Pt(0)
            run_v = p_v.add_run(v)
            apply_text_style(run_v, name="Segoe UI", size_pt=9.5, color_rgb=(51, 65, 85))
            set_cell_margins(cell_v, top=80, bottom=80, left=100, right=100)
            
        set_table_horizontal_borders_only(table)
        
        # Image insertion
        p_img_title = doc.add_paragraph()
        p_img_title.paragraph_format.space_before = Pt(12)
        p_img_title.paragraph_format.space_after = Pt(4)
        p_img_title.paragraph_format.keep_with_next = True
        run_img_title = p_img_title.add_run("Interface Capture:")
        apply_text_style(run_img_title, name="Segoe UI", size_pt=10, color_rgb=(15, 23, 42), bold=True)
        
        filename = item["filename"]
        img_path = os.path.join(screens_dir, filename) if filename else ""
        
        if filename and os.path.exists(img_path):
            # Create a 1x1 table to act as a bordered frame around the screenshot
            frame_table = doc.add_table(rows=1, cols=1)
            frame_table.alignment = WD_TABLE_ALIGNMENT.CENTER
            frame_table.autofit = False
            
            frame_cell = frame_table.cell(0, 0)
            frame_cell.width = Inches(6.5)
            set_cell_background(frame_cell, "F8FAFC")
            set_cell_margins(frame_cell, top=100, bottom=100, left=100, right=100)
            
            # Apply thin light-gray borders around the frame cell
            tcPr = frame_cell._tc.get_or_add_tcPr()
            tcBorders = OxmlElement('w:tcBorders')
            for border_name in ['top', 'left', 'bottom', 'right']:
                border = OxmlElement(f'w:{border_name}')
                border.set(qn('w:val'), 'single')
                border.set(qn('w:sz'), '4') # 1/2 pt
                border.set(qn('w:space'), '0')
                border.set(qn('w:color'), 'D1D5DB') # Light Gray
                tcBorders.append(border)
            tcPr.append(tcBorders)
            
            p_img = frame_cell.paragraphs[0]
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_after = Pt(0)
            run_pic = p_img.add_run()
            
            # Fit to page nicely (5.8 inches width prevents clipping)
            run_pic.add_picture(img_path, width=Inches(5.8))
            
            # Figure Caption
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(4)
            p_cap.paragraph_format.space_after = Pt(8)
            run_cap = p_cap.add_run(f"Figure {idx:02d}.1: {item['title'].split('—')[1].strip()} Interface Screen")
            apply_text_style(run_cap, name="Segoe UI", size_pt=8.5, color_rgb=(100, 116, 139), italic=True)
        else:
            p_missing = doc.add_paragraph()
            p_missing.paragraph_format.space_before = Pt(4)
            p_missing.paragraph_format.space_after = Pt(8)
            run_missing = p_missing.add_run(f"[Capture file '{filename}' was not found in directory. Screen omitted.]")
            apply_text_style(run_missing, name="Segoe UI", size_pt=10, color_rgb=(220, 38, 38), italic=True)
            
    # Conclusion section
    add_heading_1(doc, "Conclusion")
    p_conclusion = doc.add_paragraph()
    p_conclusion.paragraph_format.line_spacing = 1.15
    p_conclusion.paragraph_format.space_after = Pt(8)
    p_conclusion.add_run("The screenshots contained in this report illustrate the successful execution of the frontend interfaces for Humanova. The visuals confirm that spacing, color parameters, styling utilities, navigation controllers, dynamic dashboards, and organization management views comply with design standards and are functional, communicating directly with Laravel controllers.")
    
    # Save document
    doc.save(output_path)
    print(f"Screenshot Report saved to {output_path}")

# ==========================================
# MAIN EXECUTION CONTROL
# ==========================================

if __name__ == "__main__":
    # Base paths
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    week_all_dir = os.path.join(project_root, "week all")
    screens_dir = os.path.join(week_all_dir, "ui-screens")
    
    # Temporary paths
    auth_diagram_path = os.path.join(script_dir, "auth_flow.png")
    
    # Outputs
    progress_report_path = os.path.join(week_all_dir, "CSE4204-8C-T07_FrontendProgress.docx")
    screenshot_report_path = os.path.join(week_all_dir, "CSE4204-8C-T07_UI_Screenshots.docx")
    
    print("Starting generation process...")
    print(f"Project root: {project_root}")
    print(f"Screenshots folder: {screens_dir}")
    print(f"Destination folder: {week_all_dir}")
    
    # Step 1: Draw diagram
    try:
        generate_auth_flow_diagram(auth_diagram_path)
    except Exception as e:
        print(f"Error generating auth flow diagram: {e}")
        
    # Step 2: Generate Progress Report
    try:
        generate_progress_report(progress_report_path, auth_diagram_path)
    except Exception as e:
        print(f"Error generating Progress Report: {e}")
        
    # Step 3: Generate Screenshot Report
    try:
        generate_screenshot_report(screenshot_report_path, screens_dir)
    except Exception as e:
        print(f"Error generating Screenshot Report: {e}")
        
    # Clean up diagram
    if os.path.exists(auth_diagram_path):
        try:
            os.remove(auth_diagram_path)
            print("Temporary diagram file cleaned up.")
        except Exception as e:
            print(f"Error cleaning up diagram: {e}")
            
    print("Report generation complete!")

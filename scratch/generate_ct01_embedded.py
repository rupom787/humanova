import os
import sys
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Configure matplotlib to use Segoe UI/sans-serif to match Word Document typography
matplotlib.rcParams['font.sans-serif'] = ['Segoe UI', 'Arial', 'DejaVu Sans', 'sans-serif']
matplotlib.rcParams['font.family'] = 'sans-serif'

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

def add_p_border_bottom(paragraph, hex_color="0EA5E9", sz="12", space="6"):
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

def apply_text_style(run, name="Segoe UI", size_pt=10.5, color_rgb=(51, 65, 85), bold=False, italic=False):
    """Applies font styles to a run."""
    run.font.name = name
    run.font.size = Pt(size_pt)
    run.font.color.rgb = RGBColor(*color_rgb)
    run.bold = bold
    run.italic = italic

def add_page_number(run):
    """Adds an XML page number field code into a text run."""
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    
    run._r.append(fldChar1)
    run._r.append(instrText)
    run._r.append(fldChar2)
    run._r.append(fldChar3)

def setup_document_styles(doc):
    """Sets up page margins, global typography styles, headers, and footers."""
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
    
    # Force tight global paragraph formatting to avoid default Word huge gaps
    p_format = style.paragraph_format
    p_format.space_before = Pt(0)
    p_format.space_after = Pt(4)
    p_format.line_spacing = 1.15
    
    # Configure Academic Header
    header = doc.sections[0].header
    p_header = header.paragraphs[0]
    p_header.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_header.paragraph_format.space_before = Pt(0)
    p_header.paragraph_format.space_after = Pt(0)
    run_h = p_header.add_run("Embedded Systems (CT-01) Study Guide & Answer Key")
    apply_text_style(run_h, name="Segoe UI", size_pt=8.5, color_rgb=(148, 163, 184)) # Slate 400
    
    # Configure Dynamic Footer with Page Numbers
    footer = doc.sections[0].footer
    p_footer = footer.paragraphs[0]
    p_footer.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_footer.paragraph_format.space_before = Pt(0)
    p_footer.paragraph_format.space_after = Pt(0)
    run_f_text = p_footer.add_run("Page ")
    apply_text_style(run_f_text, name="Segoe UI", size_pt=8.5, color_rgb=(148, 163, 184))
    run_page = p_footer.add_run()
    apply_text_style(run_page, name="Segoe UI", size_pt=8.5, color_rgb=(148, 163, 184))
    add_page_number(run_page)

def add_header_block(doc, title, subtitle):
    """Adds a styled title header block to start the document."""
    # Top border element
    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(10)
    p_title.paragraph_format.space_after = Pt(2)
    run_title = p_title.add_run(title)
    apply_text_style(run_title, name="Segoe UI", size_pt=20, color_rgb=(15, 23, 42), bold=True)
    
    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(10)
    run_sub = p_sub.add_run(subtitle)
    apply_text_style(run_sub, name="Segoe UI", size_pt=12, color_rgb=(2, 132, 199), italic=True)
    add_p_border_bottom(p_sub, hex_color="0F172A", sz="18", space="6")

def add_heading_1(doc, text):
    """Primary Heading (styled with Cyan border)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)  # Reduced from 22
    p.paragraph_format.space_after = Pt(4)   # Reduced from 6
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    apply_text_style(run, name="Segoe UI", size_pt=14, color_rgb=(15, 23, 42), bold=True)
    add_p_border_bottom(p, hex_color="0EA5E9", sz="12", space="6")
    return p

def add_heading_2(doc, text):
    """Sub Heading (styled with Light Blue)."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)  # Reduced from 14
    p.paragraph_format.space_after = Pt(3)   # Reduced from 4
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    apply_text_style(run, name="Segoe UI", size_pt=12, color_rgb=(2, 132, 199), bold=True)
    return p

def add_paragraph_text(doc, text, space_after=4, italic=False, bold=False):
    """Adds a standard text paragraph with clean formatting."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(text)
    apply_text_style(run, name="Segoe UI", size_pt=10.5, color_rgb=(51, 65, 85), italic=italic, bold=bold)
    return p

def add_bullet_item(doc, bold_prefix, text_body):
    """Adds a clean list bullet item with tight spacing."""
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)    # Tighter spacing for list entries
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        run_bold = p.add_run(bold_prefix)
        apply_text_style(run_bold, name="Segoe UI", size_pt=10.5, color_rgb=(15, 23, 42), bold=True)
    run_body = p.add_run(text_body)
    apply_text_style(run_body, name="Segoe UI", size_pt=10.5, color_rgb=(51, 65, 85))
    return p

def add_callout(doc, text, title=""):
    """Creates a visually distinctive callout block with a thick cyan left border."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.5)
    set_cell_background(cell, "F8FAFC") # Slate 50
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
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
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.15
    
    if title:
        run_title = p.add_run(title + "\n")
        apply_text_style(run_title, name="Segoe UI", size_pt=10.5, color_rgb=(15, 23, 42), bold=True)
        
    run_body = p.add_run(text)
    apply_text_style(run_body, name="Segoe UI", size_pt=10, color_rgb=(71, 85, 105), italic=True)

# ==========================================
# DIAGRAM GENERATOR
# ==========================================

def generate_embedded_block_diagram(output_path):
    """Generates a functional block diagram for an Embedded System using matplotlib (tightened coordinates)."""
    fig, ax = plt.subplots(figsize=(10.0, 5.6), dpi=300) # Compressed figure height from 7.5 to 5.6 to save vertical space
    ax.axis('off')
    
    # Background and coordinates system configuration (compressed range)
    ax.set_xlim(0, 10)
    ax.set_ylim(0.5, 7.5)
    
    # Custom colors
    colors = {
        'power': '#FEF9C3',  # Light yellow
        'sensor': '#DCFCE7', # Light green
        'input': '#CCFBF1',  # Light teal
        'cpu': '#E0F2FE',    # Light blue
        'memory': '#F3E8FF',  # Light purple
        'output_if': '#FFEDD5', # Light orange
        'output_dev': '#FEE2E2', # Light red
        'comm': '#E0F2FE',   # Light sky-blue
        'border': '#475569', # Slate-600
    }
    
    def draw_box(x, y, w, h, title, content_lines, fill_color):
        rect = patches.FancyBboxPatch(
            (x, y), w, h,
            boxstyle="round,pad=0.1",
            fc=fill_color, ec=colors['border'], lw=1.5,
            zorder=3
        )
        ax.add_patch(rect)
        
        # Add Title text
        ax.text(x + w/2, y + h - 0.25, title, ha='center', va='top', fontsize=9.5, fontweight='bold', color='#0F172A', zorder=4)
        
        # Add content lines
        content_text = "\n".join(content_lines)
        ax.text(x + w/2, y + 0.15, content_text, ha='center', va='bottom', fontsize=8.0, color='#334155', linespacing=1.2, zorder=4)

    # 1. Draw Power Supply (top) - y coord lowered from 7.0 to 6.2
    draw_box(3.8, 6.2, 2.4, 0.8, "Power Supply", ["Battery / Adapter", "Voltage Regulators"], colors['power'])
    
    # 2. Draw Sensors (middle-left) - y coord lowered from 5.0 to 4.4
    draw_box(0.5, 4.4, 2.2, 1.0, "Sensors", ["Ultrasonic, Temp, IR", "Light, Pressure", "Convert physical -> elec"], colors['sensor'])
    
    # 3. Draw Input Interface (middle-left-lower) - y coord lowered from 3.2 to 2.7
    draw_box(0.5, 2.7, 2.2, 1.0, "Input Interface", ["ADC (Analog -> Digital)", "GPIO, Optocouplers", "Signal Conditioning"], colors['input'])
    
    # 4. Draw Core Microcontroller / CPU (center) - y coord lowered from 2.8 to 2.2, height compressed to 2.7
    draw_box(3.6, 2.2, 2.8, 2.7, "Microcontroller / CPU", [
        "ALU (Arithmetic Logic)",
        "Control Unit (Execution)",
        "Registers (Fast Storage)",
        "Timers & Counters",
        "Interrupt Controller",
        "System Clock"
    ], colors['cpu'])
    
    # 5. Draw Memories (bottom-center) - height compressed to 0.9
    draw_box(2.2, 0.8, 2.2, 0.9, "Flash / ROM", ["Program Code", "Non-Volatile Firmware", "Read-Only during execution"], colors['memory'])
    draw_box(5.6, 0.8, 2.2, 0.9, "RAM", ["Variables & Stack", "Volatile Memory", "High-speed Read/Write"], colors['memory'])
    
    # 6. Draw Output Interface (middle-right) - y coord lowered from 5.0 to 4.4
    draw_box(7.3, 4.4, 2.2, 1.0, "Output Interface", ["GPIO Registers", "PWM Controllers", "DAC (Digital -> Analog)"], colors['output_if'])
    
    # 7. Draw Output Devices (middle-right-lower) - y coord lowered from 3.2 to 2.7
    draw_box(7.3, 2.7, 2.2, 1.0, "Output Devices", ["LCD Displays & LEDs", "Motors & Relays", "Actuators & Buzzers"], colors['output_dev'])
    
    # 8. Draw Communication Interface (bottom-right) - height compressed to 1.2
    draw_box(7.3, 0.8, 2.2, 1.2, "Comm. Interface", ["Serial: UART, SPI, I2C", "Industrial: CAN Bus", "Wireless: BLE, Wi-Fi", "USB / Ethernet"], colors['comm'])

    # Arrows configuration (using filled arrowhead for professional CAD layout feel)
    arrow_args = dict(arrowstyle="-|>", color="#0284C7", lw=1.8, mutation_scale=12, zorder=2)
    bidir_arrow_args = dict(arrowstyle="<|-|>", color="#0284C7", lw=1.8, mutation_scale=12, zorder=2)
    
    # Power Supply down to Microcontroller
    ax.annotate('', xy=(5.0, 4.9), xytext=(5.0, 6.2), arrowprops=dict(arrowstyle="-|>", color="#B45309", lw=1.8, ls="--", mutation_scale=12))
    ax.text(5.1, 5.5, "Regulated VCC", fontsize=7.5, color='#B45309', fontweight='bold')
    
    # Sensors to Input Interface
    ax.annotate('', xy=(1.6, 3.7), xytext=(1.6, 4.4), arrowprops=arrow_args)
    
    # Input Interface to CPU
    ax.annotate('', xy=(3.6, 3.2), xytext=(2.7, 3.2), arrowprops=arrow_args)
    ax.text(2.85, 3.3, "Digital Data", fontsize=7.5, color='#0284C7')
    
    # CPU to Flash / ROM
    ax.annotate('', xy=(3.0, 1.7), xytext=(4.0, 2.2), arrowprops=arrow_args)
    ax.text(3.05, 1.9, "Instructions", fontsize=7.5, color='#0284C7', rotation=40)
    
    # CPU to RAM
    ax.annotate('', xy=(7.0, 1.7), xytext=(6.0, 2.2), arrowprops=bidir_arrow_args)
    ax.text(6.4, 1.9, "Data Bus", fontsize=7.5, color='#0284C7', rotation=-40)
    
    # CPU to Output Interface
    ax.annotate('', xy=(7.3, 4.9), xytext=(6.4, 4.3), arrowprops=arrow_args)
    ax.text(6.4, 4.75, "Control Signals", fontsize=7.5, color='#0284C7', rotation=30)
    
    # CPU to Comm Interface
    ax.annotate('', xy=(7.3, 1.4), xytext=(5.8, 2.2), arrowprops=bidir_arrow_args)
    
    # Output Interface to Output Devices
    ax.annotate('', xy=(8.4, 3.7), xytext=(8.4, 4.4), arrowprops=arrow_args)
    
    # Title overlay inside figure boundary
    ax.text(5.0, 7.3, "EMBEDDED SYSTEM FUNCTIONAL BLOCK DIAGRAM", ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A')

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', transparent=True)
    plt.close()
    print("Embedded system block diagram generated successfully.")

# ==========================================
# MAIN REPORT GENERATION FUNCTION
# ==========================================

def create_embedded_systems_document(output_path, diagram_path):
    doc = Document()
    setup_document_styles(doc)
    
    # Header block
    add_header_block(doc, "CT-01 Course Exam Report & Study Guide", "Question 1: Block Diagram of an Embedded System & Associated Syllabus Topics")
    
    # Marks Breakdown Callout (Academic Enhancement)
    add_callout(doc,
        "• Part A: Draw the Block Diagram (4 Marks) — Labeled modules, interconnection buses, and direction flow.\n"
        "• Part B: Explain Component Blocks (4 Marks) — Sensory input, CPU internals, memory maps, and output devices.\n"
        "• Part C: List Core Characteristics (2 Marks) — Real-time deadlines, single-function design, and constraints.",
        title="Official Grading Rubric & Marks Distribution (10 Marks Total)"
    )
    
    # Metadata Table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    
    meta_data = [
        ("Course Exam Code", "CT-01 (Continuous Test 01)"),
        ("Marks Allocation", "10 Marks (Rubric Applied)"),
        ("Suggested Time Limit", "20 Minutes"),
        ("Subject Matter", "Embedded Systems Block Diagram & Fundamental Design Metrics"),
        ("Resource Status", "Complete Exam-Style Written Answer with Matplotlib Drawing")
    ]
    
    widths = [Inches(2.0), Inches(4.5)]
    for i, (k, v) in enumerate(meta_data):
        row = meta_table.rows[i]
        
        cell_k = row.cells[0]
        cell_k.width = widths[0]
        p_k = cell_k.paragraphs[0]
        p_k.paragraph_format.space_before = Pt(0)
        p_k.paragraph_format.space_after = Pt(0)
        run_k = p_k.add_run(k)
        apply_text_style(run_k, name="Segoe UI", size_pt=10, color_rgb=(15, 23, 42), bold=True)
        set_cell_margins(cell_k, top=100, bottom=100, left=120, right=120)
        set_cell_background(cell_k, "F8FAFC")
        
        cell_v = row.cells[1]
        cell_v.width = widths[1]
        p_v = cell_v.paragraphs[0]
        p_v.paragraph_format.space_before = Pt(0)
        p_v.paragraph_format.space_after = Pt(0)
        run_v = p_v.add_run(v)
        apply_text_style(run_v, name="Segoe UI", size_pt=10, color_rgb=(51, 65, 85))
        set_cell_margins(cell_v, top=100, bottom=100, left=120, right=120)
        
    set_table_horizontal_borders_only(meta_table)
    
    # 1. Definition & Core Concept
    add_heading_1(doc, "1. Definition & Core Concept")
    add_paragraph_text(doc, "An Embedded System is a special-purpose computer system designed to perform one or a limited number of dedicated, predefined functions. Unlike general-purpose computers (e.g., personal computers or laptops) which are designed to run a wide array of application programs, an embedded system is highly optimized and customized for the specific application it serves. It tightly integrates both hardware components and firmware/software algorithms to monitor, control, or automate physical environments, often operating under stringent real-time constraints.")
    
    add_heading_2(doc, "Real-World Examples of Embedded Systems")
    add_bullet_item(doc, "Washing Machine: ", "Controls wash cycles, monitors water levels, and adjusts drum speeds based on sensor inputs.")
    add_bullet_item(doc, "Automated Teller Machine (ATM): ", "Handles secure cryptographic operations, card readings, user verification, and mechanical money dispensing.")
    add_bullet_item(doc, "Smart Television: ", "Executes media decoding, network protocol stacks, and drives display panels.")
    add_bullet_item(doc, "Office Printer: ", "Manages print queues, controls stepper motors for paper alignment, and checks toner levels.")
    add_bullet_item(doc, "Microwave Oven: ", "Regulates heating times, monitors safety interlocks, and drives the magnetron based on user settings.")
    add_bullet_item(doc, "Smart Door Lock: ", "Handles wireless authentication (BLE/Wi-Fi), biometric scanning, and controls the locking solenoid.")
    add_bullet_item(doc, "Medical Devices (Pacemakers, Insulin Pumps): ", "Continuously monitors physiological signals and administers therapy under strict real-time, low-power constraints.")

    # 2. Key Characteristics
    add_heading_1(doc, "2. Key Characteristics of Embedded Systems")
    add_paragraph_text(doc, "Based on standard design criteria and classroom syllabus notes, embedded systems are characterized by a unique set of design parameters:")
    
    add_bullet_item(doc, "Single-Functionality: ", "The system executes a dedicated program repeatedly to perform a specific task (e.g., a thermostat only controls temperature; it cannot run spreadsheets or browse the web).")
    add_bullet_item(doc, "Tightly Constrained: ", "Embedded systems must operate within strict resource boundaries. Designers must optimize for minimal size, low production cost, limited power budgets, and constrained memory size.")
    add_bullet_item(doc, "Reactive & Real-Time: ", "Many systems must continuously react to external stimuli in the environment via sensors. They must compute results and drive actuators within precise time limits (deadlines). Failure to respond within these limits can result in complete system failure.")
    add_bullet_item(doc, "High Reliability & Safety: ", "Because many embedded systems are deployed in safety-critical environments (e.g., automotive braking, flight controllers, or medical life support), they must execute with near-zero failure rates.")
    add_bullet_item(doc, "Low Power Consumption: ", "Often powered by small batteries or energy harvesting, they must maximize battery life through aggressive power management (e.g., deep sleep modes).")
    add_bullet_item(doc, "Non-Recurring Engineering (NRE) Cost Sensitivity: ", "The unit production cost must be kept low, especially for high-volume consumer goods, demanding specialized hardware-software partitioning.")

    # 3. Block Diagram of an Embedded System
    add_heading_1(doc, "3. Block Diagram of an Embedded System")
    add_paragraph_text(doc, "Below is the functional block diagram of a complete embedded system. It depicts the flow of data starting from physical stimulus detection, progressing through signal conditioning, processing, decision-making, memory retrieval, and ultimately driving external actuators or communications interfaces, all while supported by a dedicated power management system.")
    
    # Insert the block diagram image
    if os.path.exists(diagram_path):
        frame_table = doc.add_table(rows=1, cols=1)
        frame_table.alignment = WD_TABLE_ALIGNMENT.CENTER
        frame_table.autofit = False
        
        frame_cell = frame_table.cell(0, 0)
        frame_cell.width = Inches(6.5)
        set_cell_background(frame_cell, "F8FAFC")
        set_cell_margins(frame_cell, top=100, bottom=100, left=100, right=100)
        
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
        p_img.paragraph_format.space_before = Pt(0)
        p_img.paragraph_format.space_after = Pt(0)
        run_pic = p_img.add_run()
        run_pic.add_picture(diagram_path, width=Inches(6.0))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(4)
        p_cap.paragraph_format.space_after = Pt(12)
        run_cap = p_cap.add_run("Figure 1.1: Functional block diagram of an Embedded System.")
        apply_text_style(run_cap, name="Segoe UI", size_pt=8.5, color_rgb=(100, 116, 139), italic=True)
    else:
        add_paragraph_text(doc, "[Block diagram image missing - could not embed diagram]", italic=True)

    # 4. Detailed Component & Working Principle Breakdown
    add_heading_1(doc, "4. Component Breakdown & Working Principle")
    add_paragraph_text(doc, "The operation of an embedded system follows a structured sequential data flow: Data Acquisition → Conversion → Computation → Output Drive. The detailed functions of each key block are explained below:")
    
    add_heading_2(doc, "Sensors & Data Acquisition")
    add_paragraph_text(doc, "Sensors act as the primary input interface to the physical world. They detect environmental changes (such as heat, light, sound, magnetic fields, or pressure) and convert these physical quantities into measurable electrical signals (voltage, current, or frequency).")
    
    add_heading_2(doc, "Input Interface (Signal Conditioning & Conversion)")
    add_paragraph_text(doc, "Since most real-world physical signals are analog and noisy, they cannot be directly processed by digital microcontrollers. The input interface performs crucial preparation steps:")
    add_bullet_item(doc, "Signal Conditioning: ", "Uses operational amplifiers (op-amps) and filters to amplify weak sensor outputs and filter out high-frequency noise.")
    add_bullet_item(doc, "Analog-to-Digital Converter (ADC): ", "Quantizes the conditioned analog voltage signals into discrete binary values (e.g., 8-bit, 10-bit, or 12-bit digital numbers) that the processor can read.")
    add_bullet_item(doc, "General Purpose Input/Output (GPIO): ", "Reads binary status signals (ON/OFF) from switches or digital sensors directly.")

    add_heading_2(doc, "The Microcontroller (Processor Core)")
    add_paragraph_text(doc, "The Microcontroller (or CPU) serves as the core intelligence or 'brain' of the embedded system. It is responsible for reading input data, executing the system instructions loaded in memory, performing logic operations, and writing output states. It contains several key internal modules:")
    add_bullet_item(doc, "Arithmetic Logic Unit (ALU): ", "Performs mathematical calculations (addition, subtraction) and logical comparisons.")
    add_bullet_item(doc, "Control Unit (CU): ", "Directs the instruction fetch, decode, and execute cycles, routing data between registers and external components.")
    add_bullet_item(doc, "Registers: ", "Internal, high-speed temporary storage cells used to hold instruction operands and intermediate results.")
    add_bullet_item(doc, "Timers and Counters: ", "Crucial for generating precise time delays, measuring signal widths, and executing periodic scheduler ticks.")
    add_bullet_item(doc, "Interrupt Controller: ", "Suspends regular code execution instantly to handle critical external events (e.g., emergency stops, packet arrival) in real-time.")

    add_heading_2(doc, "Output Interface & Actuators")
    add_paragraph_text(doc, "The Output Interface transfers the decision commands computed by the microcontroller to the output devices. This interface translates low-power digital signals into signals capable of driving physical components:")
    add_bullet_item(doc, "Pulse-Width Modulation (PWM): ", "Varies the duty cycle of digital square waves to control analog outputs like motor speeds, LED brightness, or heater power.")
    add_bullet_item(doc, "Digital-to-Analog Converter (DAC): ", "Converts binary digital signals back into smooth analog voltages for audio generation or precision control.")
    add_bullet_item(doc, "Transistors, Relays & Motor Drivers: ", "Since processor GPIOs can only output small currents (typically 10-20mA), external switching hardware is used to control heavy loads like solenoids, AC appliances, and DC motors.")

    # 5. Memory Architecture
    add_heading_1(doc, "5. Memory Architecture & Data Flow")
    add_paragraph_text(doc, "Embedded systems utilize specialized memory architectures to store program instructions (firmware) and execute computational tasks. This is typically implemented as a Harvard Architecture (separate instruction and data buses) or Von Neumann Architecture.")
    
    # Memory comparison table
    mem_table = doc.add_table(rows=5, cols=4)
    mem_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    mem_table.autofit = False
    
    mem_headers = ["Memory Type", "Purpose", "Volatile", "Description"]
    mem_widths = [Inches(1.2), Inches(1.5), Inches(1.0), Inches(2.8)]
    
    for c_idx, text in enumerate(mem_headers):
        cell = mem_table.rows[0].cells[c_idx]
        cell.width = mem_widths[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        apply_text_style(run, name="Segoe UI", size_pt=10, color_rgb=(255, 255, 255), bold=True)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        
    mem_rows = [
        ("Flash Memory", "Stores executable program code", "No (Non-Volatile)", "Re-programmable ROM where the main firmware binary is stored permanently."),
        ("ROM / Mask ROM", "Permanent bootloader & firmware", "No (Non-Volatile)", "Programmed during chip fabrication; stores startup routines and cannot be modified."),
        ("EEPROM", "Saves user settings & configurations", "No (Non-Volatile)", "Byte-writable memory used to save non-volatile variables like calibration data or passwords."),
        ("RAM (SRAM)", "Variables, stacks, and runtime buffers", "Yes (Volatile)", "Temporary, high-speed workspace that loses all contents when power is disconnected.")
    ]
    
    for r_idx, row_data in enumerate(mem_rows):
        row = mem_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = mem_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            apply_text_style(run, name="Segoe UI", size_pt=9.5, color_rgb=(51, 65, 85))
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
                
    set_table_horizontal_borders_only(mem_table)
    
    add_heading_2(doc, "Memory Data Flow Execution Sequence")
    add_callout(doc, 
        "1. Power-On Reset: The CPU reads the boot vector from ROM/Flash.\n"
        "2. Instruction Fetch: The CPU fetches instructions sequentially from Flash memory via the program bus.\n"
        "3. Variable Allocation: Runtime variables and calculations are dynamically read from and written to RAM.\n"
        "4. Non-Volatile Write: Critical system changes or user logs are committed to EEPROM before power-down.",
        title="Execution Sequence"
    )

    # 6. Sensors Deep Dive & Selection Criteria
    add_heading_1(doc, "6. Sensor Technology & Selection Criteria")
    add_paragraph_text(doc, "Choosing the correct sensor is a critical engineering decision in embedded system design. The selection process requires balancing performance metrics against system cost and physical constraints.")
    
    # Sensor selection criteria table
    sel_table = doc.add_table(rows=9, cols=3)
    sel_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sel_table.autofit = False
    
    sel_headers = ["Selection Criteria", "Importance / Focus", "Engineering Impact"]
    sel_widths = [Inches(1.8), Inches(2.2), Inches(2.5)]
    
    for c_idx, text in enumerate(sel_headers):
        cell = sel_table.rows[0].cells[c_idx]
        cell.width = sel_widths[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        apply_text_style(run, name="Segoe UI", size_pt=10, color_rgb=(255, 255, 255), bold=True)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        
    sel_rows = [
        ("Accuracy & Precision", "Measures the closeness to true value", "Determines quality of data; critical for feedback loops."),
        ("Measurement Range", "Defines the min and max input limits", "Ensures the sensor can capture all expected environmental states."),
        ("Response Time / Bandwidth", "Speed at which output registers change", "Determines real-time responsiveness; vital for safety control."),
        ("Power Consumption", "Current draw in active and standby modes", "Directly impacts battery sizing and thermal dissipation profiles."),
        ("Cost & Form Factor", "Unit cost and physical dimensions", "Restricts placement and defines commercial feasibility of final product."),
        ("Environmental Tolerance", "IP ratings, temperature, and moisture limits", "Guarantees long-term survival in harsh industrial or outdoor spots."),
        ("Reliability & Calibration", "Mean Time Between Failures (MTBF)", "Dictates how often the system requires field servicing."),
        ("Interface Compatibility", "Analog voltage vs. digital SPI/I2C/UART", "Affects microcontroller pin allocation and PCB design complexity.")
    ]
    
    for r_idx, row_data in enumerate(sel_rows):
        row = sel_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = sel_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            apply_text_style(run, name="Segoe UI", size_pt=9.5, color_rgb=(51, 65, 85))
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
                
    set_table_horizontal_borders_only(sel_table)

    add_heading_2(doc, "Deep Dive: Ultrasonic Distance Sensor")
    add_paragraph_text(doc, "An Ultrasonic Sensor (such as the popular HC-SR04) measures the distance to a target object by emitting high-frequency acoustic waves (typically 40 kHz, beyond human hearing) and timing the interval it takes for the echo to bounce back.")
    
    # Math formula in a stylized block
    add_callout(doc, 
        "The distance to the target is calculated using the speed of sound in air (approximately 343 m/s at 20°C) and the measured time of flight (t):\n\n"
        "      Distance = (Speed of Sound × Time of Flight) / 2\n\n"
        "The division by 2 accounts for the sound wave traveling out to the target and then returning.",
        title="Physical Working Formula"
    )
    
    add_paragraph_text(doc, "Operating Sequence for Ultrasonic Measurement:")
    add_bullet_item(doc, "1. Trigger Pulse: ", "The host microcontroller outputs a short 10-microsecond high pulse to the sensor's Trigger pin.")
    add_bullet_item(doc, "2. Wave Emission: ", "The sensor internal circuitry generates a burst of eight 40 kHz ultrasonic pulses out of its transmitter transducer.")
    add_bullet_item(doc, "3. Echo Timing: ", "The sensor sets its Echo output pin to high. The wave travels through the air, strikes an obstacle, and reflects back.")
    add_bullet_item(doc, "4. Echo Detection: ", "The receiver transducer detects the returning echo. The sensor drives the Echo pin low immediately.")
    add_bullet_item(doc, "5. Calculation: ", "The microcontroller measures the pulse width of the Echo pin (in microseconds) and computes the distance.")

    # Side-by-side lists using columns in tables
    add_heading_2(doc, "Features and Limitations of Ultrasonic Sensors")
    fl_table = doc.add_table(rows=1, cols=2)
    fl_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    fl_table.autofit = False
    
    fl_widths = [Inches(3.2), Inches(3.2)]
    
    # Left cell: Features
    cell_f = fl_table.rows[0].cells[0]
    cell_f.width = fl_widths[0]
    set_cell_background(cell_f, "F0FDF4") # Subtle green background
    set_cell_margins(cell_f, top=120, bottom=120, left=150, right=150)
    p_f_title = cell_f.paragraphs[0]
    p_f_title.paragraph_format.space_before = Pt(0)
    p_f_title.paragraph_format.space_after = Pt(0)
    run_f_t = p_f_title.add_run("Features / Advantages")
    apply_text_style(run_f_t, name="Segoe UI", size_pt=10.5, color_rgb=(21, 128, 61), bold=True)
    p_f_body = cell_f.add_paragraph()
    p_f_body.paragraph_format.space_before = Pt(0)
    p_f_body.paragraph_format.line_spacing = 1.1
    p_f_body.paragraph_format.space_after = Pt(2)
    f_items = [
        "• Non-contact distance measurement.",
        "• High accuracy (within millimeters under optimal conditions).",
        "• Low unit cost; simple 4-pin hardware interface.",
        "• Works perfectly in total darkness or bright light.",
        "• Highly reliable for solid obstacle detection."
    ]
    run_f_b = p_f_body.add_run("\n".join(f_items))
    apply_text_style(run_f_b, name="Segoe UI", size_pt=9.5, color_rgb=(21, 128, 61))
    
    # Right cell: Limitations
    cell_l = fl_table.rows[0].cells[1]
    cell_l.width = fl_widths[1]
    set_cell_background(cell_l, "FEF2F2") # Subtle red background
    set_cell_margins(cell_l, top=120, bottom=120, left=150, right=150)
    p_l_title = cell_l.paragraphs[0]
    p_l_title.paragraph_format.space_before = Pt(0)
    p_l_title.paragraph_format.space_after = Pt(0)
    run_l_t = p_l_title.add_run("Limitations / Challenges")
    apply_text_style(run_l_t, name="Segoe UI", size_pt=10.5, color_rgb=(185, 28, 28), bold=True)
    p_l_body = cell_l.add_paragraph()
    p_l_body.paragraph_format.space_before = Pt(0)
    p_l_body.paragraph_format.line_spacing = 1.1
    p_l_body.paragraph_format.space_after = Pt(2)
    l_items = [
        "• Soft materials (sponge, cloth) absorb sound waves.",
        "• Impeded by ambient weather (heavy rain, fog, dust).",
        "• Restricted sensing range (typically 2cm up to 4 meters).",
        "• Temperature and humidity affect speed of sound.",
        "• Poor echoes off irregular, slanted surfaces."
    ]
    run_l_b = p_l_body.add_run("\n".join(l_items))
    apply_text_style(run_l_b, name="Segoe UI", size_pt=9.5, color_rgb=(185, 28, 28))
    
    set_table_horizontal_borders_only(fl_table, color="E2E8F0")

    # 7. Processor Technology & Design Metrics
    add_heading_1(doc, "7. Processor Technology & Design Metrics")
    add_paragraph_text(doc, "Modern embedded systems use three primary processor technology classes, selecting one based on speed, power, and unit volume requirements:")
    
    # Processor table
    proc_table = doc.add_table(rows=4, cols=3)
    proc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    proc_table.autofit = False
    
    proc_headers = ["Processor Type", "Description", "Typical Application / Trade-offs"]
    proc_widths = [Inches(1.8), Inches(2.5), Inches(2.2)]
    
    for c_idx, text in enumerate(proc_headers):
        cell = proc_table.rows[0].cells[c_idx]
        cell.width = proc_widths[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        apply_text_style(run, name="Segoe UI", size_pt=10, color_rgb=(255, 255, 255), bold=True)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        
    proc_rows = [
        ("General Purpose Processor (GPP)", "Highly flexible processors designed for general computation. Uses standard instruction sets.", "Microprocessors like ARM Cortex-A series. High flexibility but higher power and cost."),
        ("Single Purpose Processor (ASIC)", "Hardwired hardware designed to execute one specific program or logic chain. Zero instruction-fetch overhead.", "Application-Specific Integrated Circuits. Extremely fast, lowest unit cost at scale, but zero flexibility and very high NRE."),
        ("Application Specific Processor (ASIP/DSP)", "Customized instruction set optimized for a specific domain (e.g., audio processing, math arrays).", "Digital Signal Processors (DSPs), microcontrollers like ARM Cortex-M. Excellent balance of speed, power, and cost.")
    ]
    
    for r_idx, row_data in enumerate(proc_rows):
        row = proc_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = proc_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            apply_text_style(run, name="Segoe UI", size_pt=9.5, color_rgb=(51, 65, 85))
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
                
    set_table_horizontal_borders_only(proc_table)

    add_heading_2(doc, "Key Design Metrics")
    add_paragraph_text(doc, "Design metrics represent the set of measurable criteria used to gauge the success, cost-effectiveness, and operational stability of an embedded system:")
    add_bullet_item(doc, "Performance: ", "The speed or rate at which the system executes operations (e.g., instructions per second, response latency).")
    add_bullet_item(doc, "Power Consumption: ", "The energy consumed by the system. Determines battery life limits and thermal heatsink designs.")
    add_bullet_item(doc, "Unit Cost: ", "The manufacturing cost per unit (excluding NRE), which governs margins when selling high-volume consumer goods.")
    add_bullet_item(doc, "Physical Size / Weight: ", "Space constraints on PCB layouts and device enclosures (e.g., wristwatches, wearable health sensors).")
    add_bullet_item(doc, "Time-to-Market (TTM): ", "The duration required to design, manufacture, and release the product. Late entry can lead to massive revenue loss.")
    add_bullet_item(doc, "Reliability & Safety: ", "The system's mean time to failure. Must approach infinity for life-critical configurations.")

    add_heading_2(doc, "Understanding Non-Recurring Engineering (NRE) Cost")
    add_paragraph_text(doc, "Non-Recurring Engineering (NRE) Cost represents the one-time, upfront capital expenditures required to design, program, simulate, prototype, test, and manufacture tooling for a new embedded product before mass production begins.")
    
    add_callout(doc, 
        "Total Product Cost = NRE Cost + (Unit Cost × Production Volume)\n\n"
        "Key Engineering Insight:\n"
        "• High NRE is highly acceptable if production volumes are massive (e.g., microchips in smartphones), as the upfront cost is amortized across millions of units.\n"
        "• Low NRE is mandatory for low-volume, bespoke configurations (e.g., custom factory automation machines), even if the individual unit cost is very high.",
        title="Amortization Equation"
    )

    # 8. Design Methodologies: Concurrent vs Traditional
    add_heading_1(doc, "8. Design Methodologies: Concurrent Design & Co-Design")
    add_paragraph_text(doc, "Engineering workflows have evolved from rigid sequential systems to dynamic collaborative structures to shorten development times and reduce design flaws.")
    
    add_heading_2(doc, "Traditional vs. Concurrent Design Workflow")
    # Comparison table
    comp_table = doc.add_table(rows=7, cols=3)
    comp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_table.autofit = False
    
    comp_headers = ["Feature", "Traditional Sequential Design", "Concurrent Design (Parallel)"]
    comp_widths = [Inches(1.5), Inches(2.5), Inches(2.5)]
    
    for c_idx, text in enumerate(comp_headers):
        cell = comp_table.rows[0].cells[c_idx]
        cell.width = comp_widths[c_idx]
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(text)
        apply_text_style(run, name="Segoe UI", size_pt=10, color_rgb=(255, 255, 255), bold=True)
        set_cell_background(cell, "0F172A")
        set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
        
    comp_rows = [
        ("Workflow Structure", "Sequential (Hardware designed -> fabricated -> software written).", "Parallel (Hardware and software elements designed simultaneously)."),
        ("Development Time", "Long. Software team must wait for physical boards to begin integration.", "Short. Emulation, virtual prototyping, and modeling tools are used."),
        ("Total Project Cost", "High. Discovering mistakes late forces expensive PCB hardware redesigns.", "Low. Errors are detected early in simulation, avoiding physical re-spins."),
        ("Design Flexibility", "Low. Software is forced to adapt to hardware limits that are fixed late.", "High. Hardware-software boundaries are fluid and adjust to feedback."),
        ("Integration Timing", "Very Late. Happens only after physical prototype assembly.", "Continuous. Virtual prototyping platforms enable early integration."),
        ("Error Detection", "Late. Discovered during bench testing or pilot runs.", "Early. Discovered during co-simulations and model checking.")
    ]
    
    for r_idx, row_data in enumerate(comp_rows):
        row = comp_table.rows[r_idx + 1]
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = comp_widths[c_idx]
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(val)
            apply_text_style(run, name="Segoe UI", size_pt=9.5, color_rgb=(51, 65, 85))
            set_cell_margins(cell, top=100, bottom=100, left=120, right=120)
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8FAFC")
                
    set_table_horizontal_borders_only(comp_table)

    add_heading_2(doc, "Hardware–Software Co-design")
    add_paragraph_text(doc, "Hardware-Software Co-design is the systematic methodology of designing hardware and software components of a system simultaneously. The goal is to optimize performance, minimize power, reduce cost, and meet real-time requirements by dividing system operations logically:")
    
    # Division of responsibilities lists
    resp_table = doc.add_table(rows=1, cols=2)
    resp_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    resp_table.autofit = False
    
    resp_widths = [Inches(3.2), Inches(3.2)]
    
    # Hardware responsibilities
    cell_hw = resp_table.rows[0].cells[0]
    cell_hw.width = resp_widths[0]
    set_cell_background(cell_hw, "F8FAFC")
    set_cell_margins(cell_hw, top=120, bottom=120, left=150, right=150)
    p_hw_title = cell_hw.paragraphs[0]
    p_hw_title.paragraph_format.space_before = Pt(0)
    p_hw_title.paragraph_format.space_after = Pt(0)
    run_hw_t = p_hw_title.add_run("Hardware Responsibilities")
    apply_text_style(run_hw_t, name="Segoe UI", size_pt=10.5, color_rgb=(15, 23, 42), bold=True)
    p_hw_body = cell_hw.add_paragraph()
    p_hw_body.paragraph_format.space_before = Pt(0)
    p_hw_body.paragraph_format.line_spacing = 1.1
    p_hw_body.paragraph_format.space_after = Pt(2)
    hw_items = [
        "• Processor Selection (microcontroller cores, DSPs).",
        "• Memory Allocation (SRAM, Flash sizing).",
        "• Sensor & Actuator interfaces (pin routing).",
        "• PCB Layout & Schematic design.",
        "• Power supplies, filters, voltage rails.",
        "• Clock trees & oscillator circuits."
    ]
    run_hw_b = p_hw_body.add_run("\n".join(hw_items))
    apply_text_style(run_hw_b, name="Segoe UI", size_pt=9.5, color_rgb=(51, 65, 85))
    
    # Software responsibilities
    cell_sw = resp_table.rows[0].cells[1]
    cell_sw.width = resp_widths[1]
    set_cell_background(cell_sw, "F8FAFC")
    set_cell_margins(cell_sw, top=120, bottom=120, left=150, right=150)
    p_sw_title = cell_sw.paragraphs[0]
    p_sw_title.paragraph_format.space_before = Pt(0)
    p_sw_title.paragraph_format.space_after = Pt(0)
    run_sw_t = p_sw_title.add_run("Software Responsibilities")
    apply_text_style(run_sw_t, name="Segoe UI", size_pt=10.5, color_rgb=(15, 23, 42), bold=True)
    p_sw_body = cell_sw.add_paragraph()
    p_sw_body.paragraph_format.space_before = Pt(0)
    p_sw_body.paragraph_format.line_spacing = 1.1
    p_sw_body.paragraph_format.space_after = Pt(2)
    sw_items = [
        "• Firmware development (compiled C/C++ or Assembly).",
        "• Hardware abstraction layer (HAL) & register writes.",
        "• Device drivers for peripherals (I2C, SPI, UART).",
        "• Signal processing & control algorithms (PID control).",
        "• Real-Time Operating System (RTOS) task scheduling.",
        "• User interface menus & communication packets."
    ]
    run_sw_b = p_sw_body.add_run("\n".join(sw_items))
    apply_text_style(run_sw_b, name="Segoe UI", size_pt=9.5, color_rgb=(51, 65, 85))
    
    set_table_horizontal_borders_only(resp_table, color="CBD5E1")

    # 9. Complete Data Flow & Case Study
    add_heading_1(doc, "9. System Data Flow & Case Study")
    add_paragraph_text(doc, "To solidify the concepts, the system data flow can be traced through a real-world case study: An Automatic Sliding Door System.")
    
    add_paragraph_text(doc, "General System Data Flow Diagram:")
    add_callout(doc, 
        "Environment Stimulus (Person approaching)\n"
        "      ↓\n"
        "Sensors (Ultrasonic sensor captures acoustic return)\n"
        "      ↓\n"
        "Input Interface (Timer measures Echo pin width; converts time to digital distance value)\n"
        "      ↓\n"
        "Microcontroller (CPU executes comparison logic: 'Is distance < 1.5 meters?')\n"
        "      ↓\n"
        "Memory (Reads door-speed settings from Flash/EEPROM, stores active loop states in RAM)\n"
        "      ↓\n"
        "Output Interface (GPIO drives gate high; PWM output adjusts motor start ramp)\n"
        "      ↓\n"
        "Output Actuator (Relay engages power supply; DC motor spins to slide door open)\n"
        "      ↓\n"
        "Communication Interface (Wi-Fi module uploads usage count telemetry to server)",
        title="Sequential Data Flow Trace"
    )
    
    add_heading_2(doc, "Automatic Sliding Door Components mapping:")
    add_bullet_item(doc, "Sensor: ", "An ultrasonic distance sensor detects a human within range.")
    add_bullet_item(doc, "Input Interface: ", "Performs pulse-width timing to feed distance digits to the controller.")
    add_bullet_item(doc, "Microcontroller: ", "Processes variables, computes door status, and triggers interrupts if safety beam is broken.")
    add_bullet_item(doc, "Memory: ", "Keeps the compiled control logic, door timer profiles, and calibration offsets.")
    add_bullet_item(doc, "Output Interface: ", "Outputs GPIO and PWM pulses to feed commands to high-power motor drivers.")
    add_bullet_item(doc, "Actuator: ", "Opens/closes physical sliding doors using a geared DC motor.")
    add_bullet_item(doc, "Power Supply: ", "Provides isolated 5V/3.3V rails for digital chips, and 24V for heavy DC motors.")
    
    doc.save(output_path)
    print(f"Document saved to {output_path}")

# ==========================================
# SCRIPT EXECUTION ENTRY POINT
# ==========================================

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    
    diagram_path = os.path.join(script_dir, "embedded_system_block_diagram.png")
    output_docx_path = os.path.join(project_root, "CT-01_Embedded_Systems.docx")
    
    print("Generating block diagram...")
    try:
        generate_embedded_block_diagram(diagram_path)
    except Exception as e:
        print(f"Error generating block diagram image: {e}")
        
    print("Generating document...")
    try:
        create_embedded_systems_document(output_docx_path, diagram_path)
        print("Success! DOCX generated.")
    except Exception as e:
        print(f"Error generating DOCX: {e}")
        
    print("Execution complete.")

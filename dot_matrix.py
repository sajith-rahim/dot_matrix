import csv
import argparse
import os
import uuid
import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def draw_header_box(c, x, y, width, height, doc_id, date_str, title, desc, tag, author, header_text, page_num, total_pages, font_name, font_size):
    # Colors and line settings
    c.setStrokeColorRGB(0.8, 0.8, 0.8) # Light gray for lines
    c.setStrokeColorRGB(0, 0, 0)
    c.setFillColorRGB(0, 0, 0)
    c.setLineWidth(1)
    
    # Main Box dimensions
    box_top = y
    box_bottom = y - height
    
    # Draw Title (Inside Box)
    c.setFont(font_name, font_size + 4)
    c.drawString(x + 10, box_top - 20, title)
    
    # Draw Description
    c.setFont(font_name, font_size)
    c.drawString(x + 10, box_top - 40, desc)
    
    # Draw Tag
    tag_str = f"{tag}"
    c.drawRightString(x + width - 10, box_top - 20, tag_str)

    # Draw author
    author_str = f"AUTHOR: {author}"
    c.drawRightString(x + width - 10, box_top - 40, author_str)
    
    # Draw Borders
    c.line(x, box_top, x + width, box_top) # Top
    c.line(x + width, box_top, x + width, box_bottom) # Right
    c.line(x + width, box_bottom, x, box_bottom) # Bottom
    c.line(x, box_bottom, x, box_top) # Left

    # Draw Legend Box (Doc ID and Date)
    header_info = f"• DOC ID: {doc_id}      {date_str} •"
    
    c.setFont(font_name, font_size)
    info_width = c.stringWidth(header_info, font_name, font_size)
    info_x = x + (width - info_width) / 2
    
    # Clear line behind text
    c.setFillColorRGB(1, 1, 1) # White
    c.rect(info_x - 5, box_top - 2, info_width + 10, 4, fill=1, stroke=0)
    
    # Draw Text
    c.setFillColorRGB(0, 0, 0)
    c.drawString(info_x, box_top - 4, header_info)
    
    # Draw Box around Legend
    kp_box_height = font_size + 10
    kp_box_y = box_top - (kp_box_height/2)
    c.rect(info_x - 5, kp_box_y, info_width + 10, kp_box_height, stroke=1, fill=0)

    # Draw Header Text (Below Box)
    sep_y = box_bottom - 20
    c.line(x, sep_y, x + width, sep_y)
    
    # Center the header text or put it on the line?
    # Image showed "----HEADING----".
    # User said "Header below".
    # Let's draw it on the line with background clearing like the legend, 
    # or just start text.
    # If the user passes "DATA REPORT", it looks nice centered on the line.
    
    if header_text:
        c.setFont(font_name, font_size)
        h_width = c.stringWidth(header_text, font_name, font_size)
        
        # To match the "---- HEADING ----" look:
        c.setFillColorRGB(1, 1, 1)
        c.rect(x + 20, sep_y - 2, h_width + 10, 4, fill=1, stroke=0)
        c.setFillColorRGB(0, 0, 0)
        c.drawString(x + 25, sep_y - 4, header_text)

    # Draw Page Number (Right side of header line)
    if total_pages > 0:
        page_str = f"({page_num}/{total_pages})"
        c.setFont(font_name, font_size)
        # Clear background for page number
        p_width = c.stringWidth(page_str, font_name, font_size)
        c.setFillColorRGB(1, 1, 1)
        c.rect(x + width - p_width - 5, sep_y - 2, p_width + 10, 4, fill=1, stroke=0)
        c.setFillColorRGB(0, 0, 0)
        c.drawRightString(x + width, sep_y - 4, page_str)

    return sep_y - 20

def convert_csv_to_pdf(input_csv, output_pdf, font_path, font_size, doc_args):
    # Register font
    font_name = 'CustomFont'
    try:
        if font_path and os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            print(f"Using custom font: {font_path}")
        else:
            font_name = 'Courier'
            print(f"Custom font not found at {font_path}. Using Courier.")
    except Exception as e:
        print(f"Error loading font: {e}. Using Courier.")
        font_name = 'Courier'

    c = canvas.Canvas(output_pdf, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Setup
    c.setFont(font_name, font_size)
    line_height = font_size * 1.5
    margin_x = 30
    user_margin_y = 30
    
    # Basic page setup variables
    page_content_height = height - (2 * user_margin_y)
    
    try:
        with open(input_csv, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except FileNotFoundError:
        print(f"Error: Input file '{input_csv}' not found.")
        return

    if not rows:
        print("CSV file is empty.")
        return

    col_widths = []
    if rows:
        num_cols = len(rows[0])
        for i in range(num_cols):
            max_len = 0
            for row in rows:
                if i < len(row):
                    max_len = max(max_len, len(row[i]))
            col_widths.append(max_len)

    # Initial Page Setup
    # Draw Header on first page (or all? Usually headers are on all or just first.
    # Given the complexity, let's put it on the first page, or ask?
    # Usually "Header" implies top of page.
    # But "Description" etc sounds like a Cover Sheet or Document Header.
    # Let's draw it on every page but maybe compact? 
    # "Header should be like the attached image" -> Looks like a document header.
    # Let's draw it on the first page, and simple margins on others?
    # Or every page. Let's do every page for now to be safe/consistent, or maybe just first.
    # It takes a lot of space. Let's assume every page for a "form" feel, but practically first page.
    # Let's trigger it for every page.
    
    current_line = 0
    y = height - user_margin_y
    
    # Draw Header
    header_height = 60 # Box height
    # Plus margin
    
    # Start loop
    # We need to handle pagination manually
    
    # Extract headers
    headers = []
    if rows:
        headers = rows.pop(0) # Remove header from data rows
        # Recalculate cols? No, col_widths calculated from all rows including header is better?
        # Actually I already calculated col_widths including header row in the loop above.
        # But now I popped it.
        # It's fine, col_widths is already computed.
    
    # Calculate available height again because headers take space
    # Header box + separator + Column Headers + Underline
    # Let's say Column Headers take line_height + 5 padding.
    
    col_header_height = line_height + 5
    header_total_height = header_height + 20 + col_header_height
    available_height = height - (2 * user_margin_y) - header_total_height
    
    max_lines_per_page = int(available_height / line_height)
    if max_lines_per_page <= 0:
         print("Error: No space for content.")
         return

    total_rows = len(rows)
    import math
    total_pages = math.ceil(total_rows / max_lines_per_page)
    if total_pages == 0: total_pages = 1 # Handle empty data case
    
    # Doc ID generation
    doc_id = doc_args.get('doc_id')
    if not doc_id:
        doc_id = str(uuid.uuid4()).split('-')[0].upper() # Short UUID for ID
        
    date_str = datetime.date.today().strftime("%d-%m-%Y")
    
    page_num = 1
    
    def setup_page(canvas_obj, y_start, p_num, t_pages):
        # Draw Main Header Box
        new_y = draw_header_box(canvas_obj, margin_x, y_start, width - 2 * margin_x, header_height,
                                doc_id, date_str, 
                                doc_args.get('title', 'Untitled'), 
                                doc_args.get('description', ''), 
                                doc_args.get('tag', ''), 
                                doc_args.get('author', ''),
                                doc_args.get('header', ''),
                                p_num, t_pages,
                                font_name, font_size)
                                
        # Draw Column Headers
        # new_y is where content *could* start, but we want headers there.
        # draw_header_box returns "sep_y - 20".
        # Let's draw headers at new_y. (which is top of content area)
        
        header_y = new_y
        
        # Construct header string
        header_line_str = ""
        # We need to draw each header cell to handle bold/underline individually if needed,
        # but for fixed width CSV feel, constructing a string is easier for alignment.
        # But user wants "Underlined". A single line under the whole header row?
        # Or under each word? "Add the column names... and make them bold and underlined"
        # Usually means the whole header row text.
        
        c.setFont(font_name, font_size)
        # Simulate Bold by drawing twice with slight offset
        # c.setTextRenderMode(2) # method not found on Canvas
        
        current_x = margin_x
        
        # We need to match the alignment of the data.
        # Data loop uses:
        # line_str += f"{cell:<{width_chars}}"
        # We should replicate this construction or draw cell by cell.
        
        header_str = ""
        for i, h_cell in enumerate(headers):
             padding = 2
             if i < len(col_widths):
                 width_chars = col_widths[i] + padding
                 header_str += f"{h_cell.upper():<{width_chars}}" # Make it Uppercase for style? User said "bold and underlined".
             else:
                 header_str += f"{h_cell.upper()}  "
        
        # Draw bold (offset)
        c.setFillColorRGB(0,0,0)
        c.drawString(margin_x, header_y, header_str)
        c.drawString(margin_x + 0.5, header_y, header_str) # Offset X
        
        # Reset text mode (not needed if we didn't change it)
        
        # Draw Underline
        # Under the text.
        underline_y = header_y - 2
        text_width = c.stringWidth(header_str, font_name, font_size)
        c.setLineWidth(1)
        c.line(margin_x, underline_y, margin_x + text_width, underline_y)
        
        # Draw Underline
        # Under the text.
        underline_y = header_y - 2
        text_width = c.stringWidth(header_str, font_name, font_size)
        c.setLineWidth(1)
        c.line(margin_x, underline_y, margin_x + text_width, underline_y)
        
        return header_y - col_header_height
        
    y = setup_page(c, height - user_margin_y, page_num, total_pages)
    
    rows_on_page = 0
    
    for row in rows:
        # Check space (or strictly use max_lines_per_page count)
        if rows_on_page >= max_lines_per_page:
            c.showPage()
            c.setFont(font_name, font_size)
            page_num += 1
            y = setup_page(c, height - user_margin_y, page_num, total_pages)
            rows_on_page = 0
            
        # Construct line string
        line_str = ""
        for i, cell in enumerate(row):
            padding = 2
            if i < len(col_widths):
                width_chars = col_widths[i] + padding
                line_str += f"{cell:<{width_chars}}"
            else:
                line_str += f"{cell}  "
        
        c.drawString(margin_x, y, line_str)
        y -= line_height
        rows_on_page += 1
        
    c.save()
    print(f"PDF generated: {output_pdf}")

def convert_txt_to_pdf(input_txt, output_pdf, font_path, font_size, doc_args):
    # Register font
    font_name = 'CustomFont'
    try:
        if font_path and os.path.exists(font_path):
            pdfmetrics.registerFont(TTFont(font_name, font_path))
            print(f"Using custom font: {font_path}")
        else:
            font_name = 'Courier'
            print(f"Custom font not found at {font_path}. Using Courier.")
    except Exception as e:
        print(f"Error loading font: {e}. Using Courier.")
        font_name = 'Courier'

    c = canvas.Canvas(output_pdf, pagesize=landscape(A4))
    width, height = landscape(A4)
    
    # Setup
    c.setFont(font_name, font_size)
    line_height = font_size * 1.5
    margin_x = 30
    user_margin_y = 30
    
    try:
        with open(input_txt, 'r', encoding='utf-8') as f:
            lines = [line.rstrip() for line in f.readlines()]
    except FileNotFoundError:
        print(f"Error: Input file '{input_txt}' not found.")
        return

    if not lines:
        print("TXT file is empty.")
        return

    # Header calculations
    header_height = 60
    header_total_height = header_height + 20 # 20 is the separator margin
    # No column headers for TXT
    available_height = height - (2 * user_margin_y) - header_total_height
    
    max_lines_per_page = int(available_height / line_height)
    if max_lines_per_page <= 0:
         print("Error: No space for content.")
         return

    total_lines = len(lines)
    import math
    total_pages = math.ceil(total_lines / max_lines_per_page)
    if total_pages == 0: total_pages = 1
    
    # Doc ID generation
    doc_id = doc_args.get('doc_id')
    if not doc_id:
        doc_id = str(uuid.uuid4()).split('-')[0].upper()
        
    date_str = datetime.date.today().strftime("%d-%m-%Y")
    
    page_num = 1
    
    def setup_page(canvas_obj, y_start, p_num, t_pages):
        # Draw Main Header Box
        new_y = draw_header_box(canvas_obj, margin_x, y_start, width - 2 * margin_x, header_height,
                                doc_id, date_str, 
                                doc_args.get('title', 'Untitled'), 
                                doc_args.get('description', ''), 
                                doc_args.get('tag', ''), 
                                doc_args.get('author', ''),
                                doc_args.get('header', ''),
                                p_num, t_pages,
                                font_name, font_size)
        return new_y # Return Y where content starts (no column headers)
        
    y = setup_page(c, height - user_margin_y, page_num, total_pages)
    
    lines_on_page = 0
    
    for line in lines:
        if lines_on_page >= max_lines_per_page:
            c.showPage()
            c.setFont(font_name, font_size)
            page_num += 1
            y = setup_page(c, height - user_margin_y, page_num, total_pages)
            lines_on_page = 0
            
        c.drawString(margin_x, y, line)
        y -= line_height
        lines_on_page += 1
        
    c.save()
    print(f"PDF generated: {output_pdf}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert CSV/TXT to Dot Matrix PDF")
    parser.add_argument("input_file", help="Path to input CSV or TXT file")
    parser.add_argument("--output", help="Path to output PDF file (default: same name/location as input)")
    parser.add_argument("--font", default="Doto.ttf", help="Path to TTF font file")
    parser.add_argument("--font-size", type=int, default=10, help="Font size")
    
    # New arguments
    parser.add_argument("--doc-id", help="Document ID")
    parser.add_argument("--description", default="", help="Description")
    parser.add_argument("--tag", default="", help="Tag")
    parser.add_argument("--author", default="", help="Author")
    parser.add_argument("--header", default="", help="Header Text (below box)")
    parser.add_argument("--title", default="REPORT", help="Title (inside box)")
    
    args = parser.parse_args()

    output_pdf = args.output
    if not output_pdf:
        input_base = os.path.splitext(args.input_file)[0]
        output_pdf = f"{input_base}.pdf"
    
    doc_args = {
        'doc_id': args.doc_id,
        'description': args.description,
        'tag': args.tag,
        'author': args.author,
        'header': args.header,
        'title': args.title
    }
    
    ext = os.path.splitext(args.input_file)[1].lower()
    if ext == '.txt':
        convert_txt_to_pdf(args.input_file, output_pdf, args.font, args.font_size, doc_args)
    else:
        convert_csv_to_pdf(args.input_file, output_pdf, args.font, args.font_size, doc_args)

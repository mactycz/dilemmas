"""
PDF Generator for Question Sets
Creates printable PDFs with cards in 2x4 grid (8 cards per page)
This has been vibe coded, as I have no experience with reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import io
import os


def create_printable_pdf(questions_df):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    
    # Register DejaVu font for Polish characters support
    # Try to use DejaVu font if available, otherwise fall back to Helvetica
    try:
        # Try common font paths
        font_paths = [
            '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
            'C:\\Windows\\Fonts\\DejaVuSans.ttf',  # Windows
            '/System/Library/Fonts/Supplemental/Arial Unicode.ttf',  # macOS
            '/Library/Fonts/Arial Unicode.ttf',  # macOS alternative
        ]
        
        font_registered = False
        for font_path in font_paths:
            if os.path.exists(font_path):
                pdfmetrics.registerFont(TTFont('DejaVu', font_path))
                font_name = 'DejaVu'
                font_registered = True
                break
        
        if not font_registered:
            # Fall back to Helvetica (limited UTF-8 support)
            font_name = 'Helvetica'
    except:
        font_name = 'Helvetica'
    
    # Page settings
    margin = 0.5 * cm
    cards_per_page = 8
    columns = 2
    rows = 4
    
    # Calculate card dimensions
    card_width = (width - 2 * margin) / columns
    card_height = (height - 2 * margin) / rows
    
    for idx, row in questions_df.iterrows():
        position_on_page = idx % cards_per_page
        
        # Start new page if needed
        if position_on_page == 0 and idx > 0:
            c.showPage()
        
        # Calculate column and row position
        col = position_on_page % columns
        row_num = position_on_page // columns
        
        # Calculate card position
        card_x = margin + (col * card_width)
        card_y = height - margin - ((row_num + 1) * card_height)
        
        # Draw card border (solid line for cutting)
        c.setLineWidth(0.5)
        c.setDash(1, 2)  # Dashed line for cutting guide
        c.rect(card_x, card_y, card_width, card_height)
        
        # Add content with padding
        padding = 0.3 * cm
        text_x = card_x + padding
        text_y = card_y + card_height - padding - 0.4 * cm
        
        # Question number
        c.setFont(f"{font_name}-Bold" if font_name == "Helvetica" else font_name, 10)
        c.drawString(text_x, text_y, f"Pytanie {idx + 1}")
        
        # Question text
        c.setFont(font_name, 9)
        question_text = str(row['Pytanie'])
        
        # Wrap text to fit card width
        max_width = card_width - 2 * padding
        question_lines = _wrap_text(c, question_text, max_width, font_name, 9)
        
        # Draw question lines with clipping
        line_height = 0.35 * cm
        current_y = text_y - 0.6 * cm
        
        # Save state and set clipping region
        c.saveState()
        clip_path = c.beginPath()
        clip_path.rect(card_x + padding, card_y + padding, 
                      card_width - 2*padding, card_height - 2*padding)
        c.clipPath(clip_path, stroke=0)
        
        # Draw question (limit to available space)
        max_question_y = card_y + card_height * 0.45
        for line in question_lines:
            if current_y > max_question_y:
                c.drawString(text_x, current_y, line)
                current_y -= line_height
            else:
                break
        
        c.restoreState()
        
        # Draw separator line
        c.setDash()  # Solid line
        c.setLineWidth(0.3)
        separator_y = card_y + card_height * 0.4
        c.line(card_x + padding, separator_y, 
               card_x + card_width - padding, separator_y)
        
        # Options section with clipping
        c.saveState()
        clip_path = c.beginPath()
        clip_path.rect(card_x + padding, card_y + padding, 
                      card_width - 2*padding, separator_y - card_y - padding)
        c.clipPath(clip_path, stroke=0)
        
        options_y = separator_y - 0.4 * cm
        c.setFont(font_name, 8)
        
        # Option A
        option_a_text = str(row['Opcja A'])
        option_a_lines = _wrap_text(c, option_a_text, max_width - 0.5*cm, font_name, 8)
        
        c.drawString(text_x, options_y, "A:")
        for line in option_a_lines:
            if options_y > card_y + padding + 0.3*cm:
                c.setFont(font_name, 8)
                c.drawString(text_x + 0.5*cm, options_y, line)
                options_y -= 0.3 * cm
            else:
                break
        
        # Option B
        options_y -= 0.2 * cm
        c.setFont(font_name, 8)
        option_b_text = str(row['Opcja B'])
        option_b_lines = _wrap_text(c, option_b_text, max_width - 0.5*cm, font_name, 8)
        
        if options_y > card_y + padding + 0.3*cm:
            c.drawString(text_x, options_y, "B:")
            for line in option_b_lines:
                if options_y > card_y + padding + 0.3*cm:
                    c.setFont(font_name, 8)
                    c.drawString(text_x + 0.5*cm, options_y, line)
                    options_y -= 0.3 * cm
                else:
                    break
        
        c.restoreState()
    
    c.save()
    buffer.seek(0)
    return buffer


def _wrap_text(canvas_obj, text, max_width, font_name, font_size):
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        if canvas_obj.stringWidth(word, font_name, font_size) > max_width:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = []
            
            while word:
                chunk = ''
                for char in word:
                    test_chunk = chunk + char
                    if canvas_obj.stringWidth(test_chunk, font_name, font_size) < max_width:
                        chunk = test_chunk
                    else:
                        if chunk:
                            lines.append(chunk)
                            word = word[len(chunk):]
                            chunk = ''
                        break
                if chunk:
                    lines.append(chunk)
                    break
        else:
            test_line = ' '.join(current_line + [word])
            if canvas_obj.stringWidth(test_line, font_name, font_size) < max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return lines
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io

class PDFGenerator:
    @staticmethod
    def generate_treatment_plan_pdf(patient_data, recommendations):
        """Generate a PDF report of the treatment plan."""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        elements.append(Paragraph("Treatment Plan Summary", title_style))
        elements.append(Spacer(1, 12))
        
        # Patient Information
        personal_info = patient_data.get('personal_info', {})
        patient_info_data = [
            ["Patient Name:", personal_info.get('name', 'N/A')],
            ["Age:", personal_info.get('age', 'N/A')],
            ["Gender:", personal_info.get('gender', 'N/A')]
        ]
        
        patient_info_table = Table(patient_info_data, colWidths=[120, 300])
        patient_info_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.grey),
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey)
        ]))
        elements.append(patient_info_table)
        elements.append(Spacer(1, 20))
        
        # Recommendations
        elements.append(Paragraph("Recommendations:", styles['Heading2']))
        for category, items in recommendations.items():
            elements.append(Paragraph(f"{category}:", styles['Heading3']))
            for item in items:
                elements.append(Paragraph(f"• {item}", styles['Normal']))
            elements.append(Spacer(1, 12))
        
        doc.build(elements)
        buffer.seek(0)
        return buffer

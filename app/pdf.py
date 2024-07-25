from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from io import BytesIO

def create_pdf(data, image_paths):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []

    # Styles
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Center', alignment=1))
    styles.add(ParagraphStyle(name='Right', alignment=2))

    # Title
    story.append(Paragraph("Detalles del trabajo", styles['Heading1']))
    story.append(Spacer(1, 0.25*inch))

    # Código and Orden de trabajo
    codigo_ot = [
        [Paragraph(f"<b>Código:</b> {data['codigo']}", styles['Normal'])],
        [Paragraph(f"<b>N° Orden de trabajo:</b> {data['orden_trabajo']}", styles['Normal'])]
    ]
    story.append(Table(codigo_ot, colWidths=[6*inch], style=[('ALIGN', (0,0), (-1,-1), 'RIGHT')]))
    story.append(Spacer(1, 0.25*inch))

    # Details table
    details = [
        [Paragraph("<b>Fecha:</b>", styles['Normal']), 
         Paragraph("<b>Hora inicio:</b>", styles['Normal']), 
         Paragraph("<b>Hora fin:</b>", styles['Normal']), 
         Paragraph("<b>Responsable:</b>", styles['Normal'])],
        [data['fecha'], data['hora_inicio'], data['hora_fin'], data['responsable']]
    ]
    t = Table(details, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 2*inch])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.25*inch))

    # Tipo de mantenimiento
    story.append(Paragraph(f"<b>Tipo de mantenimiento:</b> {data['tipo_mantenimiento']}", styles['Center']))
    story.append(Spacer(1, 0.25*inch))

    # System details
    system_details = [
        [Paragraph("<b>Sistema:</b>", styles['Normal']), 
         Paragraph("<b>Subsistema:</b>", styles['Normal']), 
         Paragraph("<b>Elemento:</b>", styles['Normal'])],
        [data['sistema'], data['subsistema'], data['elemento']]
    ]
    t = Table(system_details, colWidths=[2*inch, 2*inch, 2*inch])
    t.setStyle(TableStyle([
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
    ]))
    story.append(t)
    story.append(Spacer(1, 0.25*inch))

    # Maintenance title
    story.append(Paragraph(data['titulo_mantenimiento'], styles['Heading2']))
    story.append(Spacer(1, 0.1*inch))

    # Description
    story.append(Paragraph("<b>Descripción:</b>", styles['Normal']))
    story.append(Paragraph(data['descripcion'], styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # Observations
    story.append(Paragraph("<b>Observaciones:</b>", styles['Normal']))
    story.append(Paragraph(data['observaciones'], styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # Photographic record
    story.append(Paragraph("<b>Registro fotográfico:</b>", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))

    # Add images (up to 10)
    for i, img_path in enumerate(image_paths[:10]):
        img = Image(img_path, width=3*inch, height=2*inch)
        story.append(img)
        story.append(Spacer(1, 0.1*inch))

    # Build the PDF
    doc.build(story)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf
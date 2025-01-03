

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import textwrap
import os


class PDFGenerator:
    @staticmethod
    def generate_laudo_pdf(laudo, user, output_path):
        if not os.path.exists('temp'):
            os.makedirs('temp')

        c = canvas.Canvas(output_path, pagesize=letter)

        # Cabeçalho
        c.setFont("Helvetica-Bold", 16)
        c.drawString(50, 750, "Laudo Psicológico")

        # Informações básicas
        c.setFont("Helvetica", 12)
        c.drawString(50, 720, f"Paciente: {laudo.paciente_nome}")
        c.drawString(50, 700, f"Data: {laudo.criado_em.strftime('%d/%m/%Y')}")
        c.drawString(50, 680, f"Psicólogo: {user.nome} - CRP: {user.crp}")

        # Diagnóstico
        text_object = c.beginText(50, 650)
        text_object.setFont("Helvetica", 12)

        wrapped_text = textwrap.fill(laudo.diagnostico, width=80)
        for line in wrapped_text.split('\n'):
            text_object.textLine(line)

        c.drawText(text_object)
        c.save()

        return output_path
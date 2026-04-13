from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class PDFMaker:
    def __init__(self, output_file):
        self.doc = SimpleDocTemplate(output_file)
        self.styles = getSampleStyleSheet()

    def build_pdf(self, data):
        story = []
        lines = data.split("\n")

        buffer = []
        table_buffer = []

        for line in lines:
            line = line.strip()

            # ---- HEADINGS ----
            if line.startswith("## "):
                story.append(Paragraph(line[3:], self.styles["Heading2"]))
                story.append(Spacer(1, 10))

            elif line.startswith("# "):
                story.append(Paragraph(line[2:], self.styles["Heading1"]))
                story.append(Spacer(1, 12))

            # ---- BULLET POINTS ----
            elif line.startswith("- "):
                buffer.append(Paragraph(line[2:], self.styles["Normal"]))

            # ---- NUMBERED LIST ----
            elif line[:2].isdigit() and line[2] == ".":
                buffer.append(Paragraph(line[3:], self.styles["Normal"]))

            # ---- TABLE DETECTION ----
            elif line.startswith("|") and line.endswith("|"):
                row = [cell.strip() for cell in line.split("|")[1:-1]]
                table_buffer.append(row)

            # ---- NORMAL TEXT ----
            else:
                # flush lists
                if buffer:
                    story.append(ListFlowable(buffer))
                    story.append(Spacer(1, 8))
                    buffer = []

                # flush tables
                if table_buffer:
                    table = Table(table_buffer)
                    table.setStyle(TableStyle([
                        ("GRID", (0,0), (-1,-1), 1, colors.black),
                        ("BACKGROUND", (0,0), (-1,0), colors.grey),
                        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
                    ]))
                    story.append(table)
                    story.append(Spacer(1, 12))
                    table_buffer = []

                if line:
                    story.append(Paragraph(line, self.styles["Normal"]))
                    story.append(Spacer(1, 8))

        # final flush
        if buffer:
            story.append(ListFlowable(buffer))

        if table_buffer:
            table = Table(table_buffer)
            table.setStyle(TableStyle([
                ("GRID", (0,0), (-1,-1), 1, colors.black),
            ]))
            story.append(table)

        self.doc.build(story)

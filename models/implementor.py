from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from io import BytesIO


class PDFMaker:
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.wrap = self.styles["BodyText"]

    # MAIN PDF CREATOR
    def generate_pdf_content(self, data):
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        elements = []

        elements += self.__build_title()

        elements += self.__build_campaign_overview(data)
        elements += self.__build_timeline(data)
        elements += self.__build_execution_workflow(data)
        elements += self.__build_channel_strategy(data)
        elements += self.__build_conversion_strategy(data)
        elements += self.__build_content_ideas(data)

        doc.build(
            elements,
            onFirstPage=self.__add_footer,
            onLaterPages=self.__add_footer
        )

        buffer.seek(0)
        return buffer.getvalue()

    # HELPER FUNCTIONS FOR DIFFERENT SECTIONS

    def __build_title(self):
        return [
            Paragraph("AI-Generated Marketing Plan", self.styles["Heading1"]),
            Spacer(1, 16)
        ]

    def __build_campaign_overview(self, data):
        elements = [
            Paragraph("1. Campaign Overview", self.styles["Heading2"]),
            Spacer(1, 10)
        ]

        for key, value in data["campaign_overview"].items():
            elements.append(
                Paragraph(
                    self.__clean_text(f"<b>{self.__format_key(key)}:</b> {value}"),
                    self.wrap
                )
            )
            elements.append(Spacer(1, 6))

        elements.append(Spacer(1, 10))
        return elements

    def __build_timeline(self, data):
        elements = [
            Paragraph("2. Marketing Timeline", self.styles["Heading2"]),
            Spacer(1, 10)
        ]

        table_data = [["Week", "Action"]]

        for item in data["marketing_timeline"]:
            table_data.append([
                str(item["week"]),
                Paragraph(self.__clean_text(item["action"]), self.wrap)
            ])

        elements.append(self.__create_table(
            table_data,[60, 360]
        ))

        elements.append(Spacer(1, 10))
        return elements

    def __build_execution_workflow(self, data):
        elements = [
            Paragraph("3. Execution Workflow", self.styles["Heading2"]),
            Spacer(1, 10)
        ]

        for i, step in enumerate(data["execution_workflow"], 1):
            elements.append(
                Paragraph(f"{i}. {self.__clean_text(step)}", self.wrap)
            )
            elements.append(Spacer(1, 4))

        elements.append(Spacer(1, 10))
        return elements

    def __build_channel_strategy(self, data):
        elements = [
            Paragraph("4. Channel Strategy", self.styles["Heading2"]),
            Spacer(1, 10)
        ]

        # ---- Organic ----
        elements.append(Paragraph("Organic", self.styles["Heading3"]))
        elements += self.__build_channel_table(data["channel_strategy"]["organic"], table_type="organic")
        elements.append(Spacer(1, 10))

        # ---- Paid ----
        elements.append(Paragraph("Paid", self.styles["Heading3"]))
        elements += self.__build_channel_table(data["channel_strategy"]["paid"], table_type="paid")

        elements.append(Spacer(1, 10))
        return elements

    # For Organic and Paid tables
    def __build_channel_table(self, rows, table_type="organic"):
        if table_type == "organic":
            headers = ["Channel", "Content", "Frequency", "Example"]

            def extract(row):
                return [
                    self.__clean_text(row.get("channel", "")),
                    self.__clean_text(row.get("content_type", "")),
                    self.__clean_text(row.get("frequency", "")),
                    self.__clean_text(row.get("example", "")),
                ]

        elif table_type == "paid":
            headers = ["Platform", "Format", "Targeting", "Budget"]

            def extract(row):
                return [
                    self.__clean_text(row.get("platform", "")),
                    self.__clean_text(row.get("ad_format", "")),
                    self.__clean_text(row.get("targeting", "")),
                    self.__clean_text(row.get("budget", "")),
                ]

        else:
            raise ValueError(f"Unknown table_type: {table_type}")

        table_data = [headers]

        for row in rows:
            table_data.append([Paragraph(cell, self.wrap) for cell in extract(row)])

        return [self.__create_table(table_data, [80, 120, 200, 100])]

    def __build_conversion_strategy(self, data):
        conv = data["conversion_strategy"]

        elements = [
            Paragraph("5. Conversion Strategy", self.styles["Heading2"]),
            Spacer(1, 10),
            Paragraph(
                f"<b>Booking Method:</b> {self.__clean_text(conv['booking_method'])}",
                self.wrap
            ),
            Spacer(1, 6),
            Paragraph("<b>Call To Action</b>", self.styles["Heading3"]),
            Paragraph(self.__clean_text(conv["cta"]["text"]), self.wrap),
            Spacer(1, 6),
            Paragraph("<b>Urgency Tactics:</b>", self.wrap),
        ]

        for text in conv["urgency_tactics"]:
            elements.append(Paragraph(f"• {self.__clean_text(text)}", self.wrap))

        elements.append(Spacer(1, 10))
        return elements

    def __build_content_ideas(self, data):
        elements = [
            Paragraph("6. Content Ideas", self.styles["Heading2"]),
            Spacer(1, 10)
        ]

        for idea in data["content_ideas"]:
            elements.append(
                Paragraph(
                    self.__clean_text(idea["title"]),
                    self.styles["Heading3"]
                )
            )
            elements.append(
                Paragraph(self.__clean_text(idea["description"]), self.wrap)
            )
            elements.append(Spacer(1, 6))

        return elements

    # Table maker
    def __create_table(self, data, col_widths):
        table = Table(data, colWidths=col_widths)

        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2E3B4E")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))

        return table

    # Helper functions
    @staticmethod
    def __format_key(key):
        return key.replace("_", " ").title()

    @staticmethod
    def __clean_text(text):   # Helps deal with LLM garbage letters that are not ASCII and could potentially lead to errors
        if not isinstance(text, str):
            return text

        return (
            text
            .replace("–", "-")
            .replace("—", "-")
            .replace("‑", "-")
            .replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("\u2022", "-")
            .encode("ascii", "ignore")
            .decode("ascii")
        )

    @staticmethod
    def __add_footer(canvas, doc):
        canvas.drawCentredString(300, 20, "Generated by AI Planner")
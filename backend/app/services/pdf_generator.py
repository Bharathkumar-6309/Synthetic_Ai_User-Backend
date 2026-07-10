"""
PDF Generator — creates downloadable research reports using ReportLab.
"""
from datetime import datetime
from pathlib import Path
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak


class PDFGenerator:
    """Generate PDF research reports from experiment data."""

    def __init__(self, output_dir: str = "reports") -> None:
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self) -> None:
        """Setup custom paragraph styles."""
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=30,
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#34495E'),
            spaceAfter=12,
        ))
        self.styles.add(ParagraphStyle(
            name='CustomBody',
            parent=self.styles['BodyText'],
            fontSize=10,
            textColor=colors.HexColor('#2C3E50'),
            spaceAfter=12,
        ))

    def generate_report(
        self,
        experiment: dict[str, Any],
        personas: list[dict[str, Any]],
        insights: dict[str, Any],
        validation_scoring: dict[str, Any],
        recommendations: list[dict[str, Any]],
        response_highlights: list[dict[str, Any]],
    ) -> str:
        """Generate a complete PDF report and return the file path."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{experiment.get('id', 'unknown')}_{timestamp}.pdf"
        filepath = self.output_dir / filename

        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        story = []
        
        # Title page
        story.append(Paragraph(experiment.get('title', 'Research Report'), self.styles['CustomTitle']))
        story.append(Spacer(1, 0.2 * inch))
        
        # Experiment overview
        story.append(Paragraph("Experiment Overview", self.styles['CustomHeading']))
        story.append(Paragraph(
            f"<b>Product:</b> {experiment.get('product_description', 'N/A')}",
            self.styles['CustomBody']
        ))
        story.append(Paragraph(
            f"<b>Target Audience:</b> {experiment.get('target_audience', 'N/A')}",
            self.styles['CustomBody']
        ))
        story.append(Paragraph(
            f"<b>Research Objectives:</b> {experiment.get('research_objectives', 'N/A')}",
            self.styles['CustomBody']
        ))
        story.append(Spacer(1, 0.3 * inch))

        # Validation scores
        story.append(Paragraph("Product Validation Scores", self.styles['CustomHeading']))
        score_data = [
            ["Metric", "Score"],
            ["Overall Adoption Score", f"{validation_scoring.get('overall_adoption_score', 0):.1f}/10"],
            ["Product Fit Score", f"{validation_scoring.get('overall_product_fit_score', 0):.1f}/10"],
            ["Would Use Percentage", f"{validation_scoring.get('would_use_percentage', 0)}%"],
            ["Would Pay Percentage", f"{validation_scoring.get('would_pay_percentage', 0)}%"],
        ]
        score_table = Table(score_data, colWidths=[3 * inch, 2 * inch])
        score_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#3498DB')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        story.append(score_table)
        story.append(Spacer(1, 0.3 * inch))

        # Insights
        story.append(PageBreak())
        story.append(Paragraph("Research Insights", self.styles['CustomHeading']))
        
        # Themes
        if insights.get('themes'):
            story.append(Paragraph("Key Themes", self.styles['CustomHeading']))
            for theme in insights['themes'][:5]:
                story.append(Paragraph(
                    f"• {theme.get('theme', 'N/A')} ({theme.get('mentions_pct', 0)}% mentioned)",
                    self.styles['CustomBody']
                ))
            story.append(Spacer(1, 0.2 * inch))

        # Sentiment
        if insights.get('sentiment'):
            story.append(Paragraph("Sentiment Analysis", self.styles['CustomHeading']))
            sentiment_text = ", ".join([
                f"{k}: {v}" for k, v in insights['sentiment'].items()
            ])
            story.append(Paragraph(sentiment_text, self.styles['CustomBody']))
            story.append(Spacer(1, 0.2 * inch))

        # Key quotes
        if insights.get('key_quotes'):
            story.append(Paragraph("Key Persona Quotes", self.styles['CustomHeading']))
            for quote in insights['key_quotes'][:5]:
                story.append(Paragraph(
                    f"<i>\"{quote.get('quote', 'N/A')}\"</i> — {quote.get('persona', 'Anonymous')}",
                    self.styles['CustomBody']
                ))
            story.append(Spacer(1, 0.2 * inch))

        # User wants summary
        if insights.get('user_wants_summary'):
            story.append(Paragraph("User Needs Summary", self.styles['CustomHeading']))
            story.append(Paragraph(insights['user_wants_summary'], self.styles['CustomBody']))
            story.append(Spacer(1, 0.3 * inch))

        # Recommendations
        if recommendations:
            story.append(PageBreak())
            story.append(Paragraph("Recommendations", self.styles['CustomHeading']))
            for i, rec in enumerate(recommendations, 1):
                priority_color = {
                    'high': colors.HexColor('#E74C3C'),
                    'medium': colors.HexColor('#F39C12'),
                    'low': colors.HexColor('#27AE60'),
                }.get(rec.get('priority', 'medium'), colors.black)
                
                story.append(Paragraph(
                    f"{i}. {rec.get('suggestion', 'N/A')} [{rec.get('category', 'General')}]",
                    self.styles['CustomBody']
                ))
                story.append(Paragraph(
                    f"   Priority: {rec.get('priority', 'medium').upper()}",
                    ParagraphStyle(
                        'Priority',
                        parent=self.styles['CustomBody'],
                        textColor=priority_color,
                        fontSize=9,
                    )
                ))
                story.append(Spacer(1, 0.1 * inch))

        # Persona profiles
        if personas:
            story.append(PageBreak())
            story.append(Paragraph("Persona Profiles", self.styles['CustomHeading']))
            for persona in personas[:6]:  # Limit to 6 personas
                story.append(Paragraph(
                    f"<b>{persona.get('name', 'Anonymous')}</b> — {persona.get('occupation', 'N/A')}, Age {persona.get('age', 'N/A')}",
                    self.styles['CustomBody']
                ))
                story.append(Paragraph(
                    f"Bio: {persona.get('bio', 'N/A')}",
                    self.styles['CustomBody']
                ))
                story.append(Paragraph(
                    f"Adoption Score: {persona.get('adoption_score', 0)}/10, Product Fit: {persona.get('product_fit_score', 0)}/10",
                    self.styles['CustomBody']
                ))
                story.append(Spacer(1, 0.2 * inch))

        # Response highlights
        if response_highlights:
            story.append(PageBreak())
            story.append(Paragraph("Response Highlights", self.styles['CustomHeading']))
            for highlight in response_highlights[:10]:
                story.append(Paragraph(
                    f"<b>Q:</b> {highlight.get('question', 'N/A')}",
                    self.styles['CustomBody']
                ))
                story.append(Paragraph(
                    f"<b>{highlight.get('persona_name', 'Anonymous')}:</b> {highlight.get('answer', 'N/A')}",
                    self.styles['CustomBody']
                ))
                story.append(Spacer(1, 0.15 * inch))

        # Footer
        story.append(PageBreak())
        story.append(Paragraph(
            f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}",
            ParagraphStyle(
                'Footer',
                parent=self.styles['CustomBody'],
                fontSize=8,
                textColor=colors.gray,
            )
        ))

        doc.build(story)
        return str(filepath)

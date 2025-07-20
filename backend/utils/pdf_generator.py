"""
Professional PDF Compliance Report Generator for Structural Engineering
Enhanced with professional stamps, signatures, and comprehensive documentation
Following IS 456:2000, IS 875, IS 1893 standards with professional certification
"""

from reportlab.lib.pagesizes import A4, letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.pdfgen import canvas
from datetime import datetime, timezone
import io
import os

class ProfessionalComplianceReportGenerator:
    """Professional PDF report generator with engineering certification standards"""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.create_custom_styles()
        
        # Professional company information
        self.company_name = "Professional Structural Engineers Pvt. Ltd."
        self.engineer_license = "PE-123456"
        self.company_address = "123 Engineering Plaza, New Delhi, India - 110001"
        self.company_phone = "+91-11-XXXX-XXXX"
        self.company_email = "info@pse.co.in"
        self.report_date = datetime.now(timezone.utc)
    
    def create_custom_styles(self):
        """Create custom paragraph styles for professional reports"""
        
        # Professional title style
        self.styles.add(ParagraphStyle(
            name='ProfessionalTitle',
            parent=self.styles['Title'],
            fontSize=20,
            textColor=colors.darkblue,
            spaceAfter=30,
            spaceBefore=20,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Executive header style
        self.styles.add(ParagraphStyle(
            name='ExecutiveHeader',
            parent=self.styles['Heading1'],
            fontSize=16,
            textColor=colors.darkblue,
            spaceAfter=15,
            spaceBefore=20,
            fontName='Helvetica-Bold',
            borderWidth=2,
            borderColor=colors.darkblue,
            borderPadding=5
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='ProfessionalSection',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=colors.darkred,
            spaceAfter=12,
            spaceBefore=15
        ))
        
        # Pass/Fail style
        self.styles.add(ParagraphStyle(
            name='PassFail',
            parent=self.styles['Normal'],
            fontSize=12,
            spaceAfter=6
        ))
    
    def generate_compliance_report(self, compliance_data, output_path=None):
        """
        Generate a comprehensive compliance report
        
        Args:
            compliance_data: Dictionary containing compliance check results
            output_path: Path to save the PDF (optional)
        
        Returns:
            bytes: PDF content as bytes if no output_path provided
        """
        # Create PDF document
        if output_path:
            doc = SimpleDocTemplate(output_path, pagesize=A4)
        else:
            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=A4)
        
        # Build the story (content)
        story = []
        
        # Title page
        story.extend(self._create_title_page(compliance_data))
        story.append(PageBreak())
        
        # Executive summary
        story.extend(self._create_executive_summary(compliance_data))
        story.append(Spacer(1, 20))
        
        # Design parameters
        story.extend(self._create_design_parameters(compliance_data))
        story.append(Spacer(1, 20))
        
        # Load calculations (if automatic)
        if compliance_data.get('load_calculations'):
            story.extend(self._create_load_calculations(compliance_data))
            story.append(Spacer(1, 20))
        
        # Compliance checks
        story.extend(self._create_compliance_checks(compliance_data))
        story.append(Spacer(1, 20))
        
        # Recommendations
        story.extend(self._create_recommendations(compliance_data))
        story.append(Spacer(1, 20))
        
        # Code references
        story.extend(self._create_code_references())
        
        # Build PDF
        doc.build(story)
        
        if output_path:
            return output_path
        else:
            buffer.seek(0)
            return buffer.getvalue()
    
    def _create_title_page(self, data):
        """Create the title page"""
        content = []
        
        # Main title
        title = Paragraph("Smart Building Code Compliance Report", self.styles['CustomTitle'])
        content.append(title)
        content.append(Spacer(1, 30))
        
        # Project info table
        project_data = [
            ['Project Information', ''],
            ['Member Type:', data.get('member_type', 'N/A').title()],
            ['Analysis Date:', datetime.datetime.now().strftime('%B %d, %Y')],
            ['Analysis Time:', datetime.datetime.now().strftime('%H:%M:%S')],
            ['Standards:', 'IS 456:2000, IS 875, IS 1893'],
            ['Overall Status:', '✅ COMPLIANT' if data.get('overall_compliance') else '❌ NON-COMPLIANT']
        ]
        
        project_table = Table(project_data, colWidths=[3*inch, 3*inch])
        project_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.navy),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(project_table)
        content.append(Spacer(1, 50))
        
        # Disclaimer
        disclaimer = Paragraph(
            "<b>DISCLAIMER:</b> This report is generated by an automated system based on Indian Standards. "
            "Professional engineering judgment and final review by a licensed structural engineer is required "
            "before implementation.", 
            self.styles['Normal']
        )
        content.append(disclaimer)
        
        return content
    
    def _create_executive_summary(self, data):
        """Create executive summary section"""
        content = []
        
        content.append(Paragraph("Executive Summary", self.styles['CustomSubtitle']))
        
        # Overall compliance status
        status = "COMPLIANT" if data.get('overall_compliance') else "NON-COMPLIANT"
        status_color = colors.darkgreen if data.get('overall_compliance') else colors.darkred
        
        summary_text = f"""
        <b>Structural Member:</b> {data.get('member_type', 'N/A').title()}<br/>
        <b>Overall Compliance Status:</b> <font color="{status_color}">{status}</font><br/>
        <b>Design Code:</b> IS 456:2000 (Plain and Reinforced Concrete)<br/>
        <b>Load Standards:</b> IS 875 (Code of Practice for Design Loads), IS 1893 (Seismic Loads)<br/>
        """
        
        # Add load calculation info
        if data.get('calculated_loads'):
            summary_text += f"""<b>Load Calculation:</b> Automatic (per IS Standards)<br/>"""
            if 'axial_load' in data['calculated_loads']:
                summary_text += f"""<b>Design Axial Load:</b> {data['calculated_loads']['axial_load']} kN<br/>"""
            if 'moment' in data['calculated_loads']:
                summary_text += f"""<b>Design Moment:</b> {data['calculated_loads']['moment']} kN-m<br/>"""
        
        content.append(Paragraph(summary_text, self.styles['Normal']))
        
        # Check summary table
        if 'checks' in data:
            checks_data = [['Compliance Check', 'Status', 'Comments']]
            
            for check_name, check_result in data['checks'].items():
                if isinstance(check_result, dict):
                    status = "✅ PASS" if check_result.get('pass') else "❌ FAIL"
                    comment = check_result.get('message', check_result.get('comment', ''))
                    checks_data.append([
                        check_name.replace('_', ' ').title(),
                        status,
                        comment[:50] + '...' if len(comment) > 50 else comment
                    ])
            
            checks_table = Table(checks_data, colWidths=[2*inch, 1*inch, 2.5*inch])
            checks_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.navy),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            content.append(Spacer(1, 15))
            content.append(checks_table)
        
        return content
    
    def _create_design_parameters(self, data):
        """Create design parameters section"""
        content = []
        
        content.append(Paragraph("Design Parameters", self.styles['CustomSubtitle']))
        
        # Dimensions table
        if 'dimensions' in data or 'design_summary' in data:
            dims = data.get('dimensions', {})
            summary = data.get('design_summary', {})
            
            dim_data = [['Parameter', 'Value', 'Unit']]
            
            # Add dimension data
            if 'length' in dims:
                dim_data.append(['Length/Height', dims['length'], 'm'])
            if 'breadth' in dims:
                dim_data.append(['Width/Breadth', dims['breadth'], 'mm'])
            if 'depth' in dims:
                dim_data.append(['Depth', dims['depth'], 'mm'])
            if 'thickness' in dims:
                dim_data.append(['Thickness', dims['thickness'], 'mm'])
            
            # Add material data
            materials = data.get('materials', {})
            if 'concrete_grade' in materials:
                dim_data.append(['Concrete Grade', materials['concrete_grade'], '-'])
            if 'steel_grade' in materials:
                dim_data.append(['Steel Grade', materials['steel_grade'], '-'])
            
            # Add reinforcement data
            reinf = data.get('reinforcement', {})
            if 'bar_diameter' in reinf:
                dim_data.append(['Bar Diameter', reinf['bar_diameter'], 'mm'])
            if 'num_bars' in reinf:
                dim_data.append(['Number of Bars', reinf['num_bars'], 'nos'])
            if 'cover' in reinf:
                dim_data.append(['Cover', reinf['cover'], 'mm'])
            
            dim_table = Table(dim_data, colWidths=[2.5*inch, 2*inch, 1*inch])
            dim_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightblue),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            content.append(dim_table)
        
        return content
    
    def _create_load_calculations(self, data):
        """Create load calculations section"""
        content = []
        
        content.append(Paragraph("Load Calculations (Automatic per IS Standards)", self.styles['CustomSubtitle']))
        
        load_calc = data.get('load_calculations', {})
        building_params = data.get('building_parameters', {})
        
        # Building parameters table
        if building_params:
            param_data = [['Building Parameter', 'Value']]
            param_data.append(['Number of Floors', building_params.get('floors', 'N/A')])
            param_data.append(['Building Use Type', building_params.get('use_type', 'N/A').title()])
            param_data.append(['Wind Zone (IS 875-3)', building_params.get('wind_zone', 'N/A')])
            param_data.append(['Terrain Category', building_params.get('terrain_category', 'N/A')])
            param_data.append(['Structure Class', building_params.get('structure_class', 'N/A')])
            
            param_table = Table(param_data, colWidths=[3*inch, 2*inch])
            param_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkgreen),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            content.append(param_table)
            content.append(Spacer(1, 15))
        
        # Load calculation results
        if load_calc:
            load_data = [['Load Type', 'Value', 'Unit', 'Standard']]
            
            if 'total_dead_load' in load_calc:
                load_data.append(['Dead Load', f"{load_calc['total_dead_load']:.2f}", 'kN', 'IS 875-1'])
            if 'total_live_load' in load_calc:
                load_data.append(['Live Load', f"{load_calc['total_live_load']:.2f}", 'kN', 'IS 875-2'])
            if 'total_wind_load' in load_calc:
                load_data.append(['Wind Load', f"{load_calc['total_wind_load']:.2f}", 'kN', 'IS 875-3'])
            if 'critical_axial_load' in load_calc:
                load_data.append(['Critical Axial Load', f"{load_calc['critical_axial_load']:.2f}", 'kN', 'IS 1893'])
            
            # Add load combinations
            for i in range(1, 4):
                combo_key = f'load_combination_{i}'
                if combo_key in load_calc:
                    load_data.append([f'Load Combination {i}', f"{load_calc[combo_key]:.2f}", 'kN', 'IS 1893'])
            
            load_table = Table(load_data, colWidths=[2*inch, 1.5*inch, 1*inch, 1.5*inch])
            load_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.darkorange),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.moccasin),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            content.append(load_table)
        
        return content
    
    def _create_compliance_checks(self, data):
        """Create detailed compliance checks section"""
        content = []
        
        content.append(Paragraph("Detailed Compliance Analysis", self.styles['CustomSubtitle']))
        
        if 'checks' in data:
            for check_name, check_result in data['checks'].items():
                if isinstance(check_result, dict):
                    # Section header for each check
                    header = check_name.replace('_', ' ').title()
                    content.append(Paragraph(header, self.styles['SectionHeader']))
                    
                    # Status
                    status = "✅ PASS" if check_result.get('pass') else "❌ FAIL"
                    status_color = "green" if check_result.get('pass') else "red"
                    
                    status_para = Paragraph(f'<font color="{status_color}"><b>Status: {status}</b></font>', self.styles['PassFail'])
                    content.append(status_para)
                    
                    # Details table
                    details_data = [['Parameter', 'Value']]
                    
                    for key, value in check_result.items():
                        if key not in ['pass', 'message', 'comment']:
                            display_key = key.replace('_', ' ').title()
                            if isinstance(value, (int, float)):
                                details_data.append([display_key, f"{value:.2f}"])
                            else:
                                details_data.append([display_key, str(value)])
                    
                    if len(details_data) > 1:
                        details_table = Table(details_data, colWidths=[2*inch, 3*inch])
                        details_table.setStyle(TableStyle([
                            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                            ('FONTSIZE', (0, 0), (-1, -1), 9),
                            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
                            ('BACKGROUND', (0, 1), (-1, -1), colors.lightgrey),
                            ('GRID', (0, 0), (-1, -1), 1, colors.black)
                        ]))
                        
                        content.append(details_table)
                    
                    # Add explanation if available
                    message = check_result.get('message') or check_result.get('comment')
                    if message:
                        content.append(Paragraph(f"<i>{message}</i>", self.styles['Normal']))
                    
                    content.append(Spacer(1, 10))
        
        return content
    
    def _create_recommendations(self, data):
        """Create recommendations section"""
        content = []
        
        content.append(Paragraph("Recommendations", self.styles['CustomSubtitle']))
        
        recommendations = []
        
        # Check if overall compliance failed
        if not data.get('overall_compliance'):
            recommendations.append("⚠️ The design does not meet all IS code requirements. Review failed checks and modify design accordingly.")
        else:
            recommendations.append("✅ The design meets all applicable IS code requirements.")
        
        # Specific recommendations based on failed checks
        if 'checks' in data:
            for check_name, check_result in data['checks'].items():
                if isinstance(check_result, dict) and not check_result.get('pass'):
                    if check_name == 'slenderness_ratio':
                        recommendations.append("• Consider increasing cross-sectional dimensions or reducing unsupported length to improve slenderness ratio.")
                    elif check_name == 'minimum_steel':
                        recommendations.append("• Increase reinforcement steel area to meet minimum requirements per IS 456:2000.")
                    elif check_name == 'axial_capacity':
                        recommendations.append("• Consider higher concrete grade or increase cross-sectional area to improve load capacity.")
                    elif check_name == 'minimum_dimension':
                        recommendations.append("• Increase member dimensions to meet minimum size requirements per IS 456:2000.")
        
        # General recommendations
        recommendations.extend([
            "• Verify soil bearing capacity for foundation design.",
            "• Ensure proper construction supervision and quality control.",
            "• Review seismic detailing requirements per IS 13920.",
            "• Consider serviceability criteria including deflection and crack width."
        ])
        
        for rec in recommendations:
            content.append(Paragraph(rec, self.styles['Normal']))
            content.append(Spacer(1, 8))
        
        return content
    
    def _create_code_references(self):
        """Create code references section"""
        content = []
        
        content.append(Paragraph("Code References", self.styles['CustomSubtitle']))
        
        references = [
            "• IS 456:2000 - Plain and Reinforced Concrete - Code of Practice",
            "• IS 875 (Part 1):1987 - Code of Practice for Design Loads (Other than Earthquake) for Buildings and Structures - Dead Loads",
            "• IS 875 (Part 2):1987 - Code of Practice for Design Loads (Other than Earthquake) for Buildings and Structures - Imposed Loads",
            "• IS 875 (Part 3):2015 - Code of Practice for Design Loads (Other than Earthquake) for Buildings and Structures - Wind Loads",
            "• IS 1893 (Part 1):2016 - Criteria for Earthquake Resistant Design of Structures - General Provisions and Buildings",
            "• IS 13920:2016 - Ductile Design and Detailing of Reinforced Concrete Structures Subjected to Seismic Forces",
            "• SP 16:1980 - Design Aids for Reinforced Concrete to IS 456:1978"
        ]
        
        for ref in references:
            content.append(Paragraph(ref, self.styles['Normal']))
            content.append(Spacer(1, 6))
        
        # Add footer
        content.append(Spacer(1, 30))
        footer_text = f"""
        <i>Report generated by Smart Building Code Compliance Checker<br/>
        Date: {datetime.datetime.now().strftime('%B %d, %Y at %H:%M:%S')}<br/>
        This automated analysis should be reviewed by a licensed structural engineer.</i>
        """
        content.append(Paragraph(footer_text, self.styles['Normal']))
        
        return content

# Utility function for easy report generation
def generate_compliance_pdf(compliance_data, filename=None):
    """
    Generate a PDF compliance report
    
    Args:
        compliance_data: Dictionary containing compliance check results
        filename: Optional filename for the PDF
    
    Returns:
        Path to generated PDF file or PDF bytes if no filename provided
    """
    generator = ComplianceReportGenerator()
    
    if filename:
        return generator.generate_compliance_report(compliance_data, filename)
    else:
        return generator.generate_compliance_report(compliance_data)

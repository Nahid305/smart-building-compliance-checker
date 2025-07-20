"""
Smart Building Code Compliance Checker - Streamlit Application
Structural design compliance verification for IS 456:2000, IS 875, ACI, and Eurocode
"""

import streamlit as st
import sys
import os
import json
import pandas as pd
from io import BytesIO

# Add backend modules to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'api'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'utils'))

try:
    from backend.api.check_code import check_compliance
    from backend.utils.pdf_generator import generate_compliance_pdf
except ImportError:
    # Fallback imports if backend is in different structure
    try:
        from api.check_code import check_compliance
        from utils.pdf_generator import generate_compliance_pdf
    except ImportError:
        st.error("Unable to import backend modules. Please check the file structure.")
        st.stop()

# Page configuration
st.set_page_config(
    page_title="Smart Building Code Compliance Checker",
    page_icon="🏗️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #1976d2, #42a5f5);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .stSuccess {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 5px;
        padding: 10px;
    }
    .stError {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        border-radius: 5px;
        padding: 10px;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🏗️ Smart Building Code Compliance Checker</h1>
        <p>Structural Design Compliance Verification</p>
        <p><em>IS 456:2000 • IS 875 • ACI • Eurocode</em></p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page:",
        ["Home", "Check Design", "About"]
    )

    if page == "Home":
        show_home_page()
    elif page == "Check Design":
        show_check_design_page()
    elif page == "About":
        show_about_page()

def show_home_page():
    """Display the home page with project overview"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("Welcome to Smart Code Compliance Checker")
        st.write("""
        This application helps structural engineers verify their designs against international building codes.
        Our system automatically calculates loads and checks compliance for various structural members.
        """)
        
        st.subheader("🎯 Key Features")
        
        features = [
            "✅ **Automatic Load Calculation** - Dead, live, wind, and seismic loads",
            "🔍 **Code Compliance Checking** - IS 456:2000, IS 875, ACI, Eurocode",
            "📊 **Detailed Analysis** - Stress analysis, deflection checks, crack width",
            "📄 **Professional Reports** - PDF generation with calculations and recommendations",
            "🏗️ **Multiple Members** - Beams, columns, slabs, and footings"
        ]
        
        for feature in features:
            st.markdown(feature)
    
    with col2:
        st.subheader("📈 Quick Stats")
        
        # Sample metrics (you can make these dynamic)
        st.metric("Supported Codes", "4", "IS 456, IS 875, ACI, Eurocode")
        st.metric("Member Types", "4", "Beam, Column, Slab, Footing")
        st.metric("Load Types", "6", "Dead, Live, Wind, Seismic, etc.")
        
        st.subheader("🚀 Getting Started")
        st.write("1. Go to **Check Design** page")
        st.write("2. Select structural member type")
        st.write("3. Enter design parameters")
        st.write("4. Get instant compliance results")
        
        st.info("💡 Use the sidebar to navigate to 'Check Design' page to start analyzing your structural design.")

def show_check_design_page():
    """Display the main design checking interface"""
    
    st.header("🔍 Structural Design Compliance Check")
    
    # Member type selection
    member_type = st.selectbox(
        "Select Structural Member Type:",
        ["beam", "column", "slab", "footing"],
        format_func=lambda x: x.capitalize()
    )
    
    # Create tabs for different input sections
    tab1, tab2, tab3 = st.tabs(["📐 Dimensions", "🏗️ Materials", "🔩 Reinforcement"])
    
    with tab1:
        st.subheader("Member Dimensions")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            length = st.number_input("Length (m)", min_value=0.1, max_value=50.0, value=6.0, step=0.1)
        with col2:
            breadth = st.number_input("Breadth/Width (mm)", min_value=100, max_value=5000, value=300, step=25)
        with col3:
            depth = st.number_input("Depth/Height (mm)", min_value=100, max_value=5000, value=600, step=25)
    
    with tab2:
        st.subheader("Material Properties")
        
        col1, col2 = st.columns(2)
        
        with col1:
            concrete_grade = st.selectbox(
                "Concrete Grade:",
                ["M20", "M25", "M30", "M35", "M40", "M45", "M50"],
                index=2  # Default to M30
            )
        
        with col2:
            steel_grade = st.selectbox(
                "Steel Grade:",
                ["Fe415", "Fe500", "Fe550"],
                index=1  # Default to Fe500
            )
    
    with tab3:
        st.subheader("Reinforcement Details")
        
        if member_type == "beam":
            col1, col2 = st.columns(2)
            with col1:
                main_steel = st.text_input("Main Steel (e.g., 4-16mm)", value="4-16mm")
                stirrups = st.text_input("Stirrups (e.g., 8mm@150c/c)", value="8mm@150c/c")
            with col2:
                cover = st.number_input("Clear Cover (mm)", min_value=15, max_value=75, value=25)
                
        elif member_type == "column":
            col1, col2 = st.columns(2)
            with col1:
                main_steel = st.text_input("Main Steel (e.g., 8-16mm)", value="8-16mm")
                ties = st.text_input("Ties (e.g., 8mm@150c/c)", value="8mm@150c/c")
            with col2:
                cover = st.number_input("Clear Cover (mm)", min_value=25, max_value=75, value=40)
                
        elif member_type == "slab":
            col1, col2 = st.columns(2)
            with col1:
                main_steel = st.text_input("Main Steel (e.g., 10mm@150c/c)", value="10mm@150c/c")
                distribution_steel = st.text_input("Distribution Steel (e.g., 8mm@200c/c)", value="8mm@200c/c")
            with col2:
                cover = st.number_input("Clear Cover (mm)", min_value=15, max_value=50, value=20)
                
        else:  # footing
            col1, col2 = st.columns(2)
            with col1:
                main_steel = st.text_input("Main Steel (e.g., 12mm@150c/c)", value="12mm@150c/c")
            with col2:
                cover = st.number_input("Clear Cover (mm)", min_value=40, max_value=100, value=50)

    # Advanced options
    with st.expander("⚙️ Advanced Options"):
        auto_calc_loads = st.checkbox("Auto-calculate loads", value=True, help="Automatically calculate loads based on IS codes")
        
        if not auto_calc_loads:
            st.subheader("Manual Load Input")
            col1, col2, col3 = st.columns(3)
            with col1:
                dead_load = st.number_input("Dead Load (kN/m²)", min_value=0.0, value=2.5)
            with col2:
                live_load = st.number_input("Live Load (kN/m²)", min_value=0.0, value=3.0)
            with col3:
                wind_load = st.number_input("Wind Load (kN/m²)", min_value=0.0, value=1.5)

    # Check compliance button
    if st.button("🔍 Check Compliance", type="primary", use_container_width=True):
        with st.spinner("Analyzing structural design..."):
            
            # Prepare design data
            design_data = {
                "member_type": member_type,
                "dimensions": {
                    "length": length,
                    "breadth": breadth / 1000,  # Convert mm to m
                    "depth": depth / 1000       # Convert mm to m
                },
                "materials": {
                    "concrete_grade": concrete_grade,
                    "steel_grade": steel_grade
                },
                "reinforcement": {
                    "main_steel": main_steel,
                    "cover": cover
                },
                "auto_calculate_loads": auto_calc_loads
            }
            
            # Add member-specific reinforcement details
            if member_type == "beam":
                design_data["reinforcement"]["stirrups"] = stirrups
            elif member_type == "column":
                design_data["reinforcement"]["ties"] = ties
            elif member_type == "slab":
                design_data["reinforcement"]["distribution_steel"] = distribution_steel
            
            # Add manual loads if not auto-calculating
            if not auto_calc_loads:
                design_data["loads"] = {
                    "dead_load": dead_load,
                    "live_load": live_load,
                    "wind_load": wind_load
                }
            
            try:
                # Perform compliance check
                result = check_compliance(design_data)
                
                # Display results
                show_compliance_results(result, design_data)
                
            except Exception as e:
                st.error(f"Error during compliance check: {str(e)}")
                st.error("Please check your input parameters and try again.")

def show_compliance_results(result, design_data):
    """Display the compliance check results"""
    
    st.header("📊 Compliance Check Results")
    
    # Overall compliance status
    overall_compliance = result.get('overall_compliance', False)
    
    if overall_compliance:
        st.success("✅ **DESIGN COMPLIES** with building codes!")
    else:
        st.error("❌ **DESIGN DOES NOT COMPLY** with building codes!")
    
    # Results tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Summary", "🔢 Calculations", "📋 Recommendations", "📄 Report"])
    
    with tab1:
        show_results_summary(result)
    
    with tab2:
        show_detailed_calculations(result)
    
    with tab3:
        show_recommendations(result)
    
    with tab4:
        show_report_generation(result, design_data)

def show_results_summary(result):
    """Display summary of compliance results"""
    
    st.subheader("Compliance Summary")
    
    # Create columns for different checks
    checks = result.get('checks', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Strength Checks:**")
        for check_name, check_result in checks.items():
            if 'strength' in check_name.lower() or 'moment' in check_name.lower():
                status = "✅ PASS" if check_result.get('status') == 'pass' else "❌ FAIL"
                st.write(f"- {check_name}: {status}")
    
    with col2:
        st.markdown("**Serviceability Checks:**")
        for check_name, check_result in checks.items():
            if 'deflection' in check_name.lower() or 'crack' in check_name.lower():
                status = "✅ PASS" if check_result.get('status') == 'pass' else "❌ FAIL"
                st.write(f"- {check_name}: {status}")
    
    # Load calculations summary
    if 'load_calculations' in result:
        st.subheader("Applied Loads")
        loads = result['load_calculations']
        
        load_cols = st.columns(4)
        
        load_types = ['dead_load', 'live_load', 'wind_load', 'seismic_load']
        load_names = ['Dead Load', 'Live Load', 'Wind Load', 'Seismic Load']
        
        for i, (load_type, load_name) in enumerate(zip(load_types, load_names)):
            if load_type in loads:
                with load_cols[i]:
                    st.metric(load_name, f"{loads[load_type]:.2f} kN/m²")

def show_detailed_calculations(result):
    """Display detailed engineering calculations"""
    
    st.subheader("Detailed Calculations")
    
    calculations = result.get('calculations', {})
    
    if calculations:
        for calc_name, calc_data in calculations.items():
            with st.expander(f"📊 {calc_name.replace('_', ' ').title()}"):
                if isinstance(calc_data, dict):
                    for key, value in calc_data.items():
                        if isinstance(value, (int, float)):
                            st.write(f"**{key.replace('_', ' ').title()}:** {value:.4f}")
                        else:
                            st.write(f"**{key.replace('_', ' ').title()}:** {value}")
                else:
                    st.write(calc_data)
    else:
        st.info("Detailed calculations will be shown here after analysis.")

def show_recommendations(result):
    """Display design recommendations"""
    
    st.subheader("Design Recommendations")
    
    recommendations = result.get('recommendations', [])
    
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            st.write(f"{i}. {rec}")
    else:
        st.success("No specific recommendations - design appears to be adequate.")
    
    # Improvement suggestions
    improvements = result.get('improvements', [])
    if improvements:
        st.subheader("Potential Improvements")
        for improvement in improvements:
            st.info(f"💡 {improvement}")

def show_report_generation(result, design_data):
    """Handle PDF report generation and download"""
    
    st.subheader("Generate Professional Report")
    
    st.write("Generate a comprehensive PDF report with all calculations and results.")
    
    if st.button("📄 Generate PDF Report", type="secondary"):
        try:
            with st.spinner("Generating PDF report..."):
                # Generate PDF report
                pdf_buffer = generate_compliance_pdf(design_data, result)
                
                if pdf_buffer:
                    st.success("✅ Report generated successfully!")
                    
                    # Provide download button
                    st.download_button(
                        label="📥 Download PDF Report",
                        data=pdf_buffer,
                        file_name=f"{design_data['member_type']}_compliance_report.pdf",
                        mime="application/pdf"
                    )
                else:
                    st.error("Failed to generate PDF report.")
                    
        except Exception as e:
            st.error(f"Error generating report: {str(e)}")

def show_about_page():
    """Display information about the application"""
    
    st.header("About Smart Building Code Compliance Checker")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.write("""
        ### 🎯 Purpose
        This application is designed to help structural engineers verify their designs against 
        international building codes, ensuring safety and compliance in structural design.
        
        ### 📚 Supported Codes
        - **IS 456:2000** - Plain and Reinforced Concrete - Code of Practice
        - **IS 875** - Code of Practice for Design Loads
        - **ACI 318** - Building Code Requirements for Structural Concrete
        - **Eurocode 2** - Design of Concrete Structures
        
        ### 🏗️ Structural Members
        - **Beams** - Flexural members with bending moment and shear checks
        - **Columns** - Compression members with buckling analysis
        - **Slabs** - Two-way and one-way slab design verification
        - **Footings** - Foundation design compliance checking
        
        ### ⚙️ Features
        - Automatic load calculation based on IS 875
        - Real-time compliance checking
        - Professional PDF report generation
        - Detailed engineering calculations
        - Design recommendations and improvements
        """)
    
    with col2:
        st.subheader("📊 Technical Specifications")
        
        specs = {
            "Calculation Engine": "Python-based",
            "Code Standards": "International",
            "Load Calculation": "Automatic/Manual",
            "Report Format": "PDF",
            "Member Types": "4 Types",
            "Material Grades": "Multiple Options"
        }
        
        for spec, value in specs.items():
            st.metric(spec, value)
        
        st.subheader("🔧 Development Info")
        st.write("""
        **Version:** 1.0.0  
        **Technology:** Streamlit + Python  
        **License:** MIT  
        **Status:** Active Development
        """)

if __name__ == "__main__":
    main()

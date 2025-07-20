"""
Main API endpoint for structural design compliance checking with automatic load calculation
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.beam_checker import check_beam_compliance
from utils.column_checker import check_column_compliance
from utils.slab_checker import check_slab_compliance
from utils.footing_checker import check_footing_compliance
from utils.load_calculator import auto_calculate_loads

def check_compliance(design_data):
    """
    Main function to check structural design compliance with automatic load calculation
    
    Args:
        design_data (dict): Dictionary containing:
            - member_type: 'beam', 'column', 'slab', 'footing'
            - dimensions: {length, breadth, depth}
            - materials: {concrete_grade, steel_grade}
            - reinforcement: reinforcement details
            - building_parameters: building info for load calculation (optional)
            - wind_parameters: wind data for load calculation (optional)
            - auto_calculate_loads: boolean flag to enable/disable auto calculation
    
    Returns:
        dict: Compliance check results with pass/fail status, recommendations, and load calculations
    """
    try:
        member_type = design_data.get('member_type', '').lower()
        
        # Auto-calculate loads if not provided or if auto_calculate flag is True
        auto_calc = design_data.get('auto_calculate_loads', True)
        if auto_calc or 'loads' not in design_data:
            print(f"Auto-calculating loads for {member_type}")
            design_data = auto_calculate_loads(member_type, design_data)
        
        # Perform compliance checking based on member type
        if member_type == 'beam':
            result = check_beam_compliance(design_data)
        elif member_type == 'column':
            result = check_column_compliance(design_data)
        elif member_type == 'slab':
            result = check_slab_compliance(design_data)
        elif member_type == 'footing':
            result = check_footing_compliance(design_data)
        else:
            return {
                "error": f"Unsupported member type: {member_type}",
                "supported_types": ["beam", "column", "slab", "footing"]
            }
        
        # Add design recommendations if any checks failed
        if not result.get('overall_compliance', True):
            # Simple recommendations for now
            recommendations = []
            if member_type == "beam":
                recommendations.append("Consider increasing beam depth if moment capacity is insufficient")
                recommendations.append("Check reinforcement spacing for shear requirements")
            elif member_type == "column":
                recommendations.append("Increase column dimensions if axial capacity is exceeded")
                recommendations.append("Check minimum reinforcement percentage")
            elif member_type == "slab":
                recommendations.append("Consider increasing slab thickness if deflection is excessive")
                recommendations.append("Check reinforcement requirements for flexure")
            elif member_type == "footing":
                recommendations.append("Increase footing dimensions if bearing pressure is excessive")
                recommendations.append("Check reinforcement for punching shear")
            
            result['recommendations'] = recommendations
        
        # Include load calculations in result if performed
        if 'load_calculations' in design_data:
            result['load_calculations'] = design_data['load_calculations']
            result['calculated_loads'] = design_data['loads']
        
        return result
        
    except Exception as e:
        return {
            "error": f"Compliance check failed: {str(e)}",
            "member_type": member_type
        }

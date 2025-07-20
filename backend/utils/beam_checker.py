"""
Beam design compliance checker as per IS 456:2000
"""

import math
from .formulas import (
    MaterialConstants, ISCodeLimits, 
    calculate_design_moment, calculate_design_shear,
    calculate_required_area_of_steel, calculate_shear_capacity,
    calculate_deflection_ratio, check_minimum_steel, check_maximum_steel
)

def check_beam_compliance(design_data):
    """
    Check beam design compliance with IS 456:2000
    
    Args:
        design_data (dict): Beam design parameters
    
    Returns:
        dict: Compliance check results
    """
    try:
        # Extract design parameters
        dimensions = design_data['dimensions']
        loads = design_data['loads']
        materials = design_data['materials']
        reinforcement = design_data['reinforcement']
        
        # Beam dimensions
        span = float(dimensions.get('length', 0)) * 1000  # Convert to mm
        width = float(dimensions.get('breadth', 0))  # mm
        depth = float(dimensions.get('depth', 0))  # mm
        cover = float(reinforcement.get('cover', 25))  # mm
        
        # Effective depth
        bar_dia = float(reinforcement.get('bar_diameter', 16))
        d = depth - cover - bar_dia/2  # Effective depth
        
        # Material properties
        concrete_grade = materials.get('concrete_grade', 'M20')
        steel_grade = materials.get('steel_grade', 'Fe500')
        fck = MaterialConstants.CONCRETE_GRADES.get(concrete_grade, 20)
        fy = MaterialConstants.STEEL_GRADES.get(steel_grade, 500)
        
        # Loads
        dead_load = float(loads.get('dead_load', 0))  # kN/m
        live_load = float(loads.get('live_load', 0))  # kN/m
        
        # Factored load
        wu = ISCodeLimits.LOAD_FACTOR_DEAD * dead_load + ISCodeLimits.LOAD_FACTOR_LIVE * live_load
        
        # Calculate design forces
        Mu = calculate_design_moment(span/1000, wu)  # kNm
        Vu = calculate_design_shear(span/1000, wu)  # kN
        
        # Convert to Nmm for calculations
        Mu_nmm = Mu * 1e6
        Vu_n = Vu * 1000
        
        # Steel calculation
        Ast_required = calculate_required_area_of_steel(Mu_nmm, fck, fy, width, d)
        
        # Provided steel
        num_bars = int(reinforcement.get('num_bars', 2))
        bar_area = math.pi * (bar_dia/2)**2
        Ast_provided = num_bars * bar_area
        
        # Compliance checks
        checks = {}
        
        # 1. Flexural strength check
        checks['flexural_strength'] = {
            'required_steel': round(Ast_required, 2),
            'provided_steel': round(Ast_provided, 2),
            'pass': Ast_provided >= Ast_required,
            'description': 'Flexural reinforcement adequacy'
        }
        
        # 2. Minimum steel check
        min_adequate, Ast_min = check_minimum_steel(Ast_provided, width, d, fy)
        checks['minimum_steel'] = {
            'minimum_required': round(Ast_min, 2),
            'provided_steel': round(Ast_provided, 2),
            'pass': min_adequate,
            'description': 'Minimum tension reinforcement (IS 456 Cl. 26.5.1.1)'
        }
        
        # 3. Maximum steel check
        max_adequate, Ast_max = check_maximum_steel(Ast_provided, width, d)
        checks['maximum_steel'] = {
            'maximum_allowed': round(Ast_max, 2),
            'provided_steel': round(Ast_provided, 2),
            'pass': max_adequate,
            'description': 'Maximum tension reinforcement (IS 456 Cl. 26.5.1.1)'
        }
        
        # 4. Shear strength check
        Vc = calculate_shear_capacity(width, d, fck, Ast_provided)
        checks['shear_strength'] = {
            'design_shear': round(Vu_n, 2),
            'shear_capacity': round(Vc, 2),
            'pass': Vc >= Vu_n,
            'description': 'Shear strength without stirrups (IS 456 Cl. 40)'
        }
        
        # 5. Deflection check
        basic_ratio = calculate_deflection_ratio(span, 'simply_supported')
        actual_ratio = span / d
        # Modification factor for tension steel
        fs = 0.58 * fy * Ast_required / Ast_provided if Ast_provided > 0 else 0.58 * fy
        kt = 1.0  # Simplified - should be calculated based on fs
        allowable_ratio = basic_ratio * kt
        
        checks['deflection'] = {
            'actual_span_depth_ratio': round(actual_ratio, 2),
            'allowable_span_depth_ratio': round(allowable_ratio, 2),
            'pass': actual_ratio <= allowable_ratio,
            'description': 'Deflection control (IS 456 Cl. 23.2.1)'
        }
        
        # 6. Development length check (simplified)
        ld = bar_dia * fy / (4 * math.sqrt(fck))  # Simplified formula
        available_length = span / 2  # Simplified
        checks['development_length'] = {
            'required_length': round(ld, 2),
            'available_length': round(available_length, 2),
            'pass': available_length >= ld,
            'description': 'Development length (IS 456 Cl. 26.2.1)'
        }
        
        # Overall compliance
        overall_pass = all(check['pass'] for check in checks.values())
        
        # Summary
        result = {
            'member_type': 'beam',
            'overall_compliance': overall_pass,
            'design_summary': {
                'span': span,
                'width': width,
                'depth': depth,
                'effective_depth': round(d, 2),
                'design_moment': round(Mu, 2),
                'design_shear': round(Vu, 2),
                'concrete_grade': concrete_grade,
                'steel_grade': steel_grade
            },
            'checks': checks,
            'status': 'PASS' if overall_pass else 'FAIL'
        }
        
        return result
        
    except Exception as e:
        return {
            'error': f'Beam compliance check failed: {str(e)}',
            'member_type': 'beam'
        }

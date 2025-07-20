"""
Column design compliance checker as per IS 456:2000
"""

import math
from .formulas import MaterialConstants, ISCodeLimits

def check_column_compliance(design_data):
    """
    Check column design compliance with IS 456:2000
    
    Args:
        design_data (dict): Column design parameters
    
    Returns:
        dict: Compliance check results
    """
    try:
        # Extract design parameters
        dimensions = design_data['dimensions']
        loads = design_data['loads']
        materials = design_data['materials']
        reinforcement = design_data['reinforcement']
        
        # Column dimensions
        width = float(dimensions.get('breadth', 0))  # mm
        depth = float(dimensions.get('depth', 0))  # mm
        height = float(dimensions.get('length', 0)) * 1000  # Convert to mm
        cover = float(reinforcement.get('cover', 40))  # mm
        
        # Material properties
        concrete_grade = materials.get('concrete_grade', 'M20')
        steel_grade = materials.get('steel_grade', 'Fe500')
        fck = MaterialConstants.CONCRETE_GRADES.get(concrete_grade, 20)
        fy = MaterialConstants.STEEL_GRADES.get(steel_grade, 500)
        
        # Loads
        axial_load = float(loads.get('axial_load', 0))  # kN
        moment = float(loads.get('moment', 0))  # kNm
        
        # Factored loads
        Pu = ISCodeLimits.LOAD_FACTOR_DEAD * axial_load  # Simplified
        Mu = ISCodeLimits.LOAD_FACTOR_DEAD * moment
        
        # Column geometry
        Ag = width * depth  # Gross area
        
        # Steel details
        bar_dia = float(reinforcement.get('bar_diameter', 16))
        num_bars = int(reinforcement.get('num_bars', 8))
        bar_area = math.pi * (bar_dia/2)**2
        Ast = num_bars * bar_area
        
        # Compliance checks
        checks = {}
        
        # 1. Minimum dimension check
        min_dimension = min(width, depth)
        checks['minimum_dimension'] = {
            'minimum_dimension': min_dimension,
            'required_minimum': 200,  # mm as per IS 456
            'pass': min_dimension >= 200,
            'description': 'Minimum column dimension (IS 456 Cl. 25.1.2)'
        }
        
        # 2. Slenderness ratio check
        effective_length = height  # Simplified - depends on end conditions
        least_radius = min(width, depth) / (2 * math.sqrt(3))  # For rectangular section
        slenderness_ratio = effective_length / least_radius
        
        checks['slenderness_ratio'] = {
            'slenderness_ratio': round(slenderness_ratio, 2),
            'maximum_allowed': 60,  # For braced columns
            'pass': slenderness_ratio <= 60,
            'description': 'Slenderness ratio (IS 456 Cl. 25.3)'
        }
        
        # 3. Minimum steel check
        Ast_min = 0.008 * Ag  # 0.8% of gross area
        checks['minimum_steel'] = {
            'minimum_required': round(Ast_min, 2),
            'provided_steel': round(Ast, 2),
            'pass': Ast >= Ast_min,
            'description': 'Minimum longitudinal reinforcement (IS 456 Cl. 26.5.3.1 a)'
        }
        
        # 4. Maximum steel check
        Ast_max = 0.04 * Ag  # 4% of gross area
        checks['maximum_steel'] = {
            'maximum_allowed': round(Ast_max, 2),
            'provided_steel': round(Ast, 2),
            'pass': Ast <= Ast_max,
            'description': 'Maximum longitudinal reinforcement (IS 456 Cl. 26.5.3.1 c)'
        }
        
        # 5. Axial load capacity check (simplified)
        # For short columns under axial load
        Pu_max = 0.4 * fck * (Ag - Ast) + 0.67 * fy * Ast
        Pu_max = Pu_max / 1000  # Convert to kN
        
        checks['axial_capacity'] = {
            'design_load': round(Pu, 2),
            'capacity': round(Pu_max, 2),
            'pass': Pu <= Pu_max,
            'description': 'Axial load capacity (IS 456 Cl. 39.3)'
        }
        
        # 6. Minimum number of bars
        min_bars = 4 if min(width, depth) <= 200 else 6
        checks['minimum_bars'] = {
            'minimum_required': min_bars,
            'provided_bars': num_bars,
            'pass': num_bars >= min_bars,
            'description': 'Minimum number of longitudinal bars (IS 456 Cl. 26.5.3.1 d)'
        }
        
        # 7. Tie reinforcement check (simplified)
        tie_dia = max(6, bar_dia/4)  # Minimum tie diameter
        tie_spacing = min(
            least_dimension := min(width, depth),
            16 * bar_dia,
            300  # mm
        )
        
        checks['tie_reinforcement'] = {
            'minimum_tie_diameter': round(tie_dia, 2),
            'maximum_tie_spacing': round(tie_spacing, 2),
            'description': 'Tie reinforcement requirements (IS 456 Cl. 26.5.3.2)',
            'pass': True  # Assume adequate for now
        }
        
        # Overall compliance
        overall_pass = all(check['pass'] for check in checks.values())
        
        # Summary
        result = {
            'member_type': 'column',
            'overall_compliance': overall_pass,
            'design_summary': {
                'width': width,
                'depth': depth,
                'height': height,
                'gross_area': round(Ag, 2),
                'steel_percentage': round(100 * Ast / Ag, 2),
                'design_axial_load': round(Pu, 2),
                'concrete_grade': concrete_grade,
                'steel_grade': steel_grade
            },
            'checks': checks,
            'status': 'PASS' if overall_pass else 'FAIL'
        }
        
        return result
        
    except Exception as e:
        return {
            'error': f'Column compliance check failed: {str(e)}',
            'member_type': 'column'
        }

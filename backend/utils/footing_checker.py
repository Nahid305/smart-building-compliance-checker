"""
Footing design compliance checker as per IS 456:2000
"""

import math
from .formulas import MaterialConstants, ISCodeLimits

def check_footing_compliance(design_data):
    """
    Check footing design compliance with IS 456:2000
    
    Args:
        design_data (dict): Footing design parameters
    
    Returns:
        dict: Compliance check results
    """
    try:
        # Extract design parameters
        dimensions = design_data['dimensions']
        loads = design_data['loads']
        materials = design_data['materials']
        reinforcement = design_data['reinforcement']
        
        # Footing dimensions
        length = float(dimensions.get('length', 0)) * 1000  # Convert to mm
        breadth = float(dimensions.get('breadth', 0)) * 1000  # Convert to mm
        thickness = float(dimensions.get('depth', 0))  # mm
        cover = float(reinforcement.get('cover', 50))  # mm (bottom cover)
        
        # Column dimensions (assumed square for simplicity)
        column_size = float(dimensions.get('column_size', 300))  # mm
        
        # Effective depth
        bar_dia = float(reinforcement.get('bar_diameter', 16))
        d = thickness - cover - bar_dia/2
        
        # Material properties
        concrete_grade = materials.get('concrete_grade', 'M20')
        steel_grade = materials.get('steel_grade', 'Fe500')
        fck = MaterialConstants.CONCRETE_GRADES.get(concrete_grade, 20)
        fy = MaterialConstants.STEEL_GRADES.get(steel_grade, 500)
        
        # Loads
        axial_load = float(loads.get('axial_load', 0))  # kN
        moment = float(loads.get('moment', 0))  # kNm (if any)
        
        # Soil bearing capacity
        sbc = float(loads.get('safe_bearing_capacity', 200))  # kN/m²
        
        # Footing area and bearing pressure
        footing_area = length * breadth / 1e6  # m²
        self_weight = footing_area * thickness/1000 * MaterialConstants.CONCRETE_DENSITY  # kN
        total_load = axial_load + self_weight
        
        bearing_pressure = total_load / footing_area  # kN/m²
        
        # Net upward pressure
        net_pressure = bearing_pressure - self_weight/footing_area  # kN/m²
        
        # Critical sections for bending moment
        # Section at face of column
        cantilever_length = (max(length, breadth) - column_size) / 2 / 1000  # m
        
        # Moment calculation
        if length >= breadth:
            moment_x = net_pressure * breadth/1000 * cantilever_length**2 / 2  # kNm
            moment_y = net_pressure * length/1000 * cantilever_length**2 / 2   # kNm
        else:
            moment_x = net_pressure * length/1000 * cantilever_length**2 / 2   # kNm
            moment_y = net_pressure * breadth/1000 * cantilever_length**2 / 2  # kNm
        
        critical_moment = max(moment_x, moment_y)
        
        # Convert to Nmm per mm width
        Mu_nmm = critical_moment * 1e6 / min(length, breadth)
        
        # Steel calculation
        b = min(length, breadth)  # Critical width
        k = Mu_nmm / (fck * b * d**2)
        
        if k <= 0.138:  # Singly reinforced
            j = 1 - k/3
            Ast_required = Mu_nmm / (0.87 * fy * j * d)
        else:
            Ast_required = Mu_nmm / (0.87 * fy * 0.9 * d)  # Simplified
        
        # Provided steel
        spacing = float(reinforcement.get('spacing', 150))  # mm c/c
        bar_area = math.pi * (bar_dia/2)**2
        num_bars = int(b / spacing) + 1
        Ast_provided = num_bars * bar_area
        
        # Compliance checks
        checks = {}
        
        # 1. Bearing pressure check
        checks['bearing_pressure'] = {
            'bearing_pressure': round(bearing_pressure, 2),
            'safe_bearing_capacity': sbc,
            'pass': bearing_pressure <= sbc,
            'description': 'Soil bearing pressure check'
        }
        
        # 2. Minimum thickness check
        min_thickness = max(150, cantilever_length * 1000 / 4)  # L/4 or 150mm minimum
        checks['minimum_thickness'] = {
            'minimum_required': round(min_thickness, 2),
            'provided_thickness': thickness,
            'pass': thickness >= min_thickness,
            'description': 'Minimum thickness requirement'
        }
        
        # 3. Flexural strength check
        checks['flexural_strength'] = {
            'required_steel': round(Ast_required, 2),
            'provided_steel': round(Ast_provided, 2),
            'pass': Ast_provided >= Ast_required,
            'description': 'Flexural reinforcement adequacy'
        }
        
        # 4. Minimum steel check
        Ast_min = 0.12 * thickness * b / 100  # 0.12% of gross area
        checks['minimum_steel'] = {
            'minimum_required': round(Ast_min, 2),
            'provided_steel': round(Ast_provided, 2),
            'pass': Ast_provided >= Ast_min,
            'description': 'Minimum reinforcement (IS 456 Cl. 26.5.2.1)'
        }
        
        # 5. Maximum spacing check
        max_spacing = min(3 * thickness, 450)  # mm
        checks['maximum_spacing'] = {
            'maximum_allowed': max_spacing,
            'provided_spacing': spacing,
            'pass': spacing <= max_spacing,
            'description': 'Maximum spacing of reinforcement'
        }
        
        # 6. One-way shear check
        # Critical section at d from column face
        shear_span = cantilever_length - d/1000  # m
        if shear_span > 0:
            Vu = net_pressure * min(length, breadth)/1000 * shear_span * 1000  # N
            tau_v = Vu / (b * d)
            
            # Allowable shear stress
            pt = 100 * Ast_provided / (b * d)
            tau_c = 0.36 * math.sqrt(fck)  # Simplified from IS 456 Table 19
            
            checks['one_way_shear'] = {
                'design_shear_stress': round(tau_v, 3),
                'allowable_shear_stress': round(tau_c, 3),
                'pass': tau_v <= tau_c,
                'description': 'One-way shear strength (IS 456 Cl. 40)'
            }
        else:
            checks['one_way_shear'] = {
                'design_shear_stress': 0,
                'allowable_shear_stress': 0,
                'pass': True,
                'description': 'One-way shear - Not critical'
            }
        
        # 7. Two-way shear (punching shear) check
        # Critical perimeter at d/2 from column face
        critical_perimeter = 4 * (column_size + d)  # mm
        punching_area = (column_size + d)**2  # mm²
        punching_force = axial_load * 1000 - net_pressure * punching_area/1e6 * 1000  # N
        
        tau_v_punch = punching_force / (critical_perimeter * d)
        tau_c_punch = 0.25 * math.sqrt(fck)  # Maximum allowable
        
        checks['punching_shear'] = {
            'punching_shear_stress': round(tau_v_punch, 3),
            'allowable_punching_stress': round(tau_c_punch, 3),
            'pass': tau_v_punch <= tau_c_punch,
            'description': 'Two-way shear (punching) strength (IS 456 Cl. 31.6)'
        }
        
        # Overall compliance
        overall_pass = all(check['pass'] for check in checks.values())
        
        # Summary
        result = {
            'member_type': 'footing',
            'overall_compliance': overall_pass,
            'design_summary': {
                'length': length,
                'breadth': breadth,
                'thickness': thickness,
                'effective_depth': round(d, 2),
                'footing_area': round(footing_area, 2),
                'bearing_pressure': round(bearing_pressure, 2),
                'critical_moment': round(critical_moment, 2),
                'concrete_grade': concrete_grade,
                'steel_grade': steel_grade
            },
            'checks': checks,
            'status': 'PASS' if overall_pass else 'FAIL'
        }
        
        return result
        
    except Exception as e:
        return {
            'error': f'Footing compliance check failed: {str(e)}',
            'member_type': 'footing'
        }

"""
Slab design compliance checker as per IS 456:2000
"""

import math
from .formulas import MaterialConstants, ISCodeLimits

def check_slab_compliance(design_data):
    """
    Check slab design compliance with IS 456:2000
    
    Args:
        design_data (dict): Slab design parameters
    
    Returns:
        dict: Compliance check results
    """
    try:
        # Extract design parameters
        dimensions = design_data['dimensions']
        loads = design_data['loads']
        materials = design_data['materials']
        reinforcement = design_data['reinforcement']
        
        # Slab dimensions
        length = float(dimensions.get('length', 0)) * 1000  # Convert to mm
        breadth = float(dimensions.get('breadth', 0)) * 1000  # Convert to mm
        thickness = float(dimensions.get('depth', 0))  # mm
        cover = float(reinforcement.get('cover', 20))  # mm
        
        # Effective depth
        bar_dia = float(reinforcement.get('bar_diameter', 10))
        d = thickness - cover - bar_dia/2
        
        # Material properties
        concrete_grade = materials.get('concrete_grade', 'M20')
        steel_grade = materials.get('steel_grade', 'Fe500')
        fck = MaterialConstants.CONCRETE_GRADES.get(concrete_grade, 20)
        fy = MaterialConstants.STEEL_GRADES.get(steel_grade, 500)
        
        # Loads
        dead_load = float(loads.get('dead_load', 0))  # kN/m²
        live_load = float(loads.get('live_load', 0))  # kN/m²
        
        # Add self weight
        self_weight = thickness/1000 * MaterialConstants.CONCRETE_DENSITY  # kN/m²
        total_dead_load = dead_load + self_weight
        
        # Factored load
        wu = ISCodeLimits.LOAD_FACTOR_DEAD * total_dead_load + ISCodeLimits.LOAD_FACTOR_LIVE * live_load
        
        # Slab type determination
        aspect_ratio = max(length, breadth) / min(length, breadth)
        slab_type = "one_way" if aspect_ratio >= 2.0 else "two_way"
        
        # Moment calculation (simplified for one-way slab)
        shorter_span = min(length, breadth) / 1000  # Convert to m
        if slab_type == "one_way":
            Mu = wu * shorter_span**2 / 8  # kNm/m
        else:
            # Two-way slab moment coefficients (simplified)
            alpha_x = 0.087  # From IS 456 for simply supported slab
            Mu = alpha_x * wu * shorter_span**2  # kNm/m
        
        # Convert to per mm width
        Mu_nmm = Mu * 1e6 / 1000  # Nmm per mm width
        
        # Steel calculation per meter width
        b = 1000  # mm (1 meter width)
        
        # Required steel
        k = Mu_nmm / (fck * b * d**2)
        if k <= 0.138:  # Singly reinforced
            j = 1 - k/3
            Ast_required = Mu_nmm / (0.87 * fy * j * d)
        else:
            Ast_required = Mu_nmm / (0.87 * fy * 0.9 * d)  # Simplified
        
        # Provided steel
        spacing = float(reinforcement.get('spacing', 150))  # mm c/c
        bar_area = math.pi * (bar_dia/2)**2
        Ast_provided = 1000 * bar_area / spacing  # per meter width
        
        # Compliance checks
        checks = {}
        
        # 1. Minimum thickness check
        min_thickness_required = shorter_span * 1000 / 20  # L/20 for simply supported
        checks['minimum_thickness'] = {
            'minimum_required': round(min_thickness_required, 2),
            'provided_thickness': thickness,
            'pass': thickness >= min_thickness_required,
            'description': 'Minimum thickness for deflection control (IS 456 Cl. 23.2.1)'
        }
        
        # 2. Flexural strength check
        checks['flexural_strength'] = {
            'required_steel': round(Ast_required, 2),
            'provided_steel': round(Ast_provided, 2),
            'pass': Ast_provided >= Ast_required,
            'description': 'Flexural reinforcement adequacy'
        }
        
        # 3. Minimum steel check
        Ast_min = 0.12 * thickness * 1000 / 100  # 0.12% of gross area for HYSD bars
        checks['minimum_steel'] = {
            'minimum_required': round(Ast_min, 2),
            'provided_steel': round(Ast_provided, 2),
            'pass': Ast_provided >= Ast_min,
            'description': 'Minimum reinforcement (IS 456 Cl. 26.5.2.1)'
        }
        
        # 4. Maximum spacing check
        max_spacing = min(3 * thickness, 300)  # mm
        checks['maximum_spacing'] = {
            'maximum_allowed': max_spacing,
            'provided_spacing': spacing,
            'pass': spacing <= max_spacing,
            'description': 'Maximum spacing of reinforcement (IS 456 Cl. 26.3.3)'
        }
        
        # 5. Shear check (usually not critical for slabs)
        Vu = wu * shorter_span / 2 * 1000  # N per mm width
        tau_v = Vu / (b * d)
        pt = 100 * Ast_provided / (b * d)
        tau_c_max = 0.25 * math.sqrt(fck)  # Maximum shear stress
        
        checks['shear_strength'] = {
            'design_shear_stress': round(tau_v, 3),
            'maximum_allowable': round(tau_c_max, 3),
            'pass': tau_v <= tau_c_max,
            'description': 'Shear strength (IS 456 Cl. 40.2.1)'
        }
        
        # 6. Distribution steel (for one-way slabs)
        if slab_type == "one_way":
            Ast_dist_min = 0.12 * thickness * 1000 / 100  # 0.12% in perpendicular direction
            dist_spacing = float(reinforcement.get('distribution_spacing', 200))
            Ast_dist_provided = 1000 * bar_area / dist_spacing
            
            checks['distribution_steel'] = {
                'minimum_required': round(Ast_dist_min, 2),
                'provided_steel': round(Ast_dist_provided, 2),
                'pass': Ast_dist_provided >= Ast_dist_min,
                'description': 'Distribution reinforcement (IS 456 Cl. 26.5.2.1)'
            }
        
        # Overall compliance
        overall_pass = all(check['pass'] for check in checks.values())
        
        # Summary
        result = {
            'member_type': 'slab',
            'overall_compliance': overall_pass,
            'design_summary': {
                'length': length,
                'breadth': breadth,
                'thickness': thickness,
                'effective_depth': round(d, 2),
                'slab_type': slab_type,
                'aspect_ratio': round(aspect_ratio, 2),
                'design_moment': round(Mu, 2),
                'factored_load': round(wu, 2),
                'concrete_grade': concrete_grade,
                'steel_grade': steel_grade
            },
            'checks': checks,
            'status': 'PASS' if overall_pass else 'FAIL'
        }
        
        return result
        
    except Exception as e:
        return {
            'error': f'Slab compliance check failed: {str(e)}',
            'member_type': 'slab'
        }

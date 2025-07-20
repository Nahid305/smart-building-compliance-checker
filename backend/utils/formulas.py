"""
General formulas and constants from IS 456:2000 and IS 875
"""

import math

# Material Properties Constants
class MaterialConstants:
    """Standard material properties as per IS codes"""
    
    # Concrete grades (fck in N/mm²)
    CONCRETE_GRADES = {
        'M15': 15, 'M20': 20, 'M25': 25, 'M30': 30, 'M35': 35, 'M40': 40,
        'M45': 45, 'M50': 50, 'M55': 55, 'M60': 60
    }
    
    # Steel grades (fy in N/mm²)
    STEEL_GRADES = {
        'Fe415': 415, 'Fe500': 500, 'Fe550': 550, 'Fe600': 600
    }
    
    # Density (kN/m³)
    CONCRETE_DENSITY = 25.0
    STEEL_DENSITY = 78.5

class ISCodeLimits:
    """Limits and factors from IS 456:2000"""
    
    # Partial safety factors
    GAMMA_C = 1.5  # Concrete
    GAMMA_S = 1.15  # Steel
    
    # Load factors
    LOAD_FACTOR_DEAD = 1.5
    LOAD_FACTOR_LIVE = 1.5
    
    # Minimum reinforcement ratios
    MIN_TENSION_STEEL = 0.85  # As per IS 456 Clause 26.5.1.1
    MIN_SHEAR_STEEL = 0.4    # As per IS 456 Clause 26.5.1.6
    
    # Maximum reinforcement ratios
    MAX_TENSION_STEEL = 4.0  # Percentage
    
    # Cover requirements (mm)
    MIN_COVER = {
        'mild': 20,
        'moderate': 30,
        'severe': 45,
        'very_severe': 50,
        'extreme': 75
    }

def calculate_design_moment(span, udl, point_loads=None):
    """
    Calculate design bending moment for simply supported beam
    
    Args:
        span (float): Beam span in meters
        udl (float): Uniformly distributed load in kN/m
        point_loads (list): List of point loads [(P, a), ...] where P is load and a is distance from left support
    
    Returns:
        float: Maximum design moment in kNm
    """
    # Moment due to UDL
    moment_udl = udl * span**2 / 8
    
    # Moment due to point loads
    moment_point = 0
    if point_loads:
        for P, a in point_loads:
            b = span - a
            moment_point += max(moment_point, P * a * b / span)
    
    return moment_udl + moment_point

def calculate_design_shear(span, udl, point_loads=None):
    """
    Calculate design shear force
    
    Args:
        span (float): Beam span in meters
        udl (float): Uniformly distributed load in kN/m
        point_loads (list): List of point loads [(P, a), ...]
    
    Returns:
        float: Maximum design shear in kN
    """
    # Shear due to UDL
    shear_udl = udl * span / 2
    
    # Shear due to point loads
    shear_point = 0
    if point_loads:
        for P, a in point_loads:
            shear_point += P / 2  # Simplified for maximum case
    
    return shear_udl + shear_point

def calculate_required_area_of_steel(moment, fck, fy, b, d):
    """
    Calculate required area of tension steel as per IS 456
    
    Args:
        moment (float): Design moment in Nmm
        fck (float): Characteristic compressive strength of concrete
        fy (float): Characteristic strength of steel
        b (float): Width of beam in mm
        d (float): Effective depth in mm
    
    Returns:
        float: Required area of steel in mm²
    """
    # Convert moment to Nmm if in kNm
    if moment < 1000:  # Assume kNm
        moment = moment * 1e6
    
    # Calculate limiting moment
    xu_max = 0.48 * d  # For Fe415 and Fe500
    Mu_lim = 0.36 * fck * b * xu_max * (d - 0.42 * xu_max)
    
    if moment <= Mu_lim:
        # Under-reinforced section
        k = moment / (fck * b * d**2)
        j = 1 - (k / 3)
        Ast = moment / (0.87 * fy * j * d)
    else:
        # Over-reinforced - need compression steel
        Ast = moment / (0.87 * fy * 0.9 * d)  # Simplified approach
    
    return Ast

def calculate_shear_capacity(b, d, fck, Ast=0):
    """
    Calculate shear capacity as per IS 456 Clause 40
    
    Args:
        b (float): Width in mm
        d (float): Effective depth in mm
        fck (float): Characteristic compressive strength
        Ast (float): Area of tension steel in mm²
    
    Returns:
        float: Shear capacity in N
    """
    # Calculate percentage of steel
    pt = 100 * Ast / (b * d) if Ast > 0 else 0.15
    pt = min(pt, 3.0)  # Maximum 3%
    
    # Shear strength from IS 456 Table 19
    if fck <= 20:
        if pt <= 0.15:
            tau_c = 0.28
        elif pt <= 0.25:
            tau_c = 0.30
        elif pt <= 0.50:
            tau_c = 0.35
        elif pt <= 0.75:
            tau_c = 0.39
        elif pt <= 1.00:
            tau_c = 0.42
        elif pt <= 1.25:
            tau_c = 0.45
        elif pt <= 1.50:
            tau_c = 0.48
        elif pt <= 1.75:
            tau_c = 0.50
        elif pt <= 2.00:
            tau_c = 0.52
        elif pt <= 2.25:
            tau_c = 0.54
        elif pt <= 2.50:
            tau_c = 0.56
        elif pt <= 2.75:
            tau_c = 0.57
        else:
            tau_c = 0.58
    else:
        # For higher grades, multiply by sqrt(fck/20)
        base_tau_c = 0.28 + (pt - 0.15) * 0.02  # Simplified
        tau_c = base_tau_c * math.sqrt(fck / 20)
    
    return tau_c * b * d

def calculate_deflection_ratio(span, loading_type='udl'):
    """
    Calculate basic span-to-depth ratio as per IS 456 Clause 23.2.1
    
    Args:
        span (float): Span in mm
        loading_type (str): 'cantilever', 'simply_supported', 'continuous'
    
    Returns:
        float: Basic span-to-depth ratio
    """
    if loading_type == 'cantilever':
        return 7
    elif loading_type == 'simply_supported':
        return 20
    elif loading_type == 'continuous':
        return 26
    else:
        return 20  # Default to simply supported

def check_minimum_steel(Ast_provided, b, d, fy):
    """
    Check minimum steel requirement as per IS 456
    
    Args:
        Ast_provided (float): Provided area of steel in mm²
        b (float): Width in mm
        d (float): Effective depth in mm
        fy (float): Yield strength of steel
    
    Returns:
        tuple: (is_adequate, min_required)
    """
    Ast_min = (0.85 / fy) * b * d
    return Ast_provided >= Ast_min, Ast_min

def check_maximum_steel(Ast_provided, b, d):
    """
    Check maximum steel requirement as per IS 456
    
    Args:
        Ast_provided (float): Provided area of steel in mm²
        b (float): Width in mm
        d (float): Effective depth in mm
    
    Returns:
        tuple: (is_adequate, max_allowed)
    """
    Ast_max = 0.04 * b * d
    return Ast_provided <= Ast_max, Ast_max

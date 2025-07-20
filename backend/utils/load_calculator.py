"""
Automatic load calculator based on IS 875 standards
Calculates dead load, live load, wind load, and axial load automatically
"""

import math
from typing import Dict, Any

class LoadCalculator:
    """
    Automatic load calculation based on IS 875 standards
    """
    
    # Material densities (kN/m³) - IS 875 Part 1
    MATERIAL_DENSITIES = {
        'concrete': 25.0,           # RCC
        'brick_masonry': 19.0,      # Brick masonry
        'stone_masonry': 24.0,      # Stone masonry
        'steel': 78.5,              # Structural steel
        'timber': 6.0,              # Timber
        'plaster': 20.0,            # Cement plaster
        'flooring': 23.0,           # Flooring materials
        'waterproofing': 1.5,       # Waterproofing layers
    }
    
    # Live loads (kN/m²) - IS 875 Part 2
    LIVE_LOADS = {
        'residential': 2.0,         # Residential buildings
        'office': 3.0,              # Office buildings
        'retail': 4.0,              # Retail/commercial
        'industrial': 5.0,          # Industrial buildings
        'warehouse': 7.5,           # Storage/warehouse
        'parking': 2.5,             # Parking areas
        'corridor': 3.0,            # Corridors/passages
        'stairs': 3.0,              # Staircases
        'terrace': 1.5,             # Accessible terraces
        'roof': 0.75,               # Non-accessible roofs
    }
    
    # Wind speed zones (m/s) - IS 875 Part 3
    WIND_SPEEDS = {
        'zone_1': 39,               # Low wind speed
        'zone_2': 44,               # Moderate wind speed
        'zone_3': 47,               # High wind speed
        'zone_4': 50,               # Very high wind speed
        'zone_5': 55,               # Extreme wind speed
        'zone_6': 60,               # Cyclonic areas
    }
    
    def __init__(self):
        self.g = 9.81  # Acceleration due to gravity (m/s²)
    
    def calculate_self_weight(self, member_type: str, dimensions: Dict[str, float], 
                            material: str = 'concrete') -> Dict[str, float]:
        """
        Calculate self-weight (dead load) of structural member
        
        Args:
            member_type: 'beam', 'column', 'slab', 'footing'
            dimensions: Dictionary with length, breadth, depth in mm
            material: Material type
            
        Returns:
            Dictionary with self-weight calculations
        """
        # Convert dimensions from mm to m
        length = float(dimensions.get('length', 0)) / 1000
        breadth = float(dimensions.get('breadth', 0)) / 1000
        depth = float(dimensions.get('depth', 0)) / 1000
        
        density = self.MATERIAL_DENSITIES.get(material, 25.0)
        
        if member_type == 'beam':
            # Beam self-weight = cross-sectional area × length × density
            volume = breadth * depth * length  # m³
            self_weight = volume * density     # kN
            udl = self_weight / length         # kN/m (uniformly distributed load)
            
            return {
                'volume': volume,
                'total_self_weight': self_weight,
                'udl_self_weight': udl,
                'unit': 'kN/m'
            }
            
        elif member_type == 'column':
            # Column self-weight = cross-sectional area × height × density
            volume = breadth * depth * length  # m³
            self_weight = volume * density     # kN
            
            return {
                'volume': volume,
                'total_self_weight': self_weight,
                'unit': 'kN'
            }
            
        elif member_type == 'slab':
            # Slab self-weight = thickness × area × density
            area = length * breadth           # m²
            volume = area * depth             # m³
            self_weight = volume * density    # kN
            self_weight_per_area = density * depth  # kN/m²
            
            return {
                'area': area,
                'volume': volume,
                'total_self_weight': self_weight,
                'self_weight_per_area': self_weight_per_area,
                'unit': 'kN/m²'
            }
            
        elif member_type == 'footing':
            # Footing self-weight = volume × density
            volume = length * breadth * depth # m³
            self_weight = volume * density    # kN
            
            return {
                'volume': volume,
                'total_self_weight': self_weight,
                'unit': 'kN'
            }
    
    def calculate_superimposed_dead_load(self, member_type: str, building_use: str = 'residential',
                                       include_partition: bool = True, 
                                       include_finishes: bool = True) -> Dict[str, float]:
        """
        Calculate superimposed dead loads (finishes, partitions, etc.)
        
        Args:
            member_type: Type of structural member
            building_use: Type of building usage
            include_partition: Include partition wall loads
            include_finishes: Include finish loads
            
        Returns:
            Dictionary with superimposed dead load values
        """
        loads = {}
        
        if member_type in ['beam', 'slab']:
            if include_finishes:
                # Floor finishes (kN/m²)
                loads['floor_finish'] = 1.0      # Flooring + screed
                loads['ceiling_finish'] = 0.5    # False ceiling + plaster
                loads['waterproofing'] = 0.3     # Waterproofing (if applicable)
            
            if include_partition:
                # Partition wall load (kN/m²)
                if building_use in ['residential', 'office']:
                    loads['partition_walls'] = 1.0
                elif building_use in ['retail', 'industrial']:
                    loads['partition_walls'] = 1.5
                else:
                    loads['partition_walls'] = 1.0
            
            # MEP services load
            loads['mep_services'] = 0.5
            
            total_sidl = sum(loads.values())
            loads['total_sidl'] = total_sidl
            loads['unit'] = 'kN/m²'
            
        return loads
    
    def calculate_live_load(self, member_type: str, building_use: str = 'residential',
                          dimensions: Dict[str, float] = None) -> Dict[str, float]:
        """
        Calculate live loads based on IS 875 Part 2
        
        Args:
            member_type: Type of structural member
            building_use: Type of building usage
            dimensions: Member dimensions
            
        Returns:
            Dictionary with live load values
        """
        base_live_load = self.LIVE_LOADS.get(building_use, 2.0)
        
        if member_type == 'beam':
            # For beams, live load is distributed load
            return {
                'live_load': base_live_load,
                'unit': 'kN/m²',
                'note': 'Apply to tributary area'
            }
            
        elif member_type == 'column':
            # For columns, live load comes from tributary area
            # This will be calculated based on floor area and number of floors
            return {
                'live_load_per_floor': base_live_load,
                'unit': 'kN/m²',
                'note': 'Multiply by tributary area and number of floors'
            }
            
        elif member_type == 'slab':
            return {
                'live_load': base_live_load,
                'unit': 'kN/m²'
            }
            
        elif member_type == 'footing':
            return {
                'live_load': base_live_load,
                'unit': 'kN/m²',
                'note': 'From superstructure'
            }
    
    def calculate_wind_load(self, height: float, wind_zone: str = 'zone_2',
                          terrain_category: int = 2, importance_factor: float = 1.0) -> Dict[str, float]:
        """
        Calculate wind loads based on IS 875 Part 3
        
        Args:
            height: Height of structure in meters
            wind_zone: Wind speed zone (zone_1 to zone_6)
            terrain_category: Terrain category (1-4)
            importance_factor: Importance factor for structure
            
        Returns:
            Dictionary with wind load calculations
        """
        # Basic wind speed
        vb = self.WIND_SPEEDS.get(wind_zone, 44)
        
        # Terrain and height factor (k2)
        if terrain_category == 1:  # Open terrain
            k2 = 1.05 if height <= 10 else 1.05 * (height/10)**0.15
        elif terrain_category == 2:  # Open terrain with scattered obstructions
            k2 = 1.00 if height <= 10 else 1.00 * (height/10)**0.15
        elif terrain_category == 3:  # Built-up terrain
            k2 = 0.91 if height <= 10 else 0.91 * (height/10)**0.15
        else:  # Dense urban terrain
            k2 = 0.80 if height <= 10 else 0.80 * (height/10)**0.15
        
        # Topography factor (k3)
        k3 = 1.0  # Assuming normal topography
        
        # Design wind speed
        vz = vb * k2 * k3
        
        # Design wind pressure
        pz = 0.6 * (vz**2) / 1000  # kN/m²
        
        # Apply importance factor
        design_wind_pressure = pz * importance_factor
        
        return {
            'basic_wind_speed': vb,
            'terrain_height_factor': k2,
            'topography_factor': k3,
            'design_wind_speed': vz,
            'wind_pressure': design_wind_pressure,
            'unit': 'kN/m²',
            'height': height,
            'zone': wind_zone
        }
    
    def calculate_column_axial_load(self, column_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate total axial load on column including:
        - Self weight of column
        - Dead load from beams and slabs
        - Live load from floors
        - Wind load effects
        
        Args:
            column_data: Dictionary containing:
                - dimensions: column dimensions
                - building_data: floors, area per floor, building use
                - wind_data: wind zone, height
                
        Returns:
            Dictionary with total axial loads
        """
        dimensions = column_data.get('dimensions', {})
        building_data = column_data.get('building_data', {})
        wind_data = column_data.get('wind_data', {})
        
        # Column self-weight
        self_weight = self.calculate_self_weight('column', dimensions)
        
        # Building parameters
        num_floors = building_data.get('num_floors', 1)
        floor_area_per_column = building_data.get('tributary_area', 20.0)  # m²
        building_use = building_data.get('building_use', 'residential')
        floor_height = building_data.get('floor_height', 3.0)  # m
        
        # Dead load from floors
        slab_thickness = building_data.get('slab_thickness', 150)  # mm
        slab_self_weight = self.MATERIAL_DENSITIES['concrete'] * (slab_thickness/1000)  # kN/m²
        
        # Superimposed dead load
        sidl = self.calculate_superimposed_dead_load('slab', building_use)
        total_sidl = sidl.get('total_sidl', 2.0)
        
        # Live load
        live_load_data = self.calculate_live_load('slab', building_use)
        live_load_per_floor = live_load_data.get('live_load', 2.0)
        
        # Calculate loads per floor
        dead_load_per_floor = (slab_self_weight + total_sidl) * floor_area_per_column
        live_load_per_floor_total = live_load_per_floor * floor_area_per_column
        
        # Total loads
        total_dead_load = (self_weight['total_self_weight'] + 
                          dead_load_per_floor * num_floors)
        total_live_load = live_load_per_floor_total * num_floors
        
        # Wind load calculation
        total_height = float(dimensions.get('length', 3000))/1000  # Column height in m
        if wind_data:
            wind_load_data = self.calculate_wind_load(
                total_height,
                wind_data.get('wind_zone', 'zone_2'),
                wind_data.get('terrain_category', 2)
            )
            wind_pressure = wind_load_data['wind_pressure']
            # Assuming wind load on building transfers to columns
            wind_area_per_column = building_data.get('wind_area_per_column', 15.0)  # m²
            total_wind_load = wind_pressure * wind_area_per_column
        else:
            total_wind_load = 0
            wind_pressure = 0
        
        # Load combinations as per IS 1893
        combination_1 = 1.5 * (total_dead_load + total_live_load)  # DL + LL
        combination_2 = 1.2 * (total_dead_load + total_live_load + total_wind_load)  # DL + LL + WL
        combination_3 = 1.5 * (total_dead_load + 0.25 * total_live_load + total_wind_load)  # DL + 0.25LL + WL
        
        critical_load = max(combination_1, combination_2, combination_3)
        
        return {
            'column_self_weight': self_weight['total_self_weight'],
            'dead_load_from_floors': dead_load_per_floor * num_floors,
            'total_dead_load': total_dead_load,
            'total_live_load': total_live_load,
            'total_wind_load': total_wind_load,
            'load_combination_1': combination_1,
            'load_combination_2': combination_2,
            'load_combination_3': combination_3,
            'critical_axial_load': critical_load,
            'wind_pressure': wind_pressure,
            'num_floors': num_floors,
            'tributary_area': floor_area_per_column,
            'unit': 'kN'
        }
    
    def calculate_beam_loads(self, beam_data: Dict[str, Any]) -> Dict[str, float]:
        """
        Calculate total loads on beam including:
        - Self weight
        - Dead load from slab
        - Live load
        - Wall loads (if any)
        
        Args:
            beam_data: Dictionary containing beam and loading information
            
        Returns:
            Dictionary with total beam loads
        """
        dimensions = beam_data.get('dimensions', {})
        loading_data = beam_data.get('loading_data', {})
        
        # Beam self-weight
        self_weight = self.calculate_self_weight('beam', dimensions)
        beam_udl = self_weight['udl_self_weight']
        
        # Slab load on beam
        tributary_width = loading_data.get('tributary_width', 3.0)  # m
        slab_thickness = loading_data.get('slab_thickness', 150)  # mm
        building_use = loading_data.get('building_use', 'residential')
        
        # Dead load from slab
        slab_self_weight = self.MATERIAL_DENSITIES['concrete'] * (slab_thickness/1000)
        sidl = self.calculate_superimposed_dead_load('slab', building_use)
        total_slab_dead_load = (slab_self_weight + sidl.get('total_sidl', 2.0)) * tributary_width
        
        # Live load from slab
        live_load_data = self.calculate_live_load('slab', building_use)
        slab_live_load = live_load_data.get('live_load', 2.0) * tributary_width
        
        # Wall load (if any)
        wall_load = loading_data.get('wall_load', 0)  # kN/m
        
        # Total loads
        total_dead_load = beam_udl + total_slab_dead_load + wall_load
        total_live_load = slab_live_load
        
        # Load combinations
        combination_1 = 1.5 * (total_dead_load + total_live_load)
        
        return {
            'beam_self_weight': beam_udl,
            'slab_dead_load': total_slab_dead_load,
            'slab_live_load': slab_live_load,
            'wall_load': wall_load,
            'total_dead_load': total_dead_load,
            'total_live_load': total_live_load,
            'factored_load': combination_1,
            'tributary_width': tributary_width,
            'unit': 'kN/m'
        }


def auto_calculate_loads(member_type: str, design_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main function to automatically calculate ALL loads for a structural member
    No manual load input required - everything calculated from building parameters
    
    Args:
        member_type: 'beam', 'column', 'slab', 'footing'
        design_data: Complete design data including dimensions and building parameters
        
    Returns:
        Updated design data with calculated loads
    """
    calculator = LoadCalculator()
    
    # Extract or set default building and environmental data
    building_data = design_data.get('building_parameters', {})
    
    # Set intelligent defaults based on member type and common practices
    if not building_data:
        building_data = {
            'building_use': 'residential',
            'num_floors': 1,
            'floor_height': 3.0,
            'slab_thickness': 150,
            'tributary_area': 20.0,
            'tributary_width': 3.0
        }
        design_data['building_parameters'] = building_data
    
    # Set default values for missing parameters
    building_data.setdefault('building_use', 'residential')
    building_data.setdefault('num_floors', 1)
    building_data.setdefault('floor_height', 3.0)
    building_data.setdefault('slab_thickness', 150)
    building_data.setdefault('tributary_area', 20.0)
    building_data.setdefault('tributary_width', 3.0)
    building_data.setdefault('wall_load', 0)  # No wall load by default
    
    wind_data = design_data.get('wind_parameters', {})
    if not wind_data:
        wind_data = {
            'wind_zone': 'zone_2',
            'terrain_category': 2,
            'importance_factor': 1.0
        }
        design_data['wind_parameters'] = wind_data
    
    # Set default values for missing wind parameters
    wind_data.setdefault('wind_zone', 'zone_2')
    wind_data.setdefault('terrain_category', 2)
    wind_data.setdefault('importance_factor', 1.0)
    
    if member_type == 'column':
        # Calculate complete column loads
        column_data = {
            'dimensions': design_data['dimensions'],
            'building_data': building_data,
            'wind_data': wind_data
        }
        
        load_results = calculator.calculate_column_axial_load(column_data)
        
        # Calculate moment from wind load (simplified approach)
        total_height = float(design_data['dimensions'].get('length', 3000))/1000  # m
        wind_load_data = calculator.calculate_wind_load(
            total_height,
            wind_data.get('wind_zone', 'zone_2'),
            wind_data.get('terrain_category', 2)
        )
        
        # Wind moment = wind pressure × height² / 6 (simplified)
        wind_moment = wind_load_data['wind_pressure'] * (total_height ** 2) / 6
        
        # Update design data with calculated loads
        design_data['loads'] = {
            'axial_load': str(load_results['critical_axial_load']),
            'moment': str(max(50, wind_moment))  # Minimum 50 kNm or calculated wind moment
        }
        design_data['load_calculations'] = load_results
        design_data['wind_calculations'] = wind_load_data
        
    elif member_type == 'beam':
        # Calculate beam loads
        beam_data = {
            'dimensions': design_data['dimensions'],
            'loading_data': building_data
        }
        
        load_results = calculator.calculate_beam_loads(beam_data)
        
        # Calculate wind load on beam (lateral load)
        beam_height = float(design_data['dimensions'].get('depth', 600))/1000  # m
        wind_load_data = calculator.calculate_wind_load(
            beam_height,
            wind_data.get('wind_zone', 'zone_2'),
            wind_data.get('terrain_category', 2)
        )
        
        # Wind load on beam face (simplified)
        beam_width = float(design_data['dimensions'].get('breadth', 300))/1000  # m
        wind_load_on_beam = wind_load_data['wind_pressure'] * beam_width  # kN/m
        
        # Update design data with calculated loads
        design_data['loads'] = {
            'dead_load': str(load_results['total_dead_load']),
            'live_load': str(load_results['total_live_load']),
            'wind_load': str(wind_load_on_beam),
            'factored_load': str(load_results['factored_load'])
        }
        design_data['load_calculations'] = load_results
        design_data['wind_calculations'] = wind_load_data
        
    elif member_type == 'slab':
        # Calculate slab loads
        self_weight = calculator.calculate_self_weight('slab', design_data['dimensions'])
        sidl = calculator.calculate_superimposed_dead_load('slab', building_data.get('building_use', 'residential'))
        live_load = calculator.calculate_live_load('slab', building_data.get('building_use', 'residential'))
        
        # Wind uplift on roof slabs
        slab_height = building_data.get('floor_height', 3.0) * building_data.get('num_floors', 1)
        wind_load_data = calculator.calculate_wind_load(
            slab_height,
            wind_data.get('wind_zone', 'zone_2'),
            wind_data.get('terrain_category', 2)
        )
        
        # Wind uplift = -0.8 × wind pressure (for roof slabs)
        wind_uplift = -0.8 * wind_load_data['wind_pressure']
        
        total_dead_load = self_weight['self_weight_per_area'] + sidl.get('total_sidl', 2.0)
        total_live_load = live_load.get('live_load', 2.0)
        
        design_data['loads'] = {
            'dead_load': str(total_dead_load),
            'live_load': str(total_live_load),
            'wind_load': str(wind_uplift),
            'total_load': str(total_dead_load + total_live_load)
        }
        design_data['load_calculations'] = {
            'self_weight': self_weight,
            'sidl': sidl,
            'live_load': live_load
        }
        design_data['wind_calculations'] = wind_load_data
        
    elif member_type == 'footing':
        # Calculate footing loads from superstructure
        # This is typically the reaction from columns
        
        # Estimate loads based on building parameters
        num_floors = building_data.get('num_floors', 1)
        tributary_area = building_data.get('tributary_area', 20.0)
        building_use = building_data.get('building_use', 'residential')
        
        # Live load
        live_load_data = calculator.calculate_live_load('slab', building_use)
        live_load_per_floor = live_load_data.get('live_load', 2.0)
        
        # Dead load (approximate)
        slab_thickness = building_data.get('slab_thickness', 150)
        slab_dead_load = calculator.MATERIAL_DENSITIES['concrete'] * (slab_thickness/1000)
        sidl = calculator.calculate_superimposed_dead_load('slab', building_use)
        total_dead_load_per_floor = (slab_dead_load + sidl.get('total_sidl', 2.0))
        
        # Total loads on footing
        total_dead_load = total_dead_load_per_floor * tributary_area * num_floors
        total_live_load = live_load_per_floor * tributary_area * num_floors
        
        # Wind load effect (overturning moment)
        building_height = building_data.get('floor_height', 3.0) * num_floors
        wind_load_data = calculator.calculate_wind_load(
            building_height,
            wind_data.get('wind_zone', 'zone_2'),
            wind_data.get('terrain_category', 2)
        )
        
        # Wind overturning moment
        wind_area = building_height * 10  # Assume 10m building width
        wind_force = wind_load_data['wind_pressure'] * wind_area
        wind_moment = wind_force * building_height / 2
        
        # Footing self-weight
        footing_self_weight = calculator.calculate_self_weight('footing', design_data['dimensions'])
        
        design_data['loads'] = {
            'vertical_load': str(total_dead_load + total_live_load + footing_self_weight['total_self_weight']),
            'dead_load': str(total_dead_load),
            'live_load': str(total_live_load),
            'wind_moment': str(wind_moment)
        }
        design_data['load_calculations'] = {
            'dead_load_per_floor': total_dead_load_per_floor,
            'live_load_per_floor': live_load_per_floor,
            'total_dead_load': total_dead_load,
            'total_live_load': total_live_load,
            'footing_self_weight': footing_self_weight['total_self_weight'],
            'num_floors': num_floors,
            'tributary_area': tributary_area
        }
        design_data['wind_calculations'] = wind_load_data
    
    return design_data

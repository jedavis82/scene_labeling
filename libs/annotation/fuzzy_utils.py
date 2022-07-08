"""
This class constructs the universes and memberships of discourse for the proximity, overlap, and spatial
relationship fuzzy variables.
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np


def create_universes_membership_functions():
    proximity = ctrl.Antecedent(universe=np.arange(-1.1, 1.1, 0.1), label='proximity')
    overlap = ctrl.Antecedent(universe=np.arange(-1.1, 1.1, 0.1), label='overlap')
    spatial_relationships = ctrl.Antecedent(universe=np.arange(-1, 361, 1), label='spatial_relationships')

    proximity['Very Close'] = fuzz.trapmf(proximity.universe, [-0.1, 0.0, 0.3, 0.6])
    proximity['Close'] = fuzz.trapmf(proximity.universe, [-0.35, -0.3, -0.05, 0.0])
    proximity['Medium'] = fuzz.trapmf(proximity.universe, [-0.7, -0.5, -0.35, -0.25])
    proximity['Far'] = fuzz.trapmf(proximity.universe, [-0.85, -0.75, -0.6, -0.5])
    proximity['Very Far'] = fuzz.trapmf(proximity.universe, [-1.0, -0.95, -0.8, -0.75])

    overlap['Overlap'] = fuzz.trapmf(overlap.universe, [0.0, 0.2, 0.7, 1.0])
    overlap['No Overlap'] = fuzz.trapmf(overlap.universe, [-1.0, -0.7, -0.2, 0.0])

    # 0 < HOF < 30 | 331 < HOF < 360: Right
    spatial_relationships['Right1'] = fuzz.trimf(spatial_relationships.universe, [-1, 15, 31])
    spatial_relationships['Right2'] = fuzz.trimf(spatial_relationships.universe, [330, 345, 360])
    # 31 < HOF < 60: Above Right
    spatial_relationships['Above Right'] = fuzz.trimf(spatial_relationships.universe, [30, 45, 61])
    # 61 < HOF < 120: Above
    spatial_relationships['Above'] = fuzz.trimf(spatial_relationships.universe, [60, 90, 121])
    # 121 < HOF < 150: Above Left
    spatial_relationships['Above Left'] = fuzz.trimf(spatial_relationships.universe, [120, 135, 151])
    # 151 < HOF < 210: Left
    spatial_relationships['Left'] = fuzz.trimf(spatial_relationships.universe, [150, 180, 211])
    # 211 < HOF < 240: Below Left
    spatial_relationships['Below Left'] = fuzz.trimf(spatial_relationships.universe, [210, 225, 241])
    # 241 < HOF < 300: Below
    spatial_relationships['Below'] = fuzz.trimf(spatial_relationships.universe, [240, 270, 301])
    # 301 < HOF < 330: Below Right
    spatial_relationships['Below Right'] = fuzz.trimf(spatial_relationships.universe, [300, 315, 331])

    return proximity, overlap, spatial_relationships

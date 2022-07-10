"""
FIS for the person-vehicle interactions
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from fuzzy_utils import create_universes_membership_functions


class VehicleRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_cycle_rules()
        self.__create_passenger_rules()
        self.__create_personal_rules()

    def __create_universes_of_discourse(self):
        self.__cycle_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='cycle_interaction')
        self.__passenger_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                       label='passenger_interaction')
        self.__personal_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                      label='personal_interaction')

    def __create_membership_functions(self):
        self.__cycle_interaction['Riding'] = fuzz.trimf(self.__cycle_interaction.universe, [0.4, 0.7, 1.0])
        self.__cycle_interaction['Not Riding'] = fuzz.trimf(self.__cycle_interaction.universe, [0.0, 0.3, 0.6])
        self.__passenger_interaction['Riding'] = fuzz.trimf(self.__passenger_interaction.universe, [0.4, 0.7, 1.0])
        self.__passenger_interaction['Not Riding'] = fuzz.trimf(self.__passenger_interaction.universe, [0.0, 0.3, 0.6])
        self.__personal_interaction['Driving'] = fuzz.trimf(self.__personal_interaction.universe, [0.4, 0.7, 1.0])
        self.__personal_interaction['Not Driving'] = fuzz.trimf(self.__personal_interaction.universe, [0.0, 0.3, 0.6])

    def __create_cycle_rules(self):
        # IF overlap AND very close AND above THEN riding
        self.__riding_rule1 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'] &
                                        (self.__spatial_relationships['Above Left'] |
                                         self.__spatial_relationships['Above'] |
                                         self.__spatial_relationships['Above Right'] |
                                         self.__spatial_relationships['Left'] |
                                         self.__spatial_relationships['Right1'] |
                                         self.__spatial_relationships['Right2']),
                                        self.__cycle_interaction['Riding'])

        # IF overlap AND very close AND not above THEN not riding
        self.__not_riding_rule1 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'] &
                                            (self.__spatial_relationships['Below Right'] |
                                             self.__spatial_relationships['Below'] |
                                             self.__spatial_relationships['Below Left']),
                                            self.__cycle_interaction['Not Riding'])

        # IF overlap AND close OR medium OR far OR very far THEN not riding
        self.__not_riding_rule2 = ctrl.Rule(self.__overlap['Overlap'] &
                                            (self.__proximity['Close'] | self.__proximity['Medium'] |
                                             self.__proximity['Far'] | self.__proximity['Very Far']),
                                            self.__cycle_interaction['Not Riding'])

        # IF no overlap THEN not riding
        self.__not_riding_rule3 = ctrl.Rule(self.__overlap['No Overlap'], self.__cycle_interaction['Not Riding'])

        self.__riding_ctrl = ctrl.ControlSystem([self.__riding_rule1, self.__not_riding_rule1,
                                                 self.__not_riding_rule2, self.__not_riding_rule3])
        self.__riding_sim = ctrl.ControlSystemSimulation(self.__riding_ctrl, flush_after_run=100)

    def __create_passenger_rules(self):
        # IF overlap AND very close THEN riding
        self.__riding_in_rule1 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'],
                                           self.__passenger_interaction['Riding'])
        # IF overlap AND close OR medium OR far OR very far THEN not riding
        self.__not_riding_in_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                               (self.__proximity['Close'] | self.__proximity['Medium'] |
                                                self.__proximity['Far'] | self.__proximity['Very Far']),
                                               self.__passenger_interaction['Not Riding'])
        # IF no overlap THEN not riding
        self.__not_riding_in_rule2 = ctrl.Rule(self.__overlap['No Overlap'],
                                               self.__passenger_interaction['Not Riding'])

        self.__passenger_ctrl = ctrl.ControlSystem([self.__riding_in_rule1, self.__not_riding_in_rule1,
                                                    self.__not_riding_in_rule2])
        self.__passenger_sim = ctrl.ControlSystemSimulation(self.__passenger_ctrl, flush_after_run=100)

    def __create_personal_rules(self):
        # IF overlap AND very close THEN driving
        self.__driving_rule1 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'] &
                                         (self.__spatial_relationships['Right1'] |
                                          self.__spatial_relationships['Right2'] |
                                          self.__spatial_relationships['Above Right'] |
                                          self.__spatial_relationships['Above'] |
                                          self.__spatial_relationships['Above Left'] |
                                          self.__spatial_relationships['Left']),
                                         self.__personal_interaction['Driving'])
        # IF overlap AND close OR medium OR far OR very far THEN not driving
        self.__not_driving_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                             (self.__proximity['Close'] | self.__proximity['Medium'] |
                                              self.__proximity['Far'] | self.__proximity['Very Far']),
                                             self.__personal_interaction['Not Driving'])
        # IF no overlap THEN not driving
        self.__not_driving_rule2 = ctrl.Rule(self.__overlap['No Overlap'], self.__personal_interaction['Not Driving'])

        # IF overlap AND very close AND below(s) THEN not driving
        self.__not_driving_rule3 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'] &
                                             (self.__spatial_relationships['Below Left'] |
                                              self.__spatial_relationships['Below'] |
                                              self.__spatial_relationships['Below Right']),
                                             self.__personal_interaction['Not Driving'])

        self.__personal_ctrl = ctrl.ControlSystem([self.__driving_rule1, self.__not_driving_rule1,
                                                   self.__not_driving_rule2, self.__not_driving_rule3])
        self.__personal_sim = ctrl.ControlSystemSimulation(self.__personal_ctrl, flush_after_run=100)

    def compute_cycle_interaction(self, giou, iou, sr_angle):
        self.__riding_sim.input['overlap'] = iou
        self.__riding_sim.input['proximity'] = giou
        self.__riding_sim.input['spatial_relationships'] = sr_angle
        self.__riding_sim.compute()
        if self.__show_sim_result:
            self.__cycle_interaction.view(sim=self.__riding_sim)
        riding_result = self.__riding_sim.output['cycle_interaction']
        riding = fuzz.interp_membership(self.__cycle_interaction.universe, self.__cycle_interaction['Riding'].mf,
                                        riding_result)
        not_riding = fuzz.interp_membership(self.__cycle_interaction.universe,
                                            self.__cycle_interaction['Not Riding'].mf, riding_result)
        membership = {'Riding': riding, 'Not Riding': not_riding}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Riding':
            return None
        else:
            return ret_label

    def compute_passenger_interaction(self, giou, iou, sr_angle):
        self.__passenger_sim.input['overlap'] = iou
        self.__passenger_sim.input['proximity'] = giou
        self.__passenger_sim.compute()
        if self.__show_sim_result:
            self.__passenger_interaction.view(sim=self.__passenger_sim)
        riding_result = self.__passenger_sim.output['passenger_interaction']
        riding = fuzz.interp_membership(self.__passenger_interaction.universe,
                                        self.__passenger_interaction['Riding'].mf, riding_result)
        not_riding = fuzz.interp_membership(self.__passenger_interaction.universe,
                                            self.__passenger_interaction['Not Riding'].mf, riding_result)
        membership = {'Riding': riding, 'Not Riding': not_riding}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Riding':
            return None
        else:
            return ret_label

    def compute_personal_interaction(self, giou, iou, sr_angle):
        self.__personal_sim.input['overlap'] = iou
        self.__personal_sim.input['proximity'] = giou
        self.__personal_sim.input['spatial_relationships'] = sr_angle
        self.__personal_sim.compute()
        if self.__show_sim_result:
            self.__personal_interaction.view(sim=self.__personal_sim)
        driving_result = self.__personal_sim.output['personal_interaction']
        driving = fuzz.interp_membership(self.__personal_interaction.universe,
                                         self.__personal_interaction['Driving'].mf, driving_result)
        not_driving = fuzz.interp_membership(self.__personal_interaction.universe,
                                             self.__personal_interaction['Not Driving'].mf, driving_result)
        membership = {'Driving': driving, 'Not Driving': not_driving}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Driving':
            return None
        else:
            return ret_label

    def compute_interaction(self, label, dom_cat, sub_cat, giou, iou, sr_angle):
        if label == 'motorcycle' or label == 'bicycle' or label == 'motorbike':
            res_label = self.compute_cycle_interaction(giou, iou, sr_angle)
            return res_label
        if dom_cat == 'passenger':
            res_label = self.compute_passenger_interaction(giou, iou, sr_angle)
            return res_label
        if dom_cat == 'personal':
            res_label = self.compute_personal_interaction(giou, iou, sr_angle)
            return res_label
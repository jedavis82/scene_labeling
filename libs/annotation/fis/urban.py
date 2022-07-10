"""
FIS for the person-urban interactions
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from fuzzy_utils import create_universes_membership_functions


class UrbanRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_bench_rules()
        self.__create_parking_meter_rules()
        self.__create_traffic_light_rules()
        self.__create_general_rules()

    def __create_universes_of_discourse(self):
        self.__bench_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='bench_interaction')
        self.__traffic_light_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                           label='traffic_light_interaction')
        self.__parking_meter_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                           label='parking_meter_interaction')
        # All other objects can be general interactions
        self.__general_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                     label='general_interaction')

    def __create_membership_functions(self):
        self.__bench_interaction['Sitting'] = fuzz.trimf(self.__bench_interaction.universe, [0.4, 0.7, 1.0])
        self.__bench_interaction['Not Sitting'] = fuzz.trimf(self.__bench_interaction.universe, [0.0, 0.3, 0.6])
        self.__traffic_light_interaction['At Intersection'] = fuzz.trimf(self.__traffic_light_interaction.universe,
                                                                         [0.4, 0.7, 1.0])
        self.__traffic_light_interaction['Not At Intersection'] = fuzz.trimf(self.__traffic_light_interaction.universe,
                                                                             [0.0, 0.3, 0.6])
        self.__parking_meter_interaction['Using'] = fuzz.trimf(self.__parking_meter_interaction.universe,
                                                               [0.4, 0.7, 1.0])
        self.__parking_meter_interaction['Not Using'] = fuzz.trimf(self.__parking_meter_interaction.universe,
                                                                   [0.0, 0.3, 0.6])
        self.__general_interaction['Interacting'] = fuzz.trimf(self.__general_interaction.universe,
                                                               [0.4, 0.7, 1.0])
        self.__general_interaction['Not Interacting'] = fuzz.trimf(self.__general_interaction.universe,
                                                                   [0.0, 0.3, 0.6])

    def __create_bench_rules(self):
        # IF overlap AND very close OR close THEN sitting
        self.__sitting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                         (self.__proximity['Very Close'] | self.__proximity['Close']),
                                         self.__bench_interaction['Sitting'])

        # IF overlap AND close OR medium OR far OR very far THEN not sitting
        self.__not_sitting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                             (self.__proximity['Medium'] | self.__proximity['Far'] |
                                              self.__proximity['Very Far']), self.__bench_interaction['Not Sitting'])

        # IF no overlap THEN not sitting
        self.__not_sitting_rule2 = ctrl.Rule(self.__overlap['No Overlap'], self.__bench_interaction['Not Sitting'])

        self.__bench_ctrl = ctrl.ControlSystem([self.__sitting_rule1, self.__not_sitting_rule1,
                                                self.__not_sitting_rule2])
        self.__bench_sim = ctrl.ControlSystemSimulation(self.__bench_ctrl, flush_after_run=100)

    def __create_traffic_light_rules(self):
        # IF not below THEN at intersection
        self.__intersection_rule1 = ctrl.Rule((self.__spatial_relationships['Left'] |
                                               self.__spatial_relationships['Below Left'] |
                                               self.__spatial_relationships['Below'] |
                                               self.__spatial_relationships['Below Right'] |
                                               self.__spatial_relationships['Right1'] |
                                               self.__spatial_relationships['Right2']),
                                              self.__traffic_light_interaction['At Intersection'])
        # IF below THEN not at intersection
        self.__not_intersection_rule1 = ctrl.Rule((self.__spatial_relationships['Above Right'] |
                                                   self.__spatial_relationships['Above'] |
                                                   self.__spatial_relationships['Above Right']),
                                                  self.__traffic_light_interaction['Not At Intersection'])
        self.__traffic_light_ctrl = ctrl.ControlSystem([self.__intersection_rule1, self.__not_intersection_rule1])
        self.__traffic_light_sim = ctrl.ControlSystemSimulation(self.__traffic_light_ctrl, flush_after_run=100)

    def __create_parking_meter_rules(self):
        # IF overlap AND very close THEN using
        self.__using_rule1 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'],
                                       self.__parking_meter_interaction['Using'])

        # IF overlap AND close OR medium OR far OR very far THEN not using
        self.__not_using_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                           (self.__proximity['Close'] | self.__proximity['Medium'] |
                                            self.__proximity['Far'] | self.__proximity['Very Far']),
                                           self.__parking_meter_interaction['Not Using'])
        # IF no overlap THEN not using
        self.__not_using_rule2 = ctrl.Rule(self.__overlap['No Overlap'], self.__parking_meter_interaction['Not Using'])

        self.__parking_meter_ctrl = ctrl.ControlSystem([self.__using_rule1, self.__not_using_rule1,
                                                        self.__not_using_rule2])
        self.__parking_meter_sim = ctrl.ControlSystemSimulation(self.__parking_meter_ctrl, flush_after_run=100)

    def __create_general_rules(self):
        # IF overlap AND very close OR close THEN interacting
        self.__interacting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                             (self.__proximity['Very Close'] | self.__proximity['Close']),
                                             self.__general_interaction['Interacting'])
        # IF overlap AND medium OR far OR very far THEN not interacting
        self.__not_interacting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                                 (self.__proximity['Medium'] | self.__proximity['Far'] |
                                                  self.__proximity['Very Far']),
                                                 self.__general_interaction['Not Interacting'])
        # IF no overlap THEN not interacting
        self.__not_interacting_rule2 = ctrl.Rule(self.__overlap['No Overlap'],
                                                 self.__general_interaction['Not Interacting'])
        self.__general_ctrl = ctrl.ControlSystem([self.__interacting_rule1, self.__not_interacting_rule1,
                                                  self.__not_interacting_rule2])
        self.__general_sim = ctrl.ControlSystemSimulation(self.__general_ctrl, flush_after_run=100)

    def compute_bench_interaction(self, giou, iou, sr_angle):
        self.__bench_sim.input['overlap'] = iou
        self.__bench_sim.input['proximity'] = giou
        self.__bench_sim.compute()
        if self.__show_sim_result:
            self.__bench_interaction.view(sim=self.__bench_sim)
        sitting_result = self.__bench_sim.output['bench_interaction']
        sitting = fuzz.interp_membership(self.__bench_interaction.universe,
                                         self.__bench_interaction['Sitting'].mf, sitting_result)
        not_sitting = fuzz.interp_membership(self.__bench_interaction.universe,
                                             self.__bench_interaction['Not Sitting'].mf, sitting_result)
        membership = {'Sitting': sitting, 'Not Sitting': not_sitting}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Sitting':
            return None
        else:
            return ret_label

    def compute_traffic_light_interaction(self, giou, iou, sr_angle):
        self.__traffic_light_sim.input['spatial_relationships'] = sr_angle
        self.__traffic_light_sim.compute()
        if self.__show_sim_result:
            self.__traffic_light_interaction.view(sim=self.__traffic_light_sim)
        intersection_result = self.__traffic_light_sim.output['traffic_light_interaction']
        at_intersection = fuzz.interp_membership(self.__traffic_light_interaction.universe,
                                                 self.__traffic_light_interaction['At Intersection'].mf,
                                                 intersection_result)
        not_at_intersection = fuzz.interp_membership(self.__traffic_light_interaction.universe,
                                                     self.__traffic_light_interaction['Not At Intersection'].mf,
                                                     intersection_result)
        membership = {'At Intersection': at_intersection, 'Not At Intersection': not_at_intersection}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not At Intersection':
            return None
        else:
            return ret_label

    def compute_parking_meter_interaction(self, giou, iou, sr_angle):
        self.__parking_meter_sim.input['overlap'] = iou
        self.__parking_meter_sim.input['proximity'] = giou
        self.__parking_meter_sim.compute()
        if self.__show_sim_result:
            self.__parking_meter_interaction.view(sim=self.__parking_meter_sim)
        using_result = self.__parking_meter_sim.output['parking_meter_interaction']
        using = fuzz.interp_membership(self.__parking_meter_interaction.universe,
                                       self.__parking_meter_interaction['Using'].mf, using_result)
        not_using = fuzz.interp_membership(self.__parking_meter_interaction.universe,
                                           self.__parking_meter_interaction['Not Using'].mf, using_result)
        membership = {'Using': using, 'Not Using': not_using}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Using':
            return None
        else:
            return ret_label

    def compute_general_interaction(self, giou, iou, sr_angle):
        self.__general_sim.input['overlap'] = iou
        self.__general_sim.input['proximity'] = giou
        self.__general_sim.compute()
        if self.__show_sim_result:
            self.__general_interaction.view(sim=self.__general_sim)
        interacting_result = self.__general_sim.output['general_interaction']
        interacting = fuzz.interp_membership(self.__general_interaction.universe,
                                             self.__general_interaction['Interacting'].mf, interacting_result)
        not_interacting = fuzz.interp_membership(self.__general_interaction.universe,
                                                 self.__general_interaction['Not Interacting'].mf, interacting_result)
        membership = {'Interacting': interacting, 'Not Interacting': not_interacting}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Interacting':
            return None
        else:
            return ret_label

    def compute_interaction(self, label, dom_cat, sub_cat, giou, iou, sr_angle):
        if label == 'bench':
            res_label = self.compute_bench_interaction(giou, iou, sr_angle)
            return res_label
        if label == 'parking_meter':
            res_label = self.compute_parking_meter_interaction(giou, iou, sr_angle)
            return res_label
        if label == 'traffic_light':
            res_label = self.compute_traffic_light_interaction(giou, iou, sr_angle)
            return res_label
        res_label = self.compute_general_interaction(giou, iou, sr_angle)
        return res_label

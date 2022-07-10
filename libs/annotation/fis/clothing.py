"""
FIS for the person-clothing interactions
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from libs.annotation.fuzzy_utils import create_universes_membership_functions


class ClothingRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_worn_clothing_rules()
        self.__create_carried_clothing_rules()

    def __create_universes_of_discourse(self):
        self.__worn_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='worn_interaction')
        self.__carried_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='carried_interaction')

    def __create_membership_functions(self):
        self.__worn_interaction['Wearing'] = fuzz.trimf(self.__worn_interaction.universe, [0.4, 0.7, 1.0])
        self.__worn_interaction['Not Wearing'] = fuzz.trimf(self.__worn_interaction.universe, [0.0, 0.3, 0.6])
        self.__carried_interaction['Carrying'] = fuzz.trimf(self.__carried_interaction.universe, [0.4, 0.7, 1.0])
        self.__carried_interaction['Not Carrying'] = fuzz.trimf(self.__carried_interaction.universe, [0.0, 0.3, 0.6])

    def __create_worn_clothing_rules(self):
        # IF overlap AND very close OR close THEN wearing
        self.__wearing_rule = ctrl.Rule(self.__overlap['Overlap'] &
                                        (self.__proximity['Close'] | self.__proximity['Very Close']),
                                        self.__worn_interaction['Wearing'])
        # IF no overlap THEN not wearing
        # Will need rule for no overlap, and rule for overlap and medium, far, very far
        self.__not_wearing_rule1 = ctrl.Rule(self.__overlap['No Overlap'], self.__worn_interaction['Not Wearing'])
        self.__not_wearing_rule2 = ctrl.Rule(self.__overlap['Overlap'] &
                                             (self.__proximity['Medium'] | self.__proximity['Far'] |
                                              self.__proximity['Very Far']), self.__worn_interaction['Not Wearing'])
        self.__wearing_ctrl = ctrl.ControlSystem([self.__wearing_rule, self.__not_wearing_rule1,
                                                  self.__not_wearing_rule2])
        self.__wearing_sim = ctrl.ControlSystemSimulation(self.__wearing_ctrl, flush_after_run=100)

        # clothing items. Go back through and check again after running these rules. Ties and umbrellas for example
        self.__carrying_rule = ctrl.Rule(self.__overlap['Overlap'] &
                                         (self.__proximity['Close'] | self.__proximity['Very Close'] |
                                          self.__proximity['Medium']), self.__carried_interaction['Carrying'])
        self.__not_carrying_rule1 = ctrl.Rule(self.__overlap['No Overlap'],
                                              self.__carried_interaction['Not Carrying'])
        self.__not_carrying_rule2 = ctrl.Rule(self.__overlap['Overlap'] &
                                              (self.__proximity['Very Far'] |
                                               self.__proximity['Far']), self.__carried_interaction['Not Carrying'])
        self.__carrying_ctrl = ctrl.ControlSystem([self.__carrying_rule, self.__not_carrying_rule1,
                                                   self.__not_carrying_rule2])
        self.__carrying_sim = ctrl.ControlSystemSimulation(self.__carrying_ctrl, flush_after_run=100)

    def __create_carried_clothing_rules(self):
        # clothing items. Go back through and check again after running these rules. Ties and umbrellas for example
        self.__carrying_rule = ctrl.Rule(self.__overlap['Overlap'] &
                                         (self.__proximity['Close'] | self.__proximity['Very Close'] |
                                          self.__proximity['Medium']), self.__carried_interaction['Carrying'])
        self.__not_carrying_rule1 = ctrl.Rule(self.__overlap['No Overlap'],
                                              self.__carried_interaction['Not Carrying'])
        self.__not_carrying_rule2 = ctrl.Rule(self.__overlap['Overlap'] &
                                              (self.__proximity['Very Far'] |
                                               self.__proximity['Far']), self.__carried_interaction['Not Carrying'])
        self.__carrying_ctrl = ctrl.ControlSystem([self.__carrying_rule, self.__not_carrying_rule1,
                                                   self.__not_carrying_rule2])
        self.__carrying_sim = ctrl.ControlSystemSimulation(self.__carrying_ctrl, flush_after_run=100)

    def compute_worn_interaction(self, giou, iou, sr_angle):
        self.__wearing_sim.input['overlap'] = iou
        self.__wearing_sim.input['proximity'] = giou
        self.__wearing_sim.compute()
        wearing_result = self.__wearing_sim.output['worn_interaction']
        if self.__show_sim_result:
            self.__worn_interaction.view(sim=self.__wearing_sim)
        wearing = fuzz.interp_membership(self.__worn_interaction.universe, self.__worn_interaction['Wearing'].mf,
                                         wearing_result)
        not_wearing = fuzz.interp_membership(self.__worn_interaction.universe,
                                             self.__worn_interaction['Not Wearing'].mf, wearing_result)
        membership = {'Wearing': wearing, 'Not Wearing': not_wearing}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Wearing':
            return None
        else:
            return ret_label

    def compute_carried_interaction(self, giou, iou, sr_angle):
        self.__carrying_sim.input['overlap'] = iou
        self.__carrying_sim.input['proximity'] = giou
        self.__carrying_sim.compute()
        carrying_result = self.__carrying_sim.output['carried_interaction']
        if self.__show_sim_result:
            self.__carried_interaction.view(sim=self.__carrying_sim)
        carrying = fuzz.interp_membership(self.__carried_interaction.universe,
                                          self.__carried_interaction['Carrying'].mf, carrying_result)
        not_carrying = fuzz.interp_membership(self.__carried_interaction.universe,
                                              self.__carried_interaction['Not Carrying'].mf, carrying_result)
        membership = {'Carrying': carrying, 'Not Carrying': not_carrying}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Carrying':
            return None
        else:
            return ret_label

    def compute_interaction(self, label, dom_cat, sub_cat, giou, iou, sr_angle):
        """Use the sub_cat to determine the rule to call"""
        if sub_cat == 'worn':
            res_label = self.compute_worn_interaction(giou, iou, sr_angle)
            return res_label
        elif sub_cat == 'carried':
            res_label = self.compute_carried_interaction(giou, iou, sr_angle)
            return res_label

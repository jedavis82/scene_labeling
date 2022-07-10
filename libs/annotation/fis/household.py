"""
FIS for the person-household interactions
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from libs.annotation.fuzzy_utils import create_universes_membership_functions


class HouseholdRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_household_rules()

    def __create_universes_of_discourse(self):
        self.__household_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                       label='household_interaction')

    def __create_membership_functions(self):
        self.__household_interaction['Interacting'] = fuzz.trimf(self.__household_interaction.universe,
                                                                 [0.4, 0.7, 1.0])
        self.__household_interaction['Not Interacting'] = fuzz.trimf(self.__household_interaction.universe,
                                                                     [0.0, 0.3, 0.6])

    def __create_household_rules(self):
        # IF overlap AND very close THEN interacting
        self.__interacting_rule1 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'],
                                             self.__household_interaction['Interacting'])
        # IF overlap AND close OR medium OR far OR very far THEN not interacting
        self.__not_interacting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                                 (self.__proximity['Close'] | self.__proximity['Medium'] |
                                                  self.__proximity['Far'] | self.__proximity['Very Far']),
                                                 self.__household_interaction['Not Interacting'])
        # IF no overlap THEN not interacting
        self.__not_interacting_rule2 = ctrl.Rule(self.__overlap['No Overlap'],
                                                 self.__household_interaction['Not Interacting'])
        self.__household_ctrl = ctrl.ControlSystem([self.__interacting_rule1, self.__not_interacting_rule1,
                                                    self.__not_interacting_rule2])
        self.__household_sim = ctrl.ControlSystemSimulation(self.__household_ctrl, flush_after_run=100)

    def compute_household_interaction(self, giou, iou, sr_angle):
        self.__household_sim.input['overlap'] = iou
        self.__household_sim.input['proximity'] = giou
        self.__household_sim.compute()
        if self.__show_sim_result:
            self.__household_interaction.view(sim=self.__household_sim)
        interacting_result = self.__household_sim.output['household_interaction']
        interacting = fuzz.interp_membership(self.__household_interaction.universe,
                                             self.__household_interaction['Interacting'].mf, interacting_result)
        not_interacting = fuzz.interp_membership(self.__household_interaction.universe,
                                                 self.__household_interaction['Not Interacting'].mf,
                                                 interacting_result)
        membership = {'Interacting': interacting, 'Not Interacting': not_interacting}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Interacting':
            return None
        else:
            return ret_label

    def compute_interaction(self, label, dom_cat, sub_cat, giou, iou, sr_angle):
        res_label = self.compute_household_interaction(giou, iou, sr_angle)
        if res_label is not None:
            if label == 'toothbrush':
                return 'Brushing Teeth'
            elif label == 'teddy_bear':
                return 'Holding'
            elif label == 'book':
                return 'Reading'
            else:
                return res_label
        else:
            return res_label

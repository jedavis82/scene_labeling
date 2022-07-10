"""
FIS for the person-appliance interactions
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from libs.annotation.fuzzy_utils import create_universes_membership_functions


class AppliancesRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_appliance_rules()

    def __create_universes_of_discourse(self):
        self.__appliance_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                       label='appliance_interaction')

    def __create_membership_functions(self):
        self.__appliance_interaction['Using'] = fuzz.trimf(self.__appliance_interaction.universe, [0.4, 0.7, 1.0])
        self.__appliance_interaction['Not Using'] = fuzz.trimf(self.__appliance_interaction.universe, [0.0, 0.3, 0.6])

    def __create_appliance_rules(self):
        # IF overlap AND very close OR close AND SR is any THEN using
        self.__using_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                       (self.__proximity['Very Close'] | self.__proximity['Close']),
                                       self.__appliance_interaction['Using'])
        # IF no overlap AND very close AND SR is any THEN using
        self.__using_rule2 = ctrl.Rule(self.__overlap['No Overlap'] & self.__proximity['Very Close'],
                                       self.__appliance_interaction['Using'])
        # IF overlap AND medium OR far OR very far AND SR is any THEN not using
        self.__not_using_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                           (self.__proximity['Medium'] | self.__proximity['Far'] |
                                            self.__proximity['Very Far']), self.__appliance_interaction['Not Using'])
        # IF no overlap AND close OR medium OR far OR very far AND SR is any THEN not using
        self.__not_using_rule2 = ctrl.Rule(self.__overlap['No Overlap'] &
                                           (self.__proximity['Close'] | self.__proximity['Medium'] |
                                            self.__proximity['Far'] | self.__proximity['Very Far']),
                                           self.__appliance_interaction['Not Using'])
        self.__appliance_ctrl = ctrl.ControlSystem([self.__using_rule1, self.__using_rule2, self.__not_using_rule1,
                                                    self.__not_using_rule2])
        self.__appliance_sim = ctrl.ControlSystemSimulation(self.__appliance_ctrl, flush_after_run=100)

    def compute_interaction(self, giou, iou, sr_angle):
        self.__appliance_sim.input['proximity'] = giou
        self.__appliance_sim.input['overlap'] = iou
        self.__appliance_sim.compute()
        app_result = self.__appliance_sim.output['appliance_interaction']
        if self.__show_sim_result:
            self.__appliance_interaction.view(sim=self.__appliance_sim)
        using = fuzz.interp_membership(self.__appliance_interaction.universe, self.__appliance_interaction['Using'].mf,
                                       app_result)
        not_using = fuzz.interp_membership(self.__appliance_interaction.universe,
                                           self.__appliance_interaction['Not Using'].mf, app_result)
        membership = {'Using': using, 'Not Using': not_using}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Using':
            return None
        else:
            return ret_label

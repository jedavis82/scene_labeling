"""
FIS for the person-electronic interactions
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from libs.annotation.fuzzy_utils import create_universes_membership_functions


class ElectronicsRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_tv_rules()
        self.__create_cell_phone_rules()
        self.__create_device_rules()

    def __create_universes_of_discourse(self):
        """
        Universe of discourse:
        TV: watching, not watching
        Cell Phone: talking on, not talking on
        Small Device: using, not using
        """
        self.__tv_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='tv_interaction')
        self.__cell_phone_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                        label='cell_phone_interaction')
        self.__device_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='device_interaction')

    def __create_membership_functions(self):
        self.__tv_interaction['Watching'] = fuzz.trimf(self.__tv_interaction.universe, [0.4, 0.7, 1.0])
        self.__tv_interaction['Not Watching'] = fuzz.trimf(self.__tv_interaction.universe, [0.0, 0.3, 0.6])
        self.__cell_phone_interaction['Talking On'] = fuzz.trimf(self.__cell_phone_interaction.universe,
                                                                 [0.4, 0.7, 1.0])
        self.__cell_phone_interaction['Not Talking On'] = fuzz.trimf(self.__cell_phone_interaction.universe,
                                                                     [0.0, 0.3, 0.6])
        self.__device_interaction['Using'] = fuzz.trimf(self.__device_interaction.universe, [0.4, 0.7, 1.0])
        self.__device_interaction['Not Using'] = fuzz.trimf(self.__device_interaction.universe, [0.0, 0.3, 0.6])

    def __create_tv_rules(self):
        # If overlap AND very close OR close OR medium THEN watching
        self.__watching_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                          (self.__proximity['Very Close'] | self.__proximity['Close'] |
                                           self.__proximity['Medium']), self.__tv_interaction['Watching'])
        # IF no overlap AND very close OR close THEN watching
        self.__watching_rule2 = ctrl.Rule(self.__overlap['No Overlap'] &
                                          (self.__proximity['Very Close'] | self.__proximity['Close']
                                           | self.__proximity['Medium']),
                                          self.__tv_interaction['Watching'])
        # IF overlap AND far OR very far THEN not watching
        self.__not_watching_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                              (self.__proximity['Far'] | self.__proximity['Very Far']),
                                              self.__tv_interaction['Not Watching'])
        # IF no overlap AND medium OR far OR very far THEN not watching
        self.__not_watching_rule2 = ctrl.Rule(self.__overlap['No Overlap'] &
                                              (self.__proximity['Far'] |
                                               self.__proximity['Very Far']), self.__tv_interaction['Not Watching'])
        self.__watching_ctrl = ctrl.ControlSystem([self.__watching_rule1, self.__watching_rule2,
                                                  self.__not_watching_rule1, self.__not_watching_rule2])
        self.__watching_sim = ctrl.ControlSystemSimulation(self.__watching_ctrl, flush_after_run=100)

    def __create_cell_phone_rules(self):
        # IF overlap AND very close OR close THEN talking
        self.__talking_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                         (self.__proximity['Very Close'] | self.__proximity['Close']),
                                         self.__cell_phone_interaction['Talking On'])

        # IF overlap AND medium OR far OR very far THEN not talking
        self.__not_talking_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                             (self.__proximity['Medium'] | self.__proximity['Far'] |
                                              self.__proximity['Very Far']),
                                             self.__cell_phone_interaction['Not Talking On'])

        # IF no overlap THEN not talking
        self.__not_talking_rule2 = ctrl.Rule(self.__overlap['No Overlap'],
                                             self.__cell_phone_interaction['Not Talking On'])
        self.__talking_ctrl = ctrl.ControlSystem([self.__talking_rule1, self.__not_talking_rule1,
                                                  self.__not_talking_rule2])
        self.__talking_sim = ctrl.ControlSystemSimulation(self.__talking_ctrl, flush_after_run=100)

    def __create_device_rules(self):
        # IF overlap OR no overlap AND very close OR close AND left OR above left OR above OR above right OR right
        # THEN using
        self.__using_rule1 = ctrl.Rule((self.__proximity['Very Close'] | self.__proximity['Close']) &
                                       (self.__spatial_relationships['Right1'] |
                                        self.__spatial_relationships['Right2'] |
                                        self.__spatial_relationships['Above Right'] |
                                        self.__spatial_relationships['Above'] |
                                        self.__spatial_relationships['Above Left'] |
                                        self.__spatial_relationships['Left']), self.__device_interaction['Using'])
        # IF overlap AND very close OR close THEN using
        self.__using_rule2 = ctrl.Rule(self.__overlap['Overlap'] &
                                       (self.__proximity['Very Close'] | self.__proximity['Close']),
                                       self.__device_interaction['Using'])
        # IF overlap OR no overlap AND medium OR far OR very far AND any sr THEN not using
        self.__not_using_rule1 = ctrl.Rule((self.__proximity['Medium'] | self.__proximity['Far'] |
                                            self.__proximity['Very Far']),
                                           self.__device_interaction['Not Using'])

        # IF very close OR close AND below left OR below OR below right THEN not using
        self.__not_using_rule2 = ctrl.Rule(self.__overlap['No Overlap'] &
                                           (self.__proximity['Very Close'] | self.__proximity['Close']) &
                                           (self.__spatial_relationships['Below Left'] |
                                            self.__spatial_relationships['Below'] |
                                            self.__spatial_relationships['Below Right']),
                                           self.__device_interaction['Not Using'])
        self.__using_ctrl = ctrl.ControlSystem([self.__using_rule1, self.__using_rule2,
                                                self.__not_using_rule1, self.__not_using_rule2])
        self.__using_sim = ctrl.ControlSystemSimulation(self.__using_ctrl, flush_after_run=100)

    def compute_tv_interaction(self, giou, iou, sr_angle):
        self.__watching_sim.input['proximity'] = giou
        self.__watching_sim.input['overlap'] = iou
        self.__watching_sim.compute()
        watching_result = self.__watching_sim.output['tv_interaction']
        if self.__show_sim_result:
            self.__tv_interaction.view(sim=self.__watching_sim)
        watching = fuzz.interp_membership(self.__tv_interaction.universe, self.__tv_interaction['Watching'].mf,
                                          watching_result)
        not_watching = fuzz.interp_membership(self.__tv_interaction.universe, self.__tv_interaction['Not Watching'].mf,
                                              watching_result)
        membership = {'Watching': watching, 'Not Watching': not_watching}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Watching':
            return None
        else:
            return ret_label

    def compute_cell_phone_interaction(self, giou, iou, sr_angle):
        self.__talking_sim.input['overlap'] = iou
        self.__talking_sim.input['proximity'] = giou
        self.__talking_sim.compute()
        talking_result = self.__talking_sim.output['cell_phone_interaction']
        if self.__show_sim_result:
            self.__cell_phone_interaction.view(sim=self.__talking_sim)
        talking = fuzz.interp_membership(self.__cell_phone_interaction.universe,
                                         self.__cell_phone_interaction['Talking On'].mf, talking_result)
        not_talking = fuzz.interp_membership(self.__cell_phone_interaction.universe,
                                             self.__cell_phone_interaction['Not Talking On'].mf, talking_result)
        membership = {'Talking On': talking, 'Not Talking On': not_talking}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Talking On':
            return None
        else:
            return ret_label

    def compute_device_interaction(self, giou, iou, sr_angle):
        self.__using_sim.input['proximity'] = giou
        self.__using_sim.input['overlap'] = iou
        self.__using_sim.input['spatial_relationships'] = sr_angle
        self.__using_sim.compute()
        using_result = self.__using_sim.output['device_interaction']
        if self.__show_sim_result:
            self.__device_interaction.view(sim=self.__using_sim)
        using = fuzz.interp_membership(self.__device_interaction.universe, self.__device_interaction['Using'].mf,
                                       using_result)
        not_using = fuzz.interp_membership(self.__device_interaction.universe,
                                           self.__device_interaction['Not Using'].mf, using_result)
        membership = {'Using': using, 'Not Using': not_using}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Using':
            return None
        else:
            return ret_label

    def compute_interaction(self, label, dom_cat, sub_cat, giou, iou, sr_angle):
        if label == 'tv' or label == 'tvmonitor':
            res_label = self.compute_tv_interaction(giou, iou, sr_angle)
            return res_label
        elif label == 'cell_phone':
            res_label = self.compute_cell_phone_interaction(giou, iou, sr_angle)
            return res_label
        else:
            res_label = self.compute_device_interaction(giou, iou, sr_angle)
            return res_label

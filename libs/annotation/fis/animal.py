"""
FIS for the person-animal interactions
"""
from fuzzy_utils import create_universes_membership_functions
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np


class AnimalRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_pet_rules()
        self.__create_large_animal_rules()
        self.__create_ridden_animal_rules()

    def __create_universes_of_discourse(self):
        self.__pet_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='pet_interaction')
        self.__ridden_animal_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                           label='ridden_animal_interaction')
        self.__large_animal_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                          label='large_animal_interaction')

    def __create_membership_functions(self):
        self.__pet_interaction['Petting'] = fuzz.trimf(self.__pet_interaction.universe, [0.4, 0.7, 1.0])
        self.__pet_interaction['Not Petting'] = fuzz.trimf(self.__pet_interaction.universe, [0.0, 0.3, 0.6])

        self.__ridden_animal_interaction['Riding'] = fuzz.trimf(self.__ridden_animal_interaction.universe,
                                                                [0.4, 0.7, 1.0])
        self.__ridden_animal_interaction['Not Riding'] = fuzz.trimf(self.__ridden_animal_interaction.universe,
                                                                    [0.0, 0.3, 0.6])

        self.__large_animal_interaction['Interacting'] = fuzz.trimf(self.__large_animal_interaction.universe,
                                                                    [0.4, 0.7, 1.0])
        self.__large_animal_interaction['Not Interacting'] = fuzz.trimf(self.__large_animal_interaction.universe,
                                                                        [0.0, 0.3, 0.6])

    def __create_pet_rules(self):
        # IF overlap OR no overlap AND very close or close AND above OR above left OR above right OR left OR right
        # THEN petting
        self.__petting_rule = ctrl.Rule((self.__overlap['Overlap'] | self.__overlap['No Overlap']) &
                                        (self.__proximity['Very Close'] | self.__proximity['Close']) &
                                        (self.__spatial_relationships['Above Left'] |
                                         self.__spatial_relationships['Above'] |
                                         self.__spatial_relationships['Above Right'] |
                                         self.__spatial_relationships['Left'] |
                                         self.__spatial_relationships['Right1'] |
                                         self.__spatial_relationships['Right2']),
                                        self.__pet_interaction['Petting'])

        # IF overlap OR no overlap AND very close OR close AND below right OR below or below left
        self.__not_petting_rule_1 = ctrl.Rule((self.__overlap['Overlap'] | self.__overlap['No Overlap']) &
                                              (self.__proximity['Very Close'] | self.__proximity['Close']) &
                                              (self.__spatial_relationships['Below Right'] |
                                               self.__spatial_relationships['Below'] |
                                               self.__spatial_relationships['Below Left']),
                                              self.__pet_interaction['Not Petting'])
        # IF overlap OR no overlap AND medium OR far OR very far AND any SR THEN not petting
        self.__not_petting_rule_2 = ctrl.Rule((self.__overlap['Overlap'] | self.__overlap['No Overlap']) &
                                              (self.__proximity['Medium'] | self.__proximity['Far'] |
                                               self.__proximity['Very Far']) &
                                              (self.__spatial_relationships['Right1'] |
                                               self.__spatial_relationships['Right2'] |
                                               self.__spatial_relationships['Below Right'] |
                                               self.__spatial_relationships['Below'] |
                                               self.__spatial_relationships['Below Left'] |
                                               self.__spatial_relationships['Above Left'] |
                                               self.__spatial_relationships['Above'] |
                                               self.__spatial_relationships['Above Right'] |
                                               self.__spatial_relationships['Left']),
                                              self.__pet_interaction['Not Petting'])
        self.__petting_ctrl = ctrl.ControlSystem([self.__petting_rule, self.__not_petting_rule_1,
                                                  self.__not_petting_rule_2])
        self.__petting_sim = ctrl.ControlSystemSimulation(self.__petting_ctrl, flush_after_run=100)

    def __create_ridden_animal_rules(self):
        # IF very close OR close AND above left OR above OR above right THEN riding
        self.__riding_rule1 = ctrl.Rule((self.__proximity['Very Close'] | self.__proximity['Close']) &
                                        (self.__spatial_relationships['Above Left'] |
                                        self.__spatial_relationships['Above'] |
                                        self.__spatial_relationships['Above Right']),
                                        self.__ridden_animal_interaction['Riding'])
        # IF very close OR close AND left OR below left OR below OR below right OR right THEN not riding
        self.__not_riding_rule1 = ctrl.Rule((self.__proximity['Very Close'] | self.__proximity['Close']) &
                                            (self.__spatial_relationships['Right1'] |
                                             self.__spatial_relationships['Right2'] |
                                             self.__spatial_relationships['Below Right'] |
                                             self.__spatial_relationships['Below'] |
                                             self.__spatial_relationships['Below Left'] |
                                             self.__spatial_relationships['Left']),
                                            self.__ridden_animal_interaction['Not Riding'])
        # IF medium OR far OR very far THEN not riding
        self.__not_riding_rule2 = ctrl.Rule((self.__proximity['Medium'] | self.__proximity['Far'] |
                                             self.__proximity['Very Far']),
                                            self.__ridden_animal_interaction['Not Riding'])
        self.__ridden_animal_ctrl = ctrl.ControlSystem([self.__riding_rule1, self.__not_riding_rule1,
                                                        self.__not_riding_rule2])
        self.__ridden_animal_sim = ctrl.ControlSystemSimulation(self.__ridden_animal_ctrl, flush_after_run=100)

    def __create_large_animal_rules(self):
        # IF overlap AND very close OR close AND SR is any THEN interacting
        self.__large_animal_interacting_rule = ctrl.Rule((self.__proximity['Very Close'] | self.__proximity['Close']),
                                                         self.__large_animal_interaction['Interacting'])

        # IF overlap OR no overlap AND medium OR far OR very far and SR is any THEN not interacting
        self.__large_animal_not_interacting_rule = ctrl.Rule((self.__proximity['Medium'] |
                                                              self.__proximity['Far'] |
                                                              self.__proximity['Very Far']),
                                                             self.__large_animal_interaction['Not Interacting'])

        self.__large_animal_ctrl = ctrl.ControlSystem([self.__large_animal_interacting_rule,
                                                       self.__large_animal_not_interacting_rule])
        self.__large_animal_sim = ctrl.ControlSystemSimulation(self.__large_animal_ctrl, flush_after_run=100)

    def compute_pet_interaction(self, giou, iou, sr_angle):
        self.__petting_sim.input['proximity'] = giou
        self.__petting_sim.input['overlap'] = iou
        self.__petting_sim.input['spatial_relationships'] = sr_angle
        self.__petting_sim.compute()
        petting_result = self.__petting_sim.output['pet_interaction']
        if self.__show_sim_result:
            self.__pet_interaction.view(sim=self.__petting_sim)
        petting = fuzz.interp_membership(self.__pet_interaction.universe, self.__pet_interaction['Petting'].mf,
                                         petting_result)
        not_petting = fuzz.interp_membership(self.__pet_interaction.universe, self.__pet_interaction['Not Petting'].mf,
                                             petting_result)
        membership = {'Petting': petting, 'Not Petting': not_petting}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Petting':
            return None
        else:
            return ret_label

    def compute_ridden_animal_interaction(self, giou, iou, sr_angle):
        self.__ridden_animal_sim.input['proximity'] = giou
        # self.__ridden_animal_sim.input['overlap'] = iou
        self.__ridden_animal_sim.input['spatial_relationships'] = sr_angle
        self.__ridden_animal_sim.compute()
        ridden_result = self.__ridden_animal_sim.output['ridden_animal_interaction']
        if self.__show_sim_result:
            self.__ridden_animal_interaction.view(sim=self.__ridden_animal_sim)
        riding = fuzz.interp_membership(self.__ridden_animal_interaction.universe,
                                        self.__ridden_animal_interaction['Riding'].mf, ridden_result)
        not_riding = fuzz.interp_membership(self.__ridden_animal_interaction.universe,
                                            self.__ridden_animal_interaction['Not Riding'].mf,
                                            ridden_result)
        membership = {'Riding': riding, 'Not Riding': not_riding}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Riding':
            return None
        else:
            return ret_label

    def compute_large_animal_interaction(self, giou, iou, sr_angle):
        self.__large_animal_sim.input['proximity'] = giou
        # self.__large_animal_sim.input['overlap'] = iou
        # self.__large_animal_sim.input['spatial_relationships'] = sr_angle
        self.__large_animal_sim.compute()
        interacting_result = self.__large_animal_sim.output['large_animal_interaction']
        if self.__show_sim_result:
            self.__large_animal_interaction.view(sim=self.__large_animal_sim)
        interacting = fuzz.interp_membership(self.__large_animal_interaction.universe,
                                             self.__large_animal_interaction['Interacting'].mf, interacting_result)
        not_interacting = fuzz.interp_membership(self.__large_animal_interaction.universe,
                                                 self.__large_animal_interaction['Not Interacting'].mf,
                                                 interacting_result)
        membership = {'Interacting': interacting, 'Not Interacting': not_interacting}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Interacting':
            return None
        else:
            return ret_label

    def compute_interaction(self, label, dom_cat, sub_cat, giou, iou, sr_angle):
        """
        Use the label to determine the appropriate rule to call
        """
        if label == 'horse' or label == 'elephant':
            res_label = self.compute_ridden_animal_interaction(giou, iou, sr_angle)
            return res_label
        if sub_cat is not None and sub_cat == 'large' or sub_cat == 'farm':
            res_label = self.compute_large_animal_interaction(giou, iou, sr_angle)
            return res_label
        if sub_cat is not None and sub_cat == 'pet':
            res_label = self.compute_pet_interaction(giou, iou, sr_angle)
            return res_label



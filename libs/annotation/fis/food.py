"""
FIS for the person-food interactions
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from libs.annotation.fuzzy_utils import create_universes_membership_functions


class FoodRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_using_rules()
        self.__create_drinking_rules()
        self.__create_eating_rules()

    def __create_universes_of_discourse(self):
        """
        Food categories break down into:
        Used: utensils->plate, fork, knife, spoon, bowl
        Drink: bottle, wine glass, cup
        Eaten: banana, apple, sandwich, orange, broccoli, carrot, hot dog, pizza, donut, cake
        """
        self.__using_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='using_interaction')
        self.__drinking_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='drinking_interaction')
        self.__eating_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1), label='eating_interaction')

    def __create_membership_functions(self):
        self.__using_interaction['Using'] = fuzz.trimf(self.__using_interaction.universe, [0.4, 0.7, 1.0])
        self.__using_interaction['Not Using'] = fuzz.trimf(self.__using_interaction.universe, [0.0, 0.3, 0.6])
        self.__drinking_interaction['Drinking'] = fuzz.trimf(self.__drinking_interaction.universe, [0.4, 0.7, 1.0])
        self.__drinking_interaction['Not Drinking'] = fuzz.trimf(self.__drinking_interaction.universe, [0.0, 0.3, 0.6])
        self.__eating_interaction['Eating'] = fuzz.trimf(self.__eating_interaction.universe, [0.4, 0.7, 1.0])
        self.__eating_interaction['Not Eating'] = fuzz.trimf(self.__eating_interaction.universe, [0.0, 0.3, 0.6])

    def __create_using_rules(self):
        """
        These rules are for utensils, plates, bowls.
        A person is only using a utensil if they overlap and are in very close proximity
        """
        # IF overlap AND very close OR close THEN using
        self.__using_rule = ctrl.Rule(self.__overlap['Overlap'] &
                                      (self.__proximity['Very Close'] | self.__proximity['Close']),
                                      self.__using_interaction['Using'])
        # IF overlap AND medium OR far OR very far THEN not using
        self.__not_using_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                           (self.__proximity['Medium'] | self.__proximity['Far'] |
                                            self.__proximity['Very Far']), self.__using_interaction['Not Using'])
        # IF no overlap THEN not using
        self.__not_using_rule2 = ctrl.Rule(self.__overlap['No Overlap'], self.__using_interaction['Not Using'])
        self.__using_ctrl = ctrl.ControlSystem([self.__using_rule, self.__not_using_rule1, self.__not_using_rule2])
        self.__using_sim = ctrl.ControlSystemSimulation(self.__using_ctrl, flush_after_run=100)

    def __create_drinking_rules(self):
        """
        These rules are for person drinking from object.
        A person is only drinking if they overlap the object and are  in very close proximity.
        Very strict rules, but avoids erroneous labels
        """
        self.__drinking_rule = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'],
                                         self.__drinking_interaction['Drinking'])
        self.__not_drinking_rule1 = ctrl.Rule(self.__overlap['No Overlap'], self.__drinking_interaction['Not Drinking'])
        self.__not_drinking_rule2 = ctrl.Rule(self.__overlap['Overlap'] &
                                              (self.__proximity['Close'] | self.__proximity['Medium'] |
                                               self.__proximity['Far'] | self.__proximity['Very Far']),
                                              self.__drinking_interaction['Not Drinking'])
        self.__drinking_ctrl = ctrl.ControlSystem([self.__drinking_rule, self.__not_drinking_rule1,
                                                   self.__not_drinking_rule2])
        self.__drinking_sim = ctrl.ControlSystemSimulation(self.__drinking_ctrl, flush_after_run=100)

    def __create_eating_rules(self):
        """
        These rules are for person eating food.
        A person is only eating food if they overlap the food and are not below it

        Starting with very strict rules. Overlap and very close entails eating. Everything else does not.
        """
        # IF overlap AND very close THEN eating
        self.__eating_rule = ctrl.Rule(self.__overlap['Overlap'] &
                                       (self.__proximity['Very Close'] | self.__proximity['Close']),
                                       self.__eating_interaction['Eating'])
        # IF overlap AND close OR medium OR far OR very far THEN not eating
        self.__not_eating_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                            (self.__proximity['Medium'] | self.__proximity['Far'] |
                                             self.__proximity['Very Far']), self.__eating_interaction['Not Eating'])
        # IF no overlap THEN not eating
        self.__not_eating_rule2 = ctrl.Rule(self.__overlap['No Overlap'], self.__eating_interaction['Not Eating'])
        self.__eating_ctrl = ctrl.ControlSystem([self.__eating_rule, self.__not_eating_rule1, self.__not_eating_rule2])
        self.__eating_sim = ctrl.ControlSystemSimulation(self.__eating_ctrl, flush_after_run=100)

    def compute_using_interaction(self, giou, iou, sr_angle):
        self.__using_sim.input['proximity'] = giou
        self.__using_sim.input['overlap'] = iou
        self.__using_sim.compute()
        using_result = self.__using_sim.output['using_interaction']
        if self.__show_sim_result:
            self.__using_interaction.view(sim=self.__using_sim)
        using = fuzz.interp_membership(self.__using_interaction.universe, self.__using_interaction['Using'].mf,
                                       using_result)
        not_using = fuzz.interp_membership(self.__using_interaction.universe, self.__using_interaction['Not Using'].mf,
                                           using_result)
        membership = {'Using': using, 'Not Using': not_using}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Using':
            return None
        else:
            return ret_label

    def compute_drinking_interaction(self, giou, iou, sr_angle):
        self.__drinking_sim.input['overlap'] = iou
        self.__drinking_sim.input['proximity'] = giou
        self.__drinking_sim.compute()
        drinking_result = self.__drinking_sim.output['drinking_interaction']
        if self.__show_sim_result:
            self.__drinking_interaction.view(sim=self.__drinking_sim)
        drinking = fuzz.interp_membership(self.__drinking_interaction.universe,
                                          self.__drinking_interaction['Drinking'].mf, drinking_result)
        not_drinking = fuzz.interp_membership(self.__drinking_interaction.universe,
                                              self.__drinking_interaction['Not Drinking'].mf, drinking_result)
        membership = {'Drinking': drinking, 'Not Drinking': not_drinking}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Drinking':
            return None
        else:
            return ret_label

    def compute_eating_interaction(self, giou, iou, sr_angle):
        self.__eating_sim.input['proximity'] = giou
        self.__eating_sim.input['overlap'] = iou
        self.__eating_sim.compute()
        eating_result = self.__eating_sim.output['eating_interaction']
        if self.__show_sim_result:
            self.__eating_interaction.view(sim=self.__eating_sim)
        eating = fuzz.interp_membership(self.__eating_interaction.universe, self.__eating_interaction['Eating'].mf,
                                        eating_result)
        not_eating = fuzz.interp_membership(self.__eating_interaction.universe,
                                            self.__eating_interaction['Not Eating'].mf, eating_result)
        membership = {'Eating': eating, 'Not Eating': not_eating}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Eating':
            return None
        else:
            return ret_label

    def compute_interaction(self, label, dom_cat, sub_cat, giou, iou, sr_angle):
        """
        Use the sub_cat to determine the appropriate simulation to call
        """
        if sub_cat is not None and sub_cat == 'drink':
            res_label = self.compute_drinking_interaction(giou, iou, sr_angle)
            return res_label
        if sub_cat is not None and sub_cat == 'eaten':
            res_label = self.compute_eating_interaction(giou, iou, sr_angle)
            return res_label
        if sub_cat is not None and sub_cat == 'used':
            res_label = self.compute_using_interaction(giou, iou, sr_angle)
            return res_label

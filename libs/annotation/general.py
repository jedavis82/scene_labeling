"""
Implement the general interaction rule base for the scene annotation system
"""
from collections import defaultdict
from fuzzy_utils import create_universes_membership_functions
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl


class GeneralRules:
    def __init__(self):
        self.__general_categories_lookup = defaultdict(list)
        prox, over, spat = create_universes_membership_functions()
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_membership_functions()
        self.__create_rules()

    def __create_membership_functions(self):
        """
        Construct the consequent membership function for the interaction fuzzy variable
        :return:
        """
        self.__interaction = ctrl.Consequent(universe=np.arange(-1.1, 1.1, 0.1), label='interaction')
        self.__interaction['Interacting'] = fuzz.trimf(self.__interaction.universe, [0.0, 0.5, 1.0])
        self.__interaction['Not Interacting'] = fuzz.trimf(self.__interaction.universe, [-1.0, -0.5, 0.0])

    def __create_rules(self):
        """
        Construct the rule base for the general categories
        These rules simply indicate whether or not objects are interacting
        :return:
        """
        self.__interacting_rule_1 = ctrl.Rule(self.__overlap['Overlap'] &
                                              (self.__proximity['Very Close'] | self.__proximity['Close']),
                                              self.__interaction['Interacting'])
        self.__interacting_rule_2 = ctrl.Rule(self.__overlap['No Overlap'] & self.__proximity['Very Close'],
                                              self.__interaction['Not Interacting'])
        self.__not_interacting_rule1 = ctrl.Rule(self.__overlap['No Overlap'] &
                                                 (self.__proximity['Close'] | self.__proximity['Medium'] |
                                                  self.__proximity['Far'] | self.__proximity['Very Far']),
                                                 self.__interaction['Not Interacting'])
        self.__not_interacting_rule2 = ctrl.Rule(self.__overlap['Overlap'] &
                                                 (self.__proximity['Medium'] | self.__proximity['Far'] |
                                                  self.__proximity['Very Far']), self.__interaction['Not Interacting'])

        self.__interaction_ctrl = ctrl.ControlSystem([self.__interacting_rule_1, self.__interacting_rule_2,
                                                      self.__not_interacting_rule1, self.__not_interacting_rule2])
        self.__interaction_sim = ctrl.ControlSystemSimulation(self.__interaction_ctrl, flush_after_run=100)

    def compute_interactions(self, sr_result=None):
        """
        Compute the general interaction annotations for an input image
        :param sr_result: GIOU and IOU scores for each tuple in the image
        :return: General interaction annotations for an image
        """
        assert sr_result is not None, "Must supply image spatial relationships"

        # Return a list of dictionaries as the result for the image
        general_annotations = list(dict())
        # All results will have the same relative path. This will be returned as a key
        rel_path = sr_result[0]['relative_path']
        for r in sr_result:
            proximity = r['proximity']
            overlap = r['overlap']
            self.__interaction_sim.input['proximity'] = proximity
            self.__interaction_sim.input['overlap'] = overlap
            self.__interaction_sim.compute()
            interaction = self.__interaction_sim.output['interaction']
            interacting = fuzz.interp_membership(self.__interaction.universe, self.__interaction['Interacting'].mf,
                                                 interaction)
            not_interacting = fuzz.interp_membership(self.__interaction.universe,
                                                     self.__interaction['Not Interacting'].mf,
                                                     interaction)
            membership = {'Interacting': interacting, 'Not Interacting': not_interacting}
            interacting_label = max(membership, key=membership.get)
            r['general_interaction'] = interacting_label
            general_annotations.append(r)
        return rel_path, general_annotations

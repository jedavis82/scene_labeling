"""
FIS for the person-furniture interactions
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from fuzzy_utils import create_universes_membership_functions


class FurnitureRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_furniture_rules()
        self.__create_decoration_rules()
        self.__create_couch_bed_rules()
        self.__create_chair_rules()

    def __create_universes_of_discourse(self):
        """
        There are two types of objects: furniture and decoration.
        Furniture will be sat on. Decorations will be 'interacted with'.
        """
        self.__furniture_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                       label='furniture_interaction')
        self.__couch_bed_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                       label='couch_bed_interaction')
        self.__chair_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                   label='chair_interaction')
        self.__decoration_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                        label='decoration_interaction')

    def __create_membership_functions(self):
        self.__furniture_interaction['Sitting'] = fuzz.trimf(self.__furniture_interaction.universe,
                                                             [0.4, 0.7, 1.0])
        self.__furniture_interaction['Not Sitting'] = fuzz.trimf(self.__furniture_interaction.universe,
                                                                 [0.0, 0.3, 0.6])
        self.__couch_bed_interaction['Interacting'] = fuzz.trimf(self.__couch_bed_interaction.universe,
                                                                 [0.4, 0.7, 1.0])
        self.__couch_bed_interaction['Not Interacting'] = fuzz.trimf(self.__couch_bed_interaction.universe,
                                                                     [0.0, 0.3, 0.6])
        self.__chair_interaction['Sitting'] = fuzz.trimf(self.__chair_interaction.universe,
                                                         [0.4, 0.7, 1.0])
        self.__chair_interaction['Not Sitting'] = fuzz.trimf(self.__chair_interaction.universe,
                                                             [0.0, 0.3, 0.6])
        self.__decoration_interaction['Interacting'] = fuzz.trimf(self.__decoration_interaction.universe,
                                                                  [0.4, 0.7, 1.0])
        self.__decoration_interaction['Not Interacting'] = fuzz.trimf(self.__decoration_interaction.universe,
                                                                      [0.0, 0.3, 0.6])

    def __create_couch_bed_rules(self):
        # IF overlap AND very close THEN sitting
        self.__couch_bed_interacting_rule1 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'],
                                                       self.__couch_bed_interaction['Interacting'])
        # IF overlap AND close or medium or far or very far THEN not sitting
        self.__couch_bed_not_interacting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                                           (self.__proximity['Close'] | self.__proximity['Medium'] |
                                                            self.__proximity['Far'] | self.__proximity['Very Far']),
                                                           self.__couch_bed_interaction['Not Interacting'])
        # IF no overlap THEN not sitting
        self.__couch_bed_not_interacting_rule2 = ctrl.Rule(self.__overlap['No Overlap'],
                                                           self.__couch_bed_interaction['Not Interacting'])
        self.__couch_bed_ctrl = ctrl.ControlSystem([self.__couch_bed_interacting_rule1,
                                                    self.__couch_bed_not_interacting_rule1,
                                                    self.__couch_bed_not_interacting_rule2])
        self.__couch_bed_sim = ctrl.ControlSystemSimulation(self.__couch_bed_ctrl, flush_after_run=100)

    def __create_chair_rules(self):
        """
        A person is only sitting in a chair if they overlap and are above the chair
        """
        # IF overlap AND very close AND above(s) THEN sitting
        self.__chair_sitting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                               self.__proximity['Very Close'] &
                                               (self.__spatial_relationships['Above Left'] |
                                                self.__spatial_relationships['Above'] |
                                                self.__spatial_relationships['Above Right']),
                                               self.__chair_interaction['Sitting'])
        # IF overlap AND very close AND left OR right OR below(s) THEN not sitting
        self.__chair_not_sitting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                                   self.__proximity['Very Close'] &
                                                   (self.__spatial_relationships['Right1'] |
                                                    self.__spatial_relationships['Right2'] |
                                                    self.__spatial_relationships['Below Right'] |
                                                    self.__spatial_relationships['Below'] |
                                                    self.__spatial_relationships['Below Left'] |
                                                    self.__spatial_relationships['Left']),
                                                   self.__chair_interaction['Not Sitting'])
        # IF overlap AND close OR medium OR far OR very far THEN not sitting
        self.__chair_not_sitting_rule2 = ctrl.Rule(self.__overlap['Overlap'] &
                                                   (self.__proximity['Close'] | self.__proximity['Medium'] |
                                                    self.__proximity['Far'] | self.__proximity['Very Far']),
                                                   self.__chair_interaction['Not Sitting'])
        # IF no overlap THEN not sitting
        self.__chair_not_sitting_rule3 = ctrl.Rule(self.__overlap['No Overlap'],
                                                   self.__chair_interaction['Not Sitting'])

        self.__chair_ctrl = ctrl.ControlSystem([self.__chair_sitting_rule1, self.__chair_not_sitting_rule1,
                                                self.__chair_not_sitting_rule2, self.__chair_not_sitting_rule3])
        self.__chair_sim = ctrl.ControlSystemSimulation(self.__chair_ctrl, flush_after_run=100)

    def __create_furniture_rules(self):
        """
        The only way a person can be sitting on furniture is if they overlap, very close/close proximity and are
        above the furniture
        """
        # IF overlap AND very close THEN sitting
        self.__furniture_sitting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                                   (self.__proximity['Very Close'] | self.__proximity['Close']),
                                                   self.__furniture_interaction['Sitting'])
        # IF overlap AND close OR medium OR far OR very far THEN not sitting
        self.__furniture_not_sitting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                                       (self.__proximity['Medium'] |
                                                        self.__proximity['Far'] | self.__proximity['Very Far']),
                                                       self.__furniture_interaction['Not Sitting'])
        # IF no overlap THEN not sitting
        self.__furniture_not_sitting_rule2 = ctrl.Rule(self.__overlap['No Overlap'],
                                                       self.__furniture_interaction['Not Sitting'])

        self.__furniture_ctrl = ctrl.ControlSystem([self.__furniture_sitting_rule1,
                                                    self.__furniture_not_sitting_rule1,
                                                    self.__furniture_not_sitting_rule2])
        self.__furniture_sim = ctrl.ControlSystemSimulation(self.__furniture_ctrl, flush_after_run=100)

    def __create_decoration_rules(self):
        """
        If a person is overlapping and very close/close to a decoration, they are interacting with it
        """
        # IF overlap AND very close OR close THEN interacting
        self.__interacting_rule1 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'],
                                             self.__decoration_interaction['Interacting'])
        # IF overlap AND medium OR far OR very far THEN not interacting
        self.__not_interacting_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                                 (self.__proximity['Close'] | self.__proximity['Medium'] |
                                                  self.__proximity['Far'] | self.__proximity['Very Far']),
                                                 self.__decoration_interaction['Not Interacting'])
        # IF no overlap THEN not interacting
        self.__not_interacting_rule2 = ctrl.Rule(self.__overlap['No Overlap'],
                                                 self.__decoration_interaction['Not Interacting'])
        self.__decoration_ctrl = ctrl.ControlSystem([self.__interacting_rule1, self.__not_interacting_rule1,
                                                     self.__not_interacting_rule2])
        self.__decoration_sim = ctrl.ControlSystemSimulation(self.__decoration_ctrl, flush_after_run=100)

    def compute_furniture_interaction(self, giou, iou, sr_angle):
        self.__furniture_sim.input['overlap'] = iou
        self.__furniture_sim.input['proximity'] = giou
        self.__furniture_sim.compute()
        sitting_result = self.__furniture_sim.output['furniture_interaction']
        if self.__show_sim_result:
            self.__furniture_interaction.view(sim=self.__furniture_sim)
        sitting = fuzz.interp_membership(self.__furniture_interaction.universe,
                                         self.__furniture_interaction['Sitting'].mf, sitting_result)
        not_sitting = fuzz.interp_membership(self.__furniture_interaction.universe,
                                             self.__furniture_interaction['Not Sitting'].mf, sitting_result)
        membership = {'Sitting': sitting, 'Not Sitting': not_sitting}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Sitting':
            return None
        else:
            return ret_label

    def compute_couch_bed_interaction(self, giou, iou, sr_angle):
        self.__couch_bed_sim.input['proximity'] = giou
        self.__couch_bed_sim.input['overlap'] = iou
        self.__couch_bed_sim.compute()
        if self.__show_sim_result:
            self.__couch_bed_interaction.view(sim=self.__couch_bed_sim)
        interacting_result = self.__couch_bed_sim.output['couch_bed_interaction']
        interacting = fuzz.interp_membership(self.__couch_bed_interaction.universe,
                                             self.__couch_bed_interaction['Interacting'].mf,
                                             interacting_result)
        not_interacting = fuzz.interp_membership(self.__couch_bed_interaction.universe,
                                                 self.__couch_bed_interaction['Not Interacting'].mf,
                                                 interacting_result)
        membership = {'Interacting': interacting, 'Not Interacting': not_interacting}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Interacting':
            return None
        else:
            return ret_label

    def compute_chair_interaction(self, giou, iou, sr_angle):
        self.__chair_sim.input['proximity'] = giou
        self.__chair_sim.input['overlap'] = iou
        self.__chair_sim.input['spatial_relationships'] = sr_angle
        self.__chair_sim.compute()
        if self.__show_sim_result:
            self.__chair_interaction.view(sim=self.__chair_sim)
        sitting_result = self.__chair_sim.output['chair_interaction']
        sitting = fuzz.interp_membership(self.__chair_interaction.universe, self.__chair_interaction['Sitting'].mf,
                                         sitting_result)
        not_sitting = fuzz.interp_membership(self.__chair_interaction.universe,
                                             self.__chair_interaction['Not Sitting'].mf, sitting_result)
        membership = {'Sitting': sitting, 'Not Sitting': not_sitting}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Sitting':
            return None
        else:
            return ret_label

    def compute_decoration_interaction(self, giou, iou, sr_angle):
        self.__decoration_sim.input['overlap'] = iou
        self.__decoration_sim.input['proximity'] = giou
        self.__decoration_sim.compute()
        if self.__show_sim_result:
            self.__decoration_interaction.view(sim=self.__decoration_sim)
        interacting_result = self.__decoration_sim.output['decoration_interaction']
        interacting = fuzz.interp_membership(self.__decoration_interaction.universe,
                                             self.__decoration_interaction['Interacting'].mf, interacting_result)
        not_interacting = fuzz.interp_membership(self.__decoration_interaction.universe,
                                                 self.__decoration_interaction['Not Interacting'].mf,
                                                 interacting_result)
        membership = {'Interacting': interacting, 'Not Interacting': not_interacting}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Interacting':
            return None
        else:
            return ret_label

    def compute_interaction(self, label, dom_cat, sub_cat, giou, iou, sr_angle):
        if dom_cat == 'decoration':
            res_label = self.compute_decoration_interaction(giou, iou, sr_angle)
            return res_label
        if label == 'couch' or label == 'bed':
            res_label = self.compute_couch_bed_interaction(giou, iou, sr_angle)
            if res_label is not None:
                if label == 'couch':
                    return 'Sitting'
                else:
                    return 'Laying'
            else:
                return res_label
        if label == 'chair':
            res_label = self.compute_chair_interaction(giou, iou, sr_angle)
            return res_label
        if dom_cat == 'furniture':
            res_label = self.compute_furniture_interaction(giou, iou, sr_angle)
            return res_label

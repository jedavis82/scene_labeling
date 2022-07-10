"""
FIS for the person-sports interactions
"""
from skfuzzy import control as ctrl
import skfuzzy as fuzz
import numpy as np
from libs.annotation.fuzzy_utils import create_universes_membership_functions


class SportsRules:
    def __init__(self, show_sim_result=None):
        prox, over, spat = create_universes_membership_functions()
        self.__show_sim_result = show_sim_result
        self.__proximity = prox
        self.__overlap = over
        self.__spatial_relationships = spat
        self.__create_universes_of_discourse()
        self.__create_membership_functions()
        self.__create_boarding_rules()
        self.__create_baseball_rules()
        self.__create_tennis_rules()
        self.__create_frisbee_rules()
        self.__create_kite_rules()
        self.__create_soccer_rules()
        self.__create_tennis_ball_rules()
        self.__create_baseball_ball_rules()

    def __create_universes_of_discourse(self):
        """
        Skiing, surfing, and snowboarding can share a rule base
        Baseball bat and glove can share a rule base. If overlapping and very close they are playing baseball
        Frisbee will need its own rule.
        Kite will need its own rule.
        Tennis racket may work with the baseball rules. Overlapping and very close, playing tennis
        Need a rule for soccer, if sports ball is soccer call soccer rule. Sports ball could also come into play
        with baseball and tennis.
        """
        self.__boarding_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                      label='boarding_interaction')
        self.__baseball_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                      label='baseball_interaction')
        self.__tennis_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                    label='tennis_interaction')
        self.__frisbee_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                     label='frisbee_interaction')
        self.__kite_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                  label='kite_interaction')
        self.__soccer_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                    label='soccer_interaction')
        self.__tennis_ball_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                         label='tennis_ball_interaction')
        self.__baseball_ball_interaction = ctrl.Consequent(universe=np.arange(-0.1, 1.1, 0.1),
                                                           label='baseball_ball_interaction')

    def __create_membership_functions(self):
        self.__boarding_interaction['Riding'] = fuzz.trimf(self.__boarding_interaction.universe, [0.4, 0.7, 1.0])
        self.__boarding_interaction['Not Riding'] = fuzz.trimf(self.__boarding_interaction.universe, [0.0, 0.3, 0.6])
        self.__baseball_interaction['Playing'] = fuzz.trimf(self.__baseball_interaction.universe, [0.4, 0.7, 1.0])
        self.__baseball_interaction['Not Playing'] = fuzz.trimf(self.__baseball_interaction.universe, [0.0, 0.3, 0.6])
        self.__tennis_interaction['Playing'] = fuzz.trimf(self.__tennis_interaction.universe, [0.4, 0.7, 1.0])
        self.__tennis_interaction['Not Playing'] = fuzz.trimf(self.__tennis_interaction.universe, [0.0, 0.3, 0.6])
        self.__frisbee_interaction['Throwing'] = fuzz.trimf(self.__frisbee_interaction.universe, [0.4, 0.7, 1.0])
        self.__frisbee_interaction['Not Throwing'] = fuzz.trimf(self.__frisbee_interaction.universe, [0.0, 0.3, 0.6])
        self.__kite_interaction['Flying'] = fuzz.trimf(self.__kite_interaction.universe, [0.4, 0.7, 1.0])
        self.__kite_interaction['Not Flying'] = fuzz.trimf(self.__kite_interaction.universe, [0.0, 0.3, 0.6])
        self.__soccer_interaction['Playing'] = fuzz.trimf(self.__soccer_interaction.universe, [0.4, 0.7, 1.0])
        self.__soccer_interaction['Not Playing'] = fuzz.trimf(self.__soccer_interaction.universe, [0.0, 0.3, 0.6])
        self.__tennis_ball_interaction['Playing'] = fuzz.trimf(self.__tennis_ball_interaction.universe,
                                                               [0.4, 0.7, 1.0])
        self.__tennis_ball_interaction['Not Playing'] = fuzz.trimf(self.__tennis_ball_interaction.universe,
                                                                   [0.0, 0.3, 0.6])
        self.__baseball_ball_interaction['Playing'] = fuzz.trimf(self.__baseball_ball_interaction.universe,
                                                                 [0.4, 0.7, 1.0])
        self.__baseball_ball_interaction['Not Playing'] = fuzz.trimf(self.__tennis_ball_interaction.universe,
                                                                     [0.0, 0.3, 0.6])

    def __create_boarding_rules(self):
        # IF overlap AND very close OR close AND above(s) THEN riding
        self.__boarding_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                          (self.__proximity['Very Close'] | self.__proximity['Close'] |
                                           self.__proximity['Medium']) &
                                          (self.__spatial_relationships['Above Right'] |
                                           self.__spatial_relationships['Above'] |
                                           self.__spatial_relationships['Above Left']),
                                          self.__boarding_interaction['Riding'])
        self.__boarding_rule2 = ctrl.Rule(self.__overlap['No Overlap'] &
                                          (self.__proximity['Very Close'] | self.__proximity['Close']) &
                                          (self.__spatial_relationships['Below Right'] |
                                           self.__spatial_relationships['Below'] |
                                           self.__spatial_relationships['Below Left']),
                                          self.__boarding_interaction['Riding'])
        # IF overlap AND very close OR close AND below(s) THEN not riding
        self.__not_boarding_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                              (self.__proximity['Very Close'] | self.__proximity['Close'] |
                                               self.__proximity['Medium']) &
                                              (self.__spatial_relationships['Right1'] |
                                               self.__spatial_relationships['Right2'] |
                                               self.__spatial_relationships['Below Right'] |
                                               self.__spatial_relationships['Below'] |
                                               self.__spatial_relationships['Below Left'] |
                                               self.__spatial_relationships['Left']),
                                              self.__boarding_interaction['Not Riding'])
        # IF overlap AND medium OR far OR very far THEN not riding
        self.__not_boarding_rule2 = ctrl.Rule(self.__overlap['Overlap'] &
                                              (self.__proximity['Far'] |
                                               self.__proximity['Very Far']),
                                              self.__boarding_interaction['Not Riding'])
        # IF no overlap AND medium OR far OR very far THEN not riding
        self.__not_boarding_rule3 = ctrl.Rule(self.__overlap['No Overlap'] &
                                              (self.__proximity['Medium'] | self.__proximity['Far'] |
                                               self.__proximity['Very Far']), self.__boarding_interaction['Not Riding'])

        self.__boarding_ctrl = ctrl.ControlSystem([self.__boarding_rule1, self.__boarding_rule2,
                                                   self.__not_boarding_rule1, self.__not_boarding_rule2,
                                                   self.__not_boarding_rule3])
        self.__boarding_sim = ctrl.ControlSystemSimulation(self.__boarding_ctrl, flush_after_run=100)

    def __create_baseball_rules(self):
        # IF overlap AND very close OR close OR medium THEN playing
        self.__baseball_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                          (self.__proximity['Very Close'] | self.__proximity['Close'] |
                                           self.__proximity['Medium']), self.__baseball_interaction['Playing'])
        # IF overlap AND far OR very far THEN not playing
        self.__not_baseball_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                              (self.__proximity['Far'] | self.__proximity['Very Far']),
                                              self.__baseball_interaction['Not Playing'])
        # IF no overlap THEN not playing
        self.__not_baseball_rule2 = ctrl.Rule(self.__overlap['No Overlap'], self.__baseball_interaction['Not Playing'])
        self.__baseball_ctrl = ctrl.ControlSystem([self.__baseball_rule1, self.__not_baseball_rule1,
                                                   self.__not_baseball_rule2])
        self.__baseball_sim = ctrl.ControlSystemSimulation(self.__baseball_ctrl, flush_after_run=100)

    def __create_tennis_rules(self):
        # IF overlap AND very close OR close THEN playing
        self.__tennis_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                        (self.__proximity['Very Close'] | self.__proximity['Close']),
                                        self.__tennis_interaction['Playing'])
        # IF overlap AND far OR very far THEN not playing
        self.__not_tennis_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                            (self.__proximity['Medium'] | self.__proximity['Far'] |
                                             self.__proximity['Very Far']),
                                            self.__tennis_interaction['Not Playing'])
        # IF no overlap THEN not playing
        self.__not_tennis_rule2 = ctrl.Rule(self.__overlap['No Overlap'], self.__tennis_interaction['Not Playing'])
        self.__tennis_ctrl = ctrl.ControlSystem([self.__tennis_rule1, self.__not_tennis_rule1,
                                                 self.__not_tennis_rule2])
        self.__tennis_sim = ctrl.ControlSystemSimulation(self.__tennis_ctrl, flush_after_run=100)

    def __create_frisbee_rules(self):
        # IF overlap AND very close THEN throwing
        self.__frisbee_rule1 = ctrl.Rule(self.__overlap['Overlap'] & self.__proximity['Very Close'],
                                         self.__frisbee_interaction['Throwing'])
        # IF no overlap AND very close OR close OR medium AND not above THEN throwing
        self.__frisbee_rule2 = ctrl.Rule(self.__overlap['No Overlap'] &
                                         (self.__proximity['Very Close'] | self.__proximity['Close'] |
                                          self.__proximity['Medium']) &
                                         (self.__spatial_relationships['Right1'] |
                                          self.__spatial_relationships['Right2'] |
                                          self.__spatial_relationships['Below Right'] |
                                          self.__spatial_relationships['Below'] |
                                          self.__spatial_relationships['Below Left'] |
                                          self.__spatial_relationships['Left']),
                                         self.__frisbee_interaction['Throwing'])
        # IF overlap AND close OR medium OR far OR very far THEN not throwing
        self.__not_frisbee_rule1 = ctrl.Rule(self.__overlap['Overlap'] &
                                             (self.__proximity['Close'] | self.__proximity['Medium'] |
                                              self.__proximity['Far'] | self.__proximity['Very Far']),
                                             self.__frisbee_interaction['Not Throwing'])
        # IF no overlap AND far OR very far THEN not throwing
        self.__not_frisbee_rule2 = ctrl.Rule(self.__overlap['No Overlap'] &
                                             (self.__proximity['Far'] | self.__proximity['Very Far']),
                                             self.__frisbee_interaction['Not Throwing'])
        # IF no overlap AND very close OR close OR medium AND above THEN not throwing
        self.__not_frisbee_rule3 = ctrl.Rule(self.__overlap['No Overlap'] &
                                             (self.__proximity['Very Close'] | self.__proximity['Close'] |
                                              self.__proximity['Medium']) &
                                             (self.__spatial_relationships['Above Right'] |
                                              self.__spatial_relationships['Above'] |
                                              self.__spatial_relationships['Above Left']),
                                             self.__frisbee_interaction['Not Throwing'])
        self.__frisbee_ctrl = ctrl.ControlSystem([self.__frisbee_rule1, self.__frisbee_rule2,
                                                  self.__not_frisbee_rule1, self.__not_frisbee_rule2,
                                                  self.__not_frisbee_rule3])
        self.__frisbee_sim = ctrl.ControlSystemSimulation(self.__frisbee_ctrl, flush_after_run=100)

    def __create_kite_rules(self):
        # IF no overlap AND far OR very far AND below THEN flying
        self.__kite_rule1 = ctrl.Rule(self.__overlap['No Overlap'] &
                                      (self.__proximity['Medium'] | self.__proximity['Far'] |
                                       self.__proximity['Very Far']) &
                                      (self.__spatial_relationships['Below Left'] |
                                       self.__spatial_relationships['Below'] |
                                       self.__spatial_relationships['Below Right'] |
                                       self.__spatial_relationships['Right1'] |
                                       self.__spatial_relationships['Right2'] |
                                       self.__spatial_relationships['Left']),
                                      self.__kite_interaction['Flying'])
        # IF no overlap AND far OR very far AND right OR left OR above THEN not flying
        self.__not_kite_rule1 = ctrl.Rule(self.__overlap['No Overlap'] &
                                          (self.__proximity['Medium'] | self.__proximity['Far'] |
                                           self.__proximity['Very Far']) &
                                          (self.__spatial_relationships['Above Right'] |
                                           self.__spatial_relationships['Above'] |
                                           self.__spatial_relationships['Above Left']),
                                          self.__kite_interaction['Not Flying'])
        # IF no overlap AND very close OR close OR medium THEN not flying
        self.__not_kite_rule2 = ctrl.Rule(self.__overlap['No Overlap'] &
                                          (self.__proximity['Very Close'] |
                                           self.__proximity['Close']),
                                          self.__kite_interaction['Not Flying'])
        # IF overlap THEN not flying
        self.__not_kite_rule3 = ctrl.Rule(self.__overlap['Overlap'], self.__kite_interaction['Not Flying'])

        self.__kite_ctrl = ctrl.ControlSystem([self.__kite_rule1, self.__not_kite_rule1,
                                              self.__not_kite_rule2, self.__not_kite_rule3])
        self.__kite_sim = ctrl.ControlSystemSimulation(self.__kite_ctrl, flush_after_run=100)

    def __create_soccer_rules(self):
        self.__soccer_rule1 = ctrl.Rule((self.__proximity['Very Close'] | self.__proximity['Close'] |
                                         self.__proximity['Medium'] | self.__proximity['Far']),
                                        self.__soccer_interaction['Playing'])
        self.__not_soccer_rule1 = ctrl.Rule(self.__proximity['Very Far'], self.__soccer_interaction['Not Playing'])
        self.__soccer_ctrl = ctrl.ControlSystem([self.__soccer_rule1, self.__not_soccer_rule1])
        self.__soccer_sim = ctrl.ControlSystemSimulation(self.__soccer_ctrl, flush_after_run=100)

    def __create_tennis_ball_rules(self):
        """
        Very strict rules here because the tennis_racket rules should cover most cases
        """
        # IF very close OR close OR medium THEN playing
        self.__tennis_ball_rule1 = ctrl.Rule((self.__proximity['Very Close'] |
                                              self.__proximity['Close'] |
                                              self.__proximity['Medium']),
                                             self.__tennis_ball_interaction['Playing'])
        self.__not_tennis_ball_rule1 = ctrl.Rule((self.__proximity['Far'] | self.__proximity['Very Far']),
                                                 self.__tennis_ball_interaction['Not Playing'])
        self.__tennis_ball_ctrl = ctrl.ControlSystem([self.__tennis_ball_rule1, self.__not_tennis_ball_rule1])
        self.__tennis_ball_sim = ctrl.ControlSystemSimulation(self.__tennis_ball_ctrl, flush_after_run=100)

    def __create_baseball_ball_rules(self):
        """
        Very strict here because the baseball bat and baseball glove rules should cover most cases
        """
        # Temp for now
        self.__baseball_ball_rule1 = ctrl.Rule((self.__spatial_relationships['Below Right'] |
                                                self.__spatial_relationships['Below'] |
                                                self.__spatial_relationships['Below Left']),
                                               self.__baseball_ball_interaction['Playing'])

        self.__not_baseball_ball_rule1 = ctrl.Rule((self.__spatial_relationships['Right1'] |
                                                    self.__spatial_relationships['Right2'] |
                                                    self.__spatial_relationships['Above Right'] |
                                                    self.__spatial_relationships['Above'] |
                                                    self.__spatial_relationships['Above Left'] |
                                                    self.__spatial_relationships['Left']),
                                                   self.__baseball_ball_interaction['Not Playing'])
        self.__baseball_ball_ctrl = ctrl.ControlSystem([self.__baseball_ball_rule1, self.__not_baseball_ball_rule1])
        self.__baseball_ball_sim = ctrl.ControlSystemSimulation(self.__baseball_ball_ctrl, flush_after_run=100)

    def compute_boarding_interaction(self, giou, iou, sr_angle):
        self.__boarding_sim.input['overlap'] = iou
        self.__boarding_sim.input['proximity'] = giou
        self.__boarding_sim.input['spatial_relationships'] = sr_angle
        self.__boarding_sim.compute()
        if self.__show_sim_result:
            self.__boarding_interaction.view(sim=self.__boarding_sim)
        boarding_result = self.__boarding_sim.output['boarding_interaction']
        riding = fuzz.interp_membership(self.__boarding_interaction.universe,
                                        self.__boarding_interaction['Riding'].mf, boarding_result)
        not_riding = fuzz.interp_membership(self.__boarding_interaction.universe,
                                            self.__boarding_interaction['Not Riding'].mf, boarding_result)
        membership = {'Riding': riding, 'Not Riding': not_riding}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Riding':
            return None
        else:
            return ret_label

    def compute_baseball_interaction(self, giou, iou, sr_angle):
        self.__baseball_sim.input['overlap'] = iou
        self.__baseball_sim.input['proximity'] = giou
        self.__baseball_sim.compute()
        if self.__show_sim_result:
            self.__baseball_interaction.view(sim=self.__baseball_sim)
        baseball_result = self.__baseball_sim.output['baseball_interaction']
        playing = fuzz.interp_membership(self.__baseball_interaction.universe,
                                         self.__baseball_interaction['Playing'].mf, baseball_result)
        not_playing = fuzz.interp_membership(self.__baseball_interaction.universe,
                                             self.__baseball_interaction['Not Playing'].mf, baseball_result)
        membership = {'Playing': playing, 'Not Playing': not_playing}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Playing':
            return None
        else:
            return ret_label

    def compute_tennis_interaction(self, giou, iou, sr_angle):
        self.__tennis_sim.input['overlap'] = iou
        self.__tennis_sim.input['proximity'] = giou
        self.__tennis_sim.compute()
        if self.__show_sim_result:
            self.__tennis_interaction.view(sim=self.__tennis_sim)
        tennis_result = self.__tennis_sim.output['tennis_interaction']
        playing = fuzz.interp_membership(self.__tennis_interaction.universe,
                                         self.__tennis_interaction['Playing'].mf, tennis_result)
        not_playing = fuzz.interp_membership(self.__tennis_interaction.universe,
                                             self.__tennis_interaction['Not Playing'].mf, tennis_result)
        membership = {'Playing': playing, 'Not Playing': not_playing}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Playing':
            return None
        else:
            return ret_label

    def compute_frisbee_interaction(self, giou, iou, sr_angle):
        self.__frisbee_sim.input['overlap'] = iou
        self.__frisbee_sim.input['proximity'] = giou
        self.__frisbee_sim.input['spatial_relationships'] = sr_angle
        self.__frisbee_sim.compute()
        if self.__show_sim_result:
            self.__frisbee_interaction.view(sim=self.__frisbee_sim)
        frisbee_result = self.__frisbee_sim.output['frisbee_interaction']
        throwing = fuzz.interp_membership(self.__frisbee_interaction.universe,
                                          self.__frisbee_interaction['Throwing'].mf, frisbee_result)
        not_throwing = fuzz.interp_membership(self.__frisbee_interaction.universe,
                                              self.__frisbee_interaction['Not Throwing'].mf, frisbee_result)
        membership = {'Throwing': throwing, 'Not Throwing': not_throwing}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Throwing':
            return None
        else:
            return ret_label

    def compute_kite_interaction(self, giou, iou, sr_angle):
        self.__kite_sim.input['overlap'] = iou
        self.__kite_sim.input['proximity'] = giou
        self.__kite_sim.input['spatial_relationships'] = sr_angle
        self.__kite_sim.compute()
        if self.__show_sim_result:
            self.__kite_interaction.view(sim=self.__kite_sim)
        kite_result = self.__kite_sim.output['kite_interaction']
        flying = fuzz.interp_membership(self.__kite_interaction.universe,
                                        self.__kite_interaction['Flying'].mf, kite_result)
        not_flying = fuzz.interp_membership(self.__kite_interaction.universe,
                                            self.__kite_interaction['Not Flying'].mf, kite_result)
        membership = {'Flying': flying, 'Not Flying': not_flying}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Flying':
            return None
        else:
            return ret_label

    def compute_soccer_interaction(self, giou, iou, sr_angle):
        self.__soccer_sim.input['proximity'] = giou
        self.__soccer_sim.compute()
        if self.__show_sim_result:
            self.__soccer_interaction.view(sim=self.__soccer_sim)
        soccer_result = self.__soccer_sim.output['soccer_interaction']
        playing = fuzz.interp_membership(self.__soccer_interaction.universe,
                                         self.__soccer_interaction['Playing'].mf, soccer_result)
        not_playing = fuzz.interp_membership(self.__soccer_interaction.universe,
                                             self.__soccer_interaction['Not Playing'].mf, soccer_result)
        membership = {'Playing': playing, 'Not Playing': not_playing}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Playing':
            return None
        else:
            return ret_label

    def compute_tennis_ball_interaction(self, giou, iou, sr_angle):
        self.__tennis_ball_sim.input['proximity'] = giou
        self.__tennis_ball_sim.compute()
        if self.__show_sim_result:
            self.__tennis_ball_interaction.view(sim=self.__tennis_ball_sim)
        tennis_ball_result = self.__tennis_ball_sim.output['tennis_ball_interaction']
        playing = fuzz.interp_membership(self.__tennis_ball_interaction.universe,
                                         self.__tennis_ball_interaction['Playing'].mf, tennis_ball_result)
        not_playing = fuzz.interp_membership(self.__tennis_ball_interaction.universe,
                                             self.__tennis_ball_interaction['Not Playing'].mf, tennis_ball_result)
        membership = {'Playing': playing, 'Not Playing': not_playing}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Playing':
            return None
        else:
            return ret_label

    def compute_baseball_ball_interaction(self, giou, iou, sr_angle):
        self.__baseball_ball_sim.input['spatial_relationships'] = sr_angle
        self.__baseball_ball_sim.compute()
        if self.__show_sim_result:
            self.__baseball_ball_interaction.view(sim=self.__baseball_ball_sim)
        ball_result = self.__baseball_ball_sim.output['baseball_ball_interaction']
        playing = fuzz.interp_membership(self.__baseball_ball_interaction.universe,
                                         self.__baseball_ball_interaction['Playing'].mf, ball_result)
        not_playing = fuzz.interp_membership(self.__baseball_ball_interaction.universe,
                                             self.__baseball_ball_interaction['Not Playing'].mf, ball_result)
        membership = {'Playing': playing, 'Not Playing': not_playing}
        ret_label = max(membership, key=membership.get)
        if ret_label == 'Not Playing':
            return None
        else:
            return ret_label

    def compute_interaction(self, label, dom_cat, sub_cat, giou, iou, sr_angle, metadata):
        if label == 'snowboard' or label == 'skateboard' or label == 'surfboard' or label == 'skis':
            res_label = self.compute_boarding_interaction(giou, iou, sr_angle)
            return res_label
        if label == 'baseball_bat' or label == 'baseball_glove':
            res_label = self.compute_baseball_interaction(giou, iou, sr_angle)
            if res_label is not None:
                return 'Playing Baseball With'
            else:
                return None
        if label == 'tennis_racket':
            res_label = self.compute_tennis_interaction(giou, iou, sr_angle)
            if res_label is not None:
                return 'Playing Tennis With'
            else:
                return None
        if label == 'frisbee':
            res_label = self.compute_frisbee_interaction(giou, iou, sr_angle)
            return res_label
        if label == 'kite':
            res_label = self.compute_kite_interaction(giou, iou, sr_angle)
            return res_label
        if label == 'sports_ball':
            if metadata == 'soccer_ball':
                res_label = self.compute_soccer_interaction(giou, iou, sr_angle)
                if res_label is not None:
                    return 'Playing Soccer With'
                else:
                    return None
            elif metadata == 'baseball':
                res_label = self.compute_baseball_ball_interaction(giou, iou, sr_angle)
                if res_label is not None:
                    return 'Playing Baseball With'
                else:
                    return None
            elif metadata == 'tennis_ball':
                res_label = self.compute_tennis_ball_interaction(giou, iou, sr_angle)
                if res_label is not None:
                    return 'Playing Tennis With'
                else:
                    return None
            else:
                return None

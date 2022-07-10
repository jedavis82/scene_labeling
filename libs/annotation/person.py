"""
Construct a person domain FIS to process all person-object interactions
"""
from collections import defaultdict
import pandas as pd
import json
from libs.annotation.fis.animal import AnimalRules
from libs.annotation.fis.appliances import AppliancesRules
from libs.annotation.fis.clothing import ClothingRules
from libs.annotation.fis.electronics import ElectronicsRules
from libs.annotation.fis.food import FoodRules
from libs.annotation.fis.furniture import FurnitureRules
from libs.annotation.fis.household import HouseholdRules
from libs.annotation.fis.sports import SportsRules
from libs.annotation.fis.urban import UrbanRules
from libs.annotation.fis.vehicle import VehicleRules
from utils import get_consensus_angle, convert_meta_labels


class PersonRules:
    def __init__(self,
                 ontology_file='./input/object_ontology.csv',
                 show_sim_result=False):
        """
        Construct the Person domain FIS for object tuple inference
        :param ontology_file: File path to the object ontology structure
        :param show_sim_result: Display the resultant output of the FIS. Default False
        """
        assert ontology_file is not None, "Must supply ontology file path"
        self.__ontology_df = pd.read_csv(ontology_file, encoding='utf-8', engine='python')
        self.__ontology_df.drop(self.__ontology_df[self.__ontology_df['object'] == 'person'].index, inplace=True)
        self.__general_categories_lookup = defaultdict(list)
        self.__domain_categories_lookup = defaultdict(list)
        self.__subdomain_categories_lookup = defaultdict(list)

        self.__create_general_categories_lookup()
        self.__create_domain_categories_lookup()
        self.__create_subdomain_categories_lookup()

        self.__animal_rules = AnimalRules(show_sim_result)
        self.__appliance_rules = AppliancesRules(show_sim_result)
        self.__clothing_rules = ClothingRules(show_sim_result)
        self.__electronics_rules = ElectronicsRules(show_sim_result)
        self.__food_rules = FoodRules(show_sim_result)
        self.__furniture_rules = FurnitureRules(show_sim_result)
        self.__household_rules = HouseholdRules(show_sim_result)
        self.__urban_rules = UrbanRules(show_sim_result)
        self.__vehicle_rules = VehicleRules(show_sim_result)
        self.__sports_rules = SportsRules(show_sim_result)

    def __create_general_categories_lookup(self):
        general_categories = self.__ontology_df['general_category'].unique().flatten().tolist()
        for gc in general_categories:
            objects = list(self.__ontology_df.loc[self.__ontology_df['general_category'] == gc]['object'])
            objects = ['_'.join(o.split(' ')) for o in objects]
            self.__general_categories_lookup[gc] = objects

    def __create_domain_categories_lookup(self):
        domain_categories = self.__ontology_df['subcategory_1'].unique().flatten().tolist()
        for dc in domain_categories:
            objects = list(self.__ontology_df.loc[self.__ontology_df['subcategory_1'] == dc]['object'])
            objects = ['_'.join(o.split(' ')) for o in objects]
            self.__domain_categories_lookup[dc] = objects

    def __create_subdomain_categories_lookup(self):
        subdomain_df = self.__ontology_df.dropna()
        subdomain_categories = subdomain_df['subcategory_2'].unique().flatten().tolist()
        for sc in subdomain_categories:
            objects = list(subdomain_df.loc[subdomain_df['subcategory_2'] == sc]['object'])
            objects = ['_'.join(o.split(' ')) for o in objects]
            self.__subdomain_categories_lookup[sc] = objects

    def __get_general_category(self, label=None):
        for k, v in self.__general_categories_lookup.items():
            if label in v:
                return k

    def __get_domain_category(self, label=None):
        for k, v in self.__domain_categories_lookup.items():
            if label in v:
                return k

    def __get_subdomain_category(self, label=None):
        for k, v in self.__subdomain_categories_lookup.items():
            if label in v:
                return k
        return 'None'  # There is no subdomain for this object

    def get_categories(self, label=None):
        base_label = '_'.join(label.split('_')[:-1])
        general_category = self.__get_general_category(base_label)
        domain_category = self.__get_domain_category(base_label)
        subdomain_category = self.__get_subdomain_category(base_label)
        return general_category, domain_category, subdomain_category, base_label

    def compute_interactions(self, sr_result=None, metadata=None):
        """
        Take in the spatial relationship results, and call the appropriate FIS to compute the person-object
        image annotation
        :param sr_result: Computed spatial relationship results for an image
        :param metadata: Computed metadata information for an image
        :return: The person domain image annotation for each object tuple in an image
        """
        assert sr_result is not None, "Must supply spatial relationship results for image"
        assert metadata is not None, "Must supply image metadata"

        # Return a list of dictionaries as the result of the image
        person_annotations = list(dict())

        # All results will have the same relative path. This will be returned as a key
        rel_path = sr_result[0]['relative_path']
        for r in sr_result:
            if 'person' not in r['arg_label']:
                r['person_interaction'] = 'None'
                person_annotations.append(r)
                continue  # Cannot compute person object annotation if tuple does not contain a person
            label = r['ref_label']
            giou = r['proximity']
            iou = r['overlap']
            f0 = r['f0']
            f2 = r['f2']
            hybrid = r['hybrid']
            sr_angle = get_consensus_angle(f0, f2, hybrid)
            meta_label = convert_meta_labels(json.loads(metadata['labels']))

            gen_cat, dom_cat, sub_cat, base_label = self.get_categories(label)
            if gen_cat == 'animal':
                res_label = self.__animal_rules.compute_interaction(base_label, dom_cat, sub_cat, giou, iou, sr_angle)
            elif gen_cat == 'appliances':
                res_label = self.__appliance_rules.compute_interaction(giou, iou, sr_angle)
            elif gen_cat == 'clothing':
                res_label = self.__clothing_rules.compute_interaction(base_label, dom_cat, sub_cat, giou, iou, sr_angle)
            elif gen_cat == 'electronics':
                res_label = self.__electronics_rules.compute_interaction(base_label, dom_cat,
                                                                         sub_cat, giou, iou, sr_angle)
            elif gen_cat == 'food and tableware':
                res_label = self.__food_rules.compute_interaction(base_label, dom_cat, sub_cat, giou, iou, sr_angle)
            elif gen_cat == 'furniture and home decor':
                res_label = self.__furniture_rules.compute_interaction(base_label, dom_cat, sub_cat, giou, iou,
                                                                       sr_angle)
            elif gen_cat == 'household items':
                res_label = self.__household_rules.compute_interaction(base_label, dom_cat, sub_cat, giou, iou,
                                                                       sr_angle)
            elif gen_cat == 'urban':
                res_label = self.__urban_rules.compute_interaction(base_label, dom_cat, sub_cat, giou, iou, sr_angle)
            elif gen_cat == 'vehicle':
                res_label = self.__vehicle_rules.compute_interaction(base_label, dom_cat, sub_cat, giou, iou, sr_angle)
            elif gen_cat == 'sports':
                res_label = self.__sports_rules.compute_interaction(base_label, dom_cat, sub_cat, giou, iou, sr_angle,
                                                                    meta_label)
            else:
                # Invalid category, assign as None
                res_label = 'None'

            # Change the res label to be 'None' if None was returned from an FIS
            if res_label is None:
                res_label = 'None'

            r['person_interaction'] = res_label
            person_annotations.append(r)
        return rel_path, person_annotations

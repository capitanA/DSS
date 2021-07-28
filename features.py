import csv
import ipdb
import math
from helper import ownship_position, area_focus_votter, updown_range_calculator, aspect_votter, \
    collision_time_determinor, get_point, calc_dists_from_target, distance_formula, coordinates, bow_stern_checker, \
    stem_angle_checker
from tkinter import messagebox
import numpy as np


class Features:

    def __init__(self, log_objects, scenario, logger, time_stamp):
        self.scenario = scenario
        self.log_objects = log_objects
        self.logger = logger
        self.time_stamp = time_stamp
        self.aspect = None
        self.orientation = None
        self.distance_from_target = None
        self.area_of_focus = None
        self.heading = None
        self.speed = None
        self.maneuver = None
        self.combination_of_technique = None
        self.time_stamp = len(
            self.log_objects) - 1  # at some seconds the server cannot receive data (with no specific reason!)  so, the assistance time cannot be used for self.log_objects list(list out of range occur)
        print(self.time_stamp)
        self.ownship_tracker = list()
        self.route_sequence = ""
        self.route_sequence_creator()
        self.ice_technique_determinor()
        self.heading_calculator()
        self.aspect_calculator()
        self.orientation_calculator()
        self.distance_calculator()
        self.area_of_focus_determinor()
        self.speed_calculator()

    def route_sequence_creator(self):
        previous_pos = ""
        route_mapper_dict = {"top_left": "_TL", "top": "_T", "top_right": "_TR", "left": "_L", "right": "_R",
                             "bottom_left": "_BL", "bottom": "_B", "bottom_right": "_BR"}
        for sec in range(180, self.time_stamp):

            ownship_pos = ownship_position(self.scenario, self.log_objects[sec].latitude,
                                           self.log_objects[sec].longitude)
            if sec > 180:  # This is for creating the string sequence of ownship position after seccond of 180!
                if previous_pos != ownship_pos:
                    if ownship_pos != "alongside":
                        self.ownship_tracker.append(route_mapper_dict[ownship_pos])
                        self.route_sequence += route_mapper_dict[ownship_pos]
                        previous_pos = ownship_pos

    # The Aspect shows the vessel pathway in relation to the target. the options for this feature could be:
    # "J_approach": getting close to the target from bellow the zone.
    # "Direct": getting close to the target directly.
    # "Up_current": getting close to the target from up_current of the target.
    # Aspect_calculator considers the first 240 seconds of the log_file (based on the replay videos this feature
    # can be determined at the first 240s). If the user ask for assistance before 240, the code will go through
    # all the seconds from the beginning until the end.
    def aspect_calculator(self):
        aspect_vot_dict = {"up_current": 0, "J_approach": 0, "direct": 0}

        # if self.scenario==" emergency":
        #     i = 0
        #     while self.log_objects[i].longitude > 146.35541:
        #         ownship_pos = ownship_position(self.scenario, self.log_objects[i].latitude,
        #                                        self.log_objects[i].longitude)
        #         down_heading, up_heading = updown_range_calculator(self.log_objects[i].latitude,
        #                                                             self.log_objects[i].longitude,
        #                                                             self.scenario, ownship_pos)
        #         degree = (down_heading, up_heading)
        #
        #         updated_aspect_vot_dict = aspect_votter(self.log_objects, i, aspect_vot_dict, degree, self.scenario)
        #         i += 1
        #
        #     if updated_aspect_vot_dict:
        #         print(updated_aspect_vot_dict)
        #
        #         paires = [(value, key) for key, value in updated_aspect_vot_dict.items()]
        #
        #     else:
        #         self.logger.info("The dictionary for aspect_calculation didn't get updated!(Check features.py module)")
        #     self.aspect = max(paires)[1]
        # else:

        # the code will check only 240 second of the log_file to determine the orientation of the ownship.
        # If the assistance occurred before 240 secconds the code will consider the last seccond of the log_file.
        checking_secconds = 240
        if self.time_stamp < 240:
            checking_secconds = self.time_stamp
        for sec in range(0, checking_secconds, 1):
            ownship_pos = ownship_position(self.scenario, self.log_objects[sec].latitude,
                                           self.log_objects[sec].longitude)
            down_heading, up_heading, down_key, up_key = updown_range_calculator(self.log_objects[sec].latitude,
                                                                                 self.log_objects[sec].longitude,
                                                                                 self.scenario, ownship_pos, False)
            degree = (down_heading, up_heading)

            updated_aspect_vot_dict = aspect_votter(self.log_objects, sec, aspect_vot_dict, degree, self.scenario)

        if updated_aspect_vot_dict:
            print(updated_aspect_vot_dict)

            paires = [(value, key) for key, value in updated_aspect_vot_dict.items()]

        else:
            self.logger.info("The dictionary for aspect_calculation didn't get updated!(Check features.py module)")
        self.aspect = max(paires)[1]

    # to calculate the distance between two coordinates(lat,long), first, we need to convert the (lat,long) to (x,y)_
    # which is the cartesian coordinates. with that said, the equation "the calc_dist_from_target" had been used to_
    # get the distance between two (lat,long) coordinates directly.

    # Distance _calculator considers the mean distance from the target when seafarers are performing their main technique,
    # (according to the replay video main techniques are conducted from 400s until the end of the scenario).
    # if the user asks for assistance before 400s, then the distance would be calculated based on that time instantly,
    # but if they ask for help after 400, the mean distance would be calculated from 400 to the end of the log_file.
    # this function generate two distances one is the average of all distances during the scenario until the user asked for assitance,
    # the another one is the instante distance of vessel at the time of getting assitance.

    def distance_calculator(self):

        distances_list = calc_dists_from_target(self.log_objects[self.time_stamp].latitude,
                                                self.log_objects[self.time_stamp].longitude,
                                                self.scenario)

        if self.heading[0] == "perpendicular":

            distance = min(distances_list) - 40
        else:
            distance = min(distances_list) - 8.5

        if distance < 0:
            self.logger.info("User hit the target!")
            print("You hit the target. please make your distance further not to have a crash!")
        self.distance_from_target = distance
        print(f"this is the instant distance{self.distance_from_target}")

        # count = 0
        # if self.time_stamp - 400 <= 0:
        #
        #     starting_sec = self.time_stamp
        #     ending_sec = self.time_stamp + 1
        #     total = 1
        #
        #
        # else:
        #     starting_sec = 400
        #     ending_sec = self.time_stamp + 1
        #     total = (self.time_stamp - 400) + 1
        #
        # for num in range(starting_sec, ending_sec, 1):
        #
        #     distances_list = calc_dists_from_target(self.log_objects[num].latitude,
        #                                             self.log_objects[num].longitude,
        #                                             self.scenario)
        #
        #     if self.heading[0] == "perpendicular":
        #
        #         distances = min(distances_list) - 40
        #     else:
        #         distances = min(distances_list) - 8.5
        #
        #     if distances < 0:
        #         self.logger.info("User hit the target!")
        #         print("You hit the target. please make your distance further not to have a crash!")
        #         distances = 0
        #         instant_distance = 0
        #     count += distances
        #     instant_distance = distances
        # self.distance_from_target = (count / total, instant_distance)
        #
        # print(f" This is the average distance {count / total} and this is the instant distance{instant_distance}")
        # print(f" This is the average distance {count / total} and this is the instant distance{instant_distance}")

    def area_of_focus_determinor(self):
        area_of_focus_dict = {"av": 0, "z": 0, "az": 0, "along_zone": 0}
        # it checks every seconds to determine the position of the ownship respect to the target and zone and vot up the "area_of_focus_dict"
        for timeslip in range(0, self.time_stamp, 1):
            area_of_focus_dict = area_focus_votter(self.scenario, self.log_objects[timeslip], area_of_focus_dict)

        if self.scenario == "pushing":
            area_of_focus_dict.update(
                {"z": int(area_of_focus_dict["z"] * 1.15), "av": int(area_of_focus_dict["av"] * 1.1),
                 "az": int(area_of_focus_dict["az"] * 0.85)})
        paires = [(value, key) for key, value in area_of_focus_dict.items()]
        print(area_of_focus_dict)
        if area_of_focus_dict["z"] == 0 and area_of_focus_dict["av"] == 0 and area_of_focus_dict["az"] == 0 and \
                area_of_focus_dict["along_zone"] == 0:
            self.area_of_focus = "unknown"

        else:
            self.area_of_focus = max(paires)[1]

    # heading _calculator will create a dictionary to check what was the ownship heading either in time of assistance
    # or from the 400 to the end of the log_file. Then based on this dictionary, the most occurrence will be considered
    # as the ownship heading! if the user asks for assistance before 400s, then the heading would be calculated based on
    # that time instantly, but if they ask for help after 400, the heading would be determined from 400 to the end of the log_file.
    # This function returmn a tup[le with this format (heading_status,average_heading,instant_heading)
    def heading_calculator(self):

        head = 0
        heading_dict = {"perpendicular": 0, "stem": 0, "angle": 0, "changing": 0}
        # This is for making sure if more than necessary data is coming from IS, cut it off.
        # if self.time_stamp > 1800:
        #     self.time_stamp = 1800
        # if self.time_stamp > 900:
        #     self.time_stamp = 900

        if self.time_stamp - 400 <= 0:
            instant_heading = stem_angle_checker(self.scenario, self.log_objects[self.time_stamp].heading)
            # If the assitance occure before 400s the average and instant heading will be the same.
            self.heading = (
                instant_heading, self.log_objects[self.time_stamp].heading, self.log_objects[self.time_stamp].heading)
            self.logger.info("the user asked an assistance at an inappropriate time! (Not recommended)")
        else:
            starting_sec = 400
            ending_sec = self.time_stamp + 1
            for sec in range(starting_sec, ending_sec, 1):
                head += self.log_objects[sec].heading
                instant_heading = stem_angle_checker(self.scenario, self.log_objects[sec].heading)
                if instant_heading:
                    heading_dict.update({instant_heading: heading_dict[instant_heading] + 1})
            print(heading_dict)

            paires = [(value, key) for key, value in heading_dict.items()]
            heading = max(paires)[1]

            average_heading = head / (ending_sec - starting_sec)
            print(f"in baraye miyangine heading hastesh{average_heading}")
            self.heading = (heading, average_heading, self.log_objects[self.time_stamp].heading)

            if self.maneuver == "C":
                self.heading = ("changing", average_heading, self.log_objects[self.time_stamp].heading)

    def orientation_calculator(self):
        orientation_mode = True
        orientation_dict = {"bow": 0, "stern": 0, "parallel": 0}

        if self.maneuver == "circular":  # if the technique is 'circular', the orientation would be changing because it al
            self.orientation = "rotating"
        else:
            if self.time_stamp <= 180:
                starting_sec = self.time_stamp
                ending_sec = self.time_stamp + 1
            else:
                starting_sec = 180
                ending_sec = self.time_stamp

            for sec in range(starting_sec, ending_sec, 1):

                ownship_pos = ownship_position(self.scenario, self.log_objects[sec].latitude,
                                               self.log_objects[sec].longitude)

                instant_heading = stem_angle_checker(self.scenario, self.log_objects[sec].heading)
                if instant_heading == "stem" and ownship_pos not in ["bottom", "top"]:
                    orientation_dict.update({"parallel": orientation_dict["parallel"] + 1})
                elif (instant_heading == "perpendicular" and ownship_pos in ["bottom",
                                                                             "top"]) or \
                        (instant_heading == "stem" and ownship_pos in ["right",
                                                                       "left"]) and self.scenario == "pushing":

                    orientation_dict.update({"parallel": orientation_dict["parallel"] + 1})
                else:

                    down_heading, up_heading, down_key, up_key = updown_range_calculator(
                        self.log_objects[sec].latitude,
                        self.log_objects[sec].longitude,
                        self.scenario, ownship_pos, orientation_mode)
                    'emergency_4tens'

                    if self.scenario in ["emergency", "emergency_4tens", "leeway"]:
                        dist_long_up = coordinates[self.scenario]["long_" + up_key]
                        dist_lat_up = coordinates[self.scenario]["lat_" + up_key]
                        dist_long_down = coordinates[self.scenario]["long_" + down_key]
                        dist_lat_down = coordinates[self.scenario]["lat_" + down_key]
                    else:
                        dist_long_up = coordinates[self.scenario + "_zone"]["long_" + up_key]
                        dist_lat_up = coordinates[self.scenario + "_zone"]["lat_" + up_key]
                        dist_long_down = coordinates[self.scenario + "_zone"]["long_" + down_key]
                        dist_lat_down = coordinates[self.scenario + "_zone"]["lat_" + down_key]

                    down_distance = distance_formula(self.log_objects[sec].latitude, self.log_objects[sec].longitude,
                                                     dist_long_down, dist_lat_down)

                    up_distance = distance_formula(self.log_objects[sec].latitude, self.log_objects[sec].longitude,
                                                   dist_long_up, dist_lat_up)

                    instant_orientation = bow_stern_checker(self.scenario, ownship_pos, up_heading, down_heading,
                                                            orientation_dict,
                                                            down_distance, up_distance,
                                                            self.log_objects[sec].heading)
                    orientation_dict.update({instant_orientation: orientation_dict[instant_orientation] + 1})
            # orientation_dict.update(
            #     {"parallel": int(orientation_dict["parallel"] * 1.2), "bow": int(orientation_dict["bow"] * 0.9),
            #      "stern": int(orientation_dict["stern"] * 1.1)})
            print(orientation_dict)
            paires = [(value, key) for key, value in orientation_dict.items()]
            orientation = max(paires)[1]

            self.orientation = orientation

    # This function fill the speed variable in a tuple with this format: (speed_status,average_speed,instant_speed )
    def speed_calculator(self):

        if self.log_objects[self.time_stamp].sog <= 3:
            self.speed = ("safe", self.log_objects[self.time_stamp].sog)
        else:
            self.speed = ("dangerous", self.log_objects[self.time_stamp].sog)
        print(f"this is the instance speed{self.speed}")
        # sumed_speed = 0
        # for num in range(self.time_stamp + 1):
        #     sumed_speed += self.log_objects[num].sog
        # avg_speed = sumed_speed / (self.time_stamp + 1)
        #
        # if avg_speed <= 3:
        #     self.speed = ("safe", avg_speed, self.log_objects[self.time_stamp].sog)
        # else:
        #     self.speed = ("dangerous", avg_speed, self.log_objects[self.time_stamp].sog)
        # print(f"this is speed average{sumed_speed / self.time_stamp} and is {self.speed[0]}")

    # def check_for_sector(self, root_sequence):
    #     tr_occurance = root_sequence.count("_TR")
    #     t_occurance = root_sequence.count("_T")
    #     tl_occurance = root_sequence.count("_TL")
    #     if tr_occurance >= 2 and t_occurance >= 3:
    #         return True
    #     elif tl_occurance >= 2 and t_occurance >= 3:
    #         return True
    #     elif tl_occurance >= 3 and tr_occurance >= 2:
    #         return True
    #     else:
    #         return False
    def check_for_sector(self, root_sequence):
        sector_list = ["_TL_T_TR_T_TL_T_TR", "_TR_T_TL_T_TR_T_TL", "_TL_T_TL_T_TL", "_TR_T_TL_T_TL_T", "_T_TR_T_TR_T"]
        result = list(filter(lambda x: (x in root_sequence), sector_list))
        if any(result):
            return True
        else:
            return False

    def ice_technique_determinor(self):
        excluded_C = ["_BR_B", "_B_BL", "_BL_L", "_R_TR", "_TR_T", "_L_TL"]
        i = 0
        technique_dict = {"PW": 0, "L": 0, "P": 0}
        start_loc_ice = {"emergency_4tens": 146.38349, "emergency": 146.3655880, "pushing": 146.36156890,
                         "leeway": self.log_objects[0].longitude}
        colision_time = collision_time_determinor(self.scenario)
        if self.time_stamp <= 180:
            self.maneuver = "N/A_maneuver"
        else:
            for sec in range(180, self.time_stamp):
                heading_delta = abs(self.log_objects[sec].heading - self.log_objects[sec].cog)
                # vessel is not in contact with ice or is not in ice field.

                if sec not in colision_time or self.log_objects[sec].longitude > start_loc_ice[
                    self.scenario]:
                    # Heading and course are in the opposite direction    and   Engines are in forward direction
                    if 135 <= heading_delta <= 225 and abs(self.log_objects[sec].portengine) > 0 and \
                            abs(self.log_objects[
                                    sec].stbdengine) > 0:
                        technique_dict.update({"PW": technique_dict["PW"] + 1})
                    # if not propwashing in open water,must just be maneuvering in open water
                else:  # vessel is in contact with iced
                    if self.log_objects[sec].sog <= 0.4 and abs(self.log_objects[sec].aftthruster) > 0 and abs(
                            self.log_objects[
                                sec].forethruster) > 0:
                        technique_dict.update({"L": technique_dict["L"] + 1})

                    if 135 <= heading_delta <= 225:  # Heading and course are in the opposite direction
                        if abs(self.log_objects[sec].portengine) > 0 and \
                                abs(self.log_objects[
                                        sec].stbdengine) > 0:
                            technique_dict.update({"PW": technique_dict["PW"] + 1})
                    elif (self.log_objects[sec].sog > 0.4 and abs(self.log_objects[sec].aftthruster) > 0 and
                          self.log_objects[sec].forethruster > 0) or (
                            self.log_objects[sec].sog > 0.4 and abs(self.log_objects[sec].portengine) > 0 and abs(
                        self.log_objects[sec].stbdengine) > 0):  # if heading and course are alligned
                        technique_dict.update({"P": technique_dict["P"] + 1})

            if len(set(self.ownship_tracker)) > 5 and self.scenario == "pushing":
                self.maneuver = "C"
            elif self.scenario == "pushing" and ((len(set(self.ownship_tracker)) == 4 or
                                                  len(set(self.ownship_tracker)) == 5) and
                                                 not (any(list(filter(lambda x: (x in self.route_sequence),
                                                                      excluded_C))))):  # check if the vessel returmn to its the previous pos

                self.maneuver = "C"

            elif self.scenario == "pushing" and not self.maneuver == "C":  # C and S cannot be performed at the same time
                print(self.ownship_tracker)

                result = self.check_for_sector(self.route_sequence)
                if result:
                    self.maneuver = "S"
                    # technique_dict.update({"S": technique_dict["S"] + 1})
            technique_dict.update(
                {"PW": int(technique_dict["PW"] * 1.3), "P": int(technique_dict["P"] * 0.9)})
            print(technique_dict)
            paires = [(value, key) for key, value in technique_dict.items()]
            first_tech = max(paires)[1]
            first_tech_occure_num = max(paires)[0]

            paires.pop(paires.index(max(paires)))
            second_tech = max(paires)[1]
            second_tech_occure_num = max(paires)[0]
            print(self.route_sequence)

            # when just one technique have been used for a scenario other technique occurance shouldn't be check.
            if self.maneuver not in ["C", "S"]:

                for tech in technique_dict.values():
                    if tech == 0:
                        i += 1
                if i == 2:
                    self.maneuver = first_tech

                elif i < 2:  # this means other techniques in the technique_dict has a value other than 0(occured at least once!)

                    # thi is to set the techniue_occur_num back to its original for only P
                    if first_tech == "P":
                        first_tech_occure_num = first_tech_occure_num / 0.9
                    elif second_tech == "P":
                        second_tech_occure_num = second_tech_occure_num / 0.9

                    if first_tech_occure_num - second_tech_occure_num > 450 or second_tech_occure_num < 35:
                        self.maneuver = first_tech
                    else:
                        self.maneuver = first_tech + "+" + second_tech
                elif i == 3:  # this is just in case that the technique havn't been determined by the software so it sets to "P"
                    self.maneuver = "P"

                if "+" in self.maneuver:  # this is to see what is the combination of technique value 0 for solo 1 for combo
                    self.combination_of_technique = 1
                else:
                    self.combination_of_technique = 0
            print(self.maneuver)

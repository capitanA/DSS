import csv
import ipdb
import math
from helper import ownship_position, area_focus_votter, updown_rannge_calculator, aspect_votter, \
    collision_time_determinor, get_point, calc_dist_from_target
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
        self.ice_technique_determinor()
        self.heading_calculator()
        self.aspect_calculator()
        self.orientation_calculator()
        self.distance_calculator()
        self.area_of_focus_determinor()
        self.speed_calculator()

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
        #         down_heading, up_heading = updown_rannge_calculator(self.log_objects[i].latitude,
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
            down_heading, up_heading = updown_rannge_calculator(self.log_objects[sec].latitude,
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

    # to calculate the distance between two coordinates(lat,long), first, we need to convert the (lat,long) to (x,y)
    # which is the cartesian coordinates. with that said, the equation "the calc_dist_from_target" had been used to
    # get the distance between two (lat,long) coordinates directly.

    # Distance _calculator considers the mean distance from the target when seafarers are performing their main technique
    # (according to the replay video main techniques are conducted from 400s until the end of the scenario).
    # if the user asks for assistance before 400s, then the distance would be calculated based on that time instantly,
    # but if they ask for help after 400, the mean distance would be calculated from 400 to the end of the log_file.

    def distance_calculator(self):
        count = 0
        if self.time_stamp - 400 <= 0:
            starting_sec = self.time_stamp
            ending_sec = self.time_stamp + 1
            total = 1
        else:
            starting_sec = 400
            ending_sec = self.time_stamp
            total = (self.time_stamp - 400) + 1

        for num in range(starting_sec, ending_sec, 1):
            distances_list = calc_dist_from_target(self.log_objects[num].latitude,
                                                   self.log_objects[num].longitude,
                                                   self.scenario)

            self.distance_from_target = min(distances_list)
            count += self.distance_from_target
        print(f"this is distance {count / total}")

    def area_of_focus_determinor(self):
        area_of_focus_dict = {"av": 0, "z": 0, "az": 0, "along_zone": 0,"unknown":0}
        # it checks every seconds from minutes 3 to determine the position of the ownship respect to the target and zone and bot up the "area_of_focus_dict"
        for timeslip in range(0, self.time_stamp, 1):
            area_of_focus_dict = area_focus_votter(self.scenario, self.log_objects[timeslip], area_of_focus_dict)
        paires = [(value, key) for key, value in area_of_focus_dict.items()]
        print(area_of_focus_dict)

        self.area_of_focus = max(paires)[1]

    # heading _calculator will create a dictionary to check what was the ownship heading either in time of assistance
    # or from the 400 to the end of the log_file. Then based on this dictionary, the most occurrence will be considered
    # as the ownship heading! if the user asks for assistance before 400s, then the heading would be calculated based on
    # that time instantly, but if they ask for help after 400, the heading would be determined from 400 to the end of the log_file.
    def heading_calculator(self):
        if self.time_stamp - 400 <= 0:
            starting_sec = self.time_stamp
            ending_sec = self.time_stamp + 1
        else:
            starting_sec = 400
            ending_sec = self.time_stamp

        if self.time_stamp - 360 < 0:
            self.logger.info("the user asked an assistance at a n inappropriate time! (Not recommended)")
        heading_dict = {"perpendicular": 0, "stem": 0, "angle": 0}
        if self.scenario == "emergency":
            # when the scenario is emergency the coordinates should be rotated by 23 degree to get the correct answer.
            for sec in range(starting_sec, ending_sec, 1):
                angle = self.log_objects[sec].heading + 23
                self.log_objects[sec].heading = angle
                print(self.log_objects[sec].heading)

                # if angle < 0:
                #     angle = 360 + angle
                #     self.log_objects[sec].heading = angle
                if 103 <= self.log_objects[sec].heading <= 123 or 283 <= self.log_objects[
                    sec].heading <= 303:
                    heading_dict.update({"perpendicular": heading_dict["perpendicular"] + 1})
                elif 13 <= self.log_objects[sec].heading <= 33 or 193 <= self.log_objects[
                    sec].heading <= 213:
                    heading_dict.update({"stem": heading_dict["stem"] + 1})
                else:
                    heading_dict.update({"angle": heading_dict["angle"] + 1})
        else:
            for sec in range(starting_sec, ending_sec + 1, 1):
                if 350 <= self.log_objects[sec].heading <= 360 or 0 <= self.log_objects[sec].heading <= 10 or 170 <= \
                        self.log_objects[sec].heading <= 190:
                    heading_dict.update({"stem": heading_dict["stem"] + 1})
                elif 80 <= self.log_objects[sec].heading <= 100 or 260 <= self.log_objects[sec].heading <= 280:
                    heading_dict.update({"perpendicular": heading_dict["perpendicular"] + 1})
                else:
                    heading_dict.update({"angle": heading_dict["angle"] + 1})
        paires = [(value, key) for key, value in heading_dict.items()]
        heading = max(paires)[1]
        print(heading_dict)
        self.heading = (heading, self.log_objects[self.time_stamp].heading)

    def orientation_calculator(self):
        orientation_dict = {"bow": 0, "stern": 0, "parallel": 0}

        if self.time_stamp <= 180:
            starting_sec = self.time_stamp
            ending_sec = self.time_stamp + 1
        else:
            starting_sec = 180
            ending_sec = self.time_stamp

        for sec in range(starting_sec, ending_sec, 1):
            if self.heading[0] == "stem":
                orientation_dict.update({"parallel": orientation_dict["parallel"] + 1})
            else:
                ownship_pos = ownship_position(self.scenario, self.log_objects[sec].latitude,
                                               self.log_objects[sec].longitude)
                down_heading, up_heading = updown_rannge_calculator(self.log_objects[sec].latitude,
                                                                    self.log_objects[sec].longitude,
                                                                    self.scenario, ownship_pos, True)

                thresh = abs((up_heading - down_heading)) / 2
                new_range = [down_heading - thresh, up_heading + thresh]
                # if the down_heading is less than thresh, so it was placed in the fourth quarter. so it needs to have a different
                # calculation for determining the range.
                if new_range[0] <= 0:
                    new_ang = 360 + new_range[0]
                    new_range = [new_range[1], new_ang]
                # This line will check the heading is closer to which point (UP or Down).
                # This number 10 was achieved by experiments and makes the code work correctly!
                if abs(new_range[0] - self.log_objects[sec].heading) < new_range[1] - self.log_objects[
                    sec].heading:
                    new_range = [new_range[0] - 10, new_range[1]]
                else:
                    new_range = [new_range[0] + 10, new_range[1] + 10]
                #
                if 270 <= new_range[1] <= 360:
                    if 0 <= self.log_objects[sec].heading <= new_range[0] or new_range[1] <= self.log_objects[
                        sec].heading <= 360:
                        orientation_dict.update({"bow": orientation_dict["bow"] + 1})
                    else:
                        orientation_dict.update({"stern": orientation_dict["stern"] + 1})
                else:
                    if new_range[0] <= self.log_objects[sec].heading <= new_range[1]:
                        orientation_dict.update({"bow": orientation_dict["bow"] + 1})
                    else:
                        orientation_dict.update({"stern": orientation_dict["stern"] + 1})
        paires = [(value, key) for key, value in orientation_dict.items()]
        orientation = max(paires)[1]
        print(orientation_dict)
        self.orientation = orientation

    def speed_calculator(self):

        if self.log_objects[self.time_stamp].sog <= 3:
            self.speed = ("safe", self.log_objects[self.time_stamp].sog)
        else:
            self.speed = ("dangerous", self.log_objects[self.time_stamp].sog)

        count = 0
        for num in range(self.time_stamp + 1):
            count += self.log_objects[num].sog
        print(f"this is speed average{count / self.time_stamp} and is {self.speed[0]}")

    def ice_technique_determinor(self):
        technique_dict = {"prop_wash": 0, "leeway": 0, "pushing": 0, "other": 0}
        start_loc_ice = {"emergency": 146.3655880, "pushing": 146.36156890, "leeway": self.log_objects[0].longitude}
        colision_time = collision_time_determinor(self.scenario)
        for sec in range(self.time_stamp - 320, self.time_stamp + 1, 5):
            heading_delta = abs(self.log_objects[self.time_stamp].heading - self.log_objects[self.time_stamp].cog)
            # vessel is not in contact with ice or is not in ice field.
            if self.time_stamp not in colision_time or self.log_objects[self.time_stamp].longitude > start_loc_ice[
                self.scenario]:
                # Heading and course are in the opposite direction    and   Engines are in forward direction
                if 135 <= heading_delta <= 225 and self.log_objects[self.time_stamp].portengine > 0 and \
                        self.log_objects[
                            self.time_stamp].stbdengine > 0:
                    self.maneuver = "prop_wash"
                    technique_dict.update({"prop_wash": technique_dict["prop_wash"] + 1})
                # if not propwashing in open water,must just be maneuvering in open water
                else:
                    self.maneuver = "other"
                    technique_dict.update({"other": technique_dict["other"] + 1})
            else:  # vessel is in contact with iced
                if 135 <= heading_delta <= 225:  # Heading and course are in the opposite direction
                    if self.log_objects[self.time_stamp].sog <= 0.3:
                        if self.log_objects[self.time_stamp].portengine > 0 and self.log_objects[
                            self.time_stamp].stbdengine > 0:
                            self.maneuver = "prop_wash"
                            technique_dict.update({"prop_wash": technique_dict["prop_wash"] + 1})
                        else:
                            self.maneuver = "leeway"
                            technique_dict.update({"leeway": technique_dict["leeway"] + 1})
                    else:  # moving above 0.3 knots in reverse while in contact with ice

                        self.maneuver = "other"
                        technique_dict.update({"other": technique_dict["other"] + 1})
                elif self.log_objects[self.time_stamp].sog <= 0.3:
                    self.maneuver = "leeway"
                    technique_dict.update({"leeway": technique_dict["leeway"] + 1})
                else:  # if heading and course are alligned
                    self.maneuver = "pushing"
                    technique_dict.update({"pushing": technique_dict["pushing"] + 1})
        paires = [(value, key) for key, value in technique_dict.items()]
        self.maneuver = max(paires)[1]

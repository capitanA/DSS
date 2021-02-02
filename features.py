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
        self.aspect_calculator()
        self.orientation_calculator()
        self.distance_calculator()
        self.area_of_focus_determinor()
        self.heading_calculator()
        self.ice_technique_determinor()
        self.speed_calculator()

    def aspect_calculator(self):

        aspect_vot_dict = {"up_current": 0, "J_approach": 0, "direct": 0}
        # this 241 is for 3 minutes of the logfile to be considered for determining the aspect of the ownship
        for sec in range(0, 241, 1):
            ownship_pos = ownship_position(self.scenario, self.log_objects[sec].latitude,
                                           self.log_objects[sec].longitude)
            down_heading, up_heading = updown_rannge_calculator(self.log_objects[sec].latitude,
                                                                self.log_objects[sec].longitude,
                                                                self.scenario, ownship_pos)
            degree = (down_heading, up_heading)

            updated_aspect_vot_dict = aspect_votter(self.log_objects, sec, aspect_vot_dict, degree)

        if updated_aspect_vot_dict:

            paires = [(value, key) for key, value in updated_aspect_vot_dict.items()]

        else:
            self.logger.info("The dictionary for aspect_calculation didn't get updated!(Check features.py module)")
        self.aspect = max(paires)[1]

    def orientation_calculator(self):
        ownship_pos = ownship_position(self.scenario, self.log_objects[self.time_stamp].latitude,
                                       self.log_objects[self.time_stamp].longitude)
        down_heading, up_heading = updown_rannge_calculator(self.log_objects[self.time_stamp].latitude,
                                                            self.log_objects[self.time_stamp].longitude,
                                                            self.scenario, ownship_pos)

        thresh = abs((up_heading - down_heading)) / 2
        new_range = [down_heading - thresh, up_heading + thresh]
        # if the down_heading is less than thresh, so it placed in the fourth quarter so need to have a different
        # calculation for  determining the range
        if new_range[0] <= 0:
            new_ang = 360 - abs(new_range[0])
            new_range = [new_range[1], new_ang]
            if abs(new_range[0] - self.log_objects[self.time_stamp].heading) < new_range[1] - self.log_objects[
                self.time_stamp].heading:
                new_range = [new_range[0] - 10, new_range[1]]
            else:
                new_range = [new_range[0] + 10, new_range[1] + 10]
            if 0 <= self.log_objects[self.time_stamp].heading <= new_range[0] or new_range[1] <= self.log_objects[
                self.time_stamp].heading <= 360:
                self.orientation = "bow"

            else:
                self.orientation = "stern"


        else:
            # this part want to undestand if the ownship heading is close to the down_heading range or up_heading range!
            # this 10 achived by experiment and make the code work correctly
            if (abs(new_range[0] - self.log_objects[self.time_stamp].heading)) < (new_range[1] - self.log_objects[
                self.time_stamp].heading):
                new_range = [new_range[0] - 10, new_range[1]]
            else:
                new_range = [new_range[0] + 10, new_range[1] + 10]

            if new_range[0] <= self.log_objects[self.time_stamp].heading <= new_range[1]:
                self.orientation = "bow"
            else:
                self.orientation = "stern"

    # to calculate the distance between two coordinates(lat,long). first we need to convert the (lat,long) to (x,y)
    # which is the cartesian coordinates then calculate the distance. with tha said the equation "the calc_dist_from_target"
    # had used to get the distance between two (lat,long) coordinates directly.
    def distance_calculator(self):
        count = 0
        for num in range(500, 901, 1):
            distances_list = calc_dist_from_target(self.log_objects[num].latitude,
                                                   self.log_objects[num].longitude,
                                                   self.scenario)

            self.distance_from_target = min(distances_list)
            count += self.distance_from_target
        print(f"this is distance{count / 400}")

    def area_of_focus_determinor(self):
        area_of_focus_dict = {"av": 0, "z": 0, "az": 0, "along_zone": 0}
        # it checks every 5 seconds to determine the position of the ownship respect to the target and zone and bot up the "area_of_focus_dict"
        for timeslip in range(0, self.time_stamp + 1, 1):
            area_of_focus_dict = area_focus_votter(self.scenario, self.log_objects[timeslip], area_of_focus_dict)
        paires = [(value, key) for key, value in area_of_focus_dict.items()]

        self.area_of_focus = max(paires)[1]

    # Thi function will create a dictionary to check what was the ownship heading from 3 minutes before requesting assistance.
    # Then based on this dictionary, the most occurance will be considered as the ownship heading!
    def heading_calculator(self):
        heading_dict = {"perpendicular": 0, "stem": 0, "angle": 0}
        if self.time_stamp - 180 < 0:
            print("Raise an warning to let the user know this is not an appropriate time to get assistance!")
        else:
            for sec in range(self.time_stamp - 180, self.time_stamp + 1, 1):
                if 350 <= self.log_objects[
                    self.time_stamp].heading <= 360 or 0 <= self.log_objects[self.time_stamp].heading <= 10 or 170 <= \
                        self.log_objects[
                            self.time_stamp].heading <= 190:
                    heading_dict.update({"stem": heading_dict["stem"] + 1, "perpendicular": 0, "angle": 0})
                    # self.heading = ("stem", self.log_objects[self.time_stamp].heading)

                elif 80 <= self.log_objects[self.time_stamp].heading <= 100 or 260 <= self.log_objects[
                    self.time_stamp].heading <= 280:
                    heading_dict.update({"perpendicular": heading_dict["perpendicular"] + 1, "stem": 0, "angle": 0})
                    # self.heading = ("perpendicular", self.log_objects[self.time_stamp].heading)
                else:
                    heading_dict.update({"perpendicular": 0, "stem": 0, "angle": heading_dict["angle"] + 1})
                    # self.heading = ("angle", self.log_objects[self.time_stamp].heading)
            paires = [(value, key) for key, value in heading_dict.items()]
            heading = max(paires)[1]
            self.heading = (heading, self.log_objects[self.time_stamp].heading)

    def speed_calculator(self):

        count = 0
        for num in range(901):
            count += self.log_objects[num].sog
        print(f"this is speed average{count / 900}")

        if self.log_objects[self.time_stamp].sog <= 3:
            self.speed = ("safe", self.log_objects[self.time_stamp].sog)
        else:
            self.speed = ("dangerous", self.log_objects[self.time_stamp].sog)

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

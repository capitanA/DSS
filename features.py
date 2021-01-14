import csv
import ipdb
import math
from helper import ownship_position, area_focus_votter, updown_rannge_calculator, aspect_votter, \
    collision_time_determinor, get_point

TOP_TARGET_POINT = (60.51040, 146.35117)
CENTER_TARGET_POINT = (60.50914510, 146.35116730)
BOTTOM_TARGET_POINT = (60.50790, 146.33115)
dicdic = {"pushing": 0, "leeway": 0, "prop_wash": 0, "other": 0}


class Features:

    def __init__(self, log_objects, scenario, time_stamp):
        self.scenario = scenario
        self.log_objects = log_objects
        self.time_stamp = time_stamp
        self.aspect = None
        self.orientation = None
        self.distance_from_target = None
        self.area_of_focus = None
        self.heading = None
        self.speed = None
        self.ice_managment = None
        self.ide_loads = None
        self.ice_concentration = None
        self.maneuver = None
        self.aspect_calculator()
        self.orientation_calculator()
        self.distance_calculator()
        self.area_of_focus_determinor()
        self.heading_calculator()
        self.ice_technique_determinor()
        self.ice_loads_calculator()
        self.speed_calculator()

    def aspect_calculator(self):

        last_sec = self.log_objects[-1].simtime
        aspect_vot_dict = {"up_current": 0, "J_approach": 0, "direct": 0}
        for sec in range(0, 181):
            ownship_pos = ownship_position(self.scenario, self.log_objects[300].latitude,
                                           self.log_objects[360].longitude)
            down_heading, up_heading = updown_rannge_calculator(self.log_objects[sec].latitude,
                                                                self.log_objects[sec].longitude,
                                                                self.scenario, ownship_pos)
            degree = (down_heading, up_heading)

            updated_aspect_vot_dict = aspect_votter(self.log_objects, sec, aspect_vot_dict, degree)
        if updated_aspect_vot_dict:
            paires = [(value, key) for key, value in updated_aspect_vot_dict.items()]
        else:
            print("the updated_aspect_vot_dict didn't update")

        self.aspect = max(paires)[1]
        print(self.aspect)

    def orientation_calculator(self):
        ownship_pos = ownship_position(self.scenario, self.log_objects[-1].latitude, self.log_objects[-1].longitude)
        down_heading, up_heading = updown_rannge_calculator(self.log_objects[-1].latitude,
                                                            self.log_objects[-1].longitude,
                                                            self.scenario, ownship_pos)

        thresh = abs((up_heading - down_heading)) / 2
        new_range = [down_heading - thresh, up_heading + thresh]
        # ipdb.set_trace()
        print(new_range)

        ownship_pos = ownship_position(self.scenario, self.log_objects[-1].latitude, self.log_objects[-1].longitude)
        if new_range[0] <= 0:
            new_ang = 360 - abs(new_range[0])
            new_range = [new_range[1], new_ang]
            if abs(new_range[0] - self.log_objects[-1].heading) < new_range[1] - self.log_objects[-1].heading:
                new_range = [new_range[0] - 10, new_range[1]]
            else:
                new_range = [new_range[0] + 10, new_range[1] + 10]
            if 0 <= self.log_objects[-1].heading <= new_range[0] or new_range[1] <= self.log_objects[
                330].heading <= 360:
                self.orientation = "bow"
            else:
                self.orientation = "stern"

        else:
            if abs(new_range[0] - self.log_objects[-1].heading) < new_range[1] - self.log_objects[-1].heading:
                new_range = [new_range[0] - 10, new_range[1]]
            else:
                new_range = [new_range[0] + 10, new_range[1] + 10]

            if new_range[0] <= self.log_objects[-1].heading <= new_range[1]:
                self.orientation = "bow"
            else:
                self.orientation = "stern"

    def distance_calculator(self):
        point = get_point(self.scenario, self.log_objects[self.time_stamp].latitude,
                          self.log_objects[self.time_stamp].longitude)

        num1 = math.pow((self.log_objects[self.time_stamp].longitude - point[1]), 2)
        num2 = math.pow((self.log_objects[self.time_stamp].latitude - point[0]), 2)
        distnace_from_bottom = math.sqrt(num1 + num2)

        self.distance_from_target = distnace_from_bottom

    def area_of_focus_determinor(self):
        area_of_focus_dict = {"av": 0, "z": 0, "az": 0, "along_zone": 0}
        # it checks every 5 seconds to determine the position of the ownship respect to the target and zone and bot up the "area_of_focus_dict"
        for timeslip in range(1, self.time_stamp + 1, 5):
            area_of_focus_dict = area_focus_votter(self.scenario, self.log_objects[timeslip], area_of_focus_dict)
        paires = [(value, key) for key, value in area_of_focus_dict.items()]

        self.area_of_focus = max(paires)[1]

    def heading_calculator(self):
        if 350 <= self.log_objects[self.time_stamp].heading <= 10 or 170 <= self.log_objects[
            self.time_stamp].heading <= 190:
            self.heading = ("stem", self.log_objects[self.time_stamp].heading)

        elif 80 <= self.log_objects[self.time_stamp].heading <= 100 or 260 <= self.log_objects[
            self.time_stamp].heading <= 280:
            self.heading = ("perpendicular", self.log_objects[self.time_stamp].heading)
        else:
            self.heading = ("angle", self.log_objects[self.time_stamp].heading)

    def speed_calculator(self):
        if self.log_objects[self.time_stamp].sog <= 3:
            self.speed = ("safe", self.log_objects[self.time_stamp].sog)
        else:
            self.speed = ("dangerous", self.log_objects[self.time_stamp].sog)

    def ice_technique_determinor(self):
        start_loc_ice = {"emergency": 146.3655880, "pushing": 146.36156890, "leeway": self.log_objects[0].longitude}
        colision_time = collision_time_determinor(self.scenario)
        heading_delta = abs(self.log_objects[390].heading - self.log_objects[390].cog)
        # vessel is not in contact with ice or is not in ice field.
        if self.time_stamp not in colision_time or self.log_objects[self.time_stamp].longitude > start_loc_ice[
            self.scenario]:
            print(colision_time)
            print("not ")
            # Heading and course are in the opposite direction    and   Engines are in forward direction
            if 135 <= heading_delta <= 225 and self.log_objects[self.time_stamp].portengine > 0 and self.log_objects[
                self.time_stamp].stbdengine > 0:
                self.maneuver = "prop_wash"
                dicdic.update({"prop_wash": dicdic["prop_wash"] + 1})
            # if not propwashing in open water,must just be maneuvering in open water
            else:
                self.maneuver = "other"
                dicdic.update({"other": dicdic["other"] + 1})


        else:  # vessel is in contact with ice
            if 135 <= heading_delta <= 225:  # Heading and course are in the opposite direction
                if self.log_objects[self.time_stamp].portengine > 0 and self.log_objects[
                    self.time_stamp].stbdengine > 0:  # Engines are in forward direction
                    self.maneuver = "prop_wash"
                    dicdic.update({"prop_wash": dicdic["prop_wash"] + 1})
                elif self.log_objects[self.time_stamp].sog <= 0.2:
                    self.maneuver = "leeway"
                    dicdic.update({"leeway": dicdic["leeway"] + 1})
                else:  # moving above 0.4 knots in reverse while in contact with ice
                    self.maneuve = "other"
                    dicdic.update({"other": dicdic["other"] + 1})
            elif self.log_objects[self.time_stamp].sog <= 0.2:
                self.maneuver = "leeway"
                dicdic.update({"leeway": dicdic["leeway"] + 1})
            else:  # if heading and course are alligned
                self.maneuver = "pushing"
                dicdic.update({"pushing": dicdic["pushing"] + 1})
        print(self.maneuver)
        print(dicdic)

    def ice_loads_calculator(self):
        pass

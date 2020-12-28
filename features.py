import csv
import math
from helper import ownship_position, area_focus_votter
TOP_TARGET_POINT = (60.51040, 146.35117)
CENTER_TARGET_POINT = (60.50914510, 146.35116730)
BOTTOM_TARGET_POINT = (60.50790, 146.33115)


class Features:

    def __init__(self, log_objects, scenario, time_stamp):
        self.scenario = scenario
        self.log_objects = log_objects
        self.time_stamp = time_stamp
        self.vessel = None
        self.orientation = None
        self.distance_from_target = {"top": 0, "center": 0, "bottom": 0}
        self.area_of_focus = None
        self.heading = None
        self.speed = None
        self.ice_managment = None
        self.ide_loads = None
        self.ice_concentration = None
        self.aspect_calculator()
        self.orientation_calculator()
        self.distance_calculator()
        self.area_of_focus_determinor()
        self.heading_calculator()
        self.ice_technique_determinor()
        self.ice_loads_calculator()
        self.ice_concentration_calculator()
        self.speed_calculator()

    def aspect_calculator(self):
        pass

    def orientation_calculator(self):

        position = ownship_position(self.scenario, self.log_objects[self.time_stamp].latitude,
                                    self.log_objects[self.time_stamp].longtitude)

        heading = 50
        latitude = 70.76
        longtitude = 56.98

        # if target_lattitude < latitude:
        #     left = False

        if self.scenario in ["pushing", "leeway"]:
            if self.log_objects[self.time_stamp].heading >= 60 and self.log_objects[self.time_stamp].heading <= 120:
                self.orientation = "bow"
            elif self.log_objects[self.time_stamp].heading >= 250 and self.log_objects[self.time_stamp].heading <= 290:
                self.orientation = "stern"
            elif (self.log_objects[self.time_stamp].heading >= 350 and self.log_objects[
                self.time_stamp].heading <= 360) or (
                    self.log_objects[self.time_stamp].heading >= 0 and self.log_objects[
                self.time_stamp].heading <= 10) or (
                    self.log_objects[self.time_stamp].heading >= 170 and self.log_objects[
                self.time_stamp].heading <= 190):
                self.orientation = "paralel"

        elif self.scenario in ["pushing", "leeway"]:
            if self.log_objects[self.time_stamp].heading >= 60 and self.log_objects[self.time_stamp].heading <= 120:
                self.orientation = "stern"
            elif self.log_objects[self.time_stamp].heading >= 250 and self.log_objects[self.time_stamp].heading <= 290:
                self.orientation = "bow"
            elif (self.log_objects[self.time_stamp].heading >= 350 and self.log_objects[
                self.time_stamp].heading <= 360) or (
                    self.log_objects[self.time_stamp].heading >= 0 and self.log_objects[
                self.time_stamp].heading <= 10) or (
                    self.log_objects[self.time_stamp].heading >= 170 and self.log_objects[
                self.time_stamp].heading <= 190):
                self.orientation = "parallel"

        elif self.scenario not in ["pushing", "leeway"]:
            if self.log_objects[self.time_stamp].heading >= 90 and self.log_objects[self.time_stamp].heading <= 180:
                self.orientation = "bow"
            elif self.log_objects[self.time_stamp].heading >= 270 and self.log_objects[self.time_stamp].heading <= 360:
                self.orientation = "stern"
            elif (self.log_objects[self.time_stamp].heading >= 35 and heading <= 55) or (
                    self.log_objects[self.time_stamp].heading >= 215 and heading <= 235):
                self.orientation = "parallel"

        elif self.scenario not in ["pushing", "leeway"]:
            if self.log_objects[self.time_stamp].heading >= 90 and self.log_objects[self.time_stamp].heading <= 180:
                self.orientation = "stern"
            elif self.log_objects[self.time_stamp].heading >= 270 and self.log_objects[self.time_stamp].heading <= 360:
                self.orientation = "bow"
            elif (self.log_objects[self.time_stamp].heading >= 35 and self.log_objects[
                self.time_stamp].heading <= 55) or (
                    self.log_objects[self.time_stamp].heading >= 215 and self.log_objects[
                self.time_stamp].heading <= 235):
                self.orientation = "parallel"

    def distance_calculator(self,):
        num1 = math.pow((self.log_objects[self.time_stamp].longtitude - TOP_TARGET_POINT[1]), 2)
        num2 = math.pow((self.log_objects[self.time_stamp].latitude - TOP_TARGET_POINT[0]), 2)
        distnace_from_top = math.sqrt(num1 + num2)

        num1 = math.pow((self.log_objects[self.time_stamp].longtitude - CENTER_TARGET_POINT[1]), 2)
        num2 = math.pow((self.log_objects[self.time_stamp].latitude - CENTER_TARGET_POINT[0]), 2)
        distnace_from_center = math.sqrt(num1 + num2)

        num1 = math.pow((self.log_objects[self.time_stamp].longtitude - BOTTOM_TARGET_POINT[1]), 2)
        num2 = math.pow((self.log_objects[self.time_stamp].latitude - BOTTOM_TARGET_POINT[0]), 2)
        distnace_from_bottom = math.sqrt(num1 + num2)

        self.distance_from_target.update(
            {"top": distnace_from_top, "center": distnace_from_center, "bottom": distnace_from_bottom})

    def area_of_focus_determinor(self):
        area_of_focus_dict = {"av": 0, "z": 0, "az": 0, "along_zone": 0}
        # it checks every 5 seconds to determine the position of the ownship respect to the target and zone and bot up the "area_of_focus_dict"
        for timeslip in range(1, self.time_stamp + 1, 5):
            area_of_focus_dict = area_focus_votter(self.scenario, self.log_objects[timeslip], area_of_focus_dict)
        paires=[(value, key) for key, value in area_of_focus_dict.items()]

        self.area_of_focus = max(paires)[1]
        print(area_of_focus_dict)
        print(self.area_of_focus)

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
        pass

    def ice_loads_calculator(self):
        pass

    def ice_concentration_calculator(self):
        pass

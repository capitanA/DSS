import math
import tkinter as tk
import ipdb

coordinates = {
    "center_target_coordinated": {"lat": 60.51724810, "long": 146.35859560},

    "pushing": {"lat_top_left": 60.51049,
                "long_top_left": 146.35544,
                "lat_top_right": 60.51049,
                "long_top_right": 146.35435,
                "lat_btm_left": 60.50997,
                "long_btm_left": 146.35544,
                "lat_btm_right": 60.50997,
                "long_btm_right": 146.35435, "center_trgt_lat": 60.51023040,
                "center_trgt_long": 146.35488790},

    "leeway": {"lat_top_left": 60.51039,
               "long_top_left": 146.35159,
               "lat_top_right": 60.51039,
               "long_top_right": 146.35074,
               "lat_btm_left": 60.50790,
               "long_btm_left": 146.35159,
               "lat_btm_right": 60.50790,
               "long_btm_right": 146.35074, "center_trgt_lat": 60.50914510,
               "center_trgt_long": 146.35116730},

    "emergency": {"lat_top_left": 60.51833,
                  "long_top_left": 146.35961,
                  "lat_top_right": 60.51833,
                  "long_top_right": 146.35749,
                  "lat_btm_left": 60.51614,
                  "long_btm_left": 146.35961,
                  "lat_btm_right": 60.51614,
                  "long_btm_right": 146.35749,
                  "center_trgt_lat": 60.51724810,
                  "center_trgt_long": 146.35859560,
                  "lat_top_center": 60.51830,
                  "long_top_center": 146.35769,
                  "lat_btm_left_vessel": 60.51624,
                  "long_btm_left_vessel": 146.35972,
                  "lat_btm_right_vessel": 60.51614,
                  "long_btm_right_vessel": 146.35929},

    "pushing_zone": {"lat_top_left": 60.51117,
                     "long_top_left": 146.35678,
                     "lat_top_right": 60.51117,
                     "long_top_right": 146.35299,
                     "lat_btm_left": 60.50930,
                     "long_btm_left": 146.35678,
                     "lat_btm_right": 60.50930,
                     "long_btm_right": 146.35299},

    "leeway_zone": {"lat_top_left": 60.50914,
                    "long_top_left": 146.35285,
                    "lat_top_right": 60.50914,
                    "long_top_right": 146.35162,
                    "lat_btm_left": 60.50853,
                    "long_btm_left": 146.35285,
                    "lat_btm_right": 60.50853,
                    "long_btm_right": 146.35162}, "emergency_zone": {"lat_top_left": 60.51773,
                                                                     "long_top_left": 146.36102,
                                                                     "lat_top_right": 60.51731,
                                                                     "long_top_right": 146.35900,
                                                                     "lat_btm_left": 60.51667,
                                                                     "long_btm_left": 146.36194,
                                                                     "lat_btm_right": 60.51624,
                                                                     "long_btm_right": 146.35993}}


def angle_decorator(ownship_pos, ownship_lattitude, ownship_longtitude, downrange, uprange, scenario):
    if scenario == "emergency":
        if ownship_pos == "top_left":
            return downrange + 90, uprange + 90
        elif ownship_pos == "top":
            return downrange + 90, 270 - uprange
        elif ownship_pos == "top_right":
            return 270 - uprange, 270 - downrange
        elif ownship_pos == "bottom":
            return 90 - downrange, 270 + uprange
        elif ownship_lattitude > coordinates[scenario]["lat_btm_left_vessel"] and ownship_lattitude < \
                coordinates[scenario]["lat_top_left"] and ownship_longtitude > coordinates[scenario][
            "long_btm_left_vessel"]:
            return 90 - downrange, 90 + uprange
        elif ownship_lattitude < coordinates[scenario]["lat_btm_left_vessel"] and ownship_longtitude > \
                coordinates[scenario][
                    "long_btm_left_vessel"]:
            return 90 - downrange, 90 - uprange
        elif ownship_lattitude > coordinates[scenario]["lat_btm_left_vessel"] and ownship_lattitude < \
                coordinates[scenario]["lat_top_left"] and ownship_longtitude < coordinates[scenario][
            "long_btm_left_vessel"]:
            return 270 - uprange, 270 + downrange
        else:
            return 270 + uprange, 270 + downrange

    else:
        if ownship_pos == "top_left":
            return downrange + 90, uprange + 90
        elif ownship_pos == "left":
            return 90 - downrange, 90 + uprange
        elif ownship_pos == "btm_left":
            return 90 - downrange, 90 - uprange
        elif ownship_pos == "top_right":
            return 270 - uprange, 270 - downrange
        elif ownship_pos == "right":
            return 270 - uprange, 270 + downrange
        elif ownship_pos == "btm_right":
            return 270 + uprange, 270 + downrange
        elif ownship_pos == "top":
            return 270 - downrange, 90 + uprange
        elif ownship_pos == "bottom":
            return 90 - downrange, 270 + uprange


def updown_rannge_calculator(ownship_lattitude, ownship_longtitude, scenario):
    ownship_pos = ownship_position(scenario, ownship_lattitude, ownship_longtitude)
    if ownship_pos in ["top_left", "left", "btm_left"]:
        downrange_rad_angle = math.atan(abs(ownship_lattitude - (
            coordinates[scenario]["lat_top_left"] if scenario != "emergency" else coordinates[scenario][
                "lat_top_center"])) / abs(
            abs(ownship_longtitude) - (
                coordinates[scenario]["long_top_left"] if scenario != "emergency" else coordinates[scenario][
                    "long_top_center"])))
        uprange_rad_angel = math.atan(abs(ownship_lattitude - (
            coordinates[scenario]["lat_btm_left"] if scenario != "emergency" else coordinates[scenario][
                "lat_btm_left_vessel"])) / abs(
            abs(ownship_longtitude) - (
                coordinates[scenario]["long_btm_left"] if scenario != "emergency" else coordinates[scenario][
                    "long_btm_left_vessel"])))
        downrange_degree = math.degrees(abs(downrange_rad_angle / 0.54307152))
        uprange_degree = math.degrees(abs(uprange_rad_angel / 0.54307152))
        angle_range = angle_decorator(ownship_pos, ownship_lattitude, ownship_longtitude, downrange_degree,
                                      uprange_degree, scenario)

        return angle_range
    elif ownship_pos in ["top_right", "right", "btm_right"]:
        downrange_rad_angle = math.atan(abs(ownship_lattitude - (
            coordinates[scenario]["lat_top_right"] if scenario != "emergency" else coordinates[scenario][
                "lat_top_center"])) / abs(
            abs(ownship_longtitude) - (
                coordinates[scenario]["long_top_right"] if scenario != "emergency" else coordinates[scenario][
                    "long_top_center"])))
        uprange_rad_angel = math.atan(abs(ownship_lattitude - (
            coordinates[scenario]["lat_btm_right"] if scenario != "emergency" else coordinates[scenario][
                "lat_btm_right_vessel"])) / abs(
            abs(ownship_longtitude) - (
                coordinates[scenario]["long_btm_right"] if scenario != "emergency" else coordinates[scenario][
                    "long_btm_right_vessel"])))
        downrange_degree = math.degrees(abs(downrange_rad_angle / 0.54307152))
        uprange_degree = math.degrees(abs(uprange_rad_angel / 0.54307152))
        angle_range = angle_decorator(ownship_pos, ownship_lattitude, ownship_longtitude, downrange_degree,
                                      uprange_degree, scenario)
        return angle_range

    elif ownship_pos == "top":
        downrange_rad_angle = math.atan(abs(ownship_lattitude -
                                            (coordinates[scenario]["lat_top_right"] if scenario != "emergency" else
                                             coordinates[scenario][
                                                 "lat_top_center"]) / abs(
            abs(ownship_longtitude) - (
                coordinates[scenario]["long_top_right"] if scenario != "emergency" else coordinates[scenario][
                    "long_top_center"]))))
        uprange_rad_angel = math.atan(abs(ownship_lattitude -
                                          (coordinates[scenario]["lat_top_left"] if scenario != "emergency" else
                                           coordinates[scenario][
                                               "lat_btm_left_vessel"])) / abs(
            abs(ownship_longtitude) -
            (coordinates[scenario]["long_top_left"] if scenario != "emergency" else coordinates[scenario][
                "long_btm_left_vessel"])))

        downrange_degree = math.degrees(abs(downrange_rad_angle / 0.54307152))
        uprange_degree = math.degrees(abs(uprange_rad_angel / 0.54307152))
        angle_range = angle_decorator(ownship_pos, ownship_lattitude, ownship_longtitude, downrange_degree,
                                      uprange_degree, scenario)
        return angle_range
    elif ownship_pos == "bottom":
        downrange_rad_angle = math.atan(abs(ownship_lattitude -
                                            (coordinates[scenario]["lat_btm_right"] if scenario != "emergency" else
                                             coordinates[scenario][
                                                 "lat_top_center"]) / abs(
            abs(ownship_longtitude) - (
                coordinates[scenario]["long_btm_right"] if scenario != "emergency" else coordinates[scenario][
                    "long_top_center"]))))
        uprange_rad_angel = math.atan(abs(ownship_lattitude -
                                          (coordinates[scenario]["lat_btm_left"] if scenario != "emergency" else
                                           coordinates[scenario][
                                               "lat_btm_left_vessel"])) / abs(
            abs(ownship_longtitude) -
            (coordinates[scenario]["long_btm_left"] if scenario != "emergency" else coordinates[scenario][
                "long_btm_left_vessel"])))

        downrange_degree = math.degrees(abs(downrange_rad_angle / 0.54307152))
        uprange_degree = math.degrees(abs(uprange_rad_angel / 0.54307152))
        angle_range = angle_decorator(ownship_pos, ownship_lattitude, ownship_longtitude, downrange_degree,
                                      uprange_degree, scenario)
        return angle_range


def ownship_position(scenario, ownship_lattitude, ownship_longtitude):
    if "_zone" in scenario:

        if scenario == "emergency_zone":
            # Translation of Coordinate axes

            x12 = coordinates[scenario]["long_btm_left"] - coordinates[scenario]["long_btm_left"]
            y12 = coordinates[scenario]["lat_btm_left"] - coordinates[scenario]["lat_btm_left"]
            x22 = coordinates[scenario]["long_btm_right"] - coordinates[scenario]["long_btm_left"]
            y22 = coordinates[scenario]["lat_btm_right"] - coordinates[scenario]["lat_btm_left"]
            x32 = coordinates[scenario]["long_top_left"] - coordinates[scenario]["long_btm_left"]
            y32 = coordinates[scenario]["lat_top_left"] - coordinates[scenario]["lat_btm_left"]
            x42 = coordinates[scenario]["long_top_right"] - coordinates[scenario]["long_btm_left"]
            y42 = coordinates[scenario]["lat_top_right"] - coordinates[scenario]["lat_btm_left"]

            ma = (y32 - y12) / (x32 - x12)
            mb = (y42 - y22) / (x42 - x22)
            mc = (y22 - y12) / (x22 - x12)
            md = (y42 - y32) / (x42 - x32)

            # Translation of Coordinate axes for point 5
            x52 = ownship_longtitude - coordinates[scenario]["long_btm_left"]
            y52 = ownship_lattitude - coordinates[scenario]["lat_btm_left"]

            # finding zone of point 5
            if y52 > ma * x52:
                if y52 < mc * x52:
                    return "bottom_left"
                elif mc * x52 < y52 < (md * (x52 - x32) + y32):
                    return "left"
                else:
                    return "top_left"
            else:
                if y52 < mc * x52:
                    return "bottom"
                elif mc * x52 < y52 < (md * (x52 - x32) + y32):
                    return "z"
                else:
                    return "top"
        else:

            # check if th owner ship is upper than the target
            if ownship_lattitude > coordinates[scenario]["lat_top_left"]:
                if abs(ownship_longtitude) > abs(coordinates[scenario]["long_top_left"]):
                    return "top_left"
                elif abs(ownship_longtitude) < abs(coordinates[scenario]["long_top_right"]):
                    return "top_right"
                else:
                    return "top"
            # check if the ownership is lower than the target
            elif ownship_lattitude < coordinates[scenario]["lat_btm_left"]:
                if abs(ownship_longtitude) > abs(coordinates[scenario]["long_btm_left"]):
                    return "bottom_left"
                elif abs(ownship_longtitude) < abs(coordinates[scenario]["long_btm_right"]):
                    return "bottom_right"
                else:
                    return "bottom"
            else:
                if abs(ownship_longtitude) < abs(coordinates[scenario]["long_btm_left"]):
                    return "z"
                else:
                    return "alongside"
    else:

        # check if th owner ship is upper than the target
        if ownship_lattitude > coordinates[scenario]["lat_top_left"]:
            if abs(ownship_longtitude) > abs(coordinates[scenario]["long_top_left"]):
                return "top_left"
            elif abs(ownship_longtitude) < abs(coordinates[scenario]["long_top_right"]):
                return "top_right"
            else:
                return "top"
        # check if the ownership is lower than the target
        elif ownship_lattitude < coordinates[scenario]["lat_btm_left"]:
            if abs(ownship_longtitude) > abs(coordinates[scenario]["long_btm_left"]):
                return "bottom_left"
            elif abs(ownship_longtitude) < abs(coordinates[scenario]["long_btm_right"]):
                return "bottom_right"
            else:
                return "bottom"
        else:

            if abs(ownship_longtitude) > abs(coordinates[scenario]["long_btm_left"]):
                return "left"
            elif abs(ownship_longtitude) < abs(coordinates[scenario]["long_btm_right"]):

                return "right"
            else:

                return "alongside"


#
def sides_angle(ownship_long, ownship_lat, top_trgt_long, top_trgt_lat, btm_trgt_long, btm_trgt_lat):
    if (ownship_long - top_trgt_long) == 0:
        m_top = 10000000000
    else:
        m_top = (ownship_lat - top_trgt_lat) / (ownship_long - top_trgt_long)
    if (ownship_long - btm_trgt_long) == 0:
        m_bottom = 1000000000
    else:
        m_bottom = (ownship_lat - btm_trgt_lat) / (ownship_long - btm_trgt_long)
    print(m_bottom)
    print(m_top)
    return 180 - (math.fabs(math.degrees(math.atan(m_top)) - math.degrees(math.atan(m_bottom))))


def area_focus_votter(scenario, instant_log, area_of_focus_dict):
    if scenario == "leeway":
        ownship_target_pos = ownship_position(scenario, instant_log.latitude, instant_log.longtitude)
        ownship_zone_pos = ownship_position(scenario + "_zone", instant_log.latitude, instant_log.longtitude)
        if ownship_zone_pos == "z":
            area_of_focus_dict.update({"z": area_of_focus_dict["z"] + 1})
        elif ownship_zone_pos == "left":
            area_of_focus_dict.update({"along_zone": area_of_focus_dict["along_zone"] + 1})
        elif "top" in ownship_zone_pos and ownship_target_pos == "left":
            area_of_focus_dict.update({"az": area_of_focus_dict["az"] + 1})
        elif "top" in ownship_target_pos:
            area_of_focus_dict.update({"av": area_of_focus_dict["av"] + 1})
        return area_of_focus_dict

    elif scenario == "pushing":
        ownship_target_pos = ownship_position(scenario, instant_log.latitude, instant_log.longtitude)
        ownship_zone_pos = ownship_position(scenario + "_zone", instant_log.latitude, instant_log.longtitude)
        if ownship_zone_pos == "z":
            area_of_focus_dict.update({"z": area_of_focus_dict["z"] + 1})
        elif "top" in ownship_zone_pos:
            area_of_focus_dict.update({"az": area_of_focus_dict["az"] + 1})
        elif "top" in ownship_zone_pos and "top" in ownship_target_pos:
            area_of_focus_dict.update({"av": area_of_focus_dict["av"] + 1})
        elif ownship_zone_pos == "left":
            area_of_focus_dict.update({"along_zone": area_of_focus_dict["along_zone"] + 1})

        return area_of_focus_dict

    else:
        ownship_target_pos = ownship_position(scenario, instant_log.latitude, instant_log.longtitude)
        ownship_zone_pos = ownship_position(scenario + "_zone", instant_log.latitude, instant_log.longtitude)
        if ownship_zone_pos == "z":
            area_of_focus_dict.update({"z": area_of_focus_dict["z"] + 1})
        elif ownship_zone_pos == "top" and ownship_target_pos == "alongside":
            area_of_focus_dict.update({"az": area_of_focus_dict["az"] + 1})
        elif ownship_target_pos in ["top", "top_right"]:
            area_of_focus_dict.update({"av": area_of_focus_dict["av"] + 1})
        elif ownship_zone_pos in ["left"]:
            area_of_focus_dict.update({"along_zone": area_of_focus_dict["along_zone"] + 1})

        return area_of_focus_dict


def aspect_votter(log_objects, current_sec, aspect_vot_dict, degree_range):
    # it will check if the ship heading is biger than uprange smaller than downrange or in between them. then decide what is the aspect.
    ## I increased and decreased 5 degree to/from the threashold to be in a safe side for making decision.
    if log_objects[current_sec].heading > degree_range[1] + 5:
        aspect_vot_dict.update({"J_approach": aspect_vot_dict["J_approach"] + 1})
    elif log_objects[current_sec].heading < degree_range[0] - 5:
        aspect_vot_dict.update({"up_current": aspect_vot_dict["up_current"] + 1})
    else:
        aspect_vot_dict.update({"direct": aspect_vot_dict["direct"] + 1})
    return aspect_vot_dict


class BLabel(object):
    b = ">>>"

    def __init__(self, master):

        self.l = tk.Label(master, bg="white")

    def add_option(self, text):
        if self.l.cget("text") == "":
            self.l.config(text=self.b + " " + text)
        else:
            self.l.config(text=self.l.cget("text") + "\n" + self.b + " " + text, font=("helvetica", 12))

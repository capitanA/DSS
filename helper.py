import math
import tkinter as tk
import xml.etree.cElementTree as ET
import os
import ipdb

angle_pos_key = {"top": ["top_right", "top_left"], "bottom": ["btm_right", "btm_left"],
                 "left": ["top_left", "btm_left"], "right": ["btm_right", "top_right"],
                 "top_left": ["top_right", "btm_left"], "top_right": ["btm_right", "top_left"],
                 "bottom_left": ["top_left", "btm_right"], "bottom_right":
                     ["btm_left", "top_right"]}
angle_pos_key_emergency = {"top": ["top_center", "btm_left_vessel"], "bottom": ["top_center", "btm_left_vessel"],
                           "left": ["top_center", "btm_right_vessel"], "right": ["btm_right_vessel", "top_center"],
                           "top_left": ["top_center", "btm_left_vessel"],
                           "top_right": ["btm_right_vessel", "top_center"],
                           "bottom_left": ["top_center", "btm_right_vessel"], "bottom_right":
                               ["btm_right_vessel", "top_center"], "alongside": ["top_center", "btm_left"]}

coordinates = {
    "emergency_circumference": {
        "lat": (
            60.51831, 60.51825, 60.51811, 60.51790, 60.51771, 60.51751, 60.51731, 60.51708, 60.51685, 60.51662,
            60.51638,
            60.51619),
        "long": (
            146.35763, 146.35801, 146.35829, 146.35850, 146.35865, 146.35883, 146.35897, 146.35919, 146.35940,
            146.35958,
            146.35969, 146.35953)},
    "leeway_circumference": {"lat": (
        60.51039, 60.51021, 60.50996, 60.50971, 60.50974, 60.50917, 60.50894, 60.50870, 60.50843, 60.50817,
        60.50796, 60.50792), "long": (
        146.35117, 146.35148, 146.35159, 146.35159, 146.35159, 146.35159, 146.35159, 146.35159, 146.35159, 146.35154,
        146.35146, 146.35114)},
    "pushing_circumference": {"lat": 60.51023, "long": 146.35488, "df_from_corner": 42.60,
                              "df_from_circumference": 28.81},

    "pushing": {"lat_top_left": 60.51049,
                "long_top_left": 146.35544,
                "lat_top_right": 60.51049,
                "long_top_right": 146.35435,
                "lat_btm_left": 60.50997,
                "long_btm_left": 146.35544,
                "lat_btm_right": 60.50997,
                "long_btm_right": 146.35435,
                "center_trgt_lat": 60.51023040,
                "center_trgt_long": 146.35488790},

    "leeway": {"lat_top_left": 60.51039,
               "long_top_left": 146.35159,
               "lat_top_right": 60.51039,
               "long_top_right": 146.35074,
               "lat_btm_left": 60.50790,
               "long_btm_left": 146.35159,
               "lat_btm_right": 60.50790,
               "long_btm_right": 146.35074,
               "center_trgt_long": 146.35116730,
               "center_trgt_lat": 60.50914510,
               "long_top_center": 146.35116730,
               "lat_top_center": 60.51038,
               "center_trgt_btm_long": 146.35116730,
               "center_trgt_btm_lat": 60.50792},

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
                  "center_trgt_btm_lat": 60.49526,
                  "center_trgt_btm_long": 146.37848,
                  "lat_top_center": 60.51830,
                  "long_top_center": 146.35769,
                  "lat_btm_left_vessel": 60.51624,
                  "long_btm_left_vessel": 146.35972,
                  "lat_btm_right_vessel": 60.51614,
                  "long_btm_right_vessel": 146.35929},

    "pushing_zone": {"lat_top_left": 60.51116,
                     "long_top_left": 146.35677,
                     "lat_top_right": 60.51116,
                     "long_top_right": 146.35300,
                     "lat_btm_left": 60.50930,
                     "long_btm_left": 146.35677,
                     "lat_btm_right": 60.50930,
                     "long_btm_right": 146.35300},

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

# This dictionary will help to create a feature row, corresponding to status of ownship at the time of assistance request
feature_keys = {"solo": 0, "combo": 1, "P": 5, "L": 1, "PW": 2, "S": 3, "C": 4, "other": 7, "N/A_technique": 6,
                "J_approach": 1,
                "direct": 2, "up_current": 0, "N/A_aspect": 3, "av": 1, "z": 2, "az": 0, "along_zone": 3,
                "unknown": 4, "angle": 2, "perpendicular": 1, "stem": 0,
                "N/A_heading": 3, "stern": 2, "bow": 0, "rotating": 1, "parallel": 4, "N/A_orientation": 3, "safe": 0,
                "dangerous": 1, "N/A_speed": 2}


# This function determine in which quarter the ship got located. Then calculated the correct angle proportional in relation to the start point.
def angle_decorator(ownship_pos, ownship_lattitude, ownship_longitude, downrange, uprange, scenario):
    if scenario == "emergency":
        if ownship_pos == "top_left":
            return downrange + 90, uprange + 90
        elif ownship_pos == "top":
            return downrange + 90, 270 - uprange
        elif ownship_pos == "top_right":
            return 270 - downrange, 270 - uprange,
        elif ownship_pos == "bottom":
            return 90 - downrange, 270 + uprange
        # it is on the left side of target
        elif ownship_lattitude > coordinates[scenario]["lat_btm_left_vessel"] and ownship_lattitude < \
                coordinates[scenario]["lat_top_left"] and ownship_longitude > coordinates[scenario][
            "long_btm_left_vessel"]:
            return 90 - downrange, 90 + uprange
        # it is on the bottom_left of the target
        elif ownship_lattitude < coordinates[scenario]["lat_btm_left_vessel"] and ownship_longitude > \
                coordinates[scenario][
                    "long_btm_left_vessel"]:
            return 90 - downrange, 90 - uprange
        # it is on the right side of the target
        elif ownship_lattitude > coordinates[scenario]["lat_btm_left_vessel"] and ownship_lattitude < \
                coordinates[scenario]["lat_top_left"] and ownship_longitude < coordinates[scenario][
            "long_top_center"]:
            return 270 - downrange, 270 + uprange
        # it is on the along side of the target
        else:
            return 90 - downrange, 270 - uprange

    else:
        if ownship_pos == "top_left":
            return downrange + 90, uprange + 90
        elif ownship_pos == "left":
            return 90 - downrange, 90 + uprange
        elif ownship_pos == "bottom_left":
            return 90 - downrange, 90 - uprange
        elif ownship_pos == "top_right":
            return 270 - downrange, 270 - uprange
        elif ownship_pos == "right":
            return 270 - downrange, 270 + uprange
        elif ownship_pos == "bottom_right":
            return 270 + downrange, 270 + uprange
        elif ownship_pos == "top":
            return 90 + downrange, 270 - uprange
        elif ownship_pos == "bottom":
            return 90 - downrange, 270 + uprange


# This function calculate the angle range between the ownship and two points which is one at the furthest up in the
# target and the lowest down in the target. to see if the heading or COG is either in between, greater, and lower than
# this range. then decide what is the approach of the seafarer in the term of Aspect. Each scenario has their own
# coordinates to calculate the angle based on.  it uses the 'angle_pos_key' and 'angle_pos_key_emergency' to see which
# points it should consider from 'coordinates' dictionary. for the pushing scenario it use the 'pushing_zone' dictionary
# to get the points for determining the angle range
def updown_rannge_calculator(ownship_lattitude, ownship_longitude, scenario, ownship_pos, orientation_mode):
    if scenario in ["pushing", "leeway"]:
        down_key, up_key = angle_pos_key[ownship_pos]
    else:
        down_key_emg, up_key_emg = angle_pos_key_emergency[ownship_pos]

    if scenario == "pushing":
        if orientation_mode:
            coord_dict_key = scenario
        else:
            coord_dict_key = scenario + "_zone"
    else:
        coord_dict_key = scenario

        # downrange_rad_angle = math.atan(
        #     abs(ownship_lattitude - (coordinates[coord_dict_key]["lat_" + down_key])) / abs(
        #         abs(ownship_longitude) - (coordinates[coord_dict_key]["long_" + down_key])))
        # uprange_rad_angel = math.atan(abs(ownship_lattitude - (coordinates[coord_dict_key]["lat_" + up_key])) / abs(
        #     abs(ownship_longitude) - (coordinates[coord_dict_key]["long_" + up_key])))
        # downrange_degree = math.degrees(abs(downrange_rad_angle))
        # uprange_degree = math.degrees(abs(uprange_rad_angel))
        # correct_downrange_degree = correct_angle(downrange_degree)
        # correct_uprange_degree = correct_angle(uprange_degree)
        # angle_range = angle_decorator(ownship_pos, ownship_lattitude, ownship_longitude, correct_downrange_degree,
        #                               correct_uprange_degree, scenario)
    # else:

    downrange_rad_angle = math.atan(abs(ownship_lattitude - (
        coordinates[coord_dict_key]["lat_" + down_key] if scenario != "emergency" else coordinates[coord_dict_key][
            "lat_" + down_key_emg])) / abs(
        abs(ownship_longitude) - (
            coordinates[coord_dict_key]["long_" + down_key] if scenario != "emergency" else coordinates[coord_dict_key][
                "long_" + down_key_emg])))
    uprange_rad_angel = math.atan(abs(ownship_lattitude - (
        coordinates[coord_dict_key]["lat_" + up_key] if scenario != "emergency" else coordinates[coord_dict_key][
            "lat_" + down_key_emg])) / abs(
        abs(ownship_longitude) - (
            coordinates[coord_dict_key]["long_" + up_key] if scenario != "emergency" else coordinates[coord_dict_key][
                "long_" + up_key_emg])))
    downrange_degree = math.degrees(abs(downrange_rad_angle))
    uprange_degree = math.degrees(abs(uprange_rad_angel))
    correct_downrange_degree = correct_angle(downrange_degree)
    correct_uprange_degree = correct_angle(uprange_degree)
    angle_range = angle_decorator(ownship_pos, ownship_lattitude, ownship_longitude, correct_downrange_degree,
                                  correct_uprange_degree, scenario)
    if scenario == "emergency":
        return angle_range[0], angle_range[1], down_key_emg, up_key_emg
    else:
        return angle_range[0], angle_range[1], down_key, up_key


# This function determine the location of ownship vessel in relation to target!
def ownship_position(scenario, ownship_lattitude, ownship_longitude):
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
            x52 = ownship_longitude - coordinates[scenario]["long_btm_left"]
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

            # check if the ownship is upper than the target
            if ownship_lattitude > coordinates[scenario]["lat_top_left"]:
                if abs(ownship_longitude) > abs(coordinates[scenario]["long_top_left"]):
                    return "top_left"
                elif abs(ownship_longitude) < abs(coordinates[scenario]["long_top_right"]):
                    return "top_right"
                else:
                    return "top"
            # check if the ownership is lower than the target
            elif ownship_lattitude < coordinates[scenario]["lat_btm_left"]:
                if abs(ownship_longitude) > abs(coordinates[scenario]["long_btm_left"]):
                    return "bottom_left"
                elif abs(ownship_longitude) < abs(coordinates[scenario]["long_btm_right"]):
                    return "bottom_right"
                else:
                    return "bottom"
            else:
                return "z"
                # if abs(ownship_longitude) < abs(coordinates[scenario]["long_btm_left"]):
                #     return "z"
                # else:
                #     return "alongside"
    else:  # this is for determining where the ownship is located in relation to the target

        # check if the ownship is upper than the target
        if ownship_lattitude >= coordinates[scenario]["lat_top_left"]:
            if abs(ownship_longitude) >= abs(coordinates[scenario]["long_top_left"]):
                return "top_left"
            elif abs(ownship_longitude) <= abs(coordinates[scenario]["long_top_right"]):
                return "top_right"
            else:
                return "top"
        # check if the ownship is lower than the target
        elif ownship_lattitude <= coordinates[scenario]["lat_btm_left"]:
            if abs(ownship_longitude) >= abs(coordinates[scenario]["long_btm_left"]):
                return "bottom_left"
            elif abs(ownship_longitude) <= abs(coordinates[scenario]["long_btm_right"]):
                return "bottom_right"
            else:
                return "bottom"
        else:

            if abs(ownship_longitude) >= abs(coordinates[scenario]["long_btm_left"]):
                return "left"
            elif abs(ownship_longitude) <= abs(coordinates[scenario]["long_btm_right"]):

                return "right"
            else:
                return "alongside"


# this function will raise an vote to the current posision of ownship whether it is above vessel, above zone, in zone!
def area_focus_votter(scenario, instant_log, area_of_focus_dict):
    if scenario == "leeway":
        ownship_target_pos = ownship_position(scenario, instant_log.latitude, instant_log.longitude)
        ownship_zone_pos = ownship_position(scenario + "_zone", instant_log.latitude, instant_log.longitude)
        if ownship_zone_pos == "z":

            area_of_focus_dict.update({"z": area_of_focus_dict["z"] + 1})
        elif "top" in ownship_zone_pos and ownship_target_pos == "left":
            area_of_focus_dict.update({"az": area_of_focus_dict["az"] + 1})

        elif ownship_zone_pos == "left":
            area_of_focus_dict.update({"along_zone": area_of_focus_dict["along_zone"] + 1})

        elif "top" in ownship_target_pos:
            area_of_focus_dict.update({"av": area_of_focus_dict["av"] + 1})

        return area_of_focus_dict

    elif scenario == "pushing":
        ownship_target_pos = ownship_position(scenario, instant_log.latitude, instant_log.longitude)
        ownship_zone_pos = ownship_position(scenario + "_zone", instant_log.latitude, instant_log.longitude)
        if ownship_zone_pos == "z" and ("top" in ownship_target_pos):
            area_of_focus_dict.update({"av": area_of_focus_dict["av"] + 1})
        elif ownship_zone_pos == "z":
            area_of_focus_dict.update({"z": area_of_focus_dict["z"] + 1})
        elif "top" in ownship_zone_pos:
            area_of_focus_dict.update({"az": area_of_focus_dict["az"] + 1})
        # elif ownship_zone_pos == "z" and ("top" in ownship_target_pos):
        #     area_of_focus_dict.update({"av": area_of_focus_dict["av"] + 1})
        elif ownship_zone_pos == "left":
            area_of_focus_dict.update({"along_zone": area_of_focus_dict["along_zone"] + 1})

        return area_of_focus_dict


    else:  # this is for emergency
        ownship_target_pos = ownship_position(scenario, instant_log.latitude, instant_log.longitude)
        ownship_zone_pos = ownship_position(scenario + "_zone", instant_log.latitude, instant_log.longitude)
        if ownship_zone_pos == "z":
            area_of_focus_dict.update({"z": area_of_focus_dict["z"] + 1})
        elif (ownship_zone_pos == "top" and ownship_target_pos == "alongside") or ownship_target_pos == "alongside":
            area_of_focus_dict.update({"az": area_of_focus_dict["az"] + 1})
        elif ownship_target_pos in ["top", "top_right"]:
            area_of_focus_dict.update({"av": area_of_focus_dict["av"] + 1})
        elif ownship_zone_pos in ["left"]:
            area_of_focus_dict.update({"along_zone": area_of_focus_dict["along_zone"] + 1})

        return area_of_focus_dict


def aspect_votter(log_objects, current_sec, aspect_vot_dict, degree_range, scenario):
    # it will check if the ownship heading is bigger than uprange , smaller than downrange or in between them. then decide what is the aspect.
    ## I increased and decreased 5 degree to/from the threashold to be in a safe side for making decision.

    if scenario == "emergency":
        if log_objects[current_sec].heading > degree_range[1] + 5 and log_objects[current_sec].heading < 225:
            aspect_vot_dict.update({"J_approach": aspect_vot_dict["J_approach"] + 1})
        elif 0 < log_objects[current_sec].heading < degree_range[0] - 5 or 315 < log_objects[current_sec].heading < 360:
            aspect_vot_dict.update({"up_current": aspect_vot_dict["up_current"] + 1})
        elif log_objects[current_sec].heading <= degree_range[1] + 5 and log_objects[current_sec].heading >= \
                degree_range[0] - 5:
            aspect_vot_dict.update({"direct": aspect_vot_dict["direct"] + 1})
        return aspect_vot_dict
    else:

        if log_objects[current_sec].cog > degree_range[1] + 5 and log_objects[current_sec].cog < 225:
            aspect_vot_dict.update({"J_approach": aspect_vot_dict["J_approach"] + 1})
        elif 0 < log_objects[current_sec].cog < degree_range[0] - 5 or 315 < log_objects[current_sec].cog < 360:
            aspect_vot_dict.update({"up_current": aspect_vot_dict["up_current"] + 1})
        elif log_objects[current_sec].cog <= degree_range[1] + 5 and log_objects[current_sec].cog >= degree_range[
            0] - 5:
            aspect_vot_dict.update({"direct": aspect_vot_dict["direct"] + 1})
        return aspect_vot_dict


def correct_angle(x):
    y = (math.pow(10, -4) * math.pow(x, 3)) - (0.0228 * math.pow(x, 2)) + (2.2484 * x) - 0.3535
    return y


# this function determine in which seconds a collision occurred {collision with ICE}.
# stored those seconds in a set named "collision_time_set"
def collision_time_determinor(scenario):
    current_path = os.getcwd()
    dic_entity = {"thisEntityID": 0}
    collision_time = list()
    xml_file = ET.parse(current_path + '/well_formed_TraceData.log').getroot()
    for log_event in xml_file.iter("log_event"):
        for index, element in enumerate(log_event):
            if element.tag == "Load":
                for item in element.items():
                    if item:
                        dic_entity.update({item[0]: item[1]})
                if dic_entity["thisEntityID"] == "1" and dic_entity["thisEntityID"] != "10":
                    if scenario == "emergency" and float(log_event.attrib["SimTime"]) < 1801:
                        collision_time.append(int(float(log_event.attrib["SimTime"])))
                    elif (scenario == "pushing" or scenario == "leeway") and float(log_event.attrib["SimTime"]) < 901:
                        collision_time.append(int(float(log_event.attrib["SimTime"])))

    collision_time_set = set(collision_time)
    return collision_time_set


def get_point(scenario, ownship_lattitude, ownship_longitude):
    ownship_pos = ownship_position(scenario, ownship_lattitude, ownship_longitude)
    if scenario == "emergency":
        if ownship_pos in ["alongside", "left", "right"]:
            return coordinates[scenario]["center_trgt_lat"], coordinates[scenario]["center_trgt_long"]
        elif ownship_pos in ["bottom_left", "bottom_right", "bottom"]:
            return coordinates[scenario]["center_trgt_btm_lat"], coordinates[scenario]["center_trgt_btm_long"]
        else:
            return coordinates[scenario]["lat_top_center"], coordinates[scenario]["long_top_center"]

    elif scenario == "leeway":
        if ownship_pos in ["left", "right"]:
            return coordinates[scenario]["center_trgt_lat"], coordinates[scenario]["center_trgt_long"]
        elif ownship_pos in ["bottom_left", "bottom_right", "bottom"]:
            return coordinates[scenario]["center_trgt_btm_lat"], coordinates[scenario]["center_trgt_btm_long"]
        else:
            return coordinates[scenario]["lat_top_center"], coordinates[scenario]["long_top_center"]
    else:
        return coordinates[scenario]["center_trgt_lat"], coordinates[scenario]["center_trgt_long"]


def distance_formula(ownship_lat, ownship_long, dist_long, dist_lat):
    dx = abs((dist_long - ownship_long) * 40000 * math.cos(
        (ownship_lat + dist_lat) * math.pi / 360) / 360)
    dy = abs((ownship_lat - dist_lat) * 40000 / 360)
    distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    return distance


def calc_dists_from_target(ownship_lat, ownship_long, scenario):
    # to calculate the distance between two coordinates the below equation was used:
    # dx = (long1 - long2) * 40000 * math.cos((lat1 + lat2) * math.pi / 360) / 360
    # dy = (lat1- lat2) * 40000 / 360
    # distance = math.sqrt(math.pow(dx, 2) + math.pow(dy, 2))
    # for emergency and leeway scenario we calculate the distance between 12 point on the target circumference.
    # then the minimum of those distances considered as the  distance of ownship from target.
    # In the pushing scenario the distance of ownship from the target centre calculated.
    # then determine what the ownship position to subtract a certain amount as it is in the coordinates["pushing"] DICT

    dist_list = []
    if scenario in ["emergency", "leeway"]:

        for i in range(12):
            distance = distance_formula(ownship_lat, ownship_long, coordinates[scenario + "_circumference"]["long"][i],
                                        coordinates[scenario + "_circumference"]["lat"][i])
            dist_list.append(round(distance * 1000, 2))
    else:  # when the scenario is pushing
        distance = distance_formula(ownship_lat, ownship_long, coordinates[scenario + "_circumference"]["long"],
                                    coordinates[scenario + "_circumference"]["lat"])
        ownship_pos = ownship_position(scenario, ownship_lat, ownship_long)
        if ownship_pos in ["top_left", "top_right", "bottom_right", "bottom_left"]:

            dist_list.append(round((distance * 1000) - coordinates[scenario + "_circumference"]["df_from_corner"], 2))

        else:
            dist_list.append(
                round((distance * 1000) - coordinates[scenario + "_circumference"]["df_from_circumference"], 2))
    return dist_list


def bow_stern_checker(scenario,ownship_pos, up_heading, down_heading, orientation_dict, down_distance, up_distance, heading):
    thresh = abs((up_heading - down_heading)) / 2
    if ownship_pos == "top_left":
        if down_distance > up_distance:
            down_heading -= 10
        else:
            up_heading += 10
        new_range = [down_heading - thresh, up_heading + thresh]

        # if down_heading - thresh <= 0:
        #     new_ang = 360 + (down_heading - thresh)
        #     new_range = [up_heading + thresh, new_ang]
        # else:
        #     new_range = [down_heading - thresh, up_heading + thresh]
        # if down_heading - thresh <= 0:
        #     if 0 <= heading <= new_range[0] or new_range[1] <= heading <= 360:
        #
        #         return "bow"
        #     else:
        #         return "stern"
        # else:
        if new_range[0] <= heading <= new_range[1]:
            return "bow"
        else:
            return "stern"

    elif ownship_pos == "left" or ownship_pos == "alongside":
        if down_distance > up_distance:
            down_heading -= 10
        else:
            up_heading += 10
        if down_heading - thresh <= 0:
            new_ang = 360 + (down_heading - thresh)
            new_range = [up_heading + thresh, new_ang]
        else:
            new_range = [down_heading - thresh, up_heading + thresh]
        if down_heading - thresh <= 0:
            if 0 <= heading <= new_range[0] or new_range[1] <= heading <= 360:

                return "bow"
            else:
                return "stern"
        else:
            if new_range[0] <= heading <= new_range[1]:
                return "bow"
            else:
                return "stern"

    elif ownship_pos == "bottom_left":
        if down_distance > up_distance:
            down_heading -= 10
        else:
            up_heading += 10
        if 355 < down_heading < 360:
            down_heading = 0
        if up_heading > 90:
            up_heading = 90
        if down_heading - thresh <= 0:
            new_ang = 360 + (down_heading - thresh)
            new_range = [up_heading + thresh, new_ang]
        else:
            new_range = [down_heading - thresh, up_heading + thresh]

        if down_heading - thresh <= 0:
            if 0 <= heading <= new_range[0] or new_range[1] <= heading <= 360:
                print("az bottom_left bow dad")
                return "bow"
            else:
                print("az bottom_left stern dad")
                return "stern"
        else:
            if new_range[0] <= heading <= new_range[1]:
                print("az bottom_left bow dad")
                return "bow"
            else:
                print("az bottom_left stern dad")
                return "stern"
    elif ownship_pos == "bottom_right":
        if down_distance > up_distance:
            down_heading -= 10
        else:
            up_heading += 10
        if 0 <= up_heading < 5:
            up_heading = 360
        if up_heading + thresh > 360:
            new_ang = (up_heading + thresh) - 360
            new_range = [new_ang, down_heading - thresh]
        else:
            new_range = [down_heading - thresh, up_heading + thresh]

        if up_heading + thresh > 360:
            if 0 <= heading <= new_range[0] or new_range[1] <= heading <= 360:
                print("az bottom_right bow dad")
                return "bow"

            else:
                print("az bottom_right stern dad")
                return "stern"
        else:
            if new_range[0] <= heading <= new_range[1]:
                print("az bottom_right bow dad")
                return "bow"

            else:
                print("az bottom_right stern dad")
                return "stern"

    elif ownship_pos == "top_right":
        if down_distance > up_distance:
            down_heading -= 10
        else:
            up_heading += 10
        new_range = [down_heading - thresh, up_heading + thresh]
        if new_range[0] <= heading <= new_range[1]:
            print("az top_right bow dad")
            return "bow"
        else:
            print("az top_right stern dad")
            return "stern"

    elif ownship_pos == "right":
        if down_distance > up_distance:
            down_heading -= 10
        else:
            up_heading += 10

        if up_heading + thresh > 360:
            new_ang = (up_heading + thresh) - 360
            new_range = [new_ang, down_heading - thresh]
        else:
            new_range = [down_heading - thresh, up_heading + thresh]

        if up_heading + thresh > 360:
            if 0 <= heading <= new_range[0] or new_range[1] <= heading <= 360:
                print("az right bow dad")
                return "bow"
            else:
                print("az right stern dad")
                return "stern"
        else:
            if new_range[0] <= heading <= new_range[1]:
                print("az right bow dad")
                return "bow"
            else:
                print("az right stern dad")
                return "stern"



    elif ownship_pos == "top":
        if down_distance > up_distance:
            down_heading -= 10
        else:
            up_heading += 10
        new_range = [down_heading - thresh, up_heading + thresh]
        if new_range[0] <= heading <= new_range[1]:
            print("too top bow dad")
            return "bow"
        else:
            print("too top stern dad")
            return "stern"

    elif ownship_pos == "bottom":
        if 0 <= up_heading < 5:
            up_heading = 360
        if 355 < down_heading <= 360:
            down_heading = 0
        if down_distance > up_distance:
            down_heading += 10
        else:
            up_heading -= 10

        if 0 <= heading <= down_heading or up_heading <= heading <= 360:
            print("az bottom bow dad")
            return "bow"
        else:
            print("az bottom stern dad")
            return "stern"


def stem_angle_checker(scenario, heading):
    if scenario == "emergency":
        heading = heading + 23
        if 103 <= heading <= 123 or 283 <= heading <= 303:
            return "perpendicular"
        elif 13 <= heading <= 33 or 193 <= heading <= 213:
            return "stem"
        else:
            return "angle"
    else:
        if 350 <= heading <= 360 or 0 <= heading <= 10 or 170 <= heading <= 190:
            return "stem"
        elif 80 <= heading <= 100 or 260 <= heading <= 280:
            return "perpendicular"
        else:
            return "angle"


def generate_feature_array(features, scenario):
    features_array = list()
    Area_of_focus = feature_keys[features.area_of_focus]
    heading = feature_keys[features.heading[0]]

    orientation = feature_keys[features.orientation]
    if features.distance_from_target <= 35:  # This range has been assumed for the ownship to be in a close distance to the target!
        vessel_Distance_from_target = 0
    elif features.distance_from_target > 75:  # When the ownship is in a normal distance to the target!
        vessel_Distance_from_target = 1
    else:
        vessel_Distance_from_target = 2

    speed = feature_keys[features.speed[0]]
    technique = feature_keys[features.maneuver]
    aspect = feature_keys[features.aspect]
    if "+" in features.aspect:
        combination_of_technique = 1
    else:
        combination_of_technique = 0
    if scenario == "emergency":
        features_array.append(
            [Area_of_focus, heading, orientation, vessel_Distance_from_target, speed, technique, aspect,
             combination_of_technique])
    else:
        features_array.append(
            [heading, orientation,Area_of_focus,speed, vessel_Distance_from_target, technique, aspect,
             combination_of_technique])
    return features_array


class BLabel(object):
    b = ">>>"

    def __init__(self, master):

        self.l = tk.Label(master, bg="white")

    def add_option(self, text):
        if self.l.cget("text") == "":
            self.l.config(text=self.b + " " + text)
        else:
            self.l.config(text=self.l.cget("text") + "\n" + self.b + " " + text, font=("helvetica", 12))

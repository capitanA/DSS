"""
This scripts is for safety at sea project design to help seafarer to drive the ships better
Created on Dec 6 Nov 8:27:27 2020
@author:Fatemeh Yazdanpanah and Arash Fassihozzaman  <a.fassihozzamanlangroudi@mun.ca>
"""

import tkinter as tk
from log_file import CsvFile
from features import Features
import os
import xml.etree.cElementTree as ET
import csv
from tkinter import messagebox
from helper import feature_array_convertor
from sklearn.metrics import pairwise_distances_argmin_min
import logging
import pandas as pd
import os
import numpy as np
from sklearn import tree
from PIL import ImageTk, Image
from HoverInfo import HoverText
from simReceiver import SimReceiver
import ipdb

engine_dic = {"pEngine": 0, "fTunnelThruster": 0, "sEngine": 0, "aTunnelThruster": 0}
rudder_dic = {"pRudder": 0, "sRudder": 0}


class PlayScenario:

    def __init__(self, root, main_frame, scenario, logger, isRealTime):
        self.root = root
        self.main_frame = main_frame
        self.scenario = scenario
        self.logger = logger
        self.main_frame_width = self.main_frame.winfo_width()
        self.main_frame_height = self.main_frame.winfo_height()
        self.features = None
        self.log_objects = []
        self.isRealTime = isRealTime
        self.name = "arash"

        if isRealTime:
            self.simReceiver = SimReceiver(self)

        # self.suggested_speed = None
        # self.suggested_heading = None
        # self.suggested_area_focus = None
        # self.suggested_aspect = None
        # self.suggested_orientation = None
        # self.suggested_distance_target = None
        # self.suggested_maneuver = None

    def addLogLine(self, csvLine):
        self.log_objects.append(csvLine)

    # this function will make the TraceData file well_formed to be ready for parsing.
    def log_reader(self):
        current_path = os.getcwd()
        wl_frmd_trcdt_path = current_path + "/well_formed_TraceData.log"
        try:

            well_formed_tracedata = open(wl_frmd_trcdt_path,
                                         "w+")
        except FileNotFoundError as e:

            self.logger.info("Well_formed_TraceData.log haven't been created!")

        try:
            f = open(current_path + '/TraceData.log', 'r')
            linelist = f.readlines()
            for line in linelist:

                if line.rfind("Throttle Pcts") != -1:
                    line = line.replace("Throttle Pcts", "Throttle_Pcts")
                if line.rfind("Rudder Angles") != -1:
                    line = line.replace("Rudder Angles", "Rudder_Angles")
                well_formed_tracedata.write(line)
        except FileNotFoundError as fnf_error:
            logging.exception("TraceData file couldn't be found!")
            self.logger.info("TraceData file couldn't be found! There is no such a file in the project directory!")

        return well_formed_tracedata.name

    # This function will generate a csv file based on the TraceDtaa logfile!
    def generate_csv_file(self, log_objects):
        current_path = os.getcwd()
        fields_name = ["SimTime", "Latitude", "Longitude", "SOG", "COG", "Heading", "AftThruster",
                       "ForeThruster",
                       "PortEngine", "StbdEngine", "PortRudder", "StbdRudder"]
        try:
            with open(current_path + '/csv_interpolatedLog.csv', "w+") as logfile_csv:
                csv_writer = csv.DictWriter(logfile_csv, fieldnames=fields_name)
                csv_writer.writeheader()
                for line_num in range(len(log_objects)):
                    csv_writer.writerow(
                        {"SimTime": log_objects[line_num].simtime, "Latitude": log_objects[line_num].latitude,
                         "Longitude": log_objects[line_num].longitude, "SOG": log_objects[line_num].sog,
                         "COG": log_objects[line_num].cog, "Heading": log_objects[line_num].heading,
                         "AftThruster": log_objects[line_num].aftthruster,
                         "ForeThruster": log_objects[line_num].forethruster,
                         "PortEngine": log_objects[line_num].portengine, "StbdEngine": log_objects[line_num].stbdengine,
                         "PortRudder": log_objects[line_num].portrudder,
                         "StbdRudder": log_objects[line_num].stbdrudder})
        except FileNotFoundError as fnf_error:
            print(fnf_error)
            self.logger.info("Couldn't open 'csv_interpolatedLog.csv' file")

        return logfile_csv.name

    # this function is aimed to parse the log file and iterate into the file to  fill the log_objects list in which,
    # each object is a row for our csv file to be generated
    def assist(self):
        if not self.isRealTime:
            i = 0
            well_formed_filename = self.log_reader()

            try:
                xml_file = ET.parse(well_formed_filename).getroot()
            except IOError:
                # except FileNotFoundError as fnf_error:
                self.logger.info("The well_formed_TraceData.log cannot be parsed! it seems there is no such a file!")

            for log_entity in xml_file.iter("log_entity"):
                if log_entity.attrib["SimTime"] == "0":
                    continue
                if float(log_entity.attrib["SimTime"]) > i:
                    for index, element in enumerate(log_entity):
                        for item in element.items():
                            if item:
                                if index == 0:
                                    engine_dic.update({item[0]: float(item[1])})
                                elif index == 1:
                                    rudder_dic.update({item[0]: float(item[1])})
                    aftthruster = engine_dic["aTunnelThruster"]
                    forethruster = engine_dic["fTunnelThruster"]
                    portengine = engine_dic["pEngine"]
                    stbdengine = engine_dic["sEngine"]
                    portrudder = rudder_dic["pRudder"]
                    stbdrudder = rudder_dic["sRudder"]
                    # in the tarceData file the longitude and lattitude was wirten visa verca, So their placed were changed to save them correct.
                    csv_obj = CsvFile(int(float(log_entity.attrib["SimTime"])),
                                      abs(float(log_entity.attrib["Longitude"])),
                                      abs(float(log_entity.attrib["Latitude"])),
                                      float(log_entity.attrib["SOG"]),
                                      float(log_entity.attrib["COG"]), float(log_entity.attrib["Heading"]),
                                      float(aftthruster), float(forethruster),
                                      float(portengine), float(stbdengine),
                                      float(portrudder), float(stbdrudder))
                    self.log_objects.append(csv_obj)
                    if (self.scenario == "emergency" and i == 1800) or (
                            self.scenario in ["pushing", "leeway"] and i == 900):
                        break
                    else:
                        i += 1
        # Either the log file was empty or we haven't received any network data yet
        if not self.log_objects:
            messagebox.askokcancel(title="No Data!",
                                   message="There is no data to use for assistance! Is the simulator running? Was the logfile valid?")

            return

        # with open('E96_ScL_R1_interpolatedLog.csv', newline='') as myFile:
        #     logrowsoperator = CsvRowsOperator()
        #     log_objects = logrowsoperator.read_file(myFile)

        instant_second = self.log_objects[-1].simtime  # this line get the last second when the user needs an assist
        if instant_second < 180:
            self.logger.info(f"Assistance occurred at: {instant_second} seconds which is too soon!(Not recommended)")
            answer = messagebox.askokcancel(title="Proceed OR Quit",
                                            message="getting Assistance at a early time is not recommended! Do you still want to get help?")
        if (instant_second < 180 and answer) or instant_second > 180:
            self.generate_csv_file(self.log_objects)  # this will generate a csv file based on DataTrace file
            self.features = Features(self.log_objects, self.scenario, self.logger,
                                     instant_second)  # this line will create the features at the time of asking asssistance

            # filling the own vessel properties attributes
            self.scale_speed.set(self.features.speed[1])
            self.scale_heading.set(int(self.features.heading[1]))
            self.scale_ice_load.set(10)
            self.scale_distance_target.set(round(self.features.distance_from_target, 4))
            # self.entry_aspect.insert(0, self.features.aspect)
            # self.entry_area_focus.insert(0, self.features.area_of_focus)
            # self.entry_orientation_target.insert(0, self.features.orientation)
            # self.entry_technique.insert(0, self.features.maneuver)
            # self.entry_heading.insert(0, self.features.heading[0])

            # this is just for capturing the snapshot of the DSS for fatemes's thesis. Example
            # self.scale_speed.set(1.5)
            # self.scale_heading.set(77)
            # self.scale_ice_load.set(0)
            # self.scale_distance_target.set(66)
            # self.entry_aspect.insert(0,"Up_Current")
            # self.entry_area_focus.insert(0, "AV")
            # self.entry_orientation_target.insert(0, "Stern")
            # self.entry_technique.insert(0, "L + PW")
            # self.entry_heading.insert(0, "Angle")

            '''creating passing the feature_array to the classifier for classification'''
            feature_array = feature_array_convertor(True, self.features.speed[1],
                                                    int(self.scale_distance_target.get()), self.features.heading[1],
                                                    self.features.aspect, self.features.area_of_focus,
                                                    self.features.orientation, self.features.maneuver)

            suggested_case, case_ID, case_name, suggested_technique = self.decision_tree_classifier(feature_array,
                                                                                                    self.scenario)

            suggested_approach_dict = feature_array_convertor(False, suggested_case[0], suggested_case[1],
                                                         suggested_case[2], suggested_case[4],
                                                         suggested_case[5],
                                                         suggested_case[6],
                                                         suggested_technique)
            # filling the suggested ownship status variables
            self.suggested_speed.config(text=suggested_approach_dict["speed"])
            self.suggested_heading.config(text=suggested_approach_dict["heading"])
            self.suggested_area_focus.config(text=suggested_approach_dict["area_of_focus"])
            self.suggested_aspect.config(text=suggested_approach_dict["aspect"])
            self.suggested_orientation.config(text=suggested_approach_dict["orientation"])
            self.suggested_distance_target.config(text=suggested_approach_dict["distance"])
            self.suggested_maneuver.config(text=suggested_technique)

            print(f"this is the name for that specific case{case_ID}")
            self.load_image(case_ID)

    def load_image(self, case_ID):

        current_path = os.getcwd()
        cases_name = pd.read_excel(
            current_path + "/Training_DataSet/" + self.scenario + "/" + self.scenario + "_class_Name.xls")
        np.array(cases_name)
        case_name = cases_name.values[case_ID][0]
        print(f"this is the number of the predicted  case  {case_name}")
        try:
            suggested_image = Image.open(
                current_path + "/images/output_images/" + self.scenario + "/" + case_name + ".png")
            resized_suggested_image = suggested_image.resize((354, 369), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(resized_suggested_image)
            self.suggested_image_id = self.canvas.create_image(352.5, 360, anchor="se", image=img)
        except:
            self.logger.info("couldn't find such a file")
        self.root.mainloop()

    def more_info(self):
        messagebox.showinfo(title="information",
                            message="1. Create a direct route to get close ahead of the FPSO (speed under 3 knots. If the FPSO was on fire choose 5 knots)\n\n 2. Position the support vessel as a block (heading=60 degrees, distance=100m above the FPSO, and position the vessel's bow far enough towards the bowline/centerline of the FPSO to avoid the ice come between the vessels). let some ice flow and then give some prop-wash flushing at the same time.\n\n 3. Once the zone is clearing from the ice, move from DP2 (leeway) to DP3 (broadside pushing). (position to the North with distance=100m)\n\n 4. Thrust to the west, try to clear out the zone, then go back and forth to make a couple of thrust passes (The range for the broadside pushing depends on the situation, but try to clear the area closer to the FPSO in the zone).")

    def get_selected_rows(self, class_id):
        rows = []
        cases_ID = []
        current_path = os.getcwd()
        data_path = current_path + "/Training_DataSet/" + self.scenario + "_N/" + self.scenario + "_Training_withclassID.csv"
        with open(data_path, newline='', encoding="ISO-8859-1") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for line_num, row in enumerate(csv_reader):

                if row[0] == str(class_id):
                    rows.append([row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
                    cases_ID.append(line_num + 1)
        datarows = np.array(rows)
        return datarows, cases_ID

    def similarity_measure(self, selected_rows, cases_number, features_array):
        res = pairwise_distances_argmin_min(selected_rows, features_array, metric='cosine')
        min_dist_value = min(np.ndarray.tolist(res[1]))
        min_index = np.ndarray.tolist(res[1]).index(min_dist_value)
        return selected_rows[min_index], cases_number[min_index]

    def decision_tree_classifier(self, features_array, scenario):
        print(features_array)
        current_path = os.getcwd()
        case_techniques = pd.read_excel(
            current_path + "/Training_DataSet/" + self.scenario + "_N" + "/" + self.scenario + "_techniques.xls")
        case_techniques = case_techniques.to_numpy()

        case_names = pd.read_excel(
            current_path + "/Training_DataSet/" + self.scenario + "_N" + "/" + self.scenario + "_className.xls")
        case_names = case_names.to_numpy()

        df_x_train = pd.read_excel(
            current_path + "/Training_DataSet/" + self.scenario + "_N" + "/" + self.scenario + "_Training.xls")
        x_train = np.array(df_x_train.astype(float))
        df_y_train = pd.read_excel(
            current_path + "/Training_DataSet/" + self.scenario + "_N" + "/" + self.scenario + "_ID.xls")
        if scenario == "emergency":
            max_depth = 4
        else:
            max_depth = 3
        clf = tree.DecisionTreeClassifier(random_state=42, max_depth=max_depth)

        clf.fit(x_train, df_y_train)
        class_id = clf.predict(features_array)
        selected_rows, cases_ID = self.get_selected_rows(int(class_id[0]))
        output_array, case_ID = self.similarity_measure(selected_rows, cases_ID, features_array)
        print(f"this is case ID for out put case{case_ID}")
        return output_array, case_ID, case_names[case_ID][0], case_techniques[case_ID][0]

    def reset_properties(self):
        # Resetting ownship status
        self.scale_speed.set(0)
        self.scale_heading.set(0)
        self.scale_ice_load.set(0)
        self.scale_distance_target.set(0)
        # self.entry_aspect.delete(0, 100)
        # self.entry_area_focus.delete(0, 100)
        # self.entry_orientation_target.delete(0, 100)
        # self.entry_technique.delete(0, 100)
        # self.entry_heading.delete(0, 100)

        # Resetting suggested approach attributes
        self.suggested_speed.config(text="")
        # self.suggested_area_focus.config(text="")
        # self.suggested_aspect.config(text="")
        self.suggested_distance_target.config(text="")
        self.suggested_heading.config(text="")
        # self.suggested_maneuver.config(text="")
        # self.suggested_orientation.config(text="")

        # Resetting output_image
        self.canvas.delete(self.suggested_image_id)

    def init_page(self):
        container = tk.Frame(self.root, width=self.main_frame_width * 0.94, height=self.main_frame_height * 0.67,
                             bg="white")
        container.config(borderwidth=6, relief="groove")
        container.place(relx=0.5, rely=0.6, anchor="center")

        own_vessel_frame = tk.Frame(container, bg="white", width=self.main_frame_width * 0.32,
                                    height=self.main_frame_height * 0.61)
        own_vessel_frame.config(borderwidth=3, relief="groove", padx=3, pady=3)
        own_vessel_frame.place(relx=0.2, rely=0.5, anchor="center")
        own_vessel_lbl = tk.Label(own_vessel_frame, text="Ownship Properties")
        own_vessel_lbl.place(relx=0.2, rely=-0.001, anchor="center")

        suggested_status_frame = tk.Frame(container, bg="white", width=self.main_frame_width * 0.22,
                                          height=self.main_frame_height * 0.61)
        suggested_status_frame.config(borderwidth=3, relief="groove", padx=25, pady=25)
        suggested_status_frame.place(relx=0.5, rely=0.5, anchor="center")
        suggested_own_ship_status_lbl = tk.Label(suggested_status_frame, text="Suggested Solution", bg="white")
        suggested_own_ship_status_lbl.place(relx=0.3, rely=0, anchor="center")

        suggested_approach_frame = tk.Frame(container, bg="white", width=self.main_frame_width * 0.32,
                                            height=self.main_frame_height * 0.61)
        suggested_approach_frame.config(borderwidth=3, relief="groove", padx=3, pady=3)
        suggested_approach_frame.place(relx=0.8, rely=0.5, anchor="center")
        suggested_approach_lbl = tk.Label(suggested_approach_frame, text="Suggested Approach", bg="white")
        suggested_approach_lbl.place(relx=0.2, rely=-0.001, anchor="center")

        ####### create the widgets for the own vessel properties frame ######

        scale_speed = tk.Label(own_vessel_frame, text="Vessel Speed", font=("helvetica", 12, "bold"))
        scale_speed.place(relx=0.1, rely=0.08, anchor="center")
        self.scale_speed = tk.Scale(own_vessel_frame, from_=0, to=10.0, resolution=0.01, orient="horizontal")
        self.scale_speed.config(length=240, tickinterval=0.001)
        self.scale_speed.place(relx=0.6, rely=0.06, anchor="center")

        scale_heading = tk.Label(own_vessel_frame, text="Vessel Heading", font=("helvetica", 12, "bold"))
        scale_heading.place(relx=0.11, rely=0.18, anchor="center")
        self.scale_heading = tk.Scale(own_vessel_frame, from_=0, to=500, resolution=0.01, orient="horizontal")
        self.scale_heading.config(length=240)
        self.scale_heading.place(relx=0.6, rely=0.16, anchor="center")

        # lbl_head = tk.Label(own_vessel_frame, text="Heading status", font=("helvetica", 12, "bold"))
        # lbl_head.place(relx=0.1, rely=0.88, anchor="center")
        # self.entry_heading = tk.Entry(own_vessel_frame)
        # self.entry_heading.place(relx=0.60, rely=0.88, anchor="center")
        # self.entry_heading.config(width=26, justify="center", relief="groove")

        scale_ice_load = tk.Label(own_vessel_frame, text="Ice Load", font=("helvetica", 12, "bold"))
        scale_ice_load.place(relx=0.06, rely=0.28, anchor="center")
        self.scale_ice_load = tk.Scale(own_vessel_frame, from_=0, to=500, orient="horizontal")
        self.scale_ice_load.config(length=240)
        self.scale_ice_load.place(relx=0.6, rely=0.26, anchor="center")

        scale_distance_target = tk.Label(own_vessel_frame, text="Distance from Target(m)",
                                         font=("helvetica", 12, "bold"))
        scale_distance_target.place(relx=0.15, rely=0.38, anchor="center")
        self.scale_distance_target = tk.Scale(own_vessel_frame, from_=0, to=300, resolution=0.01,
                                              orient="horizontal")
        self.scale_distance_target.config(length=240)
        self.scale_distance_target.place(relx=0.6, rely=0.36, anchor="center")

        # lbl_aspect = tk.Label(own_vessel_frame, text="Aspect", font=("helvetica", 12, "bold"))
        # lbl_aspect.place(relx=0.06, rely=0.48, anchor="center")
        # self.entry_aspect = tk.Entry(own_vessel_frame)
        # self.entry_aspect.place(relx=0.60, rely=0.48, anchor="center")
        # self.entry_aspect.config(width=26, justify="center", relief="groove")

        # lbl_area_focus = tk.Label(own_vessel_frame, text="Area of Focus", font=("helvetica", 12, "bold"))
        # lbl_area_focus.place(relx=0.1, rely=0.58, anchor="center")
        # self.entry_area_focus = tk.Entry(own_vessel_frame)
        # self.entry_area_focus.place(relx=0.60, rely=0.58, anchor="center")
        # self.entry_area_focus.config(width=26, justify="center", relief="groove")

        # lbl_orientation = tk.Label(own_vessel_frame, text="Orientation to Target", font=("helvetica", 12, "bold"))
        # lbl_orientation.place(relx=0.13, rely=0.68, anchor="center")
        # self.entry_orientation_target = tk.Entry(own_vessel_frame)
        # self.entry_orientation_target.place(relx=0.60, rely=0.68, anchor="center")
        # self.entry_orientation_target.config(width=26, justify="center", relief="groove")

        # lbl_technique = tk.Label(own_vessel_frame, text="Technique", font=("helvetica", 12, "bold"))
        # lbl_technique.place(relx=0.07, rely=0.78, anchor="center")
        # self.entry_technique = tk.Entry(own_vessel_frame)
        # self.entry_technique.place(relx=0.60, rely=0.78, anchor="center")
        # self.entry_technique.config(width=26, justify="center", relief="groove")

        ####### create the widgets for the suggested own ship status  ######

        speed_lbl = tk.Label(suggested_status_frame, text="Vessel Speed", font=("helvetica", 12, "bold"),
                             justify="left")
        speed_lbl.place(relx=0.1, rely=0.12, anchor="center")

        self.suggested_speed = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                        justify="left")
        self.suggested_speed.place(relx=0.75, rely=0.12, anchor="center")

        heading_lbl = tk.Label(suggested_status_frame, text="Vessel Heading", font=("helvetica", 12, "bold"),
                               justify="left")
        heading_lbl.place(relx=0.1, rely=0.23, anchor="center")
        self.suggested_heading = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                          justify="left")
        self.suggested_heading.place(relx=0.75, rely=0.23, anchor="center")

        area_focus_lbl = tk.Label(suggested_status_frame, text="Area of Focus", font=("helvetica", 12, "bold"),
                                  justify="left")
        area_focus_lbl.place(relx=0.09, rely=0.32, anchor="center")
        self.suggested_area_focus = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                             justify="left")
        self.suggested_area_focus.place(relx=0.75, rely=0.32, anchor="center")

        aspect_lbl = tk.Label(suggested_status_frame, text="Aspect", font=("helvetica", 12, "bold"),
                              justify="left")
        aspect_lbl.place(relx=0.02, rely=0.42, anchor="center")
        self.suggested_aspect = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                         justify="left")
        self.suggested_aspect.place(relx=0.75, rely=0.42, anchor="center")

        oriantation_target_lbl = tk.Label(suggested_status_frame, text="Orientation to Target",
                                          font=("helvetica", 12, "bold"), justify="left")
        oriantation_target_lbl.place(relx=0.14, rely=0.52, anchor="center")
        self.suggested_orientation = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                              justify="left")
        self.suggested_orientation.place(relx=0.75, rely=0.52, anchor="center")

        distance_target_lbl = tk.Label(suggested_status_frame, text="Distance from Target",
                                       font=("helvetica", 12, "bold"),
                                       justify="left")
        distance_target_lbl.place(relx=0.14, rely=0.62, anchor="center")
        self.suggested_distance_target = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                                  justify="left")
        self.suggested_distance_target.place(relx=0.75, rely=0.62, anchor="center")

        maneuver_lbl = tk.Label(suggested_status_frame, text="Maneuver", font=("helvetica", 12, "bold"),
                                justify="left")
        maneuver_lbl.place(relx=0.04, rely=0.72, anchor="center")
        self.suggested_maneuver = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                           justify="left")
        self.suggested_maneuver.place(relx=0.75, rely=0.72, anchor="center")

        ####### creat the canvas for the suggested approach section  #######
        assist_btn = tk.Button(suggested_approach_frame, text="Assist", bg="green", width=32, height=2, anchor="c",
                               command=self.assist)
        # now, when the features object created filling the pushing scenario variables("suggested own ship status") can be done.
        assist_btn.config(relief="groove", font=("helvetica", 12, "bold"), fg="green")
        assist_btn.place(relx=.5, rely=.95, anchor="center")

        reset_vessel_properties_btn = tk.Button(own_vessel_frame, text="RESET", relief="groove",
                                                font=("helvetica", 12, "bold"), fg="red", width=32, height=2,
                                                command=self.reset_properties)
        reset_vessel_properties_btn.place(relx=.5, rely=.95, anchor="center")
        # go_back_button = tk.Button(self.root, text="Back To Main Menue", width=20, height=3, anchor="c",
        #                            command=self.get_back,
        #                            bg="gray")
        # go_back_button.place(relx=0.5, rely=0.05, anchor="center")

        more_info_btn = tk.Button(suggested_status_frame, text="More Info!", bg="green", width=32, height=2, anchor="c",
                                  command=self.more_info)
        more_info_btn.config(relief="groove", font=("helvetica", 12, "bold"), fg="green")
        more_info_btn.place(relx=.5, rely=.99, anchor="center")

        self.canvas = tk.Canvas(suggested_approach_frame, bg='#000000')

        suggested_approach_frame.winfo_screenwidth()

        self.canvas.place(relx=0.5, rely=0.5, width=self.main_frame_width * 0.25,
                          height=self.main_frame_height * 0.4,
                          anchor="center")

        # The labels for suggested own ship attributes description!
        img = ImageTk.PhotoImage(Image.open("images/MoreInfo.png"))
        img_desc = ImageTk.PhotoImage(Image.open("images/Emergency_desc.png"))
        speed_moreinfo = tk.Label(suggested_status_frame, image=img)
        speed_moreinfo.image = img
        speed_moreinfo.place(relx=0.28, rely=0.115, anchor="center")
        HoverText(speed_moreinfo, "This is a sample hover text")

        heading_moreinfo = tk.Label(suggested_status_frame, image=img)
        heading_moreinfo.image = img
        heading_moreinfo.place(relx=0.305, rely=0.225, anchor="center")
        HoverText(heading_moreinfo, "This is a sample hover text")

        area_of_focus_moreinfo = tk.Label(suggested_status_frame, image=img)
        area_of_focus_moreinfo.image = img
        area_of_focus_moreinfo.place(relx=0.28, rely=0.315, anchor="center")
        HoverText(area_of_focus_moreinfo,
                  "Where seafarer is focusing most of the ice clearing time!\nAZ: Above Zone\nAV: Above Vessel or Target\nZ: In Zone")

        aspect_moreinfo = tk.Label(suggested_status_frame, image=img)
        aspect_moreinfo.image = img
        aspect_moreinfo.place(relx=0.14, rely=0.415, anchor="center")
        HoverText(aspect_moreinfo, "This is a sample hover text")

        orientation_moreinfo = tk.Label(suggested_status_frame, image=img)
        orientation_moreinfo.image = img
        orientation_moreinfo.place(relx=0.41, rely=0.515, anchor="center")
        HoverText(orientation_moreinfo, "This is a sample hover text")

        distance_moreinfo = tk.Label(suggested_status_frame, image=img)
        distance_moreinfo.image = img
        distance_moreinfo.place(relx=0.41, rely=0.615, anchor="center")
        HoverText(distance_moreinfo, "This is a sample hover text")

        manouver_moreinfo = tk.Label(suggested_status_frame, image=img)
        manouver_moreinfo.image = img
        manouver_moreinfo.place(relx=0.19, rely=0.715, anchor="center")
        HoverText(manouver_moreinfo, "This is a sample hover text")

        self.canvas.create_image(352.5, 360, anchor="se", image=img_desc)
        self.root.mainloop()

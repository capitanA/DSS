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
import threading
from helper import speed_warning

from helper import Decorator
import ipdb

engine_dic = {"pEngine": 0, "fTunnelThruster": 0, "sEngine": 0, "aTunnelThruster": 0}
rudder_dic = {"pRudder": 0, "sRudder": 0}


class PlayScenario:

    def __init__(self, root, main_frame, scenario, excep_logger, User_logger, isRealTime):
        self.root = root
        self.main_frame = main_frame
        self.scenario = scenario
        self.logger = excep_logger
        self.user_logger = User_logger
        self.main_frame_width = self.main_frame.winfo_width()
        self.main_frame_height = self.main_frame.winfo_height()
        self.features = None
        self.log_objects = []
        self.isRealTime = isRealTime
        self.suggested_image_id = None
        self.general_Instruction_lbl_text = None
        self.specific_Instruction_lbl_text = None
        self.spd_wrn_lbl = tk.Label(self.main_frame, text="Your speed is greater than 3 Knot. be cautious!")
        self.top_window = None
        self.username = None

        if isRealTime:
            self.simReceiver = SimReceiver(self)
            # Speed_warning_thread = threading.Thread(target=speed_warning, args=(self.log_objects, self.main_frame,))
            # Speed_warning_thread.start()

        # self.suggested_speed = None
        # self.suggested_heading = None
        # self.suggested_area_focus = None
        # self.suggested_aspect = None
        # self.suggested_orientation = None
        # self.suggested_distance_target = None
        # self.suggested_maneuver = None

    def addLogLine(self, csvLine):
        self.log_objects.append(csvLine)
        ##### this line of code will check the speed if it is mor than 3 then a warning will shows in the DSS! #####
        if self.log_objects[-1].sog > 3:
            self.spd_wrn_lbl.place(relx=0.85, rely=0.15, anchor="center", font="helvetica 15 bold")
        elif self.spd_wrn_lbl.winfo_exists():
            self.spd_wrn_lbl.place_forget()

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
        global content
        # global case_name
        if self.top_window.winfo_exists():
            messagebox.showinfo(message="please first enter your name!")
        else:
            if self.suggested_maneuver.cget("text") != "N/A":
                self.user_logger.info("User reset the DSS successfully!")
                # self.scale_speed.set(0)
                # self.scale_heading_avg.set(0)
                # self.scale_instant_heading.set(0)
                # self.scale_ice_load.set(0)
                # self.scale_distance_target_avg.set(0)
                # self.scale_instant_distance.set(0)
                # self.scale_instant_speed.set(0)

                # Resetting suggested approach attributes
                self.suggested_speed.config(text="")
                self.suggested_distance_target.config(text="")
                self.suggested_heading.config(text="")

                self.suggested_area_focus.config(text="")
                self.suggested_aspect.config(text="")
                self.suggested_maneuver.config(text="")
                self.suggested_orientation.config(text="")

                # Resetting output image
                if self.suggested_image_id:
                    self.canvas.delete(self.suggested_image_id)

            if not self.isRealTime:
                self.log_objects = []  # if the DSS is recieving data from simulator, Every time it needs to nake the log object list empty
                i = 0
                well_formed_filename = self.log_reader()

                try:
                    xml_file = ET.parse(well_formed_filename).getroot()
                except IOError:
                    # except FileNotFoundError as fnf_error:
                    self.logger.info(
                        "The well_formed_TraceData.log cannot be parsed! it seems there is no such a file!")

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
            if self.log_objects[0].simtime == 0 and self.log_objects[1].simtime == 0:
                self.log_objects.pop(0)

            if instant_second < 180:
                self.logger.info(
                    f"Assistance occurred at: {instant_second} seconds which is too soon!(Not recommended)")
                answer = messagebox.askokcancel(title="Proceed OR Quit",
                                                message="It is too soon for getting assistance which is not recommended! Do you still want to get help?")
            if (instant_second < 180 and answer) or instant_second > 180:
                self.generate_csv_file(
                    self.log_objects)  # This will generate a csv file based on self.log_objects list.
                self.features = Features(self.log_objects, self.scenario, self.logger,
                                         instant_second)  # This line will create the features once the user asks asssistance

                # filling the own vessel properties attributes
                # self.scale_speed.set(self.features.speed[1])
                # self.scale_instant_speed.set(self.features.speed[2])
                # self.scale_heading_avg.set(self.features.heading[1])
                # self.scale_instant_heading.set(self.features.heading[2])
                # self.scale_ice_load.set(10)
                # self.scale_distance_target_avg.set(round(self.features.distance_from_target[0], 4))
                # self.scale_instant_distance.set(round(self.features.distance_from_target[1], 4))

                '''creating and passing the feature_array to the classifier for classification'''
                feature_array = feature_array_convertor(True, self.features.speed[1],
                                                        int(self.features.distance_from_target[0]),
                                                        self.features.heading[1],
                                                        self.features.aspect, self.features.area_of_focus,
                                                        self.features.orientation, self.features.maneuver)

                # feature_array = feature_array_convertor(True, self.features.speed[1],
                #                                         int(self.scale_distance_target.get()), self.features.heading[1],
                #                                         self.features.aspect, self.features.area_of_focus,
                #                                         self.features.orientation, self.features.maneuver)

                suggested_case, case_ID, case_name, suggested_technique = self.decision_tree_classifier(feature_array,
                                                                                                        self.scenario)

                self.user_logger.info(
                    f"User {self.username} requested assistance at time={instant_second}s in the {self.scenario} scenario and the suggested approach was case {case_name}")

                suggested_approach_dict = feature_array_convertor(False, suggested_case[0], suggested_case[1],
                                                                  suggested_case[2], suggested_case[4],
                                                                  suggested_case[5],
                                                                  suggested_case[6],
                                                                  suggested_technique)
                # filling the suggested ownship status variables
                self.suggested_speed.config(text=suggested_approach_dict["speed"])
                self.suggested_heading.config(text=suggested_approach_dict["heading"])
                if suggested_approach_dict["area_of_focus"] == "av":
                    area_of_focus = "Above Vessel"

                elif suggested_approach_dict["area_of_focus"] == "z":
                    area_of_focus = "Zone"

                elif suggested_approach_dict["area_of_focus"] == "az":
                    area_of_focus = "Above Zone"
                elif suggested_approach_dict["area_of_focus"] == "along_zone":
                    area_of_focus = "Along_Zone"
                else:
                    area_of_focus = "Unknown"

                self.suggested_area_focus.config(text=area_of_focus)
                self.suggested_aspect.config(text=suggested_approach_dict["aspect"])
                self.suggested_orientation.config(text=suggested_approach_dict["orientation"])
                self.suggested_distance_target.config(text=suggested_approach_dict["distance"])
                self.suggested_maneuver.config(text=suggested_technique)

                ##### show the general instruction.
                self.general_Instruction_lbl_text.place(relx=0.5, rely=0.5, anchor="center")

                #######find the description file for the predicted case and show up the information to the user
                try:
                    more_info_file = open(f"description_files/{self.scenario}/{case_name}.txt", mode="r")
                    # not_recomended_cases = open(f"NotRecommendedCases_{self.scenario }.txt", mode="r")
                    # not_recomended_cases = not_recomended_cases.read()
                    more_info_content = more_info_file.read()
                    # if case_name in not_recomended_cases.split("\n"):

                    # self.specific_Instruction_lbl_text.config(font=('Helvetica 13 bold'),
                    #                                           text=f"There is no specific instruction for this approach.\n Note: If you think this in not actually an effective approach,\n change your current settings and ask for an assistance again.")
                    # self.specific_Instruction_lbl_text.config(wraplength=350, font=('Helvetica 13 bold'),
                    #                                           text=f"There is no specific instruction for this approach. Note: If you think this in not actually an effective approach, change your current settings and ask for an assistance again.")
                    self.specific_Instruction_lbl_text.config(wraplength=480, font=('Helvetica 13 bold'),
                                                              text=more_info_content)


                except:
                    # self.specific_Instruction_lbl_text.config(font=('Helvetica 13 bold'),
                    #                                           text=f"There is no specific instruction for this approach.\n Note: If you think this in not actually an effective approach,\n change your current settings and ask for an assistance again.")
                    self.specific_Instruction_lbl_text.config(wraplength=480, font=('Helvetica 13 bold'),
                                                              text=f"There is no specific instruction for this approach.\nNote: If you think this in not actually an effective approach, change your current settings and ask for an assistance again.")
                    self.logger.info(f"The description file with the name {case_name} couldn't be opened")

                ##### This  line will show the general information for the predicted approach
                if self.scenario == "emergency":
                    self.general_Instruction_lbl_text.config(font=('Helvetica 13 bold'),
                                                             text="1.If possible, adjust your heading for your final goal before you\n get to the ice edge.It’s much easier to turn in open water than in the ice.\n2. Approach the ice edge at a slow speed. \n3. Position the vessel close enough to the target to prevent the ice from \nflowing between your vessel and the target. \n4. If you want to use the leeway technique, get the stern or the bow \nfurther down to the south so the ice can flow out around the stern or bow\nof the vessel (don’t use perpendicular heading, use some angle instead).\n5. Don’t work in the zone, because the current will clear that ice.Focus\non the ice above the zone or vessel.")
                elif self.scenario == "leeway":
                    self.general_Instruction_lbl_text.config(font=('Helvetica 13 bold'),
                                                             text="1. Position the vessel close enough to the target to prevent \nthe ice from flowing between your vessel and the target.\n2. If you want to use the leeway technique, get the stern\n or the bow further down to the south so the ice can flow\n out around the stern or bow of the vessel (don’t use perpendicular\n heading, use some angle instead)\n3. Don’t work in the zone, because the current will clear that ice. Focus\n on the ice above the zone or vessel.")
                elif self.scenario == "pushing":
                    self.general_Instruction_lbl_text.config(font=('Helvetica 13 bold'),
                                                             text="1. Work upstream (above zone). Focusing a lot on clearing\n downstream (below the platform) is a waste of time because\n the current will clear that ice.")
                self.load_image(case_ID, case_name)

    def load_image(self, case_ID, case_name):

        current_path = os.getcwd()
        # cases_name = pd.read_excel(
        #     current_path + "/Training_DataSet/" + self.scenario +"_N2"+ "/" + self.scenario + "_className.xls")
        # np.array(cases_name)
        # name = cases_name.values[case_ID][0]
        print(f"this is the name of the predicted case{case_name} for {self.scenario} scenario")
        try:
            suggested_image = Image.open(
                current_path + "/images/output_images/" + self.scenario + "/" + case_name + ".png")
            resized_suggested_image = suggested_image.resize((354, 369), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(resized_suggested_image)
            self.suggested_image_id = self.canvas.create_image(352.5, 360, anchor="se", image=img)
        except:
            self.logger.info(f"The image with the name {case_name} couldn't be found")
        self.root.mainloop()

    # def more_info(self):
    #     try:
    #         more_inf_file = open(f"description_files/{self.scenario}/{case_name}.txt", mode="r")
    #         content = more_inf_file.read()
    #         messagebox.showinfo(title="information",
    #                             message=content)
    #     except:
    #         messagebox.showinfo(title="information",
    #                             message="There is no more information for this case yet!")
    #         self.logger.info(f"The description file with the name {case_name} couldn't be opened")

    def get_selected_rows(self, class_id):
        rows = []
        cases_ID = []
        current_path = os.getcwd()
        data_path = current_path + "/Training_DataSet/" + self.scenario + "_N2/" + self.scenario + "_Training_withclassID.csv"
        with open(data_path, newline='', encoding="ISO-8859-1") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',', quotechar='|')
            for line_num, row in enumerate(csv_reader):

                if row[0] == str(class_id):
                    rows.append([row[1], row[2], row[3], row[4], row[5], row[6], row[7]])
                    cases_ID.append(line_num + 1)
        datarows = np.array(rows)
        return datarows, cases_ID

    def similarity_measure(self, selected_rows, cases_number, features_array):
        res = pairwise_distances_argmin_min(selected_rows, features_array, metric='euclidean')
        min_dist_value = min(np.ndarray.tolist(res[1]))
        min_index = np.ndarray.tolist(res[1]).index(min_dist_value)
        return selected_rows[min_index], cases_number[min_index]

    def decision_tree_classifier(self, features_array, scenario):
        current_path = os.getcwd()
        case_techniques = pd.read_excel(
            current_path + "/Training_DataSet/" + self.scenario + "_N2" + "/" + self.scenario + "_techniques.xls")
        case_techniques = case_techniques.to_numpy()

        case_names = pd.read_excel(
            current_path + "/Training_DataSet/" + self.scenario + "_N2" + "/" + self.scenario + "_className.xls")
        case_names = case_names.to_numpy()

        df_x_train = pd.read_excel(
            current_path + "/Training_DataSet/" + self.scenario + "_N2" + "/" + self.scenario + "_Training.xls")
        x_train = np.array(df_x_train.astype(float))
        df_y_train = pd.read_excel(
            current_path + "/Training_DataSet/" + self.scenario + "_N2" + "/" + self.scenario + "_ID.xls")
        if scenario == "leeway":
            max_depth = 3
        else:
            max_depth = 4
        clf = tree.DecisionTreeClassifier(random_state=0, max_depth=max_depth)

        clf.fit(x_train, df_y_train)
        class_id = clf.predict(features_array)

        selected_rows, cases_ID = self.get_selected_rows(int(class_id[0]))
        output_array, case_ID = self.similarity_measure(selected_rows, cases_ID, features_array)
        print(f" This is case ID for out put case{case_ID}")
        return output_array, case_ID, case_names[case_ID - 2][0], case_techniques[case_ID - 2][0]

    def reset_properties(self):
        # Resetting ownship status
        self.user_logger.info("the DSS reset successfully!")
        # these were for resetting the own ship status
        # self.scale_speed.set(0)
        # self.scale_heading_avg.set(0)
        # self.scale_instant_heading.set(0)
        # self.scale_ice_load.set(0)
        # self.scale_distance_target_avg.set(0)
        # self.scale_instant_distance.set(0)
        # self.scale_instant_speed.set(0)

        # self.entry_aspect.delete(0, 100)
        # self.entry_area_focus.delete(0, 100)
        # self.entry_orientation_target.delete(0, 100)
        # self.entry_technique.delete(0, 100)
        # self.entry_heading.delete(0, 100)

        # Resetting suggested approach attributes
        self.suggested_speed.config(text="")
        self.suggested_distance_target.config(text="")
        self.suggested_heading.config(text="")

        self.suggested_area_focus.config(text="")
        self.suggested_aspect.config(text="")
        self.suggested_maneuver.config(text="")
        self.suggested_orientation.config(text="")

        # Resetting output_image
        if self.suggested_image_id:
            self.canvas.delete(self.suggested_image_id)

    def clean_up(self):
        self.username = self.entry_feild.get()
        self.top_window.destroy()

    def init_page(self):

        container = tk.Frame(self.root, width=self.main_frame_width * 0.94, height=self.main_frame_height * 0.67,
                             bg="white")
        container.config(borderwidth=6, relief="groove")
        container.place(relx=0.5, rely=0.6, anchor="center")

        instructions_frame = tk.Frame(container, bg="white", width=self.main_frame_width * 0.37,
                                      height=self.main_frame_height * 0.61)
        instructions_frame.config(borderwidth=3, relief="groove", padx=3, pady=3)
        instructions_frame.place(relx=0.2, rely=0.5, anchor="center")
        Instruction_lbl = tk.Label(instructions_frame, text="Instructions", font=('Helvetica 18 bold'))
        Instruction_lbl.place(relx=0.2, rely=-0, anchor="center")

        suggested_status_frame = tk.Frame(container, bg="white", width=self.main_frame_width * 0.20,
                                          height=self.main_frame_height * 0.61)
        suggested_status_frame.config(borderwidth=3, relief="groove", padx=3, pady=3)
        suggested_status_frame.place(relx=0.515, rely=0.5, anchor="center")

        suggested_own_ship_status_lbl = tk.Label(suggested_status_frame, text="Suggested Solution", bg="white",
                                                 font=('Helvetica 18 bold'))
        suggested_own_ship_status_lbl.place(relx=0.35, rely=0.001, anchor="center")

        suggested_approach_frame = tk.Frame(container, bg="white", width=self.main_frame_width * 0.32,
                                            height=self.main_frame_height * 0.61)
        suggested_approach_frame.config(borderwidth=3, relief="groove", padx=3, pady=3)
        suggested_approach_frame.place(relx=0.8, rely=0.5, anchor="center")
        suggested_approach_lbl = tk.Label(suggested_approach_frame, text="Suggested Approach", bg="white",
                                          font=('Helvetica 18 bold'))
        suggested_approach_lbl.place(relx=0.22, rely=0.001, anchor="center")

        ####### create the widgets for the own vessel properties frame ######

        general_instruction_frame = tk.Frame(instructions_frame, bg="white",
                                             width=self.main_frame_width * 0.36,
                                             height=self.main_frame_height * 0.24)
        general_instruction_frame.config(borderwidth=3, relief="groove", padx=0.03, pady=0.03)
        general_instruction_frame.place(relx=0.5, rely=0.24, anchor="center")

        specific_instruction_frame = tk.Frame(instructions_frame, bg="white",
                                              width=self.main_frame_width * 0.36,
                                              height=self.main_frame_height * 0.32)
        specific_instruction_frame.config(borderwidth=3, relief="groove", padx=0.03, pady=0.03)
        specific_instruction_frame.place(relx=0.5, rely=0.73, anchor="center")

        general_Instruction_lbl_title = tk.Label(general_instruction_frame, text="General", font=('Helvetica 15'))
        general_Instruction_lbl_title.place(relx=0.5, rely=0.01, anchor="center")

        specific_Instruction_lbl_title = tk.Label(specific_instruction_frame, text="Specific", font=('Helvetica 15'))
        specific_Instruction_lbl_title.place(relx=0.5, rely=0.01, anchor="center")

        self.general_Instruction_lbl_text = tk.Label(general_instruction_frame, justify="left",
                                                     text="There is no information yet!",
                                                     font=('Helvetica 17 bold'))

        self.general_Instruction_lbl_text.place(relx=0.5, rely=0.5, anchor="center")

        self.specific_Instruction_lbl_text = tk.Label(specific_instruction_frame, justify="left",
                                                      text="There is no information yet!",
                                                      font=('Helvetica 17 bold'))
        self.specific_Instruction_lbl_text.place(relx=0.5, rely=0.5, anchor="center")

        # scale_speed = tk.Label(instructions_frame, text=" Average Vessel Speed", font=("helvetica", 12, "bold"))
        # scale_speed.place(relx=0.15, rely=0.08, anchor="center")
        # self.scale_speed = tk.Scale(instructions_frame, from_=0, to=10.0, resolution=0.01, orient="horizontal")
        # self.scale_speed.config(length=240, tickinterval=0.001)
        # self.scale_speed.place(relx=0.6, rely=0.06, anchor="center")

        # scale_heading_avg = tk.Label(instructions_frame, text=" Average Vessel Heading", font=("helvetica", 12, "bold"))
        # scale_heading_avg.place(relx=0.16, rely=0.18, anchor="center")
        # self.scale_heading_avg = tk.Scale(instructions_frame, from_=0, to=500, resolution=0.01, orient="horizontal")
        # self.scale_heading_avg.config(length=240)
        # self.scale_heading_avg.place(relx=0.6, rely=0.16, anchor="center")

        # lbl_head = tk.Label(instructions_frame, text="Heading status", font=("helvetica", 12, "bold"))
        # lbl_head.place(relx=0.1, rely=0.88, anchor="center")
        # self.entry_heading = tk.Entry(instructions_frame)
        # self.entry_heading.place(relx=0.60, rely=0.88, anchor="center")
        # self.entry_heading.config(width=26, justify="center", relief="groove")

        # scale_distance_target_avg = tk.Label(instructions_frame, text="Average Distance(m)",
        #                                      font=("helvetica", 12, "bold"))
        # scale_distance_target_avg.place(relx=0.14, rely=0.28, anchor="center")
        # self.scale_distance_target_avg = tk.Scale(instructions_frame, from_=0, to=500, resolution=0.01,
        #                                           orient="horizontal")
        # self.scale_distance_target_avg.config(length=240)
        # self.scale_distance_target_avg.place(relx=0.6, rely=0.26, anchor="center")

        # scale_ice_load = tk.Label(instructions_frame, text="Ice Load", font=("helvetica", 12, "bold"))
        # scale_ice_load.place(relx=0.06, rely=0.38, anchor="center")
        # self.scale_ice_load = tk.Scale(instructions_frame, from_=0, to=500, orient="horizontal")
        # self.scale_ice_load.config(length=240)
        # self.scale_ice_load.place(relx=0.6, rely=0.36, anchor="center")

        # scale_instant_speed = tk.Label(instructions_frame, text="Instant Vessel Speed", font=("helvetica", 12, "bold"))
        # scale_instant_speed.place(relx=0.13, rely=0.48, anchor="center")
        # self.scale_instant_speed = tk.Scale(instructions_frame, from_=0, to=10.0, resolution=0.01, orient="horizontal")
        # self.scale_instant_speed.config(length=240, tickinterval=0.001)
        # self.scale_instant_speed.place(relx=0.6, rely=0.46, anchor="center")

        # scale_instant_heading = tk.Label(instructions_frame, text="Instant Vessel Heading",
        #                                  font=("helvetica", 12, "bold"))
        # scale_instant_heading.place(relx=0.15, rely=0.58, anchor="center")
        # self.scale_instant_heading = tk.Scale(instructions_frame, from_=0, to=500.0, resolution=0.01, orient="horizontal")
        # self.scale_instant_heading.config(length=240, tickinterval=0.001)
        # self.scale_instant_heading.place(relx=0.6, rely=0.56, anchor="center")

        # scale_instant_distance = tk.Label(instructions_frame, text="Instant Distance",
        #                                   font=("helvetica", 12, "bold"))
        # scale_instant_distance.place(relx=0.11, rely=0.68, anchor="center")
        # self.scale_instant_distance = tk.Scale(instructions_frame, from_=0, to=500.0, resolution=0.01,
        #                                        orient="horizontal")
        # self.scale_instant_distance.config(length=240, tickinterval=0.001)
        # self.scale_instant_distance.place(relx=0.6, rely=0.66, anchor="center")

        # lbl_aspect = tk.Label(instructions_frame, text="Aspect", font=("helvetica", 12, "bold"))
        # lbl_aspect.place(relx=0.06, rely=0.48, anchor="center")
        # self.entry_aspect = tk.Entry(instructions_frame)
        # self.entry_aspect.place(relx=0.60, rely=0.48, anchor="center")
        # self.entry_aspect.config(width=26, justify="center", relief="groove")

        # lbl_area_focus = tk.Label(instructions_frame, text="Area of Focus", font=("helvetica", 12, "bold"))
        # lbl_area_focus.place(relx=0.1, rely=0.58, anchor="center")
        # self.entry_area_focus = tk.Entry(instructions_frame)
        # self.entry_area_focus.place(relx=0.60, rely=0.58, anchor="center")
        # self.entry_area_focus.config(width=26, justify="center", relief="groove")

        # lbl_orientation = tk.Label(instructions_frame, text="Orientation to Target", font=("helvetica", 12, "bold"))
        # lbl_orientation.place(relx=0.13, rely=0.68, anchor="center")
        # self.entry_orientation_target = tk.Entry(instructions_frame)
        # self.entry_orientation_target.place(relx=0.60, rely=0.68, anchor="center")
        # self.entry_orientation_target.config(width=26, justify="center", relief="groove")

        # lbl_technique = tk.Label(instructions_frame, text="Technique", font=("helvetica", 12, "bold"))
        # lbl_technique.place(relx=0.07, rely=0.78, anchor="center")
        # self.entry_technique = tk.Entry(instructions_frame)
        # self.entry_technique.place(relx=0.60, rely=0.78, anchor="center")
        # self.entry_technique.config(width=26, justify="center", relief="groove")

        ####### create the widgets for the suggested own ship status  ######
        # suggested_status_explanation_frame = tk.Frame(suggested_status_frame, bg="white",
        #                                                   width=self.main_frame_width * 0.20,
        #                                                   height=self.main_frame_height * 0.30)
        # suggested_status_explanation_frame.config(borderwidth=3, relief="groove", padx=3, pady=3)
        # suggested_status_explanation_frame.place(relx=0.5, rely=0.32, anchor="center")

        ownship_properties_explanation_lbl = tk.Label(suggested_status_frame, wraplength=270, fg="red",
                                                      text="These features show the properties of the suggested approach (shown in diagram). If you want to follow this approach, your final features could be close to these values.",
                                                      font=("helvetica", 14, "bold"),
                                                      justify="left")
        ownship_properties_explanation_lbl.place(relx=0.5, rely=0.14, anchor="center")

        speed_lbl = tk.Label(suggested_status_frame, text="Vessel Speed", font=("helvetica", 16, "bold"),
                             justify="left")
        speed_lbl.place(relx=0.2, rely=0.30, anchor="center")

        self.suggested_speed = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 16, "bold"),
                                        justify="left")
        self.suggested_speed.place(relx=0.75, rely=0.30, anchor="center")

        heading_lbl = tk.Label(suggested_status_frame, text="Vessel Heading", font=("helvetica", 16, "bold"),
                               justify="left")
        heading_lbl.place(relx=0.22, rely=0.4, anchor="center")
        self.suggested_heading = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 16, "bold"),
                                          justify="left")
        self.suggested_heading.place(relx=0.75, rely=0.4, anchor="center")

        area_focus_lbl = tk.Label(suggested_status_frame, text="Area of Focus", font=("helvetica", 16, "bold"),
                                  justify="left")
        area_focus_lbl.place(relx=0.2, rely=0.5, anchor="center")
        self.suggested_area_focus = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 16, "bold"),
                                             justify="left")
        self.suggested_area_focus.place(relx=0.75, rely=0.5, anchor="center")

        aspect_lbl = tk.Label(suggested_status_frame, text="Aspect", font=("helvetica", 16, "bold"),
                              justify="left")
        aspect_lbl.place(relx=0.13, rely=0.6, anchor="center")
        self.suggested_aspect = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 16, "bold"),
                                         justify="left")
        self.suggested_aspect.place(relx=0.75, rely=0.6, anchor="center")

        oriantation_target_lbl = tk.Label(suggested_status_frame, text="Orientation to Target",
                                          font=("helvetica", 16, "bold"), justify="left")
        oriantation_target_lbl.place(relx=0.28, rely=0.7, anchor="center")
        self.suggested_orientation = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 16, "bold"),
                                              justify="left")
        self.suggested_orientation.place(relx=0.75, rely=0.7, anchor="center")

        distance_target_lbl = tk.Label(suggested_status_frame, text="Distance from Target",
                                       font=("helvetica", 16, "bold"),
                                       justify="left")
        distance_target_lbl.place(relx=0.28, rely=0.8, anchor="center")
        self.suggested_distance_target = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 16, "bold"),
                                                  justify="left")
        self.suggested_distance_target.place(relx=0.75, rely=0.8, anchor="center")

        maneuver_lbl = tk.Label(suggested_status_frame, text="Maneuver", font=("helvetica", 16, "bold"),
                                justify="left")
        maneuver_lbl.place(relx=0.15, rely=0.9, anchor="center")
        self.suggested_maneuver = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 16, "bold"),
                                           justify="left")
        self.suggested_maneuver.place(relx=0.72, rely=0.9, anchor="center")

        ####### creat the canvas for the suggested approach section  #######
        assist_btn = tk.Button(suggested_approach_frame, text="Assist", bg="green", width=32, height=2, anchor="c",
                               command=self.assist)
        # now, when the features object created filling the pushing scenario variables("suggested own ship status") can be done.
        assist_btn.config(relief="groove", font=("helvetica", 12, "bold"), fg="green")
        assist_btn.place(relx=.5, rely=.95, anchor="center")

        #### this is a button to reset the properties of the vessel and suggested approach
        # reset_vessel_properties_btn = tk.Button(instructions_frame, text="RESET", relief="groove",
        #                                         font=("helvetica", 12, "bold"), fg="red", width=32, height=2,
        #                                         command=self.reset_properties)
        # reset_vessel_properties_btn.place(relx=.5, rely=.95, anchor="center")

        ####### the button for more information about the suggested scenario#####3
        # more_info_btn = tk.Button(suggested_status_frame, text="More Info!", bg="green", width=32, height=2, anchor="c",
        #                           command=self.more_info)
        # more_info_btn.config(relief="groove", font=("helvetica", 12, "bold"), fg="green")
        # more_info_btn.place(relx=.5, rely=.95, anchor="center")

        self.canvas = tk.Canvas(suggested_approach_frame, bg='#000000')

        suggested_approach_frame.winfo_screenwidth()

        self.canvas.place(relx=0.5, rely=0.5, width=self.main_frame_width * 0.25,
                          height=self.main_frame_height * 0.4,
                          anchor="center")
        #### this is a explanation for the suggested approach picture
        suggested_approach_explanation_lbl = tk.Label(suggested_approach_frame, fg="red",
                                                      text="The diagram can be similar to your current approach\nand situation but it does not mean that it is \nhow you are performing now.",
                                                      font=("helvetica", 14, "bold"),
                                                      justify="left")
        suggested_approach_explanation_lbl.place(relx=0.5, rely=0.12, anchor="center")
        #### The labels for suggested own ship attributes description!
        img = ImageTk.PhotoImage(Image.open("images/MoreInfo.png"))
        #### the image for description section must be the size of 353*360 pixels
        img_desc = ImageTk.PhotoImage(Image.open("images/" + self.scenario + "_image.png"))

        speed_moreinfo = tk.Label(suggested_status_frame, image=img)
        speed_moreinfo.image = img
        HoverText(speed_moreinfo, "Keep your vessel speed at this rate!")
        speed_moreinfo.place(relx=0.42, rely=0.3, anchor="center")

        heading_moreinfo = tk.Label(suggested_status_frame, image=img)
        heading_moreinfo.image = img
        HoverText(heading_moreinfo,
                  "Vessel heading in relation to target: \n   Stem: Making headway against the current(0 Degrees).\n   Prependicular: Perpendicular to the target(90 degrees).\n   Angle: All other degrees but not changing during the execution.\n   Changing: In the case of the circular technique, the heading changes constantly, so it was converted to the changing option.")
        heading_moreinfo.place(relx=0.47, rely=0.4, anchor="center")

        area_of_focus_moreinfo = tk.Label(suggested_status_frame, image=img)
        area_of_focus_moreinfo.image = img
        HoverText(area_of_focus_moreinfo,
                  f"Where seafarer is focusing most of the ice clearing time:\n Above Zone.\n Above Vessel.\n Zone: In Zone.\n Along_Zone: Left side of the zone.")
        area_of_focus_moreinfo.place(relx=0.45, rely=0.5, anchor="center")

        aspect_moreinfo = tk.Label(suggested_status_frame, image=img)
        aspect_moreinfo.image = img
        HoverText(aspect_moreinfo,
                  "The vessel pathway in relation to the target:\n J-approach: Getting close to the target from below the zone.\n Direct: Getting close to the target directly.\n Up-current: Getting close to the target from up-current of the target.")
        aspect_moreinfo.place(relx=0.27, rely=0.6, anchor="center")

        orientation_moreinfo = tk.Label(suggested_status_frame, image=img)
        orientation_moreinfo.image = img
        HoverText(orientation_moreinfo,
                  "The ownship vessel’s orientation in relation to the target:\n Bow: Ownship vessel’s bow facing the target.\n Stern: Ownship vessel’s stern facing the target.\n Parallel: Ownship is parallel with the target.\n Changing: Ownship’s orientation is constantly changing.")
        orientation_moreinfo.place(relx=0.6, rely=0.7, anchor="center")

        distance_moreinfo = tk.Label(suggested_status_frame, image=img)
        distance_moreinfo.image = img
        HoverText(distance_moreinfo, "How far the ownship vessel should be from the target.")
        distance_moreinfo.place(relx=0.6, rely=0.8, anchor="center")

        manouver_moreinfo = tk.Label(suggested_status_frame, image=img)
        manouver_moreinfo.image = img
        HoverText(manouver_moreinfo,
                  "Techniques that each participant used in their ice management performance:\n Pushing: Using the bow or broadside of the vessel to clear ice around the indicated zone.\n Sector: Using the bow or broadside of the vessel and having a back and forth motion at the same time to clear the ice up current from the zone.\n Prop-Wash: Having a maintained position above the zone and flushing the ice from the target using the vessel’s propeller wake wash.\n Leeway: Keeping the position and blocking the flowing ice using the side of the vessel above the target area.\n Circular: Using the pushing and prop-wash techniques and having a circular motion at the same time above the target area")
        manouver_moreinfo.place(relx=0.34, rely=0.9, anchor="center")

        self.canvas.create_image(352.5, 360, anchor="se", image=img_desc)

        self.top_window = tk.Toplevel()
        self.top_window.geometry("310x200")
        ok_button = tk.Button(self.top_window, text="Enter", bg="black", width=10, height=2, anchor="c",
                              command=self.clean_up)
        self.entry_feild = tk.Entry(self.top_window, width=28, justify="center")
        entry_lbl = tk.Label(self.top_window, text="Please put your user name in this box:")
        entry_lbl.place(x=170, y=90, anchor="center")
        ok_button.place(x=170, y=160, anchor="center")
        self.entry_feild.place(x=170, y=115, anchor="center")
        self.top_window.attributes('-topmost', True)

        self.root.mainloop()

"""
This scripts is for safety at sea project design to help seafarer to drive the ships better
Created on Fr 6 Nov 8:27:27 2020
@author:Fatemeh Yazdanpanah and Arash Fassihozzaman  <a.fassihozzamanlangroudi@mun.ca>
"""

import tkinter as tk
from log_file import CsvRowsOperator, CsvFile
from features import Features
import os
import xml.etree.cElementTree as ET
import ipdb

engine_dic = {"pEngine": 0, "fTunnelThruster": 0, "sEngine": 0, "aTunnelThruster": 0}
rudder_dic = {"pRudder": 0, "sRudder": 0}


class PlayScenario:

    def __init__(self, root, main_frame, scenario):
        self.root = root
        self.main_frame = main_frame
        self.scenario = scenario
        self.main_frame_width = self.main_frame.winfo_width()
        self.main_frame_height = self.main_frame.winfo_height()
        self.features = None

    # this function will make the TraceData log file well_formed to be ready for parsing.
    def log_reader(self):
        f = open('/Users/arash/project/my_project/extracting_features/TraceData.log', 'r')
        linelist = f.readlines()
        well_formed_tracedata = open('/Users/arash/project/my_project/extracting_features/well_formed_TraceData.log',
                                     "w+")
        for line in linelist:

            if line.rfind("Throttle Pcts") != -1:
                line = line.replace("Throttle Pcts", "Throttle_Pcts")
            if line.rfind("Rudder Angles") != -1:
                line = line.replace("Rudder Angles", "Rudder_Angles")
            well_formed_tracedata.write(line)
        return well_formed_tracedata.name

    # this function is aimed to parse the log file and iterate into the file to  fill the log_objects list in wich,
    # each object is a row for our csv file to be generated
    def assist(self):

        log_objects = []
        well_formed_filename = self.log_reader()
        i = 0
        if os.path.isfile(well_formed_filename):
            xml_file = ET.parse(well_formed_filename).getroot()

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

                    csv_obj = CsvFile(int(float(log_entity.attrib["SimTime"])), float(log_entity.attrib["Latitude"]),
                                      float(log_entity.attrib["Longitude"]), float(log_entity.attrib["SOG"]),
                                      float(log_entity.attrib["COG"]), float(log_entity.attrib["Heading"]),
                                      float(aftthruster), float(forethruster),
                                      float(portengine), float(stbdengine),
                                      float(portrudder), float(stbdrudder))
                    log_objects.append(csv_obj)
                    if (self.scenario == "emergency" and i == 1800) or (
                            self.scenario in ["pushing", "leeway"] and i == 900):
                        break
                    else:
                        i += 1

        with open('E96_ScL_R1_interpolatedLog.csv', newline='') as myFile:
            logrowsoperator = CsvRowsOperator()
            log_objects = logrowsoperator.read_file(myFile)
            self.features = Features(log_objects, self.scenario, 900)

    def init_page(self):
        container = tk.Frame(self.root, width=self.main_frame_width * 0.94, height=self.main_frame_height * 0.67,
                             bg="white")
        container.config(borderwidth=6, relief="groove")
        container.place(relx=0.5, rely=0.6, anchor="center")

        own_vessel_frame = tk.Frame(container, bg="white", width=self.main_frame_width * 0.32,
                                    height=self.main_frame_height * 0.61)
        own_vessel_frame.config(borderwidth=3, relief="groove", padx=3, pady=3)
        own_vessel_frame.place(relx=0.2, rely=0.5, anchor="center")
        own_vessel_lbl = tk.Label(own_vessel_frame, text="Own Vessel Properties")
        own_vessel_lbl.place(relx=0.2, rely=-0.001, anchor="center")

        suggested_status_frame = tk.Frame(container, bg="white", width=self.main_frame_width * 0.22,
                                          height=self.main_frame_height * 0.61)
        suggested_status_frame.config(borderwidth=3, relief="groove", padx=25, pady=25)
        suggested_status_frame.place(relx=0.5, rely=0.5, anchor="center")
        suggested_own_ship_status_lbl = tk.Label(suggested_status_frame, text="suggested Own Ship status", bg="white")
        suggested_own_ship_status_lbl.place(relx=0.3, rely=0, anchor="center")

        suggested_approach_frame = tk.Frame(container, bg="white", width=self.main_frame_width * 0.32,
                                            height=self.main_frame_height * 0.61)
        suggested_approach_frame.config(borderwidth=3, relief="groove", padx=3, pady=3)
        suggested_approach_frame.place(relx=0.8, rely=0.5, anchor="center")
        suggested_approach_lbl = tk.Label(suggested_approach_frame, text="suggested Approach", bg="white")
        suggested_approach_lbl.place(relx=0.2, rely=-0.001, anchor="center")

        ####### create the widgets for the own vessel properties frame ######
        scale_1_lbl = tk.Label(own_vessel_frame, text="Vessel Speed", font=("helvetica", 12, "bold"))
        scale_1_lbl.place(relx=0.1, rely=0.12, anchor="center")
        scale_1 = tk.Scale(own_vessel_frame, from_=-500, to=500, orient="horizontal")
        scale_1.config(length=240)
        scale_1.place(relx=0.6, rely=0.1, anchor="center")

        scale_1_lbl = tk.Label(own_vessel_frame, text="Vessel Heading", font=("helvetica", 12, "bold"))
        scale_1_lbl.place(relx=0.11, rely=0.22, anchor="center")
        scale_2 = tk.Scale(own_vessel_frame, from_=-500, to=500, orient="horizontal")
        scale_2.config(length=240)
        scale_2.place(relx=0.6, rely=0.2, anchor="center")

        scale_1_lbl = tk.Label(own_vessel_frame, text="Ice Concentration", font=("helvetica", 12, "bold"))
        scale_1_lbl.place(relx=0.12, rely=0.32, anchor="center")
        scale_3 = tk.Scale(own_vessel_frame, from_=-500, to=500, orient="horizontal")
        scale_3.config(length=240)
        scale_3.place(relx=0.6, rely=0.3, anchor="center")

        scale_1_lbl = tk.Label(own_vessel_frame, text="Ice Load", font=("helvetica", 12, "bold"))
        scale_1_lbl.place(relx=0.06, rely=0.42, anchor="center")
        scale_4 = tk.Scale(own_vessel_frame, from_=-500, to=500, orient="horizontal")
        scale_4.config(length=240)
        scale_4.place(relx=0.6, rely=0.4, anchor="center")

        scale_1_lbl = tk.Label(own_vessel_frame, text="Distance from Target", font=("helvetica", 12, "bold"))
        scale_1_lbl.place(relx=0.13, rely=0.52, anchor="center")
        scale_5 = tk.Scale(own_vessel_frame, from_=-500, to=500, orient="horizontal")
        scale_5.config(length=240)
        scale_5.place(relx=0.6, rely=0.5, anchor="center")

        entry_aspect = tk.Entry(own_vessel_frame)
        entry_aspect.place(relx=0.60, rely=0.62, anchor="center")
        entry_aspect.config(width=26, justify="center", relief="groove")
        scale_1_lbl = tk.Label(own_vessel_frame, text="Aspect", font=("helvetica", 12, "bold"))
        scale_1_lbl.place(relx=0.06, rely=0.62, anchor="center")

        entry_area_focus = tk.Entry(own_vessel_frame)
        entry_area_focus.place(relx=0.60, rely=0.72, anchor="center")
        entry_area_focus.config(width=26, justify="center", relief="groove")
        scale_1_lbl = tk.Label(own_vessel_frame, text="Area of Focus", font=("helvetica", 12, "bold"))
        scale_1_lbl.place(relx=0.1, rely=0.72, anchor="center")

        entry_orientation_target = tk.Entry(own_vessel_frame)
        entry_orientation_target.place(relx=0.60, rely=0.82, anchor="center")
        entry_orientation_target.config(width=26, justify="center", relief="groove")
        scale_1_lbl = tk.Label(own_vessel_frame, text="Orientation to Target", font=("helvetica", 12, "bold"))
        scale_1_lbl.place(relx=0.13, rely=0.82, anchor="center")

        ####### create the widgets for the suggested own ship status  ######

        speed_lbl = tk.Label(suggested_status_frame, text="Vessel Speed:", font=("helvetica", 12, "bold"),
                             justify="left")
        speed_lbl.place(relx=0.1, rely=0.12, anchor="center")
        suggested_speed = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                   justify="left")
        suggested_speed.place(relx=0.75, rely=0.12, anchor="center")

        heading_lbl = tk.Label(suggested_status_frame, text="Vessel Heading:", font=("helvetica", 12, "bold"),
                               justify="left")
        heading_lbl.place(relx=0.1, rely=0.23, anchor="center")
        suggested_heading = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                     justify="left")
        suggested_heading.place(relx=0.75, rely=0.23, anchor="center")

        area_focus_lbl = tk.Label(suggested_status_frame, text="Area of Focus:", font=("helvetica", 12, "bold"),
                                  justify="left")
        area_focus_lbl.place(relx=0.09, rely=0.32, anchor="center")
        suggested_area_focus = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                        justify="left")
        suggested_area_focus.place(relx=0.75, rely=0.32, anchor="center")

        aspect_lbl = tk.Label(suggested_status_frame, text="Aspect:", font=("helvetica", 12, "bold"),
                              justify="left")
        aspect_lbl.place(relx=0.02, rely=0.42, anchor="center")
        suggested_aspect = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                    justify="left")
        suggested_aspect.place(relx=0.75, rely=0.42, anchor="center")

        oriantation_target_lbl = tk.Label(suggested_status_frame, text="Orientation to Target:",
                                          font=("helvetica", 12, "bold"), justify="left")
        oriantation_target_lbl.place(relx=0.14, rely=0.52, anchor="center")
        suggested_aspect = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                    justify="left")
        suggested_aspect.place(relx=0.75, rely=0.52, anchor="center")

        distance_target_lbl = tk.Label(suggested_status_frame, text="Distance from Target:",
                                       font=("helvetica", 12, "bold"),
                                       justify="left")
        distance_target_lbl.place(relx=0.14, rely=0.62, anchor="center")
        suggested_distance_target = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                             justify="left")
        suggested_distance_target.place(relx=0.75, rely=0.62, anchor="center")

        maneuver_lbl = tk.Label(suggested_status_frame, text="Maneuver:", font=("helvetica", 12, "bold"),
                                justify="left")
        maneuver_lbl.place(relx=0.04, rely=0.72, anchor="center")
        suggested_maneuver = tk.Label(suggested_status_frame, text="N/A", font=("helvetica", 12, "bold"),
                                      justify="left")
        suggested_maneuver.place(relx=0.75, rely=0.72, anchor="center")

        ####### creat the canvas for the suggested approach section  #######
        assist_btn = tk.Button(suggested_approach_frame, text="Assist", bg="green", width=32, height=2, anchor="c",
                               command=self.assist)
        # now, when the features object created filling the pushing scenario variables("suggested own ship status") can be done.
        assist_btn.config(relief="groove", font=("helvetica", 12, "bold"), fg="green")
        assist_btn.place(relx=.5, rely=.9, anchor="center")

        canvas = tk.Canvas(suggested_approach_frame)
        canvas.place(relx=0.5, rely=0.5, anchor="center")
        canvas.create_line((100, 200, 150, 300))

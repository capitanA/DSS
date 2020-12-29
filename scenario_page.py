import tkinter as tk
from log_file import LogRowsOperator
from features import Features
from functools import partial


class PlayScenario:

    def __init__(self, root, main_frame):
        self.root = root
        self.main_frame = main_frame
        self.main_frame_width = self.main_frame.winfo_width()
        self.main_frame_height = self.main_frame.winfo_height()
        self.features = None

    # this is a function which by create an object of Feature class. Then fill all the variables of pushing scenario.
    def start(self):
        with open('F69_ScA_7ten_interpolatedLog.csv', newline='') as myFile:
            logrowsoperator = LogRowsOperator()
            log_objects = logrowsoperator.read_file(myFile)
            self.features = Features(log_objects, "emergency", 180)

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
                               command=self.start)
        # now, when the features object created filling the pushing scenario variables("suggested own ship status") can be done.
        assist_btn.config(relief="groove", font=("helvetica", 12, "bold"), fg="green")
        assist_btn.place(relx=.5, rely=.9, anchor="center")

        canvas = tk.Canvas(suggested_approach_frame)
        canvas.place(relx=0.5, rely=0.5, anchor="center")
        canvas.create_line((100, 200, 150, 300))

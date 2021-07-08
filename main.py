import tkinter as tk
from PIL import ImageTk, Image
from helper import BLabel
from functools import partial
from scenario_page import PlayScenario
from simReceiver import SimReceiver
import logging
import sys
from tkinter import messagebox
import ipdb


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s %(message)s')
    handler = logging.FileHandler(log_file, mode="a+")
    handler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


def resize_image(img, root):
    resized_img = img.resize((int(((root.winfo_screenwidth() - 30) / 3) * 0.5), 200))
    return resized_img


def do_the_scenario(pushing_frame, leeway_frame, emergency_frame, scenario, main_frame, root):
    start_scenario(pushing_frame, leeway_frame, emergency_frame, scenario, main_frame, root)


# def do_leeway_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root):
#     pushing_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root)


# def do_emergency_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root):
#     pushing_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root)


def start_scenario(pushing_frame, leeway_frame, emergency_frame, scenario, main_frame, root):
    pushing_frame.destroy()
    leeway_frame.destroy()
    emergency_frame.destroy()
    scenario_obj = PlayScenario(root, main_frame, scenario, exceptio_logger, user_assist_logger, isRealTime)

    back_command = partial(get_back, scenario_obj)

    go_back_button = tk.Button(root, text="Back To Main Menu", width=20, height=3, anchor="c",
                               command=back_command,
                               bg="gray")
    go_back_button.place(relx=0.5, rely=0.05, anchor="center")
    scenario_obj.init_page()


# def leeway_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root):
#     scenario_1_frame.destroy()
#     scenario_2_frame.destroy()
#     scenario_3_frame.destroy()
#     ff = tk.Button(root, text="adssfsdfafafa", anchor="c", command=get_back, bg="red")
#     ff.place(relx=0.5, rely=0.03, anchor="n")


# def emergency_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root):
#     scenario_1_frame.destroy()
#     scenario_2_frame.destroy()
#     scenario_3_frame.destroy()
#     ff = tk.Button(root, text="adssfsdfafafa", anchor="c", command=get_back, bg="red")
#     ff.place(relx=0.5, rely=0.03, anchor="n")


def get_back(scenario_obj):

    if arg == "-realTime":
        scenario_obj.simReceiver.close_port()

    if scenario_obj.top_window.winfo_exists():
        scenario_obj.top_window.destroy()
    user_assist_logger.info(
        f"{scenario_obj.username if scenario_obj.username else 'Unknown'} user get Back to main menu!")
    init_main_page(root)

    # if scenario_obj.top_window.winfo_exists():
    #     messagebox.showinfo(message="please first enter your name!")
    # else:
    #     init_main_page(root)


def init_main_page(root):
    frame_width = root.winfo_screenwidth()
    frame_height = root.winfo_screenheight()
    main_frame = tk.Frame(root, width=frame_width - 30, height=frame_height)
    background_img = Image.open("images/background_image2.jpg")
    resized_back_img = background_img.resize((frame_width, frame_height))
    back_img = ImageTk.PhotoImage(resized_back_img)
    img_1_lbl = tk.Label(main_frame, image=back_img)
    img_1_lbl.place(relx=0.5, rely=0.5, anchor="center")
    main_frame.place(relx=.5, rely=.5, anchor="center")

    pushing_frame = tk.Frame(main_frame, width=(frame_width - 100) / 3, height=400, bg="white")
    pushing_frame.config(borderwidth=6, relief="groove")
    pushing_frame.place(relx=0.17, rely=0.5, anchor="center")

    leeway_frame = tk.Frame(main_frame, width=(frame_width - 100) / 3, height=400, bg="white")
    leeway_frame.config(borderwidth=6, relief="groove")

    leeway_frame.place(relx=0.5, rely=0.5, anchor="center")

    emergency_frame = tk.Frame(main_frame, width=(frame_width - 100) / 3, height=400, bg="white")
    emergency_frame.config(borderwidth=6, relief="groove")

    emergency_frame.place(relx=0.83, rely=0.5, anchor="center")

    Button_Pushing_img = tk.PhotoImage(file="images/Pushing_look.png")
    Button_Leeway_img = tk.PhotoImage(file="images/Leaway_look.png")
    Button_Emergency_img_4tens = tk.PhotoImage(file="images/Emergency_look_4tens.png")
    Button_Emergency_img_7tens = tk.PhotoImage(file="images/Emergency_look_7tens.png")

    ######   First button for Pushing scenario  ######
    pushing_command = partial(do_the_scenario, pushing_frame, leeway_frame, emergency_frame, "pushing", main_frame,
                              root)
    pushing_btn = tk.Button(pushing_frame, image=Button_Pushing_img, anchor="c", command=pushing_command,
                            relief="raised")
    pushing_btn.place(relx=0.5, rely=0.03, anchor="n")

    ######   Seccond button for Leeway scenario  ######
    leeway_command = partial(do_the_scenario, pushing_frame, leeway_frame, emergency_frame, "leeway", main_frame,
                             root)
    leeway_btn = tk.Button(leeway_frame, image=Button_Leeway_img, anchor="c", command=leeway_command,
                           relief="raised")
    leeway_btn.place(relx=0.5, rely=0.03, anchor="n")

    ######   Third button for Emergency Scenario  ######
    emergency_command = partial(do_the_scenario, pushing_frame, leeway_frame, emergency_frame, "emergency",
                                main_frame,
                                root)
    emergency_4tens_command = partial(do_the_scenario, pushing_frame, leeway_frame, emergency_frame, "emergency_4tens",
                                      main_frame,
                                      root)
    emergency_btn = tk.Button(emergency_frame, image=Button_Emergency_img_7tens, anchor="c", command=emergency_command,
                              relief="raised")

    emergency_4tens_btn = tk.Button(emergency_frame, image=Button_Emergency_img_4tens, anchor="c",
                                    command=emergency_4tens_command,
                                    relief="raised")
    emergency_btn.place(relx=0.2, rely=0.03, anchor="n")
    emergency_4tens_btn.place(relx=0.8, rely=0.03, anchor="n")

    ######   the image for pushing scenario   ######
    opend_img_1 = Image.open("images/pushing.png")
    resize_image_1 = resize_image(opend_img_1, root)
    image_1 = ImageTk.PhotoImage(resize_image_1)
    img_1_lbl = tk.Label(pushing_frame, image=image_1)
    img_1_lbl.place(relx=0.5, rely=0.45, anchor="center")

    ######   the image for leeway scenario   ######
    opened_img_2 = Image.open("images/leeway.png")
    resize_image_2 = resize_image(opened_img_2, root)
    image_2 = ImageTk.PhotoImage(resize_image_2)
    img_2_lbl = tk.Label(leeway_frame, image=image_2)
    img_2_lbl.place(relx=0.5, rely=0.45, anchor="center")

    ######   the image for emergency scenario   ######
    opened_img_3 = Image.open("images/emergency.png")
    resize_image_3 = resize_image(opened_img_3, root)
    image_3 = ImageTk.PhotoImage(resize_image_3)
    img_3_lbl = tk.Label(emergency_frame, image=image_3)
    img_3_lbl.place(relx=0.5, rely=0.45, anchor="center")

    ######   The frames for descriptions   ######
    dsc_frame_sce_1 = tk.Frame(pushing_frame, width=350, height=((frame_width - 30) / 3) * 0.25, bg="white")
    dsc_frame_sce_1.place(relx=0.55, rely=0.85, anchor="center")
    dsc_frame_sce_1.config(borderwidth=2, relief="groove")

    dsc_frame_sce_2 = tk.Frame(leeway_frame, width=350, height=((frame_width - 30) / 3) * 0.25, bg="white")
    dsc_frame_sce_2.place(relx=0.55, rely=0.85, anchor="center")
    dsc_frame_sce_2.config(borderwidth=2, relief="groove")

    dsc_frame_sce_3 = tk.Frame(emergency_frame, width=350, height=((frame_width - 30) / 3) * 0.25, bg="white")
    dsc_frame_sce_3.place(relx=0.55, rely=0.85, anchor="center")
    dsc_frame_sce_3.config(borderwidth=2, relief="groove")

    ######   The description for pushing scenario   ######
    # label = BLabel(dsc_frame_sce_1)
    # label.add_option("Objective: Clear the encroaching pack ice from the indicated area using the pushing technique")
    # label.add_option("Time: 15min")
    # label.add_option("Vessel heading: 120deg")
    # label.add_option("Current: 0.4kn")
    # label.add_option("Current direction: 180deg S")
    # label.add_option("Wind: Light")
    # label.add_option("Ice: 0.3-0.7m first year ice, 4-tenths concentration")
    # label.l.place(relx=0.5, rely=0.5, anchor="center")

    # llbb = tk.Label(dsc_frame_sce_1,
    #                 text="Objective: Clear the encroaching pack ice from the indicated area\n\tusing the pushing technique\n Time: 15min\nVessel heading: 120deg\nCurrent direction: 180deg\nwind: light\nIce: 0.3-0.7m first year ice, 4-tenths concentration",
    #                 bg="white", justify="left")
    llbb = tk.Label(dsc_frame_sce_1,
                    text="Objective: Clear the encroaching pack ice from the\n\tindicated area using pushing technique\nTime: 15min\nVessel heading: 120deg\nCurrent direction: 180deg\nIce: 0.3-0.7m first year ice, 4-tenths concentration",
                    bg="white", justify="left")
    llbb.place(relx=0.5, rely=0.5, anchor="center")

    # llbb = tk.Label(dsc_frame_sce_2,
    #                 text="Objective: Clear the indicated area aft of \n\tmidships using the leeway technique\n Time: 15min\nVessel heading: 60deg\nTarget heading: 0deg!\nCurrent: 1kn\nCurrent direction: 180deg\n Wind: Light\nIce: 0.3-0.7m first year ice, 5-tenths concentration ",
    #                 bg="white", justify="left")
    llbb = tk.Label(dsc_frame_sce_2,
                    text="Objective: Clear the indicated area aft of\n\tmidships using the leeway technique\nTime: 15min\nVessel heading: 60deg\nCurrent direction: 180deg\nIce: 0.3-0.7m first year ice, 5-tenths concentration ",
                    bg="white", justify="left")

    llbb.place(relx=0.5, rely=0.5, anchor="center")

    # llbb = tk.Label(dsc_frame_sce_3,
    #                 text="Objective: Clear the encroaching pack ice from the boxed area\n Time: 30min\nTarget heading: 0deg!\nCurrent: 0.5kn\nCurrent direction: 180deg\n Wind: Light\nIce: 0.3-0.7m first year ice, 7-tenths concentration",
    #                 bg="white", justify="left")
    llbb = tk.Label(dsc_frame_sce_3,
                    text="Objective: Clear the encroaching pack ice from the\n\tboxed area\nTime: 30min\nCurrent: 0.5kn\nCurrent direction: 180deg\nIce: 0.3-0.7m first year ice, 7-tenths concentration",
                    bg="white", justify="left")
    llbb.place(relx=0.5, rely=0.5, anchor="center")
    root.mainloop()


if __name__ == "__main__":
    global arg
    """ setting loogers for information/exceptions"""
    exceptio_logger = setup_logger("Exception_log", "exc_log.log")
    user_assist_logger = setup_logger("User_assist_log", "user_log.log")

    isRealTime = False
    for i, arg in enumerate(sys.argv):
        if arg == "-realTime":
            isRealTime = True
            print("Command Arg -realTime detected " + str(isRealTime))

    root = tk.Tk()
    root.title("DSS")
    root.geometry("1200x800")
    init_main_page(root)

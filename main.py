import tkinter as tk
from PIL import ImageTk, Image

from helper import BLabel
from functools import partial
from scenario_page import PlayScenario


def resize_image(img, root):
    resized_img = img.resize((int(((root.winfo_screenwidth() - 30) / 3) * 0.5), 200))
    return resized_img


def do_the_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root):
    start_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root)


# def do_leeway_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root):
#     pushing_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root)


# def do_emergency_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root):
#     pushing_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root)


def start_scenario(scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root):
    scenario_1_frame.destroy()
    scenario_2_frame.destroy()
    scenario_3_frame.destroy()
    ff = tk.Button(root, text="Back To Main Menue", width=20, height=3, anchor="c", command=get_back, bg="gray")
    ff.place(relx=0.5, rely=0.05, anchor="center")
    scenario_obj = PlayScenario(root, main_frame)
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


def get_back():
    init_page(root)


def init_page(root):
    frame_width = root.winfo_screenwidth()
    frame_height = root.winfo_screenheight()
    main_frame = tk.Frame(root, width=frame_width - 30, height=frame_height)
    background_img = Image.open("images/background_image2.jpg")
    resized_back_img = background_img.resize((frame_width, frame_height))
    back_img = ImageTk.PhotoImage(resized_back_img)
    img_1_lbl = tk.Label(main_frame, image=back_img)
    img_1_lbl.place(relx=0.5, rely=0.5, anchor="center")
    main_frame.place(relx=.5, rely=.5, anchor="center")

    # label = tk.Label(main_frame, text='DSS for Offshore ships', font=('Helvetica', 60, 'bold'),bg="grey")
    # label.place(relx=0.5, rely=0.15, anchor="center")
    # root.wm_attributes("-transparent", root["bg"])
    scenario_1_frame = tk.Frame(main_frame, width=(frame_width - 100) / 3, height=400, bg="white")
    scenario_1_frame.config(borderwidth=6, relief="groove")
    scenario_1_frame.place(relx=0.17, rely=0.5, anchor="center")

    scenario_2_frame = tk.Frame(main_frame, width=(frame_width - 100) / 3, height=400, bg="white")
    scenario_2_frame.config(borderwidth=6, relief="groove")

    scenario_2_frame.place(relx=0.5, rely=0.5, anchor="center")

    scenario_3_frame = tk.Frame(main_frame, width=(frame_width - 100) / 3, height=400, bg="white")
    scenario_3_frame.config(borderwidth=6, relief="groove")

    scenario_3_frame.place(relx=0.83, rely=0.5, anchor="center")

    Button_Pushing_img = tk.PhotoImage(file="images/Pushing_look.png")
    Button_Leeway_img = tk.PhotoImage(file="images/Leaway_look.png")
    Button_Emergency_img = tk.PhotoImage(file="images/Emergency_look.png")

    ######   First button for first scenario  ######
    command_1 = partial(do_the_scenario, scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root)
    scenario_btn_1 = tk.Button(scenario_1_frame, image=Button_Pushing_img, anchor="c", command=command_1,
                               relief="raised")
    scenario_btn_1.place(relx=0.5, rely=0.03, anchor="n")

    ######   Second button for second scenario  ######
    command_2 = partial(do_the_scenario, scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root)
    scenario_btn_2 = tk.Button(scenario_2_frame, image=Button_Leeway_img, anchor="c", command=command_2,
                               relief="raised")
    scenario_btn_2.place(relx=0.5, rely=0.03, anchor="n")

    ######   Third button for third scenario  ######
    command_3 = partial(do_the_scenario, scenario_1_frame, scenario_2_frame, scenario_3_frame, main_frame, root)
    scenario_btn_3 = tk.Button(scenario_3_frame, image=Button_Emergency_img, anchor="c", command=command_3,
                               relief="raised")
    scenario_btn_3.place(relx=0.5, rely=0.03, anchor="n")

    ######   the image for pushing scenario   ######
    opend_img_1 = Image.open("images/pushing.png")
    resize_image_1 = resize_image(opend_img_1, root)
    image_1 = ImageTk.PhotoImage(resize_image_1)
    img_1_lbl = tk.Label(scenario_1_frame, image=image_1)
    img_1_lbl.place(relx=0.5, rely=0.45, anchor="center")

    ######   the image for leeway scenario   ######
    opened_img_2 = Image.open("images/leeway.png")
    resize_image_2 = resize_image(opened_img_2, root)
    image_2 = ImageTk.PhotoImage(resize_image_2)
    img_2_lbl = tk.Label(scenario_2_frame, image=image_2)
    img_2_lbl.place(relx=0.5, rely=0.45, anchor="center")

    ######   the image for emergency scenario   ######
    opened_img_3 = Image.open("images/emergency.png")
    resize_image_3 = resize_image(opened_img_3, root)
    image_3 = ImageTk.PhotoImage(resize_image_3)
    img_3_lbl = tk.Label(scenario_3_frame, image=image_3)
    img_3_lbl.place(relx=0.5, rely=0.45, anchor="center")

    ######   The frames for descriptions   ######
    dsc_frame_sce_1 = tk.Frame(scenario_1_frame, width=350, height=((frame_width - 30) / 3) * 0.25, bg="white")
    dsc_frame_sce_1.place(relx=0.55, rely=0.85, anchor="center")
    dsc_frame_sce_1.config(borderwidth=2, relief="groove")

    dsc_frame_sce_2 = tk.Frame(scenario_2_frame, width=350, height=((frame_width - 30) / 3) * 0.25, bg="white")
    dsc_frame_sce_2.place(relx=0.55, rely=0.85, anchor="center")
    dsc_frame_sce_2.config(borderwidth=2, relief="groove")

    dsc_frame_sce_3 = tk.Frame(scenario_3_frame, width=350, height=((frame_width - 30) / 3) * 0.25, bg="white")
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
    llbb = tk.Label(dsc_frame_sce_1,
                    text="Objective: Clear the indicated area aft of\n\tmidships using the leeway technique\n Time: 15min\nVessel heading: 60deg\nTarget heading: 0deg!\nCurrent: 1kn",
                    bg="white", justify="left")
    llbb.place(relx=0.5, rely=0.5, anchor="center")

    ######   The description for leeway scenario   ######
    label = BLabel(dsc_frame_sce_2)
    label.add_option("Objective: Clear the indicated area aft of midships using the leeway technique")
    label.add_option("Time: 15min")
    label.add_option("Vessel heading: 60deg")
    label.add_option("Target heading: 0deg!")
    label.add_option("Current: 1kn")
    label.add_option("Current direction: 180deg S")
    label.add_option("Wind: Light")
    label.add_option("Ice: 0.3-0.7m first year ice, 5-tenths concentration")
    label.l.place(relx=0.5, rely=0.5, anchor="center")

    ######   The description for emergency scenario   ######
    label = BLabel(dsc_frame_sce_3)
    label.add_option("Objective: Clear encroaching pack ice from the boxed area shown")
    label.add_option("Time: 30min")
    label.add_option("Current: 0.5kn")
    label.add_option("Current direction: 180deg S")
    label.add_option("Wind: Light")
    label.add_option("Ice: 0.3-0.7m first year ice")
    label.l.place(relx=0.5, rely=0.5, anchor="center")
    root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    root.title("DSS")
    root.geometry("1200x800")
    init_page(root)

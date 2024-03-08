"""
INTRODUCTION: This project is created for adjust brightness. This file is source code of project.
AUTHOR: Zephyrus
Date and time: 2024 Q1 - Release 1.0.2
"""
import os
from configparser import ConfigParser
from tkinter import messagebox
from PIL import Image
import pystray
import screen_brightness_control as sbc
import ttkbootstrap as tb


class DesktopBrightnessApp:

    def __init__(self):
        self.root = tb.Window(themename="darkly")

        self.config = ConfigParser()
        self.config.read('options.ini')

        self.img = Image.open(
            r'C:\Users\ekber\OneDrive\Masaüstü\Desktop_brightness_app_github\light.ico')  # Your img path here.
        self.root.iconbitmap(
            r'C:\Users\ekber\OneDrive\Masaüstü\Desktop_brightness_app_github\light.ico')  # Your icon img path here.

        # Window initialization
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        self.x = (self.screen_width / 2) - (500 / 2)
        self.y = (self.screen_height / 2) - (250 / 2)
        self.root.geometry('%dx%d+%d+%d' % (500, 250, self.x, self.y))
        self.root.title("Desktop Brightness App")

        get_monitor = sbc.list_monitors()
        self.label_main_name = tb.Label(self.root, text=get_monitor[0], font=("Arial bold", 13))
        self.label_main_name.pack(pady=30)

        self.checkbutton_label = tb.Label(self.root)

        self.minimize_button = tb.Button(self.root, text="Minimize", command=self.minimize_app)
        self.minimize_button.place(x=215, y=200)

        self.menu = pystray.Menu(
            pystray.MenuItem("Open GUI", self.on_move_clicked),
            pystray.MenuItem("Exit", self.on_move_clicked)
        )

        self.scale_1 = tb.Scale(self.root, from_=0, to=100, orient="horizontal", length=200,
                                command=self.set_brightness_for_selected_monitor)
        self.scale_1.place(x=150, y=125)

        self.label_brightness = tb.Label(self.root)
        self.label_brightness.place(x=210, y=90)

        self.button_to_0 = tb.Button(self.root, text="0", command=lambda: self.scale_1.set(0))
        self.button_to_0.place(x=130, y=155)

        self.button_to_25 = tb.Button(self.root, text="25", command=lambda: self.scale_1.set(25))
        self.button_to_25.place(x=180, y=155)

        self.button_to_50 = tb.Button(self.root, text="50", command=lambda: self.scale_1.set(50))
        self.button_to_50.place(x=230, y=155)

        self.button_to_75 = tb.Button(self.root, text="75", command=lambda: self.scale_1.set(75))
        self.button_to_75.place(x=280, y=155)

        self.button_to_100 = tb.Button(self.root, text="100", command=lambda: self.scale_1.set(100))
        self.button_to_100.place(x=330, y=155)

        self.get_monitors()
        self.theme_list = self.root.style.theme_names()
        self.themes = tb.StringVar(value=self.root.style.theme_use())
        self.c_box = tb.Combobox(self.root, values=self.theme_list, state="readonly", width=15)
        self.c_box.place(x=0, y=0)
        self.c_box.bind("<<ComboboxSelected>>", self.change_theme)

    # Disable maximize of window.
    def maximize_disabled(self):
        self.root.resizable(0, 0)  # type: ignore

    def get_monitors(self):
        global c_box_monitor
        self.monitors = sbc.list_monitors()
        if len(self.monitors) >= 2:
            self.c_box_monitor = tb.Combobox(self.root, values=self.monitors, state="readonly", width=15)
            self.c_box_monitor.place(x=383, y=0)
            self.c_box_monitor.bind("<<ComboboxSelected>>", self.set_brightness_for_selected_monitor)

    # Checking for send notify if there not selected any monitor.
    def check_c_box(self):
        selected_monitor = c_box_monitor.current()
        if selected_monitor == -1:
            self.scale_1.config(state="disabled", takefocus=False)
            messagebox.showinfo("Desktop Brightness App",
                                "No monitors are selected\nIf u want adjust brightness select a monitor")

    def set_brightness_for_selected_monitor(self, event):
        self.monitors = sbc.list_monitors()

        if hasattr(self, 'c_box_monitor'):
            selected_monitor = self.c_box_monitor.get()
            self.label_main_name.config(text=selected_monitor)

        else:
            self.label_brightness.config(text=f"Brightness: {int(self.scale_1.get())}")
            val = int(self.scale_1.get())
            sbc.set_brightness(val)
            self.config['MONITOR SETTINGS']['brightness'] = str(val)

        with open('options.ini', 'w') as configfile:
            self.config.write(configfile)

    def change_theme(self, event):

        self.root.style.theme_use(self.c_box.get())
        self.config['GENERAL SETTINGS']['theme'] = (event.widget.get())
        with open('options.ini', 'w') as configfile:
            self.config.write(configfile)

    # Load user last settings.
    def load_last_settings(self):

        # If there not options file and options features set default settings.
        if not os.path.exists('options.ini') or 'GENERAL SETTINGS' and 'MONITOR SETTINGS' not in self.config:
            messagebox.showinfo("Desktop Brightness App", "Hello, Welcome to Adjust Screen Brightness App")
            self.config['GENERAL SETTINGS'] = {
                'theme': 'darkly',
            }
            self.config['MONITOR SETTINGS'] = {
                'brightness': '50'
            }
            with open('options.ini', 'w') as configfile:
                self.config.write(configfile)

        monitors = sbc.list_monitors()
        brightness = self.config['MONITOR SETTINGS'].getint('brightness')
        monitor = self.config['MONITOR SETTINGS'].get('monitor')
        theme = self.config['GENERAL SETTINGS'].get('theme')
        self.scale_1.set(brightness)
        self.root.style.theme_use(theme)

        # Settings for one monitor.
        if len(monitors) == 1:
            if theme != self.config['GENERAL SETTINGS']['theme'] and brightness != self.config[
                'MONITOR SETTINGS'].getint(
                'brightness'):
                print("Settings not successfully loaded")

            else:
                self.scale_1.set(brightness)
                self.root.style.theme_use(theme)
                print("Settings successfully loaded")

        # Settings for two and more monitors.
        elif len(monitors) >= 2:
            if theme != self.config['GENERAL SETTINGS']['theme'] and brightness != self.config[
                'MONITOR SETTINGS'].getint(
                'brightness') \
                    and monitor != self.config['MONITOR SETTINGS'].get('monitor'):
                print("Settings not successfully loaded")

            else:
                self.scale_1.set(brightness)
                self.root.style.theme_use(theme)
                print("Settings successfully loaded")

    def on_move_clicked(self, icon, item):
        if str(item) == "Open GUI":
            self.icon.stop()
            self.root.deiconify()
            self.root.attributes('-topmost', True)
            self.root.lift()
        elif str(item) == "Exit":
            self.icon.stop()
            self.root.destroy()

    def minimize_app(self):
        self.root.withdraw()
        self.icon = pystray.Icon('icon', self.img, menu=self.menu)
        self.icon.run()

    # Run functions.
    def run_script(self):
        self.maximize_disabled()
        self.load_last_settings()
        self.root.mainloop()


if __name__ == "__main__":
    app = DesktopBrightnessApp()
    app.run_script()

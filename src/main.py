from application import Application
import tkinter as tk
import json

controls_str = """
        WASD - Movement

        X - Spawn Cube

        C - Shoot Cube

        V - Spawn 100 Cubes

        B - Spawn Tower

        SPACE - Spawn Bomb

        G - Clear Cubes

        Q - Toggle Slo Mo
        """

shadow_qualities = (
    "Off",
    "Low",
    "Medium",
    "High"
)
shadow_qualities_conv = {
    "Off" : (0, 30),
    "Low" : (1024, 30),
    "Medium" : (2048, 50),
    "High" : (4096, 70)
}

window_resolutions = (
    "1280 x 720",
    "1920 x 1080",
    "2560 x 1440",
    "3840 x 2160"
)
window_resolutions_conv = {
    "1280 x 720" : (1280, 720),
    "1920 x 1080" : (1920, 1080),
    "2560 x 1440" : (2560, 1440),
    "3840 x 2160" : (3840, 2160)
}

msaa_samples = (
    "Off",
    "2x",
    "4x",
    "8x"
)
msaa_conv = {
    "Off" : 0,
    "2x" : 2,
    "4x" : 4,
    "8x" : 8
}

vsync_options = (
    "Off",
    "On"
)
vsync_conv = {
    "Off" : 0,
    "On" : 1
}


class Launcher(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Physics Sandbox")
        self.iconbitmap(default = "icon.ico")
        self.resizable(width=False, height=False)
        self.geometry("480x520")

        line = tk.Label(self, font = ("Rockwell", 12), text = "___________________________________________________", fg = "gray")
        line.place(anchor = "center", x = 240, y = 60)

        title = tk.Label(self, font = ("Rockwell", 30, "bold"), text = "Physics Sandbox")
        title.place(anchor = "center", x = 240, y = 30)

        launch_button = tk.Button(self, font = ("Rockwell", 12), text = "Play", width = 20, height = 2, command = self.launchGame, bg = "green yellow")
        launch_button.place(anchor = "center", x = 240, y = 110)

        line2 = tk.Label(self, font = ("Rockwell", 12), text = "___________________________________________________", fg = "gray")
        line2.place(anchor = "center", x = 240, y = 150)

        controls_header = tk.Label(self, font = ("Rockwell", 20, "bold"), text = "Controls")
        controls_header.place(anchor = "center", x = 115, y = 185)

        controls = tk.Label(self, font = ("Rockwell", 12), text = controls_str)
        controls.place(anchor = "n", x = 100, y = 198)

        settings_header = tk.Label(self, font = ("Rockwell", 20, "bold"), text = "Settings")
        settings_header.place(anchor = "center", x = 360, y = 185)


        self.window_res = tk.StringVar()
        self.window_res.set(window_resolutions[0])

        res_label = tk.Label(self, font = ("Rockwell", 12), text = "Window Resolution")
        res_label.place(anchor = "n", x = 360, y = 217)

        res_menu = tk.OptionMenu(self, self.window_res, *window_resolutions)
        res_menu.place(anchor = "n", x = 360, y = 240)


        self.shadow_quality = tk.StringVar()
        self.shadow_quality.set(shadow_qualities[2])

        shadow_label = tk.Label(self, font = ("Rockwell", 12), text = "Shadow Quality")
        shadow_label.place(anchor = "n", x = 360, y = 280)

        shadow_menu = tk.OptionMenu(self, self.shadow_quality, *shadow_qualities)
        shadow_menu.place(anchor = "n", x = 360, y = 303)


        self.msaa_mode = tk.StringVar()
        self.msaa_mode.set(msaa_samples[0])

        msaa_label = tk.Label(self, font = ("Rockwell", 12), text = "Anti-Aliasing (MSAA)")
        msaa_label.place(anchor = "n", x = 360, y = 340)

        msaa_menu = tk.OptionMenu(self, self.msaa_mode, *msaa_samples)
        msaa_menu.place(anchor = "n", x = 360, y = 363)


        self.vsync_mode = tk.StringVar()
        self.vsync_mode.set(vsync_options[1])

        vsync_label = tk.Label(self, font = ("Rockwell", 12), text = "Vertical Sync")
        vsync_label.place(anchor = "n", x = 360, y = 400)

        vsync_menu = tk.OptionMenu(self, self.vsync_mode, *vsync_options)
        vsync_menu.place(anchor = "n", x = 360, y = 423)


        self.loadSettings()

        self.mainloop()


    def launchGame(self):
        self.saveSettings()

        resolution = window_resolutions_conv[self.window_res.get()]
        shadow = shadow_qualities_conv[self.shadow_quality.get()]
        msaa = msaa_conv[self.msaa_mode.get()]
        vsync = vsync_conv[self.vsync_mode.get()]

        self.destroy()
        
        app = Application(window_resolution = resolution, shadow_resolution = shadow, msaa = msaa, vsync = vsync)
        app.run()

    def saveSettings(self):
        save_data = {}

        save_data["resolution"] = self.window_res.get()
        save_data["shadow"] = self.shadow_quality.get()
        save_data["msaa"] = self.msaa_mode.get()
        save_data["vsync"] = self.vsync_mode.get()

        try:
            save_file = open("config/settings.json", "w")
            save_file.write(json.dumps(save_data))
        finally:
            save_file.close()

    def loadSettings(self):
        try:
            save_file = open("config/settings.json", "r")
            save_data = json.loads(save_file.read())

            self.window_res.set(save_data["resolution"])
            self.shadow_quality.set(save_data["shadow"])
            self.msaa_mode.set(save_data["msaa"])
            self.vsync_mode.set(save_data["vsync"])

        except:
            save_file = open("config/settings.json", "a")
        finally:
            save_file.close()
        



if __name__ == "__main__":
    launcher = Launcher()
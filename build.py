from setuptools import setup

setup(
    name="Physics Sandbox",
    options={
        "build_apps": {

            "gui_apps": {
                "Physics Sandbox": "main.py",
            },

            "icons": {
                "Physics Sandbox": "../icon.bmp",
            },

            "build_base": "../build",

            "requirements_path": "../requirements.txt",

            "log_filename": "output.log",
            "log_append": False,

            "include_patterns": [
                "config/config.prc",
                "models/*",
                "textures/*",
                "icon.ico",
            ],

            "plugins": [
                "pandagl",
            ],

            "platforms": [
                'win_amd64',
            ],
        }
    }
)
import customtkinter as ct
import functions

ct.set_appearance_mode("dark")
ct.set_default_color_theme("dark-blue")

appIcon = functions.resourcepath("Images/Favicon.ico")
mainWinImage = functions.resourcepath("Images/Favicon.ico")
linkImage = functions.resourcepath("Images/Link2.png")


def formatMain(self):
    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=0)
    self.grid_rowconfigure(2, weight=0)
    self.grid_rowconfigure(3, weight=2)

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)
    self.grid_columnconfigure(2, weight=1)








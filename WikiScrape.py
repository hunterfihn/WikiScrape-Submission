from tkinter import *
from tkinter import filedialog
import customtkinter as ct
import random as rd


import functions  
import formatting 


#Main Window Class
class wikiScrapeApp(ct.CTk):
    def __init__(self):
        super().__init__()

        #Set title, favicon, geometry, open splash screen
        self.title("WikiScrape")
        self.iconbitmap(default = formatting.appIcon)
        self.protocol("WM_DELETE_WINDOW", functions.onCloseApp)
        functions.setMainGeometry(self)
        

        self.dialogBoxOpen = False
        self.openSplash()  #Comment out splash screen for quick testing

        #Create main window frames and widgets and place the frames in grid
        searchFrame = ct.CTkFrame(self,
                                  fg_color="transparent"
                                  )
        
        recentFrame = ct.CTkFrame(self,
                                  fg_color="transparent"
                                  )
        buttonsFrame = ct.CTkFrame(self,
                                   fg_color="transparent"
                                   )

        searchHeader = ct.CTkLabel(searchFrame, 
                                   text="Search for any Wikipedia Page", 
                                   font=("Trebuchet MS", 50)
                                   )
        
        #random message choice selection
        rand = rd.randint(0, 5)
        match rand:
            case 1:
                searchHeader.configure(text="Scrape The Wikis")
            case 2:
                searchHeader.configure(text="Sources? WikiScrape.")
            case 3:
                searchHeader.configure(text="Wikipedia? Nah, WikiScrape!")
            case 4:
                searchHeader.configure(text='"Wikipedia is Unreliable"')
            case 5:
                searchHeader.configure(text="WikiScrape > Wikipedia")

        #function to disable/enable buttons
        def updateButtons(*args):
            text = searchVar.get()
            anyText = len(text) > 0
            currentState = searchButton.cget("state")

            if anyText and currentState == "disabled":
                self.bind("<Return>", lambda event: [functions.enterKeyHandler(event, searchBox, functions.onClickSearch), performSearch(recentBox)])
                searchButton.configure(state="normal")
                clearButton.configure(state="normal")
            elif not anyText and currentState == "normal":
                self.bind("<Return>", None)
                searchButton.configure(state="disabled")
                clearButton.configure(state="disabled")

        #Variables for handling button states and the "enter" key
        searchVar = ct.StringVar()
        searchVar.trace_add("write", updateButtons)


        
        searchBox = ct.CTkEntry(searchFrame, 
                                bg_color="transparent", 
                                width=500, 
                                height=50,
                                corner_radius=50,
                                placeholder_text="Enter your topic here:",
                                font=("Trebucet MS", 20),
                                textvariable=searchVar
                                )

        searchButton = ct.CTkButton(buttonsFrame, 
                                    text="Search", 
                                    font=("Trebuchet MS", 20), 
                                    width=150,
                                    text_color="white",
                                    state="disabled",
                                    command= lambda: [functions.onClickSearch(searchBox.get()), performSearch(recentBox)]
                                    )
        
        clearButton = ct.CTkButton(buttonsFrame,
                                   text="Clear",
                                   width=150,
                                   font=("Trebuchet MS", 20), 
                                   fg_color="white",
                                   text_color="dark blue",
                                   hover_color="grey",
                                   state="disabled",
                                   command= lambda: functions.onClickClear(searchBox),
                                   )
        
        recentLabel = ct.CTkLabel(recentFrame, 
                                  text="Recent Searches: ",
                                  font=("Trebuchet MS", 25)
                                  )

        recentBox = ct.CTkTextbox(recentFrame,
                                  width=350,
                                  height=180,
                                  font=("Trebuchet MS", 22)
                                  )
        
        copyrightBox = ct.CTkFrame(self,
                                  fg_color="transparent"
                                  )
        copyrightLabel = ct.CTkLabel(copyrightBox,
                                     font=("Trebuchet MS", 12),
                                     text="© 2024 WikiScrape, All Rights Reserved.")
        
        searchFrame.grid(column=1, row=1)
        buttonsFrame.grid(column=1, row=2)
        recentFrame.grid(column=1, row=3)
        
        copyrightBox.grid(column=1, row=4)
        copyrightLabel.grid(column=0, row=0, pady=10)

        #Format the main window grid and place widgets in frames
        formatting.formatMain(self)
    
        searchFrame.rowconfigure(1, weight=0)

        searchHeader.grid(column=0, row=0, columnspan=2)
        searchBox.grid(column=0, row=1, pady=5, columnspan=2)
        searchButton.grid(column=0, row=0, padx=10, pady=5, sticky=N)
        clearButton.grid(column=1, row=0, padx=10, pady=5, sticky=N)

        #Create empty list and perfSearch function to manage recent searches
        #Also place recent searches widgets
        recents = []
        recentBox.insert(1.0, "No recent searches")
        recentBox.configure(state="disabled")


        def performSearch(recentBox):
            latestSearch = searchBox.get()
            functions.updateRecentsList(latestSearch, recents, recentBox)

        recentLabel.grid(column=0, row=0, sticky=N)
        recentBox.grid(column=0, row=1, sticky=N)

    
    #Splash Initialization
    def openSplash(self):
        self.withdraw()
        splashScreen(self)

class splashScreen(ct.CTkToplevel):
    def __init__(self, app):
        super().__init__(app)

        self.title("WikiScrape")
        self.after(200, lambda: self.iconbitmap(functions.resourcepath("Images/Favicon.ico")))
        functions.setSplashGeometry(self)
        self.protocol("WM_DELETE_WINDOW", functions.onCloseSplash)

        splashLab = ct.CTkLabel(self, text="WikiScrape", font=("Trebuchet MS", 30, 'bold'))
        splashLab.place(relx=.5,rely=.35, anchor=ct.CENTER)

        self.progressbar = ct.CTkProgressBar(self, orientation="horizontal", mode='determinate', determinate_speed=1.5)
        self.progressbar.place(rely=.5, relx=.5, anchor=ct.CENTER)

        self.progressbar.set(0)
        self.runProg(0, app)
    
#Run and Update Progress Bar
    def runProg(self, i, app):
        if i <= 1.5:
            self.progressbar.set(i)
            i+=.01
            self.after(10, self.runProg, i, app)  # Schedule the next update
        else:
            self.after(300, lambda: self.closeSplash(app))  # Delay before closing splash

    def closeSplash(self, app):
        self.destroy()
        app.deiconify()



if __name__=="__main__":
    app = wikiScrapeApp()
    app.mainloop()

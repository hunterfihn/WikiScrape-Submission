from bs4 import BeautifulSoup
import requests
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
import sys
from PIL import Image, ImageTk
from dotenv import load_dotenv


#Global Variables and Functions

def resourcepath(relativepath):
        try:
            basepath = sys._MEIPASS
        except Exception:
            basepath = os.path.abspath(".")
        return os.path.join(basepath, relativepath)

dialogBoxOpen = False



#Create Splash Screen
def showSplash(root):
    splash = Toplevel()
    splash.title("WikiScrape")

    icon = resourcepath("Images/Favicon.ico")
    splash.iconbitmap(icon)

    splashWindowWidth = 400
    splashWindowHeight = 200

    screenWidth=root.winfo_screenwidth()
    screenHeight=root.winfo_screenheight()
    x = (screenWidth // 2 ) - (splashWindowWidth // 2)
    y = (screenHeight // 2) - (splashWindowHeight // 2)

    splash.geometry(f"{splashWindowWidth}x{splashWindowHeight}+{x}+{y}")
    splash.config(background="#80C0FF")

    splashLabel = Label(splash, text ="Loading WikiScrape...", font=('Segoe UI', 20, 'bold'), bg="#80C0FF")
    splashLabel.pack(expand=True)

    progress = ttk.Progressbar(splash, orient='horizontal', length=300, mode='determinate')
    progress.pack(pady=10)
    
    def updateProg(value):
        progress['value']=value
        splash.update_idletasks()
        if value < 100:
            splash.after(20, updateProg, value + 1)
        else:
            splash.after(500, lambda: [splash.destroy(), showMainWindow()])
    
    updateProg(0)


#Create GUI root, adjust size, set title and favicon
def showMainWindow():
    global root
    root = Tk()
    root.config(background="#80C0FF")

    mainWindowWidth = 1200
    mainWindowHeight = 625

    screenWidth=root.winfo_screenwidth()
    screenHeight=root.winfo_screenheight()
    x = (screenWidth // 2 ) - (mainWindowWidth // 2)
    y = (screenHeight // 2) - (mainWindowHeight // 2)

    root.geometry(f"{mainWindowWidth}x{mainWindowHeight}+{x}+{y}")

    root.title("WikiScrape")
    icon = resourcepath("Images/Favicon.ico")
    linkImage = resourcepath("Images/Link2.png")
    root.iconbitmap(icon)

    def onClose():
        root.destroy()
        sys.exit()

    root.protocol("WM_DELETE_WINDOW", onClose)


    #Create onClick for Clear Results and Clear Saved Buttons
    def onClickClear():
        resultsReturn.config(state = 'normal')
        resultsReturn.delete(1.0,'end')
        resultsReturn.insert('end', "Sources are just a topic away!", 'placeholder')
        resultsReturn.config(state = 'disabled')

    def onClickClearSaved():
        savedBox.delete(1.0, 'end')
    
    

    def onClickExport(toSaveInput):
        global dialogBoxOpen

        if not dialogBoxOpen:
            dialogBoxOpen = True

            contentToSave = toSaveInput.get(1.0, END)

            FP = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save File As"
            )

            if FP:
                try:
                    with open(FP, 'w') as file:
                        file.write(contentToSave)
                    print(f"File saved to: {FP}")
                except Exception as exec:
                    print(f"An error occurred: {exec}")

            dialogBoxOpen = False

    #Create onClick for Search Button, allow user to press "Enter" to search
    def onClickSearch():
        resultsReturn.config(state = 'normal')
        resultsReturn.delete(1.0, 'end')
        topic = e.get()
        topicParsed = topic.replace(" ", "_")

        genlink = "https://en.wikipedia.org/wiki/" + topicParsed
        sources = scrapeWiki(genlink)
        #sources_global = "\n".join(sources)

        if sources:
            resultsReturn.insert('end', topic, 'header')
            for source in sources:
                resultsReturn.insert('end', source, 'normal')
        elif(sources == []):
            resultsReturn.insert('end', "No Source Section Found")
        else:
            '''
            noReturn = Image.open(linkImage)
            noReturn = noReturn.resize((200, 200))
            noReturnPhoto = ImageTk.PhotoImage(noReturn)
            
            resultsReturn.image = noReturnPhoto
            resultsReturn.image_create(1.0, image=noReturnPhoto)
            '''
            resultsReturn.tag_add('center', 1.0)
            resultsReturn.insert('end', "Invalid Link! No Wikipedia page found.", 'invalid',)

        resultsReturn.config(state = 'disabled')
        

    def enterKeyHandler(event):
        if root.focus_get() == savedBox:
            savedBox.insert(INSERT, "\n")
        else:
            searchButton.invoke()

    root.bind("<Return>", enterKeyHandler)

    #Scrape from search term
    def scrapeWiki(input):
        try:
            targetPage = requests.get(input)
            if targetPage.status_code == 200:
                soup = BeautifulSoup(targetPage.text, "html.parser")
                references = soup.find_all("div", attrs= {'class':'reflist'})
                reflist = []
                for reference in references:
                    reflist.append(reference.text)
                return reflist
            else:
                print("Error -- Could not find page -- Code: " + str(targetPage.status_code))
        except requests.exceptions.RequestException as e:
            return []




    #Create and Fill Search/Description Frame
    searchFrame = Frame(root, pady=15, bg='#80C0FF', highlightbackground='#000000', highlightthickness=1)

    searchHeader = Label(searchFrame, text = "Enter your topic here:", font =('Segoe UI', 20, 'bold'), bg="#80C0FF")
    e = Entry(searchFrame, width=50, borderwidth=3, bg = '#adc9e5')
    searchButton = Button(searchFrame, text ="Search!", padx=15, command = onClickSearch)
    clearButton = Button(searchFrame, text = "Clear Results", padx=15, command = onClickClear)
    description = Label(searchFrame, text = "Welcome to WikiScrape! \n \nEnter your topic of choice and have the sources cited in the respective Wikipedia article in a matter of moments!", 
                        wraplength=300, font=('Segoe UI', 15), bg='#80C0FF')



    searchFrame.grid(column=0, row=0, sticky=NSEW)

    searchHeader.grid(column=0, row=0, sticky=NSEW)
    e.grid(column=0, row=1, padx=20)
    searchButton.grid(column=0, row=2, sticky=NW, padx=20, pady=5)
    clearButton.grid(column=0, row=2, sticky=NE, padx=20, pady=5)
    description.grid(column=0, row=3, padx=20, pady=15, sticky=N)



    #Create and Fill Results Frame
    resultsFrame = Frame(root, highlightbackground='#000000', highlightthickness=1)

    resultsReturn = Text(resultsFrame, wrap = 'word', height=20, width=150)
    resultsReturn.insert('end', "Sources are just a topic away!", 'placeholder')
    resultsReturn.config(state = 'disabled')


    resultsFrame.grid(column=1, row=0, sticky=NSEW)
    resultsReturn.pack(expand='true', fill='both', anchor=NW)

    scroll = Scrollbar(root, command=resultsReturn.yview)
    resultsReturn.config(yscrollcommand=scroll.set, bg = '#D3D3DF')
    scroll.grid(row=0, column=2, rowspan=1, sticky=NS+W)


    #Formate ResultsReturn
    resultsReturn.tag_config("header", font=('Segoe UI', 15, 'bold'))
    resultsReturn.tag_config("normal", font=('Segoe UI', 9))
    resultsReturn.tag_config("placeholder",font=('Segoe UI', 45, 'italic'), foreground='blue',justify='center', spacing1= 130)
    resultsReturn.tag_config("invalid", font=('Segou UI', 35, 'bold'), justify='center', foreground='brown', spacing1= 70)
    resultsReturn.tag_config("center", justify='center')



    #Create and Fill Saved Sources Frame
    savedFrame = Frame(root, padx=41, pady=15, bg='#80C0FF')

    savedHeader = Label(savedFrame, text="Saved Sources", font=('Courier', 25, 'bold'), bg = '#80C0FF')
    savedBox = Text(savedFrame, wrap='word', width=150, height= 15, font=('Courier', 11), bg = '#80C0FF')
    exportSavedButton = Button(savedFrame, text="Export", padx= 10, command= lambda: onClickExport(savedBox))

    savedFrame.grid(column=0, row=1, sticky=NSEW, columnspan=3)

    savedHeader.grid(column=0, row=0, sticky=W)
    savedBox.grid(column=0, row=1, sticky="NSEW")
    exportSavedButton.grid(column=0, row=0, sticky=E)



    #Create MiscFrame
    miscFrame = Frame(root, pady=5, bg='#80C0FF')

    miscFrame.grid(column=0, row=2, columnspan=2, sticky=EW)

    legal = Label(miscFrame, text = "© 2024 WikiScrape, All Rights Reserved.", font=('Courier', 7))
    quitButton = Button(miscFrame, text = "Quit", padx = 17, command = root.quit )
    clearSavedButton = Button(miscFrame, text="Clear Saved", padx=10, command=onClickClearSaved)

    legal.grid(column=0, row=0, sticky=W)
    quitButton.grid(column=2, row=0)
    clearSavedButton.grid(column=1, row=0) 


    #Create SizeGrip
    grip = ttk.Sizegrip(root)
    grip.grid(column=2,row=2, sticky=SE)
    root.resizable(True, True)



    #Column and Row Configuration
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=4)
    root.rowconfigure(0, weight=1)
    root.rowconfigure(1, weight=2)

    savedFrame.columnconfigure(0, weight=1)
    savedFrame.columnconfigure(1, weight=1)

    miscFrame.columnconfigure(0, weight=1)
    miscFrame.columnconfigure(1, weight=1)
    miscFrame.columnconfigure(2, weight=1)




if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    showSplash(root)
    root.mainloop()
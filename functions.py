import os
import sys
import requests
from bs4 import BeautifulSoup
import customtkinter as ct
from tkinter import filedialog
import google.generativeai as genai
from PIL import Image


googAPIkey = "" #insert gemini api key here, AI summary will not work without it
genai.configure(api_key=googAPIkey)

model = genai.GenerativeModel('gemini-1.5-flash')

#Global variable to avoid multiple save boxes
dialogBoxOpen = False


#Create onClose functions
def onCloseApp():
    sys.exit()
    self.destroy()
def onCloseSplash():
     sys.exit()
     self.destroy()

#Create Image pathing function
def resourcepath(relativepath):
        try:
            basepath = sys._MEIPASS
        except Exception:
            basepath = os.path.abspath(".")
        return os.path.join(basepath, relativepath)

#Create geometry setting functions
def setMainGeometry(self):
    self.mainWindowWidth = 1125
    self.mainWindowHeight = 625

    self.update_idletasks()

    screenWidth=self.winfo_screenwidth()
    screenHeight=self.winfo_screenheight()
    x = (screenWidth // 2 ) - (self.mainWindowWidth // 2)
    y = (screenHeight // 2) - (self.mainWindowHeight // 2)

    self.geometry(f"{self.mainWindowWidth}x{self.mainWindowHeight}+{x}+{y}")

def setSourceGeometry(self):
    self.mainWindowWidth = 800
    self.mainWindowHeight = 500

    self.update_idletasks()

    screenWidth=self.winfo_screenwidth()
    screenHeight=self.winfo_screenheight()
    x = (screenWidth // 4 ) - (self.mainWindowWidth // 4)
    y = (screenHeight // 4) - (self.mainWindowHeight // 4)

    self.geometry(f"{self.mainWindowWidth}x{self.mainWindowHeight}+{x}+{y}")

def setSplashGeometry(self):
    self.splashWindowWidth = 400
    self.splashWindowHeight = 200

    self.update_idletasks()

    screenWidth=self.winfo_screenwidth()
    screenHeight=self.winfo_screenheight()
    x = (screenWidth // 2 ) - (self.splashWindowWidth // 2)
    y = (screenHeight // 2) - (self.splashWindowHeight // 2)

    self.geometry(f"{self.splashWindowWidth}x{self.splashWindowHeight}+{x}+{y}")

#Format sources window (circular call if put in formatting file)
def formatSourcesWin(self):
    self.grid_rowconfigure(0, weight=1)
    self.grid_rowconfigure(1, weight=0)
    self.grid_rowconfigure(2, weight=0)
    self.grid_rowconfigure(3, weight=2)

    self.grid_columnconfigure(0, weight=1)
    self.grid_columnconfigure(1, weight=1)
    self.grid_columnconfigure(2, weight=1)

#Create scraping function
def scrapeWiki(inp):
    try:
        targetPage = requests.get(inp)
        if targetPage.status_code == 200:
            soup = BeautifulSoup(targetPage.text, "html.parser")
            references = soup.find_all("div", attrs={'class': 'reflist'})
            bibliography = soup.find_all("div", attrs={'class': 'refbegin'})
            reflist = []

            for reference in references:
                entries = reference.find_all("li")
                for entry in entries:
                    # Extract the text of the reference
                    referenceText = entry.text.strip()

                    # Find the hyperlink within the reference, if it exists
                    link = entry.find('a', attrs={'class': "external text"}, href=True)
                    hyperlink = link['href'] if link else None

                    # Ensure the hyperlink is absolute if it is a relative URL
                    if hyperlink and not hyperlink.startswith("http"):
                        hyperlink = f"https://en.wikipedia.org{hyperlink}"

                    # Append the text and hyperlink (if available) to the reference list
                    if hyperlink:
                        reflist.append(f"{referenceText} \n (Link: {hyperlink})")
                    else:
                        reflist.append(referenceText)

            for bibentry in bibliography:
                bibentries = bibentry.find_all("li")
                for entry in bibentries:
                    # Extract the text of the bibliography entry
                    bibText = entry.text.strip()
                    link = entry.find('a', attrs={'class': "external text"}, href=True)
                    hyperlink = link['href'] if link else None

                    # Ensure the hyperlink is absolute if it is a relative URL
                    if hyperlink and not hyperlink.startswith("http"):
                        hyperlink = f"https://en.wikipedia.org{hyperlink}"

                    # Append the text and hyperlink (if available) to the reference list
                    if hyperlink:
                        reflist.append(f"{bibText} \n (Link: {hyperlink})")
                    else:
                        reflist.append(bibText)
                    reflist.append(bibText)

                
            return reflist
        else:
            print("Error -- Could not find page -- Code: " + str(targetPage.status_code))
    except requests.exceptions.RequestException as e:
        print(f"Request Exception: {e}")
        return []

#Create Search and Clear onClick
def onClickSearch(inp):
    topicParsed = inp.replace(" ", "_")

    genlink = "https://en.wikipedia.org/wiki/" + topicParsed
    sources = scrapeWiki(genlink)

    if sources:
        sourcesWin(inp, sources, genlink)
    elif(sources == []):
        noSourcesWin(inp, sources)
    else:
        invalidLinkWin()

def onClickClear(entry):
    entry.delete(0, 'end')

#Create and update recent searches
def updateRecentsDisplay(recentsDisplay, recents):
    recentsDisplay.configure(state="normal")
    recentsDisplay.delete(1.0, "end")

    for i, search in enumerate(recents, 1):
        recentsDisplay.insert("end", f"{i}. {search}\n")
    
    recentsDisplay.configure(state="disabled")

def updateRecentsList(searchTerm, recents, recentsDisplay):
    if searchTerm:
        if searchTerm in recents:
            recents.remove(searchTerm)

        recents.insert(0, searchTerm)

        if len(recents) > 5:
            recents.pop(5)
        
        updateRecentsDisplay(recentsDisplay, recents)

#Create sources, no sources, and invalid link windows
def sourcesWin(inp, sources, genlink):
    sourcesWindow = ct.CTkToplevel()
    sourcesWindow.after(200, lambda: sourcesWindow.iconbitmap(resourcepath("Images/Favicon.ico")))
    sourcesWindow.title(f"{inp} Sources")
    sourcesWindow.geometry(setSourceGeometry(sourcesWindow))
    sourcesWindow.lift()
    sourcesWindow.focus()
    sourcesWindow.attributes('-topmost', True)
    sourcesWindow.after(10, lambda: sourcesWindow.attributes('-topmost', False))
    

    sourcesWindow.grid_columnconfigure(0, weight=2)
    sourcesWindow.grid_columnconfigure(1, weight=1)
    sourcesWindow.grid_rowconfigure(0, weight=1)

    sourcesFrame = ct.CTkFrame(sourcesWindow)
    widgetsFrame = ct.CTkFrame(sourcesWindow)

    widgetsFrame.rowconfigure(0, weight=1)
    widgetsFrame.rowconfigure(1, weight=1)
    widgetsFrame.rowconfigure(2, weight=1)
    widgetsFrame.rowconfigure(3, weight=1)


    sourcesFrame.grid(column=0, row=0, sticky="NSEW")
    widgetsFrame.grid(column=1, row=0, sticky="NSEW")

    

    exportButton = ct.CTkButton(widgetsFrame,
                                text="Export",
                                font=("Trebuchet MS", 17),
                                command= lambda: onClickExport(checkedSources)
                                )
    
    summarizeButton = ct.CTkButton(widgetsFrame,
                                   text="AI Summary",
                                   font=("Trebuchet MS", 17),
                                   command= lambda: onClickSummarize(inp, checkedSources, genlink)
                                   )
    summarizeButton.grid(column=0, row=2)
    exportButton.grid(column=0, row=1)

    scrollFrame = newScrollFrame(sourcesFrame)
    checkedSources = parseSourceData(sources, scrollFrame, exportButton, summarizeButton)

def noSourcesWin(inp, sources):
    sourcesWindow = ct.CTkToplevel()
    sourcesWindow.title(f"{inp} Sources")
    sourcesWindow.after(200, lambda: sourcesWindow.iconbitmap(resourcepath("Images/Favicon.ico")))
    sourcesWindow.geometry(setSourceGeometry(sourcesWindow))
    sourcesWindow.lift()
    sourcesWindow.focus()
    sourcesWindow.attributes('-topmost', True)
    sourcesWindow.after(10, lambda: sourcesWindow.attributes('-topmost', False))
    noSourcesLabel = ct.CTkLabel(sourcesWindow,
                                       font=("Trebuchet MS", 55, "underline"),
                                       text = "No Sources Found"
                                       )
    noSourcesExplanationLabel = ct.CTkLabel(sourcesWindow,
                                       font=("Trebuchet MS", 30),
                                       text = f"A Wikipedia Page Exists For '{inp}', But \n It Does Not Have A Reference Section."
                                       )
    noSourcesLabel.pack()
    noSourcesExplanationLabel.pack(pady = 50)

def invalidLinkWin():
    sourcesWindow = ct.CTkToplevel()
    sourcesWindow.title(f"Link Not Found!")
    sourcesWindow.after(200, lambda: sourcesWindow.iconbitmap(resourcepath("Images/Favicon.ico")))
    sourcesWindow.geometry(setSourceGeometry(sourcesWindow))
    sourcesWindow.lift()
    sourcesWindow.focus()
    sourcesWindow.attributes('-topmost', True)
    sourcesWindow.after(10, lambda: sourcesWindow.attributes('-topmost', False))

    path = resourcepath("Images/Link2.png")
    image = Image.open(path)
    setimage=ct.CTkImage(image, size= (200,200))

    noLink = ct.CTkLabel(sourcesWindow,
                             text="",
                             image= setimage
                             )
    noLinkMsg = ct.CTkLabel(sourcesWindow,
                            text ="Invalid Link\n Page Does Not Exist!",
                            font=("Trebuchet MS", 35),
                            pady = 15)
    noLink.pack()
    noLinkMsg.pack()


# Parse and change sources list to checkboxes with wrapped text
def parseSourceData(sources, frame, exportButton, summaryButton, maxLen=80):  # Set max line length based on frame size

    selectedSources = []

    exportButton.configure(state="disabled")
    summaryButton.configure(state="disabled")

    def onCheckTog(source, var):
        if var.get():
            selectedSources.append(source)
            exportButton.configure(state="normal")
            summaryButton.configure(state="normal")
        else:
            selectedSources.remove(source)
            if(len(selectedSources) == 0):
                exportButton.configure(state="disabled")
                summaryButton.configure(state="disabled")

    for i, source in enumerate(sources):
        sourcetext = source.split(" \n")[0]
        wrappedSource = wrapText(sourcetext, maxLen)
        var = ct.BooleanVar()
        checkbox = ct.CTkCheckBox(frame,
                                  text=wrappedSource,
                                  variable=var,
                                  onvalue=True,
                                  offvalue=False,
                                  command=lambda s=source, v=var: onCheckTog(s, v))
        checkbox.grid(row=i, column=0, sticky="w", padx=5, pady=5)

    return selectedSources

#frame to handle scrolling and scrollbar, functions
def newScrollFrame(parentFrame):
    canvas = ct.CTkCanvas(parentFrame, borderwidth = 0, background = "#303030", highlightthickness = 0)

    scrollbar = ct.CTkScrollbar(parentFrame, orientation="vertical", command=canvas.yview)
    scrollableFrame = ct.CTkFrame(canvas)

    scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.grid(row=0, column=0, sticky="NSEW")
    scrollbar.grid(row=0, column=1, sticky="NS")

    bindMouseWheel(canvas)

    canvas.grid_columnconfigure(1, weight=0)

    parentFrame.grid_rowconfigure(0, weight=1)
    parentFrame.grid_columnconfigure(0, weight=1)
    return scrollableFrame

def bindMouseWheel(canvas):
     canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda event: onMouseWheel(event, canvas)))
     canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

def onMouseWheel(event, canvas):
     canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

#text wrap to fit area
def wrapText(text, maxLen):
    words = text.split()
    wrappedLines = []
    curLine = []
    curLength = 0

    for word in words:
        if curLength + len(word) + 1 > maxLen:
            wrappedLines.append(' '.join(curLine))
            curLine = [word]
            curLength = len(word)
        else:
            curLine.append(word)
            curLength += len(word) + 1

    wrappedLines.append(' '.join(curLine))
    return '\n'.join(wrappedLines)

#function for AI summary
def onClickSummarize(inp, sources, genlink):
    aiResultsWin = ct.CTkToplevel()
    aiResultsWin.title(f"{inp} AI Summary")
    aiResultsWin.after(200, lambda: aiResultsWin.iconbitmap(resourcepath("Images/Favicon.ico")))
    aiResultsWin.geometry(setSourceGeometry(aiResultsWin))
    aiResultsWin.lift()
    aiResultsWin.focus()
    aiResultsWin.attributes('-topmost', True)
    aiResultsWin.after(10, lambda: aiResultsWin.attributes('-topmost', False))

    aiResultsFrame = ct.CTkFrame(aiResultsWin)
    aiResultsText = ct.CTkTextbox(aiResultsFrame)

    aiResultsWin.rowconfigure(0, weight=1)
    aiResultsWin.columnconfigure(0, weight=1)
    aiResultsFrame.rowconfigure(0, weight=1)
    aiResultsFrame.columnconfigure(0, weight=1)

    aiResultsFrame.grid(column=0, row=0, sticky="NSEW")
    aiResultsText.grid(column=0, row=0, sticky="NSEW")


    all_summaries = []
    
    for source in sources:
        response = model.generate_content(f"""Considering the Wikipedia page found at {genlink},
                                          provide a 1-2 sentence summary of the source given in the context of the article.
                                          Please visit the page and find the context in which this source is used.
                                          Print the title of the source above the summary. The title should be the actual
                                          title of the source that published the relevant information, not just the Wikipedia
                                          shorthand citation. Below the summary, if it is a website
                                          please provide the URL for the website of the source; 
                                          if it is from a book, please provide the title and the link also provided.
                                          Source: {source}""")
        all_summaries.append(response.text)
    
    # Print all summaries
    for summary in all_summaries:
        aiResultsText.configure(state="normal")
        aiResultsText.insert("end",f"{summary}\n")
        aiResultsText.insert("end","-------------------------------------------------------------------------------------\n")
        aiResultsText.configure(state="disabled")
    

#export function
def onClickExport(sources):
    global dialogBoxOpen
    cleanedSources = [source.strip() for source in sources]  # Remove newlines and extra spaces
    if not dialogBoxOpen:
        dialogBoxOpen = True

        FP = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Save File As"
            )
        
        if FP:
            try:
                with open(FP, 'w') as file:
                    file.write("Exported Sources: \n \n")
                    for source in cleanedSources:
                        file.write(f"{source}\n\n")
                print(f"File saved to {FP}")
            except Exception as e:
                print(f"Save error {e}")

        dialogBoxOpen = False


#Event Handling
def enterKeyHandler(event, searchBox=None, searchFunction=None):
    if searchBox and searchFunction:
        searchFunction(searchBox.get()) 
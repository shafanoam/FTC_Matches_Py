import tkinter as tk
from tkinter import messagebox
import requests
import base64
import json


# print(requests.get(url="https://ftc-api.firstinspires.org/v2.0/2024/teams?teamNumber=2",
#                    headers={"Authorization": "Basic " + base64.b64encode("shafanoam:59A5D18B-9FD0-46CF-8ECB-F55DE8B27354".encode()).decode()}).json())


def setup_match_list(team=str(), event=str(), key=str(), year=str()):

    # for API purposes
    team = int(team)

    # loading match list
    matchJson = requests.get(
        url=f"https://ftc-api.firstinspires.org/v2.0/{year}/schedule/{event}/qual/hybrid",
        headers={"Authorization": "Basic "
                                  + base64.b64encode(key.encode()).decode()})

    print(matchJson)
    matchJson = matchJson.json()
    matchList = []

    for match in matchJson["schedule"]:
        inmatch = False  # temp variable

        if match["teams"][0]["teamNumber"] == team:
            inmatch = True
        elif match["teams"][1]["teamNumber"] == team:
            inmatch = True
        elif match["teams"][2]["teamNumber"] == team:
            inmatch = True
        elif match["teams"][3]["teamNumber"] == team:
            inmatch = True

        if inmatch:
            matchList.append(match)

    print(matchList)
    # delete old stuff in frame
    for match in scrollFrame.winfo_children():
        match.destroy()
    matchShowings = []

    # displayFirst = matchDisplay(scrollFrame, match_name=matchList[0]["description"])
    # displayFirst.pack()

    i = 0
    for item in matchList:
        matchShowings.append(matchDisplay(scrollFrame,
                                          match_name=matchList[i]["description"],
                                          red_score=matchList[i]["scoreRedFinal"],
                                          blue_score=matchList[i]["scoreBlueFinal"],
                                          match_status="TODO: match status"
                                          ).pack())
        i += 1


    return [True, "9fohsohfsoe"]


# verify that the API key is valid. if error code is not 200 (means OK), return it.
def verify_api_connection(key=str(), year=str()):
    # if the API is bad, sometimes it just zoinks out...
    try:
        code = requests.get(f"https://ftc-api.firstinspires.org/v2.0/{year}",
                            headers={"Authorization": "Basic " + base64.b64encode(key.encode()).decode()}).status_code
    except:
        return "Bad API\n The API key you used is invalid. Make sure it's in the same format as the" \
               " following example:\nsampleuser:7eaa6338-a097-4221-ac04-b6120fcc4d49"

    if code == 200:
        return "200"
    elif code == 400:
        return "400: Malformed Request\nPlease contact the developers for help."
    elif code == 401:
        return "401: Unauthorized\nThe API key you used is invalid. Make sure it's in the same format as the" \
               " following example:\nsampleuser:7eaa6338-a097-4221-ac04-b6120fcc4d49"
    elif code == 404:
        return "404: Event Not Found\nThis happened while simply verifying the API key, so if you're seeing this, " \
               "something's gone seriously wrong. Please contact the developers for help."
    elif code == 500:
        return "500: Internal Server Error\nThe FTC-Events server encountered an unexpected condition which prevented" \
               " it from fulfilling the request. Please try again in a few minutes."
    elif code == 501:
        return "501: Request Did Not Match Any Current API Pattern\nThis happened while simply verifying the API key," \
               " so if you're seeing this, something's gone seriously wrong. Please contact the developers for help."
    elif code == 503:
        return "503: Service Unavailable\nThe server is currently unable to handle the request due to a temporary" \
               " overloading or maintenance of the server."



# returns the name if it worked, False if it didn't.
def get_team_name(key=str(), number=str(), year=str()):
    teamInfoJson = requests.get(url=f"https://ftc-api.firstinspires.org/v2.0/{year}/teams?teamNumber={number}",
                                headers={"Authorization": "Basic "
                                                          + base64.b64encode(key.encode()).decode()}).json()

    # check if team even exists! The second half of the 'if' is in case a team's name contains "malformed" lol
    if ("Malformed" in teamInfoJson) and ("{" not in teamInfoJson):
        return False
    else:
        return str(teamInfoJson["teams"][0]["nameShort"])


def verify_and_start():

    if not str.isdigit(teamNum.get()):
        messagebox.showerror(title="Team Number NaN", message="Ensure the team number is a valid number.")
        return

    root.withdraw()

    api_result = verify_api_connection(key=apiKey.get(), year=eventYear.get())
    if api_result == "200":
        pass
    else:
        root.deiconify()
        messagebox.showerror(title="Uh oh!", message=api_result)

    teamName = get_team_name(key=apiKey.get(), number=teamNum.get(), year=eventYear.get())
    if teamName:
        teamNameLabel.configure(text=teamName)
    else:
        root.deiconify()
        messagebox.showerror(title="Team Error",
                             message="Could not find a team with the number " + str(teamNum.get()) + ".")
        return

    global eventDict
    # eventDict = json.loads(eventReturn[1])

    # SETUP AND OPEN MATCHES WINDOW
    mainViewerWindow.title("FTC Matches: Team " + str(teamNum.get()))
    teamNumberLabel.configure(text=str(teamNum.get()))

    setup_match_list(key=apiKey.get(), team=teamNum.get(), event=eventCode.get(), year=eventYear.get())

    mainViewerWindow.deiconify()




root = tk.Tk()
root.geometry("400x300")
root.resizable(False, False)

root.title("'FTC Matches' by 7159 Robo Ravens")

# team number input
teamNum = tk.StringVar()
teamNumLabel = tk.Label(root, text="Team Number")
teamNumLabel.place(relx=0.5, rely=0.1, relwidth=0.5, anchor="center")
teamNumEntry = tk.Entry(root, textvariable=teamNum)
teamNumEntry.place(relx=0.5, rely=0.2, relwidth=0.5, anchor="center")

# event code input
eventCode = tk.StringVar()
eventCodeLabel = tk.Label(root, text="Event Code")
eventCodeLabel.place(relx=0.333, rely=0.35, relwidth=0.25, anchor="center")
eventCodeEntry = tk.Entry(root, textvariable=eventCode)
eventCodeEntry.place(relx=0.333, rely=0.45, relwidth=0.25, anchor="center")

# event year input
eventYear = tk.StringVar()
eventYearLabel = tk.Label(root, text="Event Year")
eventYearLabel.place(relx=0.666, rely=0.35, relwidth=0.25, anchor="center")
eventYearEntry = tk.Entry(root, textvariable=eventYear)
eventYearEntry.place(relx=0.666, rely=0.45, relwidth=0.25, anchor="center")

# API key input
apiKey = tk.StringVar()
apiKey.set("shafanoam:59A5D18B-9FD0-46CF-8ECB-F55DE8B27354")
apiKeyLabel = tk.Label(root, text="API: 'Username:Token'")
apiKeyLabel.place(relx=0.5, rely=0.6, relwidth=0.5, anchor="center")
apiKeyEntry = tk.Entry(root, textvariable=apiKey, show='*')
apiKeyEntry.place(relx=0.5, rely=0.7, relwidth=0.5, anchor="center")

# start using program button
startProgramButton = tk.Button(root, text="Start", state="disabled", command=verify_and_start)
startProgramButton.place(relx=0.5, rely=0.85, relwidth=0.25, anchor="center")


# checks if the user really wants to exit
def exiter():
    if messagebox.askokcancel(title="Exit FTC Matches", message="Are you sure you want to exit FTC Matches?"):
        root.destroy()


# exit upon closing
root.protocol("WM_DELETE_WINDOW", exiter)


# ACTUAL VIEWING WINDOW

mainViewerWindow = tk.Toplevel(root)
# mainViewerWindow.withdraw()

mainViewerWindow.title("FTC Matches: Team " + str(teamNum.get()))
mainViewerWindow.geometry("800x600")
mainViewerWindow.minsize(640,480)

# create top banner
topBannerFrame = tk.Frame(mainViewerWindow, bg="red")
topBannerFrame.place(relx=0, rely=0, relwidth=1, relheight=0.15)

ftcMatchesLabel = tk.Label(topBannerFrame, fg='white', bg='red', font='Helvetica 30', text="FTC Matches")
ftcMatchesLabel.place(relx=0.05, rely=0.5, anchor="w")

teamNumberLabel = tk.Label(topBannerFrame, fg='white', bg='red', font='Helvetica 18')
teamNumberLabel.place(relx=0.95, rely=0.3333, anchor="e")
teamNameLabel = tk.Label(topBannerFrame, fg='white', bg='red', font='Helvetica 18')
teamNameLabel.place(relx=0.95, rely=0.6666, anchor="e")


# SCROLLING AREA STUFF

# scrolling frame container
sscrollingContainer = tk.LabelFrame(mainViewerWindow, text="Matches")
sscrollcanvas = tk.Canvas(sscrollingContainer)
sscrollbar = tk.Scrollbar(sscrollingContainer, orient="vertical", command=sscrollcanvas.yview)
scrollFrame = tk.Frame(sscrollcanvas)


# setting up scrollable area that updates whenever contents of scrollFrame change
scrollFrame.bind("<Configure>", lambda e: sscrollcanvas.configure(scrollregion=sscrollcanvas.bbox("all")))
# mainViewerWindow.bind("<Configure>", lambda e: sscrollcanvas.configure(scrollregion=sscrollcanvas.bbox("all")))

# drawing scrollFrame within the canvas
sscrollcanvas.create_window((0, 0), window=scrollFrame, anchor='nw')
sscrollcanvas.configure(yscrollcommand=sscrollbar.set)

sscrollingContainer.place(relx=0, rely=0.15, relwidth=1, relheight=0.65)
sscrollcanvas.pack(side="left", fill="both", expand=True)
sscrollbar.pack(side="right", fill="y")


# create a class for the group of stuff that form a match in the match viewer
class matchDisplay(tk.Frame):
    def __init__(self, parent,
                 match_name=str(), red_score=int(), blue_score=str(), match_status=str()):
        tk.Frame.__init__(self, parent)
        # self.tkraise()
        self.matchNameLabel = tk.Label(self, text=match_name, font="helvetica 18")
        self.matchNameLabel.grid(row=0, column=0, sticky="ew")

        self.redScoreLabel = tk.Label(self, text=(red_score if red_score != None else "???"),
                                      bg="red", fg="white", font="helvetica 24")
        self.redScoreLabel.grid(row=0, column=1, sticky="ew")

        self.blueScoreLabel = tk.Label(self, text=(blue_score if blue_score != None else "???"),
                                      bg="blue", fg="white", font="helvetica 24")
        self.blueScoreLabel.grid(row=0, column=2, sticky="ew")

        self.matchStatusLabel = tk.Label(self, text=match_status, font="helvetica 18")
        self.matchStatusLabel.grid(row=0, column=3, sticky="ew")

        # configure the sizing of the first row
        self.rowconfigure(0, minsize=75)
        self.columnconfigure(0, minsize=200)
        self.columnconfigure(1, minsize=100)
        self.columnconfigure(2, minsize=100)
        self.columnconfigure(3, minsize=200)


# return to root upon closing
def return_to_rooter():
    mainViewerWindow.withdraw()
    root.deiconify()


# return upon closing
mainViewerWindow.protocol("WM_DELETE_WINDOW", return_to_rooter)


while True:
    # update "start" button
    if teamNum.get() and eventCode.get() and eventYear.get() and apiKey.get():
        startProgramButton.configure(state="normal")
    else:
        startProgramButton.configure(state="disabled")

    root.update()
    mainViewerWindow.update()

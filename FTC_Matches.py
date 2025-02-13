import tkinter as tk
from tkinter import messagebox
# import requests
import json


# TODO: ARIANNA! Get hybrid schedule here, returning [True, (JSON)] if success and [False, error code] if failed.
def get_schedule_json(Team, Event):
    return [True, "9fohsohfsoe"]


def get_team_name():
    transformed_json = {"teams": [{"teamNumber": 4466, "nameFull": "R.A.B.B.I."},
                                  {"teamNumber": 7159, "nameFull": "Robo Ravens"}]}
    name = False
    for i in range(len(transformed_json["teams"])):
        if str(transformed_json["teams"][i]["teamNumber"]) == teamNum.get():
            name = str(transformed_json["teams"][i]["nameFull"])
    return name


def verify_and_start():
    if not str.isdigit(teamNum.get()):
        messagebox.showerror(title="Team Number NaN", message="Ensure the team number is a valid number.")
        return

    eventReturn = get_schedule_json(teamNum.get(), eventCode.get())
    if not eventReturn[0]:
        messagebox.showerror(title="EVENT RETRIEVAL ERROR",
                             message="The event could not be found. Ensure it's spelled correctly!" + eventReturn[1])
    else:
        root.withdraw()

        teamName = get_team_name()
        if teamName:
            teamNameLabel.configure(text=teamName)
        else:
            root.deiconify()
            messagebox.showerror(title="Team Error",
                                 message="Could not find a team with the number " + str(teamNum.get()) + ".")
            return

        global eventDict
        # eventDict = json.loads(eventReturn[1])

        # setup and open matches window
        mainViewerWindow.title("FTC Matches: Team " + str(teamNum.get()))
        teamNumberLabel.configure(text=str(teamNum.get()))
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
eventCodeLabel.place(relx=0.5, rely=0.35, relwidth=0.5, anchor="center")
eventCodeEntry = tk.Entry(root, textvariable=eventCode)
eventCodeEntry.place(relx=0.5, rely=0.45, relwidth=0.5, anchor="center")

# event code input
apiKey = tk.StringVar()
apiKeyLabel = tk.Label(root, text="API Key")
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
mainViewerWindow.withdraw()

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

# drawing scrollFrame within the canvas
sscrollcanvas.create_window((0, 0), window=scrollFrame, anchor='nw')
sscrollcanvas.configure(yscrollcommand=sscrollbar.set)

sscrollingContainer.place(relx=0, rely=0.15, relwidth=1, relheight=0.65)
sscrollcanvas.pack(side="left", fill="both", expand=True)
sscrollbar.pack(side="right", fill="y")


# return to root upon closing
def return_to_rooter():
    mainViewerWindow.withdraw()
    root.deiconify()


# return upon closing
mainViewerWindow.protocol("WM_DELETE_WINDOW", return_to_rooter)


while True:
    # update "start" button
    if teamNum.get() and eventCode.get() and apiKey.get():
        startProgramButton.configure(state="normal")
    else:
        startProgramButton.configure(state="disabled")

    root.update()
    mainViewerWindow.update()

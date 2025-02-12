import tkinter as tk
from tkinter import messagebox


# TODO: ARIANNA! EVENT CODE VERIFICATION HERE!
def verifyEventCode():
    return False


def verifyAndStart():
    if not str.isdigit(teamNum.get()):
        messagebox.showerror(title="Team Number NaN", message="Ensure the team number is a valid number.")
        return
    elif not verifyEventCode():
        messagebox.showerror(title="Event Code Error", message="Check the event code and try again.")
    else:
        root.withdraw()


root = tk.Tk()
root.geometry("400x300")
root.resizable(False, False)

root.title("FTC Matches, Developed by 7159 Robo Ravens")

# team number input
teamNum = tk.StringVar()
teamNumLabel = tk.Label(root, text="Team Number")
teamNumLabel.place(relx=0.5, rely=0.15, relwidth=0.5, anchor="center")
teamNumEntry = tk.Entry(root, textvariable=teamNum)
teamNumEntry.place(relx=0.5, rely=0.25, relwidth=0.5, anchor="center")

# event code input
eventCode = tk.StringVar()
eventCodeLabel = tk.Label(root, text="Event Code")
eventCodeLabel.place(relx=0.5, rely=0.4, relwidth=0.5, anchor="center")
eventCodeEntry = tk.Entry(root, textvariable=eventCode)
eventCodeEntry.place(relx=0.5, rely=0.5, relwidth=0.5, anchor="center")

# start using program button
startProgramButton = tk.Button(root, text="Start", state="disabled", command=verifyAndStart)
startProgramButton.place(relx=0.5, rely=0.65, relwidth=0.25, anchor="center")

# hides root window
# root.withdraw()


while True:
    # update "start" button
    if teamNum.get() and eventCode.get():
        startProgramButton.configure(state="normal")
    else:
        startProgramButton.configure(state="disabled")
    root.update()

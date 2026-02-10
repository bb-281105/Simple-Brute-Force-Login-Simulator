import tkinter as tk
from tkinter import messagebox
from logger import log_event

# ---- Key capture function (APP-ONLY) ----
def capture_key(event):
    if event.char:
        log_event("KEY", event.char)
    else:
        log_event("SPECIAL_KEY", event.keysym)

# ---- Submit handler ----
def submit():
    user = username.get()
    pwd = password.get()

    log_event("USERNAME_SUBMIT", user)
    log_event("PASSWORD_SUBMIT", "*" * len(pwd))

    messagebox.showinfo("Demo", "Login submitted (educational demo).")

# ---- GUI ----
root = tk.Tk()
root.title("copy_tip – Secure Login (Demo)")
root.geometry("360x260")

# Consent banner
messagebox.showwarning(
    "Consent Required",
    "This educational demo captures keystrokes typed\n"
    "INSIDE this window only.\n\n"
    "For ethical hacking learning purposes."
)

tk.Label(root, text="Username").pack(pady=5)
username = tk.Entry(root)
username.pack()
username.bind("<Key>", capture_key)

tk.Label(root, text="Password").pack(pady=5)
password = tk.Entry(root, show="*")
password.pack()
password.bind("<Key>", capture_key)

tk.Button(root, text="Login", command=submit).pack(pady=20)

root.mainloop()

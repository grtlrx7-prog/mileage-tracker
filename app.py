import threading
import os
import tkinter as tk
from tkinter import messagebox

from backend.parsers.sars_export import parse_timeline


def run_export(status_label, button):

    try:
        status_label.config(text="Running SARS export...")
        button.config(state="disabled")

        parse_timeline()

        status_label.config(text="Done ✔")

        messagebox.showinfo(
            "SARS Export",
            "Report generated successfully!"
        )

        os.startfile(os.path.join("backend", "exports"))

    except Exception as e:
        status_label.config(text="Error ❌")
        messagebox.showerror("Error", str(e))

    finally:
        button.config(state="normal")


def start(status_label, button):
    threading.Thread(
        target=run_export,
        args=(status_label, button),
        daemon=True
    ).start()


def main():

    app = tk.Tk()
    app.title("SARS Mileage App")
    app.geometry("420x220")

    tk.Label(
        app,
        text="🚗 SARS Mileage System",
        font=("Arial", 14, "bold")
    ).pack(pady=15)

    status_label = tk.Label(app, text="Ready")
    status_label.pack(pady=10)

    button = tk.Button(
        app,
        text="Generate SARS Report",
        bg="#1F4E78",
        fg="white",
        width=25,
        height=2,
        command=lambda: start(status_label, button)
    )
    button.pack(pady=20)

    app.mainloop()


if __name__ == "__main__":
    main()
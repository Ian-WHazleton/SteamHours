import tkinter as tk

root = tk.Tk()
root.configure(bg="#222")
frame = tk.Frame(root, bg="#444", bd=0, relief="flat")
frame.pack(padx=40, pady=40)
label = tk.Label(frame, text="Lighter Box with White Text", bg="#444", fg="white", font=("Arial", 16))
label.pack(padx=30, pady=30)
root.title("Tkinter Dark UI")
root.geometry("400x200")
root.mainloop()
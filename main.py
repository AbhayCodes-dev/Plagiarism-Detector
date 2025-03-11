import tkinter as tk
from tkinter import filedialog
from difflib import SequenceMatcher

def load_file(entry, text_box):
    path = filedialog.askopenfilename()
    if path:
        entry.delete(0, tk.END)
        entry.insert(tk.END, path)
        with open(path, 'r') as file:
            content = file.read()
            text_box.delete(1.0, tk.END)
            text_box.insert(tk.END, content)

def compare_texts(text_box1, text_box2, result_box):
    content1 = text_box1.get(1.0, tk.END).strip()
    content2 = text_box2.get(1.0, tk.END).strip()
    
    if not content1 or not content2:
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, "Please load or enter text in both fields.")
        return
    
    similarity = SequenceMatcher(None, content1, content2).ratio()
    percentage = int(similarity * 100)
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, f"Similarity: {percentage}%")
    
    text_box1.tag_remove("match", "1.0", tk.END)
    text_box2.tag_remove("match", "1.0", tk.END)
    
    for tag, start1, end1, start2, end2 in SequenceMatcher(None, content1, content2).get_opcodes():
        if tag == "equal":
            text_box1.tag_add("match", f"1.0+{start1}c", f"1.0+{end1}c")
            text_box2.tag_add("match", f"1.0+{start2}c", f"1.0+{end2}c")

def reset_fields():
    text_box1.delete(1.0, tk.END)
    text_box2.delete(1.0, tk.END)
    result_box.delete(1.0, tk.END)
    file_input1.delete(0, tk.END)
    file_input2.delete(0, tk.END)

root = tk.Tk()
root.title("Text Similarity Checker")
root.configure(bg="#2C3E50")
root.geometry(f"{root.winfo_screenwidth()}x{root.winfo_screenheight()}+0+0")
root.state("zoomed")

def create_button(text, command):
    return tk.Button(root, text=text, command=command, bg="#E74C3C", fg="white", font=("Arial", 12, "bold"),
                     bd=0, relief=tk.RIDGE, padx=20, pady=10, borderwidth=5, highlightthickness=0,
                     activebackground="#C0392B", cursor="hand2", width=15, height=2)

frame = tk.Frame(root, bg="#34495E")
frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

text_box1 = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12))
text_box1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

text_box2 = tk.Text(frame, wrap=tk.WORD, font=("Arial", 12))
text_box2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

file_input1 = tk.Entry(frame, font=("Arial", 10))
file_input1.grid(row=1, column=0, pady=5, sticky="ew")

file_input2 = tk.Entry(frame, font=("Arial", 10))
file_input2.grid(row=1, column=1, pady=5, sticky="ew")

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(0, weight=1)

button_frame = tk.Frame(root, bg="#2C3E50")
button_frame.pack(pady=10)

load_button1 = create_button("Load File 1", lambda: load_file(file_input1, text_box1))
load_button1.pack(side=tk.LEFT, padx=5)

load_button2 = create_button("Load File 2", lambda: load_file(file_input2, text_box2))
load_button2.pack(side=tk.LEFT, padx=5)

compare_button = create_button("Compare", lambda: compare_texts(text_box1, text_box2, result_box))
compare_button.pack(side=tk.LEFT, padx=5)

clear_button = create_button("Clear All", reset_fields)
clear_button.pack(side=tk.LEFT, padx=5)

result_box = tk.Text(root, wrap=tk.WORD, font=("Arial", 12), bg="#ECF0F1", height=2)
result_box.pack(pady=10, fill=tk.X, padx=20)

text_box1.tag_configure("match", background="lightyellow", foreground="red")
text_box2.tag_configure("match", background="lightyellow", foreground="red")

def adjust_layout(event=None):
    frame.pack_propagate(False)
    frame.config(width=root.winfo_width() - 40, height=root.winfo_height() - 200)
    text_box1.config(width=int(root.winfo_width() / 2.5), height=int(root.winfo_height() / 30))
    text_box2.config(width=int(root.winfo_width() / 2.5), height=int(root.winfo_height() / 30))
    result_box.config(width=int(root.winfo_width() / 30))

root.bind("<Configure>", adjust_layout)
root.mainloop()
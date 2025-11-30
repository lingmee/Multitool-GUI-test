import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
from core.utils import read_file, write_file
from core.cleaner_basic import strip_leading_numbers
from core.cleaner_duplicates import remove_duplicate_and_empty_lines
from core.cleaner_json import extract_json_prompts

# kisuppuccin mocha colors
COLORS = {
    "base": "#1e1e2e",
    "mantle": "#181825",
    "crust": "#11111b",
    "text": "#cdd6f4",
    "subtext": "#a6adc8",
    "surface0": "#313244",
    "surface1": "#45475a",
    "surface2": "#585b70",
    "overlay0": "#6c7086",
    "overlay1": "#7f849c",
    "overlay2": "#9399b2",
    "lavender": "#b4befe",
    "mauve": "#cba6f7",
    "green": "#a6e3a1",
    "red": "#f38ba8"
}


# style help xdd
def style_button(btn, bg=COLORS["surface1"], fg=COLORS["text"], hover=COLORS["mauve"]):
    def on_enter(e): btn.config(bg=hover)
    def on_leave(e): btn.config(bg=bg)
    btn.config(
        bg=bg, fg=fg, activebackground=hover, activeforeground=COLORS["base"],
        relief="flat", font=("Segoe UI", 10, "bold"), padx=8, pady=4
    )
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


def style_entry(entry, bg_color):
    entry.config(
        bg=bg_color, fg=COLORS["text"],
        insertbackground=COLORS["text"],
        relief="flat", font=("Consolas", 10),
        highlightthickness=1,
        highlightbackground=COLORS["surface2"],
        highlightcolor=COLORS["mauve"]
    )


def style_label(label):
    label.config(bg=COLORS["base"], fg=COLORS["lavender"], font=("Segoe UI", 10, "bold"))


#  shared GUI layout
def create_clean_tab(tab, title, process_func, input_types=[("Text Files", "*.txt")]):
    def select_input_file():
        file_path = filedialog.askopenfilename(
            title="Select a file",
            filetypes=input_types
        )
        if file_path:
            input_entry.delete(0, tk.END)
            input_entry.insert(0, file_path)

    def select_output_location():
        save_path = filedialog.asksaveasfilename(
            title="Save cleaned file as...",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt")]
        )
        if save_path:
            output_entry.delete(0, tk.END)
            output_entry.insert(0, save_path)

    def run_clean():
        input_path = Path(input_entry.get())
        output_path = Path(output_entry.get())

        if not input_path.exists():
            messagebox.showerror("Error", "Please select a valid input file.")
            return
        if not output_path:
            messagebox.showerror("Error", "Please specify an output file name and location.")
            return

        try:
            text = read_file(input_path)
            cleaned = process_func(text)
            write_file(output_path, cleaned)
            messagebox.showinfo("Success", f"✨ {title} done!\nSaved as:\n{output_path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # layout
    tab.configure(bg=COLORS["base"])
    tk.Label(tab, text="Input File:", bg=COLORS["base"], fg=COLORS["lavender"],
             font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    input_frame = tk.Frame(tab, bg=COLORS["base"])
    input_frame.pack(fill="x", padx=10)
    input_entry = tk.Entry(input_frame)
    input_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
    style_entry(input_entry, COLORS["surface0"])
    browse_btn = tk.Button(input_frame, text="Browse", command=select_input_file)
    browse_btn.pack(side="right")
    style_button(browse_btn)

    tk.Label(tab, text="Output File:", bg=COLORS["base"], fg=COLORS["lavender"],
             font=("Segoe UI", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
    output_frame = tk.Frame(tab, bg=COLORS["base"])
    output_frame.pack(fill="x", padx=10)
    output_entry = tk.Entry(output_frame)
    output_entry.pack(side="left", fill="x", expand=True, padx=(0, 6))
    style_entry(output_entry, COLORS["surface1"])
    saveas_btn = tk.Button(output_frame, text="Save As", command=select_output_location)
    saveas_btn.pack(side="right")
    style_button(saveas_btn)

    clean_btn = tk.Button(tab, text=f"🧹 Run {title}", command=run_clean)
    clean_btn.pack(pady=20)
    style_button(clean_btn, bg=COLORS["mauve"], hover=COLORS["lavender"], fg=COLORS["base"])


# SETUP FOR ROOT WINDOW
root = tk.Tk()
root.title("🐈‍⬛ What am i doing?")
root.geometry("560x280")
root.minsize(560, 280)
root.resizable(True, True)
root.configure(bg=COLORS["base"])

# tabs
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

# style notebook tabs
style = ttk.Style()
style.theme_use("clam")
style.configure("TNotebook", background=COLORS["base"], borderwidth=0)
style.configure("TNotebook.Tab",
                background=COLORS["surface0"],
                foreground=COLORS["text"],
                padding=[10, 5],
                borderwidth=0,  # Remove tab borders
                focuscolor=COLORS["base"])
style.configure("TNotebook.Tab",
                background=COLORS["surface0"],
                foreground=COLORS["text"],
                padding=[10, 5],
                borderwidth=0)  # Remove tab borders
style.map("TNotebook.Tab",
          background=[("selected", COLORS["mauve"])],
          foreground=[("selected", COLORS["base"])])

# Add this to remove the content area border
style.configure("TNotebook", borderwidth=0)
style.layout("TNotebook", [])  # This removes the border around tab content

# create tabs
tab_numbers = tk.Frame(notebook, bg=COLORS["base"])
tab_duplicates = tk.Frame(notebook, bg=COLORS["base"])
tab_json = tk.Frame(notebook, bg=COLORS["base"])
notebook.add(tab_numbers, text="Strip Numbers")
notebook.add(tab_duplicates, text="Remove Duplicates")
notebook.add(tab_json, text="Extract JSON Prompts")

create_clean_tab(tab_numbers, "Strip Numbers", strip_leading_numbers)
create_clean_tab(tab_duplicates, "Remove Duplicates", remove_duplicate_and_empty_lines)
create_clean_tab(
    tab_json,
    "Extract JSON Prompts",
    extract_json_prompts,
    input_types=[("JSON Files", "*.json"), ("All Files", "*.*")]
)

footer = tk.Label(root, text="Drinking alone is like shitting with company.", fg=COLORS["overlay1"],
                  bg=COLORS["base"], font=("Segoe UI", 8))
footer.pack(side="bottom", pady=4)

root.mainloop()

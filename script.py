import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


folder_name = None
base_directory = None
image_paths = None
variants = []


def create_folder(base_directory, folder_name):
    new_folder_path = os.path.join(base_directory, folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    return new_folder_path


def copy_images(image_paths, folder_name):
    for image in image_paths:
        shutil.copy(image, folder_name)


def create_json(folder_path, name, variants):
    catpack_data = {
        "name": name,
        "variants": variants
    }

    # Writing the JSON file
    json_file = os.path.join(folder_path, "catpack.json")
    with open(json_file, 'w') as f:
        json.dump(catpack_data, f, indent=4)


def select_directory():
    global base_directory
    base_directory = filedialog.askdirectory(title="Select Output Directory")
    if base_directory:
        output_dir_button.config(text=f"Output Folder: {base_directory}")


def select_dates_for_image(image_name):
    date_window = tk.Toplevel(root)
    date_window.title(f"Select Dates for {image_name}")
    date_window.geometry("300x300")

    tk.Label(date_window, text=f"Select Start and End Dates for {image_name}").pack(pady=10)

    tk.Label(date_window, text="Start Day:").pack(pady=5)
    start_day = ttk.Combobox(date_window, values=list(
        range(1, 32)), state="readonly")
    start_day.pack()

    tk.Label(date_window, text="Start Month:").pack(pady=5)
    start_month = ttk.Combobox(
        date_window, values=list(range(1, 13)), state="readonly")
    start_month.pack()

    tk.Label(date_window, text="End Day:").pack(pady=5)
    end_day = ttk.Combobox(date_window, values=list(
        range(1, 32)), state="readonly")
    end_day.pack()

    tk.Label(date_window, text="End Month:").pack(pady=5)
    end_month = ttk.Combobox(date_window, values=list(
        range(1, 13)), state="readonly")
    end_month.pack()

    def save_dates():
        start_day_val = int(start_day.get())
        start_month_val = int(start_month.get())
        end_day_val = int(end_day.get())
        end_month_val = int(end_month.get())

        variant = {
            "startTime": {"day": start_day_val, "month": start_month_val},
            "endTime": {"day": end_day_val, "month": end_month_val},
            "path": image_name  # Relative path
        }
        variants.append(variant)
        date_window.destroy()

    confirm_button = tk.Button(date_window, text="Confirm", command=save_dates)
    confirm_button.pack(pady=10)


def select_images():
    global image_paths, variants
    filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp")]
    image_paths = filedialog.askopenfilenames(
        title="Select Images", filetypes=filetypes)

    if image_paths:
        images_button.config(text=f"Selected {len(image_paths)} images")
        variants = []

        for image in image_paths:
            image_name = os.path.basename(image)
            select_dates_for_image(image_name)


def on_confirm():
    global folder_name

    folder_name = folder_name_entry.get()

    if not folder_name:
        messagebox.showerror("Error", "Please enter a folder name.")
        return

    if not base_directory:
        messagebox.showerror("Error", "Please select an output folder.")
        return

    if not image_paths:
        messagebox.showerror("Error", "Please select at least one image.")
        return

    new_folder_path = create_folder(base_directory, folder_name)

    copy_images(image_paths, new_folder_path)

    create_json(new_folder_path, folder_name, variants)

    messagebox.showinfo("Success", "CatPack created successfully!")


root = tk.Tk()
root.title("CatPack Creator")
root.geometry("800x600")

tk.Label(root, text="Enter Folder Name:").pack(pady=5)
folder_name_entry = tk.Entry(root)
folder_name_entry.pack(pady=5)

# Output directory selection button
output_dir_button = tk.Button(
    root, text="Select Output Folder", command=select_directory)
output_dir_button.pack(pady=5)

# Image selection button
images_button = tk.Button(root, text="Select Images", command=select_images)
images_button.pack(pady=5)

confirm_button = tk.Button(root, text="Confirm", command=on_confirm)
confirm_button.pack(pady=20)

root.mainloop()

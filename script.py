import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk


folder_name = None
base_directory = None
image_paths = None
variants = []
default_image = None
default_image_preview = None  # To store the preview image


def create_folder(base_directory, folder_name):
    new_folder_path = os.path.join(base_directory, folder_name)
    if not os.path.exists(new_folder_path):
        os.makedirs(new_folder_path)
    return new_folder_path


def copy_images(image_paths, folder_name):
    if isinstance(image_paths, str):
        shutil.copy(image_paths, folder_name)
    elif isinstance(image_paths, list):
        for image in image_paths:
            shutil.copy(image, folder_name)


def create_json(folder_path, name, variants, default_image):
    catpack_data = {
        "name": name,
        "variants": variants
    }

    # If a default image is selected, add it to the JSON
    if default_image:
        catpack_data["default"] = default_image

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

    tk.Label(date_window, text=f"Select Start and End Dates for {image_name}").pack(
        pady=10)

    # Select start date
    tk.Label(date_window, text="Start Day:").pack(pady=5)
    start_day = ttk.Combobox(date_window, values=list(
        range(1, 32)), state="readonly")
    start_day.pack()

    tk.Label(date_window, text="Start Month:").pack(pady=5)
    start_month = ttk.Combobox(
        date_window, values=list(range(1, 13)), state="readonly")
    start_month.pack()

    # Select end date
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
            "path": image_name
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


def select_default_image():
    global default_image, default_image_full_path, default_image_preview

    filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp")]
    default_image_full_path = filedialog.askopenfilename(title="Select Default Image", filetypes=filetypes)

    if default_image_full_path:
        default_image = os.path.basename(default_image_full_path)
        default_image_button.config(text=f"Default Image: {default_image}")

        # Load and display the image preview
        img = Image.open(default_image_full_path)
        img.thumbnail((100, 100))
        default_image_preview = ImageTk.PhotoImage(img)

        default_image_label.config(image=default_image_preview)
        default_image_label.pack(pady=5)


def on_confirm():
    global folder_name

    # Get the folder name from the text entry
    folder_name = folder_name_entry.get()

    if not folder_name:
        messagebox.showerror("Error", "Please enter a folder name.")
        return

    if not base_directory:
        messagebox.showerror("Error", "Please select an output folder.")
        return

    if not image_paths and not default_image:
        messagebox.showerror("Error", "Please select at least one image.")
        return

    new_folder_path = create_folder(base_directory, folder_name)

    if image_paths:
        copy_images(image_paths, new_folder_path)

    if default_image_full_path:
        copy_images(default_image_full_path, new_folder_path)

    create_json(new_folder_path, default_image, folder_name, variants)

    messagebox.showinfo("Success", "CatPack created successfully.")


root = tk.Tk()
root.title("CatPack Creator")
root.geometry("800x600")

# Folder name entry
tk.Label(root, text="Enter Folder Name:").pack(pady=5)
folder_name_entry = tk.Entry(root)
folder_name_entry.pack(pady=5)

# Output directory selection button
output_dir_button = tk.Button(
    root, text="Select Output Folder", command=select_directory)
output_dir_button.pack(pady=5)

# Default image selection button (optional)
default_image_button = tk.Button(
    root, text="Select Default Image (Optional)", command=select_default_image)
default_image_button.pack(pady=5)

# Image selection button
images_button = tk.Button(root, text="Select Images", command=select_images)
images_button.pack(pady=5)

# Default image preview label (empty initially)
default_image_label = tk.Label(root)
default_image_label.pack()

# Confirm button
confirm_button = tk.Button(root, text="Confirm", command=on_confirm)
confirm_button.pack(pady=20)

root.mainloop()

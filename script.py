import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk
from datetime import datetime

folder_name = None
base_directory = None
image_paths = None
variants = []
default_image = None
default_image_preview = None
mode = "9.0"  # Default mode is 9.0


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


def create_json_84(folder_path, name, variants, default_image):
    catpack_data = {
        "name": name,
        "variants": variants
    }

    if default_image:
        catpack_data["default"] = default_image

    json_file = os.path.join(folder_path, "catpack.json")
    with open(json_file, 'w') as f:
        json.dump(catpack_data, f, indent=4)


def create_json_90(folder_path, name, image_dir):
    catpack_data = {
        "name": name,
        "default": image_dir
    }

    json_file = os.path.join(folder_path, "catpack.json")
    with open(json_file, 'w') as f:
        json.dump(catpack_data, f, indent=4)


def select_directory():
    global base_directory
    base_directory = filedialog.askdirectory(title="Select Output Directory")
    if base_directory:
        output_dir_button.config(text=f"Output Folder: {base_directory}")


def select_dates_for_images(callback):
    def dates_done():
        if len(variants) == len(image_paths):
            callback()

    for image in image_paths:
        image_name = os.path.basename(image)
        select_dates(image_name, dates_done)


def select_dates(image_name, done_callback):
    dates_window = tk.Toplevel(root)
    dates_window.title(f"Select Dates for {image_name}")
    dates_window.geometry("300x400")

    tk.Label(dates_window, text=f"Start Date for {image_name}").pack(pady=10)
    start_day_combo = ttk.Combobox(
        dates_window, values=[f"{i:02d}" for i in range(1, 32)])
    start_day_combo.pack(pady=5)

    tk.Label(dates_window, text=f"Start Month for {image_name}").pack(pady=10)
    start_month_combo = ttk.Combobox(
        dates_window, values=[f"{j:02d}" for j in range(1, 13)])
    start_month_combo.pack(pady=5)

    tk.Label(dates_window, text=f"End Date for {image_name}").pack(pady=10)
    end_day_combo = ttk.Combobox(
        dates_window, values=[f"{i:02d}" for i in range(1, 32)])
    end_day_combo.pack(pady=5)

    tk.Label(dates_window, text=f"End Month for {image_name}").pack(pady=10)
    end_month_combo = ttk.Combobox(
        dates_window, values=[f"{j:02d}" for j in range(1, 13)])
    end_month_combo.pack(pady=5)

    def save_dates():
        start_day = start_day_combo.get()
        start_month = start_month_combo.get()
        end_day = end_day_combo.get()
        end_month = end_month_combo.get()

        variant = {
            "startTime": {"day": start_day, "month": start_month},
            "endTime": {"day": end_day, "month": end_month},
            "path": image_name
        }
        variants.append(variant)
        dates_window.destroy()
        done_callback()

    confirm_button = tk.Button(
        dates_window, text="Confirm", command=save_dates)
    confirm_button.pack(pady=10)


def sort_variants_by_dates(variants):
    def date_key(variant):
        start_date = datetime.strptime(
            f"{variant['startTime']['day']}/{variant['startTime']['month']}",
            "%d/%m")
        end_date = datetime.strptime(
            f"{variant['endTime']['day']}/{variant['endTime']['month']}",
            "%d/%m")
        return (start_date, end_date)

    sorted_variants = sorted(variants, key=date_key)
    return sorted_variants


def select_images():
    global image_paths
    filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp")]
    new_image_paths = filedialog.askopenfilenames(
        title="Select Images", filetypes=filetypes)

    if new_image_paths:
        if image_paths:
            image_paths = list(image_paths) + list(new_image_paths)
        else:
            image_paths = list(new_image_paths)

        images_button.config(text=f"Selected {len(image_paths)} images")


def select_default_image():
    global default_image, default_image_full_path, default_image_preview

    filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp")]
    default_image_full_path = filedialog.askopenfilename(
        title="Select Default Image", filetypes=filetypes)

    if default_image_full_path:
        default_image = os.path.basename(default_image_full_path)
        default_image_button.config(text=f"Default Image: {default_image}")

        img = Image.open(default_image_full_path)
        img.thumbnail((100, 100))
        default_image_preview = ImageTk.PhotoImage(img)

        default_image_label.config(image=default_image_preview)
        default_image_label.pack(pady=5)


def prompt_subfolder_name():
    subfolder_window = tk.Toplevel(root)
    subfolder_window.title("Set Subfolder Name")
    subfolder_window.geometry("300x150")

    tk.Label(subfolder_window,
             text="Enter the subfolder name for images:").pack(pady=10)
    subfolder_name_entry = tk.Entry(subfolder_window)
    subfolder_name_entry.pack(pady=5)

    tk.Label(subfolder_window,
             text="Note: Setting the name to 'random' randomizes the images."
             ).pack(pady=10)

    def confirm_subfolder_name():
        subfolder_name = subfolder_name_entry.get()

        if not subfolder_name:
            messagebox.showerror("Error", "Please enter a subfolder name.")
            return

        subfolder_path = os.path.join(
            base_directory, folder_name, subfolder_name)
        os.makedirs(subfolder_path, exist_ok=True)

        copy_images(image_paths, subfolder_path)
        create_catpack(folder_name, [], default_image, subfolder_name)

        subfolder_window.destroy()
        messagebox.showinfo(
            "Success", "9.0 catpack successfully created.")

    confirm_button = tk.Button(
        subfolder_window, text="Confirm", command=confirm_subfolder_name)
    confirm_button.pack(pady=10)


def create_catpack(folder_name, variants, default_image, subfolder_name=None):
    manifest = {
        "name": folder_name,
        "default": subfolder_name if subfolder_name else "logos",
    }

    if variants:
        manifest["variants"] = variants

    manifest_path = os.path.join(base_directory, folder_name, "catpacks.json")
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=4)


def on_confirm():
    global folder_name, default_image

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

    if mode == "9.0":
        # 9.0 mode: Prompt for subfolder and create JSON in the subfolder
        prompt_subfolder_name()
    elif mode == "8.4":
        # 8.4 mode: Copy images to the main folder
        copy_images(image_paths, new_folder_path)

        # Copy the default image if it exists
        if default_image_full_path:
            shutil.copy(default_image_full_path, new_folder_path)
            default_image = os.path.basename(default_image_full_path)

        # Select dates for images and create the JSON
        select_dates_for_images(lambda: create_json_84(
            new_folder_path, folder_name, sort_variants_by_dates(variants),
            default_image))


def set_mode_90():
    global mode
    mode = "9.0"


def set_mode_84():
    global mode
    mode = "8.4"


root = tk.Tk()
root.title("CatPack Creator")
root.geometry("800x600")

tk.Label(root, text="Enter Folder Name:").pack(pady=5)
folder_name_entry = tk.Entry(root)
folder_name_entry.pack(pady=5)

output_dir_button = tk.Button(
    root, text="Select Output Folder", command=select_directory)
output_dir_button.pack(pady=5)

tk.Label(root, text="Select Mode:").pack(pady=5)
mode_90_button = tk.Radiobutton(
    root, text="9.0 Mode", variable=mode, value="9.0", command=set_mode_90)
mode_90_button.pack(pady=5)
mode_90_button.select()

mode_84_button = tk.Radiobutton(
    root, text="8.4 Mode", variable=mode, value="8.4", command=set_mode_84)
mode_84_button.pack(pady=5)

images_button = tk.Button(root, text="Add Images", command=select_images)
images_button.pack(pady=5)

default_image_button = tk.Button(
    root, text="Select Default Image", command=select_default_image)
default_image_button.pack(pady=5)

default_image_label = tk.Label(root)
default_image_label.pack()

confirm_button = tk.Button(root, text="Confirm", command=on_confirm)
confirm_button.pack(pady=10)

root.mainloop()

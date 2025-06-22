import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk

folder_name = None
base_directory = None
image_paths = []
default_image = None
default_image_preview = None


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
        output_dir_button.config(text=f"Will be placed in: {base_directory}")


def select_images():
    global image_paths
    filetypes = [("Image files", "*.png *.jpg *.jpeg *.bmp")]
    new_image_paths = filedialog.askopenfilenames(
        title="Select Images", filetypes=filetypes)

    if new_image_paths:
        image_paths.extend(new_image_paths)
        images_button.config(text=f"Selected {len(image_paths)} image(s)")
        update_image_list()


def remove_image(image_path):
    global image_paths
    image_paths.remove(image_path)
    update_image_list()
    images_button.config(text=f"Selected {len(image_paths)} image(s)")


def view_image(image_path):
    view_window = tk.Toplevel(root)
    view_window.title(f"Viewing: {os.path.basename(image_path)}")

    img = Image.open(image_path)
    img.thumbnail((500, 500))  # Resize for display
    img_preview = ImageTk.PhotoImage(img)

    label = tk.Label(view_window, image=img_preview)
    label.image = img_preview  # Keep a reference to avoid garbage collection
    label.pack()

    close_button = tk.Button(view_window, text="Close", command=view_window.destroy)
    close_button.pack(pady=10)


def update_image_list():
    for widget in image_list_frame.winfo_children():
        widget.destroy()

    for image_path in image_paths:
        frame = tk.Frame(image_list_frame)
        frame.pack(fill="x", pady=2)

        label = tk.Label(frame, text=os.path.basename(image_path), anchor="w")
        label.pack(side="left", fill="x", expand=True)

        view_button = tk.Button(
            frame, text="View", command=lambda p=image_path: view_image(p))
        view_button.pack(side="right", padx=5)

        remove_button = tk.Button(
            frame, text="Remove", command=lambda p=image_path: remove_image(p))
        remove_button.pack(side="right")

        # Add a separator line
        separator = tk.Frame(image_list_frame, height=1, bg="gray")
        separator.pack(fill="x", pady=2)


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
        create_catpack(folder_name, subfolder_name)

        subfolder_window.destroy()
        messagebox.showinfo(
            "Success", "9.0 catpack successfully created.")

    confirm_button = tk.Button(
        subfolder_window, text="Confirm", command=confirm_subfolder_name)
    confirm_button.pack(pady=10)


def create_catpack(folder_name, subfolder_name=None):
    manifest = {
        "name": folder_name,
        "default": subfolder_name if subfolder_name else "logos",
    }

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

    # 9.0 mode: Prompt for subfolder and create JSON in the subfolder
    prompt_subfolder_name()


root = tk.Tk()
root.title("CatPack Creator")
root.geometry("800x600")

tk.Label(root, text="Enter Catpack Name:").pack(pady=5)
folder_name_entry = tk.Entry(root)
folder_name_entry.pack(pady=5)

output_dir_button = tk.Button(
    root, text="Select Folder", command=select_directory)
output_dir_button.pack(pady=5)

images_button = tk.Button(root, text="Add Images", command=select_images)
images_button.pack(pady=5)

# New frame to display selected images
image_list_frame = tk.Frame(root)
image_list_frame.pack(fill="both", expand=True, pady=5)

default_image_button = tk.Button(
    root, text="Select Default Image", command=select_default_image)
default_image_button.pack(pady=5)

default_image_label = tk.Label(root)
default_image_label.pack()

confirm_button = tk.Button(root, text="Confirm", command=on_confirm)
confirm_button.pack(pady=10)

root.mainloop()

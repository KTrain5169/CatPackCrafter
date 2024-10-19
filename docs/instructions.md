# How to use

Using the app should be fairly simple, so hopefully this will be a walk in the park.

## 1. Locate your images

It's a good idea to consolidate the images you will be using in a singular folder, or *at least* remember the path to get to them. Otherwise, you'll have take very long time trying to find the images you want.

## 2. Using the app

Assuming you have already [downloaded the program](./downloads.md), run it and you'll be presented with a couple of options.

- `CatPack Name`: THe name of the CatPack, both in the JSON and the folder name. Be careful - if a folder with that name already exists and has a CatPack setup in it, the new JSON file will overwrite it.
- `Select Output Folder`: Where the CatPack's folder will be located in.
- `Select Default Image (Optional)`: Allows you to select an image that will be set as a "default", which means it wll show if no other image can be shown. The default image will be previewed at a smaller size beneath the options.
- `Add Images`: Adds images to your CatPack. Each image will ask you for a Start and End date/month. Be cautious: the program does not have sanity checks for the calendar dates, so be sure not to accidentally input the 31st of Febuary (or something of that vein)!
- `Confirm`: Creates the CatPack using the above options.

## Using the CatPack

Once your CatPack is created, you can move the folder with all the CatPack stuff into your Prism installation's `catpacks` folder.
This should be located at `../PrismLauncher/catpacks`, where `..` varies depending on the form of Prism you are using:

<details>
    <summary>"What would .. mean in my case?"</summary>

    If you are using a portable build of Prism, .. represents the directory where your portable build resides.

    If you are using a fully installed build of Prism, .. is represented differently depending on OS:

    - Windows: `%appdata%`
    - macOS: `~/Library/Application Support`
    - Linux: `~/.local/share`

    However, if you use either of the following package managers, they will instead be located at:

    - Scoop: `%HOMEPATH%/scoop/persist` - Note that the directory may be seen as `prismlauncher` instead of `PrismLauncher`. This is as intended.
    - Flatpak: `~/.var/app/org.prismlauncher.PrismLauncher/data`
</details

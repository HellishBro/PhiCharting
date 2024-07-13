import shutil
import os
from pathlib import Path
import json5

class Color:
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[39m"


while not os.path.exists(directory := input(Color.YELLOW + "Enter pez: " + Color.MAGENTA)):
    print(Color.BLUE + os.path.abspath(directory) + Color.RED + " is not a valid pez")

directory = Path(directory)
print(Color.GREEN + "Pezifying " + Color.BLUE + directory.absolute().as_posix())

os.mkdir("temp")
temp_folder = Path("temp")
print(Color.GREEN + "Creating temporary folder: " + Color.BLUE + Path("temp").absolute().as_posix())

info_json5 = directory / "info.json5"
info_txt = temp_folder / "info.txt"
print(Color.GREEN + "Transforming " + Color.BLUE + info_json5.absolute().as_posix() + Color.GREEN + " into " + Color.BLUE + info_txt.absolute().as_posix())
with open(info_json5, encoding="utf-8") as info_json5_file:
    info = json5.loads(info_json5_file.read())
with open(info_txt, "w", encoding="utf-8") as info_txt_file:
    info_txt_file.writelines((
        f"#\n",
        f"Name: {info["name"]}\n",
        f"Path: {directory}\n",
        f"Song: {info["song"]}\n",
        f"Picture: {info["thumbnail"]}\n",
        f"Chart: {info["chart"]}\n",
        f"Level: {info["level"]}\n",
        f"Composer: {info["composer"]}\n",
        f"Charter: {info["charter"]}\n",
        f"Illustrator: {info["illustrator"]}"
    ))

song = directory / info["song"]
song_output = temp_folder / info["song"]
print(Color.GREEN + "Copying " + Color.BLUE + song.absolute().as_posix() + Color.GREEN + " to " + Color.BLUE + song_output.absolute().as_posix())
shutil.copy2(song, song_output)

thumbnail = directory / info["thumbnail"]
thumbnail_output = temp_folder / info["thumbnail"]
print(Color.GREEN + "Copying " + Color.BLUE + thumbnail.absolute().as_posix() + Color.GREEN + " to " + Color.BLUE + thumbnail_output.absolute().as_posix())
shutil.copy2(thumbnail, thumbnail_output)

chart = directory / info["chart"]
chart_output = temp_folder / info["chart"]
print(Color.GREEN + "Copying " + Color.BLUE + chart.absolute().as_posix() + Color.GREEN + " to " + Color.BLUE + chart_output.absolute().as_posix())
shutil.copy2(chart, chart_output)

while not os.path.exists(output_directory := input(Color.YELLOW + "Enter output pez: " + Color.MAGENTA)):
    print(Color.BLUE + os.path.abspath(output_directory) + Color.RED + " is not a valid pez")

output_directory = Path(output_directory)
zip_output = output_directory / (directory.name + ".pez")
print(Color.GREEN + "Zipping " + Color.BLUE + temp_folder.absolute().as_posix() + Color.GREEN + " into " + Color.BLUE + zip_output.absolute().as_posix())
shutil.make_archive((output_directory / directory.name).as_posix(), "zip", temp_folder)
os.rename(output_directory / (directory.name + ".zip"), zip_output)
print(Color.GREEN + "Deleting temp pez")
shutil.rmtree(temp_folder)
print(Color.WHITE + "Done!" + Color.RESET)
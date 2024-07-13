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


while not os.path.exists(pez := input(Color.YELLOW + "Enter .pez path: " + Color.MAGENTA)):
    print(Color.BLUE + os.path.abspath(pez) + Color.RED + " is not a valid .pez file")

while os.path.exists(directory := input(Color.YELLOW + "Enter destination path: " + Color.MAGENTA)):
    print(Color.BLUE + os.path.abspath(directory) + Color.RED + " already exists")

directory = Path(directory)
os.mkdir(directory.absolute().as_posix())
pez = Path(pez)
print(Color.GREEN + "Unzipping " + Color.BLUE + pez.absolute().as_posix() + Color.GREEN + " Into " + Color.BLUE + directory.absolute().as_posix())

os.mkdir("temp")
temp = Path("temp")
print(Color.GREEN + "Creating temporary folder: " + Color.BLUE + temp.absolute().as_posix())
shutil.unpack_archive(pez, "temp", "zip")

info_txt = temp / "info.txt"
info_json5 = directory / "info.json5"
print(Color.GREEN + "Transforming " + Color.BLUE + info_txt.absolute().as_posix() + Color.GREEN + " into " + Color.BLUE + info_json5.absolute().as_posix())
with open(info_txt, encoding="utf-8") as info_txt_file:
    lines = info_txt_file.read().split("\n")
    lines = lines[1:-1] # ignore leading # and trailing \n
    pairs = [line.split(": ") for line in lines]
    json = {}
    replacement_map = {
        "Name": "name",
        "Song": "song",
        "Picture": "thumbnail",
        "Chart": "chart",
        "Level": "level",
        "Composer": "composer",
        "Charter": "charter",
        "Illustrator": "illustrator"
    }
    for k, v in pairs:
        if k in replacement_map:
            json[replacement_map[k]] = v


with open(info_json5, "w+", encoding="utf-8") as info_json5_file:
    info_json5_file.write(json5.dumps(json))

song = temp / json["song"]
song_output = directory / json["song"]
print(Color.GREEN + "Copying " + Color.BLUE + song.absolute().as_posix() + Color.GREEN + " to " + Color.BLUE + song_output.absolute().as_posix())
shutil.copy2(song, song_output)

thumbnail = temp / json["thumbnail"]
thumbnail_output = directory / json["thumbnail"]
print(Color.GREEN + "Copying " + Color.BLUE + thumbnail.absolute().as_posix() + Color.GREEN + " to " + Color.BLUE + thumbnail_output.absolute().as_posix())
shutil.copy2(thumbnail, thumbnail_output)

chart = temp / json["chart"]
chart_output = directory / json["chart"]
print(Color.GREEN + "Copying " + Color.BLUE + chart.absolute().as_posix() + Color.GREEN + " to " + Color.BLUE + chart_output.absolute().as_posix())
shutil.copy2(chart, chart_output)

print(Color.GREEN + "Deleting temp folder")
shutil.rmtree(temp)
print(Color.WHITE + "Done!" + Color.RESET)
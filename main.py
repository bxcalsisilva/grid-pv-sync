from datetime import date
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
from pathlib import Path
import json

settings_file = Path(__file__).parent / "settings.yaml"

gauth = GoogleAuth(settings_file)
gauth.CommandLineAuth()

drive = GoogleDrive(gauth)

day = date.today()

config = json.load(open("config.json"))

local_folder = Path(config["local_folder"])
locations = config["locations"]
systems = config["systems"]


def sfcr_filename(sfcr: str, mod: str, loc: str, day: date):
    day = day.strftime("%Y_%m_%d")
    sfcr = sys["sfcr"].upper()
    mod = sys["mod"].upper()
    loc = sys["loc"].upper()
    filename = f"{sfcr}-{mod}-{loc}_{day}.csv"
    return filename


def daq_filename(daq: str, loc: str, day: date):
    day = day.strftime("%Y_%m_%d")
    daq = daq.upper()
    loc = loc.upper()
    filename = f"{daq}-{loc}_{day}.csv"
    return filename


def download_path(folder_path: Path, loc: str, day: date):
    subfolder = day.strftime(f"{loc.upper()}/%Y/%Y_%m")
    subfolder_path = folder_path / subfolder
    subfolder_path.mkdir(parents=True, exist_ok=True)
    return subfolder_path


for sys in systems:
    print("sfcr", sys["sys"])
    filename = sfcr_filename(sys["sfcr"], sys["mod"], sys["loc"], day)
    q = f"title = '{filename}' and trashed=false"
    try:
        f = drive.ListFile({"q": q}).GetList()[0]
    except:
        print(f"{filename} not found")
        continue
    file1 = drive.CreateFile({"id": f["id"]})
    folder_path = download_path(local_folder, sys["loc"], day)
    file_path = folder_path / f["title"]
    file1.GetContentFile(file_path, mimetype="text/csv", remove_bom=True)

for loc in locations:
    print("daq", loc["loc"])
    filename = daq_filename(loc["daq"], loc["loc"], day)
    q = f"title = '{filename}' and trashed=false"
    try:
        f = drive.ListFile({"q": q}).GetList()[0]
    except:
        print(f"{filename} not found")
        continue
    file1 = drive.CreateFile({"id": f["id"]})
    folder_path = download_path(local_folder, sys["loc"], day)
    file_path = folder_path / f["title"]
    file1.GetContentFile(file_path, mimetype="text/csv", remove_bom=True)

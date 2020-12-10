import PySimpleGUI as sg

from pathlib import Path

from modules.attendee_report import AttendeeReport
from modules.pre_process import PreProcessorImpl


def generate_target_files(select_file, select_folder):
    if select_file:
        yield Path(select_file)
    elif select_folder:
        for f in Path(select_folder).glob("*.csv"):
            yield f


sg.theme("DarkBrown1")

layout = [
    [sg.Text("ファイルかフォルダを選択")],
    [sg.Text("ファイル"), sg.Input(key="select_file"), sg.FileBrowse("ファイルを選択")],
    [sg.Text("フォルダ"), sg.Input(key="select_folder"), sg.FolderBrowse("フォルダを選択")],
    [sg.Button("実行", key="ok"), sg.Cancel()],
]

window = sg.Window("sample", layout)

while True:
    event, values = window.read()
    if event in (sg.WIN_CLOSED, "Cancel"):
        break
    elif event in "ok":
        select_file = values["select_file"]
        select_folder = values["select_folder"]
        target_files = generate_target_files(select_file, select_folder)

        for target_file in target_files:
            print(target_file)
            attendee_target_file = AttendeeReport(target_file)

            output_df = attendee_target_file.create_dataframe(PreProcessorImpl())
            n = int(target_file.name.split("_")[0])
            output_df.to_csv(f"{n}_視聴者一覧.csv", encoding="utf_8_sig", index=False)
        sg.popup("process complete!")

window.close()

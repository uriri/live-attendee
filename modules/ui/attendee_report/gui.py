from pathlib import Path

import PySimpleGUI as sg

from ...application.read_attendee_report import ReadAttendeeReportService
from ...model.attendee_report import AttendeeReport


def get_read_files(select_file, select_folder):
    if select_file:
        yield AttendeeReport.build(Path(select_file))
    elif select_folder:
        for f in Path(select_folder).glob("*.csv"):
            yield AttendeeReport.build(f)


def start_gui(read_report_service: ReadAttendeeReportService):
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
            attendee_reports = get_read_files(select_file, select_folder)
            read_report_service.execute(attendee_reports)
            sg.popup("process complete!")

    window.close()

import json


from modules.pre_process import PreProcessorImpl
from modules.application.read_attendee_report import ReadAttendeeReportService
from modules.ui.attendee_report.gui import start_gui


def read_company_list():
    try:
        return json.load(open("company_domain.json", "r", encoding="utf-8"))
    except FileNotFoundError:
        print("company_domain.jsonを新規作成します")
        with open("company_domain.json", "w", encoding="utf-8") as f:
            f.write(json.dumps({}))
        return dict()


if __name__ == "__main__":
    company_domain = read_company_list()
    pre_processor = PreProcessorImpl(company_domain)
    read_report_service = ReadAttendeeReportService(pre_processor)
    start_gui(read_report_service)

from pathlib import Path

import pandas as pd

from modules.elapsed_time import ElapsedTime
from modules.pre_process import PreProcessor, PreProcessorImpl


class AttendeeReport:
    def __init__(self, csv_file: Path) -> None:
        self.df = pd.read_csv(csv_file, encoding="utf_8_sig")
        self.no = int(csv_file.name.split("_")[0])

        self.output_df = pd.DataFrame(
            columns=[
                "No",
                "氏名",
                "視聴日(yyyy/mm/dd)",
                "視聴開始(hh:mm:ss)",
                "視聴終了(hh:mm:ss)",
                "視聴時間(mm:ss)",
            ]
        )

    def create_dataframe(self, pre_processor: PreProcessor) -> pd.DataFrame:
        pre_processed_df = pre_processor.execute(self.df)
        for row in self.generate_groupby_session_id(pre_processed_df):
            self.output_df = self.output_df.append(row)

        return self.output_df.sort_values(["視聴開始(hh:mm:ss)"])

    def generate_groupby_session_id(self, df: pd.DataFrame):
        for session_id, row in df.groupby("Session Id"):
            full_name = row["Full Name"].iloc[0]
            # name_jp = " ".join(full_name.split(" ")[::-1])

            join_time = (row[row["Action"] == "Joined"])["Timestamp"].iloc[0]
            left_time = (row[row["Action"] == "Left"])["Timestamp"].iloc[0]

            elapsed = ElapsedTime(join_time, left_time)

            if elapsed.is_over_10_minute():
                yield pd.Series(
                    [
                        self.no,
                        full_name,
                        join_time.strftime("%Y/%m/%d"),
                        join_time.strftime("%H:%M:%S"),
                        left_time.strftime("%H:%M:%S"),
                        elapsed.generate_hhmm(),
                    ],
                    index=self.output_df.columns,
                    name=session_id,
                )


def summary_attendee_reports(n: int):
    with open("視聴者一覧.csv", "a", encoding="utf-8") as summary:
        with open(f"{n}_視聴者一覧.csv", encoding="utf_8_sig") as f:
            for row in f.readlines()[1:]:
                summary.write(row)


if __name__ == "__main__":
    read_report_dir = Path("attendee_reports")
    for report in read_report_dir.glob("*AttendeeReport.csv"):
        attendee_report = AttendeeReport(report)

        output_df = attendee_report.create_dataframe(PreProcessorImpl())
        n = int(report.name.split("_")[0])
        output_df.to_csv(f"{n}_視聴者一覧.csv", encoding="utf_8_sig", index=False)

    # summary_attendee_reports(n)

from typing import Iterator

import pandas as pd

from ..model.attendee_report import AttendeeReport
from ..pre_process import PreProcessor
from ..elapsed_time import ElapsedTime


class ReadAttendeeReportService:
    def __init__(self, pre_processor: PreProcessor):
        self.pre_processor = pre_processor

    def generate_groupby_session_id(self, no, df: pd.DataFrame):
        for session_id, row in df.groupby("Session Id"):
            full_name = row["Full Name"].iloc[0]

            company = row["Participant Id"].iloc[0]

            join_time = (row[row["Action"] == "Joined"])["Timestamp"].iloc[0]
            left_time = (row[row["Action"] == "Left"])["Timestamp"].iloc[0]

            elapsed = ElapsedTime(join_time, left_time)

            if elapsed.is_over_10_minute():
                yield pd.Series(
                    [
                        no,
                        full_name,
                        company,
                        join_time.strftime("%Y/%m/%d"),
                        join_time.strftime("%H:%M:%S"),
                        left_time.strftime("%H:%M:%S"),
                        elapsed.generate_hhmm(),
                    ],
                    index=self.output_df.columns,
                    name=session_id,
                )

    def execute(self, attendee_reports: Iterator[AttendeeReport]):
        self.output_df = pd.DataFrame(
            columns=[
                "No",
                "氏名",
                "所属",
                "視聴日",
                "視聴開始時間",
                "視聴終了時間",
                "視聴時間",
            ]
        )

        for attendee_report in attendee_reports:
            pre_processed_df = self.pre_processor.execute(attendee_report.csv)
            for row in self.generate_groupby_session_id(
                attendee_report.no, pre_processed_df
            ):
                self.output_df = self.output_df.append(row)
            self.output_df = self.output_df.sort_values(["視聴開始時間"])
            self.output_df.to_csv(
                f"{attendee_report.no}_視聴者一覧.csv", encoding="utf_8_sig", index=False
            )

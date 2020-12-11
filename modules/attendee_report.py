from pathlib import Path

import pandas as pd

from .elapsed_time import ElapsedTime
from .pre_process import PreProcessor


class AttendeeReport:
    def __init__(self, csv_file: Path) -> None:
        self.df = pd.read_csv(csv_file, encoding="utf_8_sig")
        self.no = int(csv_file.name.split("_")[0])

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

    def create_dataframe(self, pre_processor: PreProcessor) -> pd.DataFrame:
        pre_processed_df = pre_processor.execute(self.df)
        for row in self.generate_groupby_session_id(pre_processed_df):
            self.output_df = self.output_df.append(row)

        return self.output_df.sort_values(["視聴開始時間"])

    def generate_groupby_session_id(self, df: pd.DataFrame):
        for session_id, row in df.groupby("Session Id"):
            full_name = row["Full Name"].iloc[0]
            # name_jp = " ".join(full_name.split(" ")[::-1])

            company = row["Participant Id"].iloc[0]

            join_time = (row[row["Action"] == "Joined"])["Timestamp"].iloc[0]
            left_time = (row[row["Action"] == "Left"])["Timestamp"].iloc[0]

            elapsed = ElapsedTime(join_time, left_time)

            if elapsed.is_over_10_minute():
                yield pd.Series(
                    [
                        self.no,
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


def summary_attendee_reports(n: int):
    with open("視聴者一覧.csv", "a", encoding="utf-8") as summary:
        with open(f"{n}_視聴者一覧.csv", encoding="utf_8_sig") as f:
            for row in f.readlines()[1:]:
                summary.write(row)

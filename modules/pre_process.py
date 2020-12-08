import pandas as pd
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class PreProcessor(ABC):
    @abstractmethod
    def execute(self, df: pd.DataFrame):
        raise NotImplementedError


class PreProcessorImpl(PreProcessor):
    def execute(self, df: pd.DataFrame):
        df = df.drop(columns=[" Participant Id", " UserAgent"])

        not_attendee_index = df.index[df[" Role"] != " Attendee"]
        df = df.drop(not_attendee_index).drop(columns=" Role")

        df[" Full Name"] = df[" Full Name"].apply(
            lambda name: " ".join(name[1:].split(" ")[::-1])
        )

        df[" UTC Event Timestamp"] = df[" UTC Event Timestamp"].apply(_add_9_hours)
        df[" Action"] = df[" Action"].apply(lambda x: x[1:])

        df = df.rename(
            columns={
                " Full Name": "Full Name",
                " UTC Event Timestamp": "Timestamp",
                " Action": "Action",
            }
        )
        return df


def _add_9_hours(utc_timestamp: str):
    utc_time = datetime.strptime(utc_timestamp, " %m/%d/%Y %I:%M:%S %p")
    return utc_time + timedelta(hours=+9)

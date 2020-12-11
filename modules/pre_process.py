from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import pandas as pd


class PreProcessor(ABC):
    @abstractmethod
    def execute(self, df: pd.DataFrame):
        raise NotImplementedError


class PreProcessorImpl(PreProcessor):
    def __init__(self, company_domain_dict):
        self.company_domain_dict = company_domain_dict

    def execute(self, df: pd.DataFrame):
        not_attendee_index = df.index[df[" Role"] != " Attendee"]
        df = df.drop(not_attendee_index)

        df[" Full Name"] = df[" Full Name"].apply(
            lambda name: " ".join(name[1:].split(" ")[::-1])
        )

        df[" Participant Id"] = df[" Participant Id"].apply(self.conv_to_company)

        df[" UTC Event Timestamp"] = df[" UTC Event Timestamp"].apply(_add_9_hours)
        df[" Action"] = df[" Action"].apply(lambda x: x[1:])

        df = df.rename(
            columns={
                " Full Name": "Full Name",
                " Participant Id": "Participant Id",
                " UTC Event Timestamp": "Timestamp",
                " Action": "Action",
            }
        )
        return df[["Session Id", "Full Name", "Participant Id", "Timestamp", "Action"]]

    def conv_to_company(self, address: str):
        for key, company in self.company_domain_dict.items():
            if key in address:
                return company
        return "unknown"


def _add_9_hours(utc_timestamp: str):
    utc_time = datetime.strptime(utc_timestamp, " %m/%d/%Y %I:%M:%S %p")
    return utc_time + timedelta(hours=+9)

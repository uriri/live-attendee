import json
from io import StringIO

import pandas as pd
from flask import Blueprint, redirect, render_template, request, url_for
from modules.application.read_attendee_report import ReadAttendeeReportService
from modules.model.attendee_report import AttendeeReport
from modules.pre_process import PreProcessorImpl
from ms_teams_live import db
from ms_teams_live.models.attendee import Attendee
from datetime import datetime


def read_company_list():
    try:
        return json.load(open("company_domain.json", "r", encoding="utf-8"))
    except FileNotFoundError:
        print("company_domain.jsonを新規作成します")
        with open("company_domain.json", "w", encoding="utf-8") as f:
            f.write(json.dumps({}))
        return dict()


attendee = Blueprint("attendee", __name__)


@attendee.route("/", methods=["GET"])
def home():
    attendees = (
        Attendee.query.with_entities(Attendee.event_title)
        .distinct()
        .order_by(Attendee.event_title.desc())
    )
    return render_template("attendees/index.html", attendees=attendees)


@attendee.route("/attendees", methods=["POST"])
def add_attendee():
    company_domain = read_company_list()
    pre_processor = PreProcessorImpl(company_domain)
    read_report_service = ReadAttendeeReportService(pre_processor)

    ar = AttendeeReport(
        no=int((request.form["files"]).split("_")[0]),
        csv=pd.read_csv(StringIO(request.form["csv"]), encoding="utf_8_sig"),
    )
    results = read_report_service.execute([ar])

    for result in results:
        join_timestamp = datetime.strptime(
            " ".join([result[4], result[5]]), "%Y/%m/%d %H:%M:%S"
        )
        left_timestamp = datetime.strptime(
            " ".join([result[4], result[6]]), "%Y/%m/%d %H:%M:%S"
        )
        attendee = Attendee(
            event_title=request.form["title"],
            name=result[2],
            is_presenter=False,
            join_timestamp=join_timestamp,
            left_timestamp=left_timestamp,
        )
        db.session.add(attendee)
        db.session.commit()
    return redirect(url_for("attendee.home"))


@attendee.route("/attendees", methods=["GET"])
def new_attendee():
    return render_template("attendees/new.html")

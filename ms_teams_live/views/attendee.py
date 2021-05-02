import csv
import json
from datetime import datetime
from io import StringIO

import pandas as pd
from flask import Blueprint, make_response, redirect, render_template, request, url_for
from modules.application.read_attendee_report import ReadAttendeeReportService
from modules.model.attendee_report import AttendeeReport
from modules.pre_process import PreProcessorImpl
from ms_teams_live import db
from ms_teams_live.models.attendee import Attendee


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


@attendee.route("/attendees/new", methods=["GET"])
def new_attendee():
    return render_template("attendees/new.html")


@attendee.route("/attendees/<string:event_title>", methods=["GET"])
def show(event_title):
    attendees = Attendee.query.filter_by(event_title=event_title).all()
    return render_template(
        "attendees/show.html", title=event_title, attendees=attendees
    )


@attendee.route("/download/csv/attendees/<string:event_title>", methods=["GET"])
def download_csv(event_title):
    f = StringIO()
    writer = csv.writer(f, quotechar='"', quoting=csv.QUOTE_NONE, lineterminator="\n")

    writer.writerow(["氏名", "視聴開始", "視聴終了"])
    writer.writerows(
        [
            [a.name, a.join_timestamp, a.left_timestamp]
            for a in Attendee.query.filter_by(event_title=event_title).all()
        ]
    )

    response = make_response()
    response.data = f.getvalue()
    response.headers["Content-Type"] = "text/csv"
    response.headers["Content-Disposition"] = f"attachment; filename={event_title}.csv"
    return response

from flask import Blueprint, request, jsonify
from ..models import User, Agent, Schedule, Localisation
from .users import Response
from .utils import Utils
from flask_pymongo import pymongo, ObjectId
import datetime


dashboard_router = Blueprint(
    "dashboard_router", "dashboard_router", url_prefix="/api/v1/dashboard"
)


@dashboard_router.route("/schedule", methods=["POST", "PUT", "GET", "DELETE"])
def schedule_registrement():
    model = Schedule()
    match request.method:
        case "GET":
            allowed_filters = ["start", "end", "action", "_id"]
            filters = {}
            for key, value in request.args.items():
                if key in allowed_filters:
                    if key == "_id":
                        try:
                            filters[key] = ObjectId(value)
                        except (ValueError, TypeError):
                            pass
                    else:
                        filters[key] = value

            return (
                Response({"code": 200, "data": model.find(filters)}),
                200,
            )

        case "POST":
            utils = Utils()
            data = request.get_json()
            isDataValid = utils.dataValidator(data, ["start", "end", "action"])

            if isDataValid == False:
                return {
                    "code": 400,
                    "message": "certaines données sont manquante. Vérifiez si vous envoyer toutes ces clé : start, end, action",
                    "error": utils.error,
                }, 400

            schedule_data = {
                "start": data["start"],
                "end": data["end"],
                "action": data["action"],
            }

            modelSchedule = Schedule(schedule_data)
            modelSchedule.save()
            if modelSchedule.error is not None:
                return (
                    Response(
                        {
                            "code": 400,
                            "message": "une erreur s'est produite lors de la création de l'horraire",
                            "error": modelSchedule.error,
                        }
                    ),
                    400,
                )
            return (
                Response(
                    {"code": 201, "message": "horraire ajouté", "data": schedule_data}
                ),
                201,
            )
        case "PUT":
            id = request.args.get("_id")
            if id is None:
                return {
                    "code": 400,
                    "message": "veuillez renseignez l'id de l'élément à mettre à jour",
                }
            schedule_data = request.get_json()
            schedule_data["_id"] = id
            allowed_filters = ["start", "end", "action", "_id"]
            data = {}
            for key, value in schedule_data.items():
                if key in allowed_filters:
                    if key == "_id":
                        try:
                            data[key] = ObjectId(value)
                        except (ValueError, TypeError):
                            pass
                    else:
                        data[key] = value
            model = Schedule(data)
            model.save()
            if model.error is not None:
                return (
                    Response(
                        {
                            "code": 400,
                            "message": "une erreur s'est produite lors de la mise à jour",
                            "error": modelSchedule.error,
                        }
                    ),
                    400,
                )
            return Response(
                {"code": 200, "message": "mise à jour réussie", "data": schedule_data}
            )
        case "DELETE":
            id = request.args.get("_id")
            if id is None:
                return {
                    "code": 400,
                    "message": "veuillez renseignez l'id de l'élément à supprimer",
                }
            return {
                "code": 200,
                "message": "l'horraire a été supprimer avec succès",
                "data": model.delete(id),
            }


import datetime


def is_between(start_time, end_time):
    current_time = datetime.datetime.now()
    now = current_time.strftime("%H:%M %p")

    start_time_obj = datetime.datetime.strptime(start_time, "%H:%M %p")
    end_time_obj = datetime.datetime.strptime(end_time, "%H:%M %p")

    start_time_timestamp = start_time_obj.timestamp()
    end_time_timestamp = end_time_obj.timestamp()

    # Convert timestamps to milliseconds and round to nearest integer
    start_time_ms = int(round(start_time_timestamp * 1000))
    end_time_ms = int(round(end_time_timestamp * 1000))

    return [start_time_ms, now, end_time_ms]
    if start_time_obj <= now and now <= end_time_obj:
        return True
    else:
        return False


@dashboard_router.route("/point", methods=["GET", "POST", "PUT", "DELETE"])
def pointArrive():
    try:
        model = Localisation()
        match request.method:
            case "GET":
                allowed_filters = ["action", "agent"]
                filters = {}
                for key, value in request.args.items():
                    # if key == "location.lat":
                    #     filters["location"]["lat"] = float(value)
                    # if key == "location.lng":
                    #     filters["location"]["lng"] = float(value)
                    if key in allowed_filters:
                        if key == "_id":
                            try:
                                filters[key] = ObjectId(value)
                            except (ValueError, TypeError):
                                pass
                        else:
                            filters[key] = value

                return (
                    Response(
                        {"code": 200, "data": model.find(filters), "filter": filters}
                    ),
                    200,
                )
            case "POST":
                utils = Utils()
                data = request.get_json()
                isDataValid = utils.dataValidator(
                    data,
                    ["location", "action", "agent"],
                )

                if isDataValid == False:
                    return {
                        "code": 400,
                        "message": "certaines données sont manquante. Vérifiez si vous envoyer toutes ces clé : start, end, action",
                        "error": utils.error,
                    }, 400

                isDataValid = utils.dataValidator(
                    data["location"],
                    [
                        "lat",
                        "lng",
                    ],
                )
                if isDataValid == False:
                    return {
                        "code": 400,
                        "message": "certaines données sont manquante. Vérifiez si vous envoyer toutes ces clé : start, end, action",
                        "error": utils.error,
                    }, 400
                scheduleModel = Schedule
                horraire = scheduleModel.find({"action": data["action"]})
                is_late = is_between(horraire[0].get("start"), horraire[0].get("end"))

                data["is_late"] = is_late

                model = Localisation(data)
                model.save()
                if model.error is not None:
                    return (
                        Response(
                            {
                                "code": 400,
                                "message": "une erreur s'est produite lors du pointage",
                                "error": model.error,
                            }
                        ),
                        400,
                    )
                return (
                    Response(
                        {
                            "code": 201,
                            "message": "pointé effectué avec succès",
                            "data": data,
                            "horraire": horraire[0],
                        }
                    ),
                    201,
                )
    except TypeError as error:
        return {
            "code": 400,
            "message": "une erreur s'est produite.",
            "details": str(error),
        }
    except ValueError as error:
        return {
            "code": 400,
            "message": "une erreur s'est produite.",
            "details": str(error),
        }
    except KeyError as error:
        return {
            "code": 400,
            "message": "une erreur s'est produite.",
            "details": str(error),
        }

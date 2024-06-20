from flask import Blueprint, request, jsonify
from ..models import User, Agent, Schedule
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
                            "message": "une erreur s'est produite lors de la création du compte",
                            "error": modelSchedule.error,
                        }
                    ),
                    400,
                )
            return (
                Response(
                    {
                        "code": 201,
                        "message": "horraire ajouté",
                        "data": schedule_data,
                        # "actual_hour": now.strftime("%H:%M %p"),
                    }
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


@dashboard_router.route("/point/arrive", methods=["GET"])
def pointArrive():
    model = Schedule()
    return Response({"code": 200, "data": model.find({"action": "ARRIVE"})}), 200

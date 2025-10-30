from django.shortcuts import render
import http.client
import json
from datetime import datetime

def home(request):
    train_data = {}
    stations = []
    error_message = None

    if request.method == "POST":
        train_no = request.POST.get("train_no")
        departure_date = datetime.now().strftime("%Y%m%d")  # today's date

        try:
            conn = http.client.HTTPSConnection("indian-railway-irctc.p.rapidapi.com")
            headers = {
                # "x-rapidapi-key": "7a1663011bmsh1cbb5a37d385867p1ece23jsn625b83093673",
                "x-rapidapi-key": "58acbeb8c9msh078442c4ac7a83bp17d343jsn18ccc94438d8",
                "x-rapidapi-host": "indian-railway-irctc.p.rapidapi.com"
            }

            url = f"/api/trains/v1/train/status?departure_date={departure_date}&isH5=true&client=web&deviceIdentifier=Mozilla%20Firefox-138.0.0.0&train_number={train_no}"
            conn.request("GET", url, headers=headers)
            res = conn.getresponse()
            data = res.read()
            result_json = json.loads(data.decode("utf-8"))

            body = result_json.get("body", {})
            status = result_json.get("status", {})

            if status.get("result") != "success":
                error_message = status.get("message", {}).get("message", "Something went wrong.")
            else:
                train_data = {
                    "current_station": body.get("current_station"),   # station code
                    "terminated": body.get("terminated"),
                    "train_status_message": body.get("train_status_message")
                }
                stations = body.get("stations", [])

        except Exception as e:
            error_message = str(e)

    return render(request, "tracker/home.html", {
        "train_data": train_data,
        "stations": stations,
        "error_message": error_message
    })

import os
import traceback
from flask import jsonify, request, abort

from . import app
from poget.analytics.ml.logistic_regression import LogisticRegression
from poget.analytics.ml.terminal_traffic import TerminalTraffic
from poget import API_LOGGER as LOGGER


dir = os.getcwd()
lr_model = LogisticRegression()
name = 'terminal-traffic'
main_directory = 'poget'
models_directory = 'models'
dir = os.getcwd()
main_dir = os.path.join(dir, main_directory, models_directory, name)

lr_model.load(main_dir)


@app.route("/health")
def get_health():
    return "Health OK"


@app.route("/predictTraffic", methods=["POST"])
def get_timeslot():
    try:

        payload = request.get_json()
        LOGGER.info("payload is %s" % payload)
        data = payload["data"]

        terminal_traffic = TerminalTraffic()
        LOGGER.info("build features for payload")
        df = terminal_traffic.get_features_for_prediction(data)

        LOGGER.info("will predict traffic for %s" % data)
        LOGGER.info(df)

        prediction = lr_model.predict(df=df)
        LOGGER.info(type(prediction))

        response = []
        for i in range(0,len(prediction)):
            response_dict = {}
            response_dict['hour_slot'] = data[i]["hour_slot"]
            response_dict['day_of_week'] = data[i]["day_of_week"]
            response_dict['terminal_code'] = data[i]["terminal_code"]
            if int(prediction[i] is 0):
                response_dict["traffic"] = "low"
            else:
                response_dict["traffic"] = "high"

            response.append(response_dict)

        return jsonify(data=response, error=False)

    except Exception:
        LOGGER.error(traceback.format_exc())
        abort(500)

import os
import traceback
from flask import jsonify, request, abort
from functools import wraps

from . import app, cfg
from . import terminal_traffic
from poget.analytics.ml.logistic_regression import LogisticRegression
from poget import API_LOGGER as LOGGER


LOGGER.info("predictTime route")
dir = os.getcwd()
lr_model = LogisticRegression()
lr_model.load("poget/data/traffic")



@app.route("/health")
def get_health():
    return "Health OK"


@app.route("/predictTraffic", methods=["POST"])
def get_timeslot():
    try:

        payload = request.get_json()
        phone_numbers = payload["phoneNumbers"]

        df = prob_call.get_data_for_number(phone_number_list=phone_numbers)
        LOGGER.info("phone details")
        LOGGER.info(df)
        LOGGER.info("will predict time slot for phone number %s"%phone_numbers)
        LOGGER.info(df)

        prediction = rf_model.predict(df)
        LOGGER.info(type(prediction))
        response = []
        for i in range(0,len(prediction)):
            response_dict = {}
            response_dict['phone_number'] = phone_numbers[i]
            max_time = int(prediction[i]) * 4
            min_time = int(max_time) - 4
            time_slot = str(min_time) + '-' + str(max_time)
            response_dict['time_slot'] = time_slot
            response.append(response_dict)

        return jsonify(data=response, error=False)

    except Exception as e:
        LOGGER.error(traceback.format_exc())
        abort(500)

from phue import PhueException
from twilio.twiml.messaging_response import MessagingResponse
from flask import Flask, request
from hue_controller import HueController
import logging

logging.basicConfig(level=logging.INFO, filename="hue_log.log",
                    format="%(asctime)s:%(levelname)s:%(message)s")

app = Flask(__name__)
controller = HueController()


@app.route('/', methods=['POST', 'GET'])
def set_color():
    print(request.json["Body"])
    x, y, saturation_val = request.json["Body"].split(" ")
    x, y, saturation_val = float(x), float(y), int(saturation_val)
    try:
        controller.connect()
    except PhueException:
        logging.info("Server unable to connect to the Hue Light")
        response = MessagingResponse()
        response.message("Server unable to connect to the Hue Light")

    try:
        controller.light.xy = (x, y)
        controller.light.saturation = saturation_val
        logging.info("The light was changed")

    except PhueException:
        logging.info("Server unable to connect to the Hue Light")
        response = MessagingResponse()
        response.message("I'm sorry, but I cannot connect to the Hue Light. Please try again later.")
    return "successfully changed light."


if __name__ == '__main__':
    app.run()
    logging.info("Server has been stopped")

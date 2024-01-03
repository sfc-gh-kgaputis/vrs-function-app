import json
import logging

import azure.functions as func
from ga4gh.core import parse_ga4gh_identifier


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        payload = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    try:
        # This is basically an array of arrays. The inner array contains the
        # row number, and a value for each parameter passed to the function.
        input_rows = payload["data"]

        # The return value will contain an array of arrays (one inner array per input row).
        output_rows = []

        # For each input row in the JSON object...
        for input_row in input_rows:
            identifier = input_row[1]

            parsed_identifier = parse_ga4gh_identifier(identifier)

            output_rows.append([input_row[0], parsed_identifier])

        response = json.dumps({"data": output_rows})

        return func.HttpResponse(response, mimetype="application/json")

    except Exception as err:
        logging.exception('Unable to parse ga4gh identifier')
        # Tell caller what this function could not handle.
        # In this case, a string representation of the exception
        error_message = getattr(err, 'message', repr(err))
        # 400 implies some type of error.
        return func.HttpResponse(error_message, status_code=400)

import azure.functions as func
import json


async def main(req: func.HttpRequest) -> func.HttpResponse:
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
            name = input_row[1]
            message = f"Hello, {name}!"

            output_rows.append([input_row[0], message])

        response = json.dumps({"data": output_rows})

        return func.HttpResponse(response, mimetype="application/json")

    except Exception as err:
        # Tell caller what this function could not handle.
        # In this case, a string representation of the exception
        error_message = getattr(err, 'message', repr(err))
        # 400 implies some type of error.
        return func.HttpResponse(error_message, status_code=400)

import azure.functions as func
import json

async def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    num1 = req_body.get('num1')
    num2 = req_body.get('num2')

    if num1 is not None and num2 is not None:
        sum_result = num1 + num2
        return func.HttpResponse(json.dumps({"sum": sum_result}), mimetype="application/json")
    else:
        return func.HttpResponse("Please pass num1 and num2 in the JSON body", status_code=400)

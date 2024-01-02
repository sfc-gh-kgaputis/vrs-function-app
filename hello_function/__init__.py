import azure.functions as func
import json

async def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    name = req_body.get('name')

    if name:
        return func.HttpResponse(json.dumps({"message": f"Hello, {name}!"}), mimetype="application/json")
    else:
        return func.HttpResponse("Please pass a name in the JSON body", status_code=400)

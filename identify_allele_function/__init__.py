import json
import logging
import os

import azure.functions as func
from ga4gh.core import ga4gh_identify
from ga4gh.vrs.extras.translator import AlleleTranslator
from ga4gh.vrs.dataproxy import create_dataproxy


async def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        payload = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    try:
        # Configure data services
        repo_url = os.environ.get('VRS_REPO_URL')
        if repo_url is None:
            raise RuntimeError("Please populate the VRS_REPO_URL environment variable")
        logging.info(f'Using VRS repo: {repo_url}')
        dp = create_dataproxy(repo_url)
        tlr = AlleleTranslator(data_proxy=dp)

        # This is basically an array of arrays. The inner array contains the
        # row number, and a value for each parameter passed to the function.
        input_rows = payload["data"]

        # The return value will contain an array of arrays (one inner array per input row).
        output_rows = []

        # For each input row in the JSON object...
        for input_row in input_rows:
            input_expr = input_row[1]
            input_format = input_row[2]
            logging.debug(
                f'Processing row {input_row[0]} - identify allele for expression: {input_expr}, in format: {input_format}')

            # Translate and identify allele
            allele = tlr.translate_from(input_expr, input_format)
            allele_id = ga4gh_identify(allele)
            logging.debug(
                f'Processing row {input_row[0]} - obtained allele_id: {allele_id}')

            output_rows.append([input_row[0], allele_id])

        response = json.dumps({"data": output_rows})

        return func.HttpResponse(response, mimetype="application/json")

    except Exception as err:
        logging.exception('Unable to parse ga4gh identifier')
        # Tell caller what this function could not handle.
        # In this case, a string representation of the exception
        error_message = getattr(err, 'message', repr(err))
        # 400 implies some type of error.
        return func.HttpResponse(error_message, status_code=400)

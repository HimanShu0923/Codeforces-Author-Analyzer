import json
# import requests


def lambda_handler(event, context):
    """
    Request handler : takes author name as input and provide problem info as output

    input : {"body" : <string>}
    outptut : { output schema }
    """
    body = json.loads(event.get("body"))
    author=  body.get("author")

    #TODO: Fetch data from database and return the data.

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"Author name : {author}"
        }),
    }

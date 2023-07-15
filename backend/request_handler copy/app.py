import json
# import requests


def lambda_handler(event, context):
    """
    Request handler : takes author name as input and provide problem info as output

    input : {"body" : <string>}
    outptut : { output schema }
    """
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }

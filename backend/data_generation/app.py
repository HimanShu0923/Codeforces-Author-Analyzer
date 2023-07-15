import json
# import requests


def lambda_handler(event, context):
    """
    Data Generation : Calls codeforces API,fetches data and updates the database.
    input : None
    outptut : { output schema }
    """

    #TODO: Database updation from codeforces API
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Hello there!"
        }),
    }

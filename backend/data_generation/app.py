import json
import requests


def get_request_api(endpoint):
    url = f"https://codeforces.com/api/{endpoint}"
    response = requests.get(url)
    return response.status_code, response.json()

def lambda_handler(event, context):
    """
    Data Generation : Calls codeforces API,fetches data and updates the database.
    input : None
    outptut : { output schema }
    """

    #TODO: Database updation from codeforces API
    status, response = get_request_api("problemset.problems")
    
    if status == 200:
        problems = response["result"]["problems"]
    else:
        return {
            "statusCode" : status,
            "message" : "Codeforces API failed"
        }

    
    
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"{l1}, {l2}"
        }),
    }

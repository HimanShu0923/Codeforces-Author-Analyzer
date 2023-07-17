import json
import boto3
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

dynamodb = boto3.resource("dynamodb")
TABLE_NAME = "Codeforces-Author-Analyzer"
CODEFORCES_BASE_URL = "https://codeforces.com/problemset/problem"
table = dynamodb.Table(TABLE_NAME)

def create_url(contest_id, index):
    return f"{CODEFORCES_BASE_URL}/{contest_id}/{index}"


def lambda_handler(event, context):
    """
    Request handler : takes author name as input and provide problem info as output

    input : {"body" : {"author" : <string>}}
    
    outptut : {"tag name" : []problem_obj}
    problem_obj : {"problem_url" : string, "name" : string}
    """
    body = json.loads(event.get("body"))
    author=  body.get("author")
    logger.info(f"Author  : {author}")
    
    response = table.get_item(
        TableName=TABLE_NAME,
        Key={
            'AuthorID': author
        }
    )
    
    row = response.get('Item')
    if row is None:
        return {
            "statusCode" : 404,
            "body" : json.dumps({
                "message" : f"No contest made by : {author}"
            })
        }
        
    problems = row.get("Problems")
    response = {}
    
    
    for problem in problems:
        problem_obj = {"problem_url" : create_url(problem.get("contestId"), problem.get("index")), "name" : problem.get("name")}
        tags = problem.get("tags")
        for tag in tags:
            if tag in response:
                response[tag].append(problem_obj)
            else:
                response[tag] = [problem_obj]
    
    logger.info("returning the response")
    
    return {
        "statusCode": '200',
        "body": json.dumps({
            "message": response
        }),
    }

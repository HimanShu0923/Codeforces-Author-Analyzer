import json
import requests
import logging
import time
from bs4 import BeautifulSoup
from models import Content
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def get_request_api(endpoint):
    url = f"https://codeforces.com/api/{endpoint}"
    response = requests.get(url)
    return response.status_code, response.json()

def lambda_handler(event, context):
    """
    Data Generation : Calls codeforces API,fetches data and updates the database.
    """

    try:
        url = "https://codeforces.com/contests?complete=true"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        contests = soup.select('.contests-table tr')
        contests = contests[1:]
        contest_author= []
        for contest in contests:
            contest_id = contest['data-contestid']
            authors = contest.select('.rated-user')
            author_list = []
            for author in authors:
                author_list.append(author.text)
            contest_author.append({"contest_id" : int(contest_id), "authors" : author_list})
        logger.info(f"Contests fetched")
    except Exception as e:
        return {
            "error" : e,
            "statusCode" : 503
        }

    try:
        status, response = get_request_api("problemset.problems")
        if status == 200:
            problems = response["result"]["problems"]
        else:
            return {
                "statusCode" : status,
                "message" : "Codeforces API failed"
            }
        logger.info("Problems fetched")
    except Exception as e:
        return {
            "statusCode" : 503
        }
    
    try:
        content = Content.query(
            "LatestContest"
        ).next()
        latest_updated = content.ContestId
    except Exception as e:
        return {
            "statusCode" : 503
        }
    
    new_contest = {}
    new_contest_ids = []

    for contest in contest_author:
        if(contest["contest_id"] == latest_updated):
            break
        new_contest[contest["contest_id"]] = contest["authors"]
        new_contest_ids.append(contest["contest_id"])
    
    logger.info(f"new contests : {str(new_contest_ids)}")
     
    if len(new_contest_ids) == 0:
        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": f"Database already updated"
            }),
        }
    new_problems = {}

    for problem in problems:
        contest_id = problem["contestId"]
        if contest_id in new_contest:
            if contest_id in new_problems:
                new_problems[contest_id].append(problem)
            else:
                new_problems[contest_id] = [problem]
    
    data_to_update = {}

    for contest_id in new_contest_ids:
        authors_name = new_contest[contest_id]
        problems = new_problems[contest_id]

        for author in authors_name:
            if author in data_to_update:
                data_to_update[author].extend(problems)
            else:
                data_to_update[author] = problems

    try: 
        for author, problems in data_to_update.items():
            try:
                content = Content.query(
                    author
                ).next()
                content.Problems.extend(problems)
                content.save()
            except:
                content = Content(
                    AuthorID=author,
                    Problems=problems
                )
                content.save()
            time.sleep(3)
    except Exception as e:
        return {
            "error" : e,
            "statusCode" : 503
        }
    logger.info("data updated")
    try:
        content = Content.query(
            "LatestContest"
        ).next()
        content.ContestId = new_contest_ids[0]
    except Exception as e:
        return {
            "error" : e,
            "statusCode" : 503
        }
    logger.info(f"Latest Contest updated : {new_contest_ids[0]}")
    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "updated the database"
        }),
    }

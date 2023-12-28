import json
from helpers.stats.player_stats import *



def hello(event, context):
    message = test()
    body = {
        "message": message,
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}

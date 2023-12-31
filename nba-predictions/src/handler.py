
import json
from src.helpers.stats.player_stats import test



def hello(event, context):
    message = test()
    body = {
        "message": message,
        "input": event,
    }

    return {"statusCode": 200, "body": json.dumps(body)}

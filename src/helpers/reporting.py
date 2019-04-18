import redis

from src.utils.config_manager import config


def parse_solution_id(solution_id):
    return solution_id.split(":")


def make_solution_id(user_id, task_id):
    return f"{user_id}:{task_id}"


def new_in_msg(solution_id, payload):
    user_id, task_id = parse_solution_id(solution_id)
    return {"user_id": user_id,
            "task_id": task_id,
            "payload": payload,
            }


def new_out_msg(user_id, task_id, code="", info=""):
    return {"user_id": user_id,
            "task_id": task_id,
            "code": code,
            "info": info,
            }


class RedisReporter:
    def __init__(self, url=None):
        url = url or config["celery_app"]["outgoing"]
        self.client = redis.Redis.from_url(url)

    def report(self, result, *args, **kwargs):
        self.client.hmset(make_solution_id(result["user_id"], result["task_id"]),
                          {'code': result["code"], 'info': result["info"]})

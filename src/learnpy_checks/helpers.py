import json

from src.utils.log import logger

check_result = {
    "error": {"status": False, "message": ""},
    "success": {"status": False, "message": ""}
}


def change_check_result(type, message):
    check_result[type]["status"] = True
    check_result[type]["message"] = message


def generate_check_result_file(file):
    logger.debug(f"writing file {file}")
    f = open(file, "w")
    f.write(json.dumps(check_result))
    f.close()


def set_error(message, file):
    change_check_result("error", message)
    generate_check_result_file(file)
    quit()


def set_success(message, file):
    change_check_result("success", message)
    generate_check_result_file(file)
    quit()

# -*- coding: utf-8 -*-
import os

import ast
from src.learnpy_checks.checker import ScriptVisitor
from src.learnpy_checks.helpers import set_error, set_success
from src.utils.config_manager import config
from src.utils.log import logger


def check_script(file_name):
    logger.debug(f"open file {file_name}")
    f = open(file_name, "r")
    out_dir = config["watcher"]["results_dir"]
    out_file_path = os.path.join(out_dir, 'check_result.json')

    tree = ast.parse(f.read())

    main_visitor = ScriptVisitor()
    main_visitor.visit(tree)

    assigns = main_visitor.get_assigns()
    calls = main_visitor.get_calls()

    names_variables = []
    for assign in assigns:
        targets = assign.targets
        for target in targets:
            if isinstance(target, ast.Name) and target.id == "name":
                names_variables.append(assign)
                break

    if not names_variables:
        set_error("Переменная name - не создана", out_file_path)

    if len(names_variables) != 1:
        set_error("Переменная name - изменена", out_file_path)

    name_variable = names_variables[0]
    name_variable_value = name_variable.value

    if not isinstance(name_variable_value, ast.Str):
        set_error("Переменная name должна быть строкой", out_file_path)

    if len(name_variable_value.s) < 2:
        set_error("Переменная name должна содержать минимум 2 символа",
                  "check_result.json")

    if name_variable_value.s == "LearnPy":
        set_error("Измените LearnPy на ваше имя", out_file_path)

    is_print_call_with_name = False
    for call in calls:
        func = call.func
        args = call.args

        if not isinstance(func, ast.Name):
            continue

        if func.id != "print":
            continue

        if not args or len(args) != 1:
            continue

        names_visitor = ScriptVisitor()
        names_visitor.visit(args[0])
        names = names_visitor.get_names()

        for name in names:
            if name.id == "name" and isinstance(name.ctx, ast.Load):
                is_print_call_with_name = True
                break

    if not is_print_call_with_name:
        set_error("Выведите переменную name с помощью print", out_file_path)

    set_success("Вы успешно выполнили упражнение", out_file_path)

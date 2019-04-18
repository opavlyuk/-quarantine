# -*- coding: utf-8 -*-
import ast

from src.helpers.reporting import new_out_msg
from src.learnpy_checks.checker import ScriptVisitor

SYNTAX_ERR = 1
VAR_NOT_SET = 2
VAR_CHANGED = 3
VAR_NOT_CHANGED = 4
VAR_REQ_TYPE_STR = 5
VAR_REQ_LEN = 6
FUNC_NOT_CALLED = 7


def check_script(in_msg):
    code = str(in_msg["payload"])
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return new_out_msg(in_msg["user_id"], in_msg["task_id"],
                           code=SYNTAX_ERR, info=str(e))

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
        return new_out_msg(in_msg["user_id"], in_msg["task_id"],
                           code=VAR_NOT_SET, info="name")

    if len(names_variables) != 1:
        return new_out_msg(in_msg["user_id"], in_msg["task_id"],
                           code=VAR_CHANGED, info="name")

    name_variable = names_variables[0]
    name_variable_value = name_variable.value

    if not isinstance(name_variable_value, ast.Str):
        return new_out_msg(in_msg["user_id"], in_msg["task_id"],
                           code=VAR_REQ_TYPE_STR, info="name")

    if len(name_variable_value.s) < 2:
        return new_out_msg(in_msg["user_id"], in_msg["task_id"],
                           code=VAR_REQ_LEN, info="name")

    if name_variable_value.s == "LearnPy":
        return new_out_msg(in_msg["user_id"], in_msg["task_id"],
                           code=VAR_NOT_CHANGED, info="LearnPy")

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
        return new_out_msg(in_msg["user_id"], in_msg["task_id"],
                           code=FUNC_NOT_CALLED, info="print")

    out_msg = {"user_id": in_msg["user_id"],
               "task_id": in_msg["task_id"],
               "code": 0,
               "info": ""}
    return out_msg

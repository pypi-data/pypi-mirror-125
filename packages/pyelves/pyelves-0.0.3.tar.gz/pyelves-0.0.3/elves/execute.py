from .errors import ExecuteError


def check_args(args, datatypes):
    if len(args) != len(datatypes):
        raise ExecuteError(f"Expected {len(datatypes)} arguments, got {len(args)}")
    for arg, datatype, index in zip(args, datatypes, range(len(datatypes))):
        if not isinstance(arg, datatype):
            raise ExecuteError(f"Argument position {index}: Expected {datatype}, got {type(arg).__name__}")


def execute(code, *args):
    code = code.lower()
    if code == "add to the end of array":
        check_args(args, [list, object])
        args[0].append(args[1])
        return args[0]
    elif code == "make array with numbers":
        check_args(args, [int, int])
        if args[0] < args[1]:
            return list(range(*args))
        elif args[1] < args[0]:
            return list(range(*args, -1))
        else:
            return [args[0]]
    else:
        raise ExecuteError("Invalid syntax error - please input valid code.")


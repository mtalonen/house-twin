
def flatten(nested_list):
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            flat_list.extend(flatten(item))
        else:
            flat_list.append(item)
    return flat_list


def get_value(var):
    if isinstance(var, list):
        return sum(flatten(var))
    elif isinstance(var, dict):
        if var["fn"] == "sum":
            return sum(flatten(var["args"]))
        if var["fn"] == "neg_sum":
            return -sum(flatten(var["args"]))
    else:
        return var

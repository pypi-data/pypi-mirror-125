


def flatten(list_) -> list:
    if isinstance(list_, list):
        return [a for i in list_ for a in flatten(i)]
    return [list_]

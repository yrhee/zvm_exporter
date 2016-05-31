def compare_lists(s, t):
    return sorted(s) == sorted(t)


def compare_lists_of_dict(s, t, key=None):
    return sorted(s, key=lambda x: x[key]) == sorted(t, key=lambda x: x[key])

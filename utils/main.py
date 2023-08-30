from collections import Counter
recorder = []
def duplicate(val: list) -> list:
    #add a dict the count value for dict object
    di = Counter(val)
    for key, value in di.items():
        if value > 1:
            exist_more.append(key)
    return exist_more

def list_available_course():
    pass

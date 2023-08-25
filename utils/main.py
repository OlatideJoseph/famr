from collections import Counter
def get_grade_point(grade_score):
    grade = grade_score.upper()
    var_score = {
        "A1":6,
        "B1":4,
        "B2":4,
        "B3":4,
        "C1":3,
        "C2":3,
        "C3":3,
        "C4":3,
        "C5":3,
        "C6":3
    }
    return var_score[grade]
recorder = []
def duplicate(val: list) -> list:
    #add a dict the count value for dict object
    di = Counter(val)
    for key, value in di.items():
        if value > 1:
            exist_more.append(key)
    return exist_more

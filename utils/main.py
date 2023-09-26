from collections import Counter
import functools
from flask import redirect, url_for, request, Response, abort
from app import auth


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


def user_logged_in(func):
    """\
        A function decorators that check if a user is logged in
        and redirect them to the match and to the login page otherwise
    """
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
        if not auth.current_user():
            return redirect(url_for('users.login'))
        return func(*args, **kwargs)
    return inner_func


def admin_protected(func):
    def inner_func(*args, **kwargs):
        if auth.current_user().is_admin:
            pass
        else:
            abort(403)
        return func(*args, **kwargs)

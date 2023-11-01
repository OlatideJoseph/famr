from collections import Counter
import functools
import secrets
import os
from flask import redirect, url_for, request, Response, abort
from app import auth
from PIL import Image

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

class AcceptedImage:
    """
        it is a class meant to mimick the image module and
        improve it
    """
    def __init__(self, byt):
        self.image = byt

    def generate_random_image_names(self):
        return secrets.token_hex(10)

    def convert_image(self, size: tuple = (480, 480)):
        self.size = size
        self.img = Image.open(self.image).thumbnail(size)
        return self

    def save_image(self, loc: str ='default'):
        if loc == 'default':
            pass

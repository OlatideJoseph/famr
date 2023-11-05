from collections import Counter
import functools
import secrets
import os
from flask import redirect, url_for, request, Response, abort
from main import auth, BASE_DIR
from PIL import Image

recorder = []
def duplicate(val: list) -> list:
    pass

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
    def __init__(self, byt, size: list[tuple, list] = (480, 480)):
        self.image = byt
        self.convert_image(size)

    def generate_random_image_names(self) -> str:
        """
            generates random names for the image
        """
        return secrets.token_hex(10)+".jpg"

    def convert_image(self, size: tuple):
        """
           converts the image size to the given size
        """
        self.size = size
        self.img = Image.open(self.image)
        self.img.thumbnail(size)
        return self

    def save_image(self, loc: str ='default') -> bool:
        if loc == 'default':
            name = self.generate_random_image_names()
            self.filename = name
            path = os.path.join(BASE_DIR+'/static/img/users', name)
            self.img.save(path)
            return True
        else:
            name = self.generate_random_image_names()
            self.filename = name
            path = os.path.join(loc, name)
            self.img.save(path)
            return True
        return False

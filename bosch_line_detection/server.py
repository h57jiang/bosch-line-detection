from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

sv = Blueprint("detection", __name__)


@sv.route("/")
def index():
    return 'Welcome to Bosch line failure detection'


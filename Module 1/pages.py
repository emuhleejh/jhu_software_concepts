# Necessary modules to operate programs
from flask import Blueprint, render_template, request

bp = Blueprint("pages", __name__, template_folder = "templates")

# Return 'home' html template when endpoint matches '/'
@bp.route("/")

def home():
    return render_template("home.html")

# Return 'projects' html template when endpoint matches 'projects'
@bp.route("/projects")

def projects():
    return render_template("projects.html")

# Return 'contact' html template when endpoint matches '/contact'
@bp.route("/contact")

def contact():
    return render_template("contact.html")
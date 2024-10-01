from flask import Blueprint, current_app, redirect, render_template, request

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("pages/welcome_page.html")


@main.route("/submit_csr")
def submit_csr():
    return render_template("pages/submit_csr_page.html")

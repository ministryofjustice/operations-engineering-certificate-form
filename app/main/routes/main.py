from flask import Blueprint, render_template, request, flash

from app.main.validators.index import validate_certificate_form

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("pages/welcome_page.html")


@main.route('/submit-a-csr', methods=['GET', 'POST'])
def submit_csr():

    if request.method == "POST":
        form_data = request.form.to_dict()
        errors = validate_certificate_form(form_data)
        if errors:
            for field, error_message in errors.items():
                flash((field, error_message), "form_error")
            return render_template(
                "pages/submit_csr_page.html", form_data=form_data, errors=errors
            )

        if not errors:
            return render_template("pages/confirmation.html", issue_number=2)

    return render_template('pages/submit_csr_page.html')

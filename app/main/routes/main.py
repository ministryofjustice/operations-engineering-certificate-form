from flask import Blueprint, render_template, request

main = Blueprint("main", __name__)


@main.route("/")
def index():
    return render_template("pages/welcome_page.html")


@main.route('/submit-a-csr', methods=['GET', 'POST'])
def submit_csr():
    form_data = {}
    errors = {}

    if request.method == 'POST':
        requestor_name = request.form.get('requestor_name')
        requestor_email = request.form.get('requestor_email')
        csr_input_field = request.form.get('csr_input_field')

        if not requestor_name:
            errors['requestor_name'] = "Requestor name is required."
        if not requestor_email:
            errors['requestor_email'] = "Requestor email is required."
        if not csr_input_field or len(csr_input_field) <= 20:
            errors['csr_input_field'] = "CSR must be more than 20 characters."

        form_data = {
            'requestor_name': requestor_name,
            'requestor_email': requestor_email,
            'csr_input_field': csr_input_field
        }

        if not errors:
            return render_template("pages/confirmation.html", issue_number=2)

    return render_template('pages/submit_csr_page.html', form_data=form_data, errors=errors)

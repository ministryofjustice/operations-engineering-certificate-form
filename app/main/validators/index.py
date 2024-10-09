import re
from cryptography import x509
from cryptography.hazmat.backends import default_backend


def is_contains_only_alphabetic_chars(value):
    pattern = r"^[A-Za-z\s]+$"
    regex = re.compile(pattern)
    result = regex.fullmatch(value)
    return result is not None


def is_valid_email_pattern(email):
    pattern = "^[a-zA-Z0-9._-]+@{1}[a-zA-Z0-9.-]+$"
    regex = re.compile(pattern)
    result = regex.fullmatch(email)
    return result is not None


def is_empty(value):
    return value is None or value.strip() == ""


def is_certificate_signing_request_valid(csr_string):
    try:
        if not csr_string.startswith("-----BEGIN CERTIFICATE REQUEST-----"):
            csr_string = "-----BEGIN CERTIFICATE REQUEST-----\n" + csr_string
        if not csr_string.strip().endswith("-----END CERTIFICATE REQUEST-----"):
            csr_string = csr_string.strip() + "\n-----END CERTIFICATE REQUEST-----\n"

        csr = x509.load_pem_x509_csr(csr_string.encode('utf-8'), default_backend())

        common_name_attributes = csr.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
        if common_name_attributes:
            common_name = common_name_attributes[0].value
            print(f"Domain Name (Common Name): {common_name}")
        else:
            print("Common Name (CN) not found in CSR.")
            return False

        return True
    except Exception as e:
        print(f"Invalid CSR: {e}")
        return False


def validate_certificate_form(form_data):
    errors = {}
    if not is_contains_only_alphabetic_chars(form_data.get("requestor_name")):
        errors["requestor_name"] = "Please enter a valid full name. It should only contain alphabetic characters"
    if not is_valid_email_pattern(form_data.get("requestor_email")):
        errors["requestor_email"] = "Please enter a valid email address"
    if not is_certificate_signing_request_valid(form_data.get("csr_input_field")):
        errors["csr_input_field"] = "You have entered an invalid CSR"

    return errors

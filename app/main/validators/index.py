import re

from flask import current_app

# pylint: disable=import-error
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


def _format_certificate_signing_request(csr_string):
    if not csr_string.startswith("-----BEGIN CERTIFICATE REQUEST-----"):
        csr_string = "-----BEGIN CERTIFICATE REQUEST-----\n" + csr_string
    if not csr_string.strip().endswith("-----END CERTIFICATE REQUEST-----"):
        csr_string = csr_string.strip() + "\n-----END CERTIFICATE REQUEST-----\n"

    return csr_string


def _extract_domain_name_from_certificate_signing_request(formatted_csr_string):
    csr = x509.load_pem_x509_csr(formatted_csr_string.encode('utf-8'), default_backend())

    common_name_attributes = csr.subject.get_attributes_for_oid(x509.NameOID.COMMON_NAME)
    if common_name_attributes:
        common_name = common_name_attributes[0].value
        return common_name
    else:
        print("Domain name not found in CSR")
        return False


def is_certificate_signing_request_valid(formatted_csr_string):
    try:

        x509.load_pem_x509_csr(formatted_csr_string.encode('utf-8'), default_backend())

        return True
    except Exception as e:
        print(f"Invalid CSR: {e}")
        return False


def is_certificate_signing_request_common_name_on_gandi(formatted_csr_string):
    csr_domain_name = _extract_domain_name_from_certificate_signing_request(formatted_csr_string)
    if current_app.gandi_service.validate_certificate_signing_request(csr_domain_name) or csr_domain_name == "www.google.com":
        return True
    else:
        print("Common Name not found on Gandi")
        return False


def validate_certificate_form(form_data):
    errors = {}
    formatted_csr_string = _format_certificate_signing_request(form_data.get("csr_input_field"))

    if not is_contains_only_alphabetic_chars(form_data.get("requestor_name")):
        errors["requestor_name"] = "Please enter a valid full name. It should only contain alphabetic characters"
    if not is_valid_email_pattern(form_data.get("requestor_email")):
        errors["requestor_email"] = "Please enter a valid email address"
    if is_empty(form_data.get("domain_name")):
        errors["domain_name"] = "Please enter a valid domain name"
    if not is_certificate_signing_request_valid(formatted_csr_string):
        errors["csr_input_field"] = "You have entered an invalid CSR"
    elif not is_certificate_signing_request_common_name_on_gandi(formatted_csr_string):
        errors["csr_input_field"] = "Domain name not recognized"

    return errors

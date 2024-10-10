import json
import http


class GandiService:
    def __init__(self, token) -> None:
        self.headers = {'Authorization': f'ApiKey {token}'}

    def get_certificate_list(self):
        conn = http.client.HTTPSConnection("api.gandi.net")
        conn.request("GET", "/v5/certificate/issued-certs?per_page=1000", headers=self.headers)
        res = conn.getresponse()
        data = res.read()

        return data.decode("utf-8")

    def validate_certificate_signing_request(self, domain_name: str):

        certificate_list = self.get_certificate_list()
        certificate_json = json.loads(certificate_list)

        for certificate in certificate_json:
            if certificate['cn'] == domain_name:
                return True

        return False

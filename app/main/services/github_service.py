import logging

from github import Github
from github.GithubException import GithubException

logger = logging.getLogger(__name__)


# pylint: disable=R0903, R0914
class GithubService:
    def __init__(
        self, org_token: str, issues_repository: str
    ) -> None:
        self.issues_repository = issues_repository
        self.github_client_core_api: Github = Github(org_token)
        self.issues_repo = self.github_client_core_api.get_repo(issues_repository)

    def submit_issue(self, form_data: dict) -> str:
        title = f"📑 Certificate Renewal Request for {form_data['domain_name']}"
        body = (
            f"**Requestor Name:** {form_data['requestor_name']}\n\n"
            f"**Requestor Email:** {form_data['requestor_email']}\n\n"
            f"**Domain Name:** {form_data['domain_name']}\n\n"
            f"**CSR:** \n{form_data['csr_input_field']}\n\n"
        )

        labels = ["certificates"]

        try:
            issue = self.issues_repo.create_issue(title=title, body=body, labels=labels)
            issue_link = (
                f"https://github.com/{self.issues_repository}/issues/{issue.number}"
            )
            logger.info("Issue created: %s", title)
            return issue_link
        except GithubException as e:
            logger.error("Error creating issue: %s", e)
            raise

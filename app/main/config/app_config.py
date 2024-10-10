import os
from types import SimpleNamespace


def __get_env_var(name: str) -> str | None:
    return os.getenv(name)


app_config = SimpleNamespace(
    flask=SimpleNamespace(
        app_secret_key=__get_env_var("APP_SECRET_KEY"),
    ),
    logging_level=__get_env_var("LOGGING_LEVEL"),
    sentry=SimpleNamespace(
        dsn_key=__get_env_var("SENTRY_DSN_KEY"), environment=__get_env_var("SENTRY_ENV")
    ),
    github=SimpleNamespace(
        issues_repository="ministryofjustice/operations-engineering-certificate-form",
        token=__get_env_var("ADMIN_GITHUB_TOKEN"),
    ),
    gandi=SimpleNamespace(
        token=__get_env_var("ADMIN_GANDI_TOKEN")
    )
)

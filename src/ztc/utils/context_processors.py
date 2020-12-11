from django.conf import settings as django_settings


def settings(request):
    public_settings = (
        "GOOGLE_ANALYTICS_ID",
        "ENVIRONMENT",
        "SHOW_ALERT",
        "PROJECT_NAME",
        "SITE_TITLE",
        "API_VERSION",
        "GIT_SHA",
        "GITHUB_API_SPEC",
        "SELF_REPO",
        "SELF_BRANCH",
    )

    return {
        "settings": dict(
            [(k, getattr(django_settings, k, None)) for k in public_settings]
        )
    }

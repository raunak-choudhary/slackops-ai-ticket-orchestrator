"""OAuth helpers for Slack authentication."""

from urllib.parse import urlencode


def build_authorization_url(
    client_id: str,
    redirect_uri: str,
    scopes: list[str],
) -> str:
    params = {
        "client_id": client_id,
        "scope": " ".join(scopes),
        "redirect_uri": redirect_uri,
    }
    return "https://slack.com/oauth/v2/authorize?" + urlencode(params)


def exchange_code_for_tokens(
    http_post,
    client_id: str,
    client_secret: str,
    code: str,
    redirect_uri: str,
) -> dict:
    resp = http_post(
        "https://slack.com/api/oauth.v2.access",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "redirect_uri": redirect_uri,
        },
    )
    resp.raise_for_status()
    return resp.json()

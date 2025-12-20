"""Export FastAPI OpenAPI schema for a given service."""

from __future__ import annotations

import json
import logging
import pathlib
import sys

from fastapi.openapi.utils import get_openapi

logger = logging.getLogger(__name__)


def add_service_to_path(service: str) -> None:
    """
    Add the correct src/<service>_service/src directory to sys.path
    so the FastAPI app can be imported.
    """
    service_src = pathlib.Path(f"src/{service}_service/src").resolve()
    if service_src.exists():
        sys.path.insert(0, str(service_src))
    else:
        raise RuntimeError(f"Service source path not found: {service_src}")


def get_app(service: str):
    add_service_to_path(service)

    if service == "mail":
        from mail_client_service.app import app
        return app

    if service == "ai":
        from ai_service.main import app
        return app

    if service == "tickets":
        from tickets_service.main import app
        return app

    raise ValueError(
        f"Unknown service '{service}'. Expected one of: mail, ai, tickets"
    )


def main() -> None:
    service = sys.argv[1] if len(sys.argv) > 1 else "mail"
    app = get_app(service)

    spec = get_openapi(
        title=app.title,
        version=app.version,
        routes=app.routes,
    )

    out = pathlib.Path(f"src/{service}_service")
    out.mkdir(parents=True, exist_ok=True)
    (out / "openapi.json").write_text(json.dumps(spec, indent=2))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
    logger.info("OpenAPI spec exported successfully")

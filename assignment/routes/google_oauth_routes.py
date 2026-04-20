from starlette.requests import Request
import secrets  # python's crypto secure random generator
from assignment.core import (
    GOOGLE_CLIENT_ID,
    GOOGLE_REDIRECT_URI,
    GOOGLE_AUTH_URL,
    GOOGLE_TOKEN_URL,
    GOOGLE_CLIENT_SECRET,
)
from starlette.responses import RedirectResponse, JSONResponse
from starlette import status
import httpx
from jose import jwt
from assignment.repository.user_repo import create_user_repo
from assignment.core import LoggerSetup

logger = LoggerSetup.setup_logger(__name__)


# build the authorization url and redirect to google
async def google_login(request: Request):
    state = secrets.token_urlsafe(16)
    request.session["oauth_state"] = state

    params = (
        f"?client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        f"&response_type=code"
        f"&scope=openid%20email%20profile"
        f"&access_type=offline"
        f"&state={state}"
        f"&prompt=consent"
    )
    return RedirectResponse(GOOGLE_AUTH_URL + params)


# google redirect here with the code and state
async def google_callback(request: Request):
    code = request.query_params.get("code")
    state = request.query_params.get("state")

    if not code or state != request.session.get("oauth_state"):
        return JSONResponse({"error": "Invalid state or missing code"}, status_code=400)

    del request.session["oauth_state"]

    async with httpx.AsyncClient() as client:
        token_response = await client.post(
            GOOGLE_TOKEN_URL,
            data={  # <-- form data, not json=
                "code": code,
                "client_id": GOOGLE_CLIENT_ID,
                "client_secret": GOOGLE_CLIENT_SECRET,
                "redirect_uri": GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",  # always this value
            },
        )

        token_data = token_response.json()

        if "error" in token_data:
            return JSONResponse(
                {"error": "Token exchange failed", "detail": token_data},
                status_code=400,
            )
        access_token = token_data["access_token"]
        id_token_raw = token_data["id_token"]
        refresh_token = token_data.get("refresh_token")

        user_info = jwt.decode(
            id_token_raw,
            key="",
            options={
                "verify_signature": False,
                "verify_aud": False,
                "verify_at_hash": False,
            },
            algorithms=["RS256"],
        )
        user = create_user_repo(new_user=user_info)
        request.session["user"] = {
            "google_id": user_info["sub"],
            "email": user_info["email"],
            "name": user_info.get("name"),
            "picture": user_info.get("picture"),
        }
        request.session["tokens"] = {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }
        logger.info(user)
        return RedirectResponse("/me")


# protected page
async def me(request: Request):
    user = request.session.get("user")
    if not user:
        return JSONResponse({"error": "Not logged in"}, status_code=401)
    return JSONResponse(user)


async def logout(request: Request):
    request.session.clear()
    return RedirectResponse("/")

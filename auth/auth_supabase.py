from typing import Literal
from fastapi import APIRouter, Header, HTTPException, status
from pydantic import BaseModel
from client.supabase import supabase


router = APIRouter()


PortalRole = Literal["advisory", "developer", "admin"]

class LoginRequest(BaseModel):
    email: str
    password: str
    portal: PortalRole = "advisory"


class SignUpRequest(BaseModel):
    full_name: str
    email: str
    password: str
    portal: PortalRole = "advisory"


class VerifyRequest(BaseModel):
    portal: PortalRole = "advisory"


class UserPayload(BaseModel):
    id: str
    email: str
    full_name: str
    portal: PortalRole
    user_metadata: dict
    app_metadata: dict


class SessionUserPayload(BaseModel):
    id: str
    email: str
    user_metadata: dict
    app_metadata: dict


class SessionPayload(BaseModel):
    access_token: str
    refresh_token: str | None = None
    expires_in: int | None = None
    user: SessionUserPayload


class AuthResponse(BaseModel):
    session: SessionPayload | None
    user: UserPayload | None
    email_confirmation_required: bool = False
    message: str | None = None


def _extract_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing Authorization header.",
        )

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must be a Bearer token.",
        )

    return token


def _get_allowed_portals(user) -> list[str]:
    """Extracts all allowed portals for a user, handling both lists and strings."""
    user_metadata = user.user_metadata or {}
    app_metadata = user.app_metadata or {}

    # Check for the multi-role JSON array first
    portals = user_metadata.get("portals") or app_metadata.get("portals")
    if isinstance(portals, list):
        return portals

    # Fallback to the legacy single-string role
    single_portal = (
        user_metadata.get("portal")
        or app_metadata.get("portal")
        or app_metadata.get("role")
    )
    if single_portal in {"advisory", "developer", "admin"}:
        return [single_portal]

    return ["advisory"]  # Default fallback


def _ensure_portal_access(allowed_portals: list[str], requested_portal: PortalRole) -> None:
    """Validates if the requested portal is within the user's allowed list."""
    if requested_portal not in allowed_portals:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"This account does not have access to the {requested_portal} portal.",
        )


def _serialize_user(user, portal: PortalRole) -> UserPayload:
    user_metadata = user.user_metadata or {}
    app_metadata = user.app_metadata or {}
    full_name = user_metadata.get("full_name") or user.email or "Pangaea User"

    return UserPayload(
        id=user.id,
        email=user.email or "",
        full_name=full_name,
        portal=portal,
        user_metadata=user_metadata,
        app_metadata=app_metadata,
    )


def _serialize_session(session, user, portal: PortalRole) -> SessionPayload:
    return SessionPayload(
        access_token=session.access_token,
        refresh_token=session.refresh_token,
        expires_in=session.expires_in,
        user=SessionUserPayload(
            id=user.id,
            email=user.email or "",
            user_metadata=user.user_metadata or {},
            app_metadata=user.app_metadata or {},
        ),
    )


@router.post("/auth/login", response_model=AuthResponse)
async def login(payload: LoginRequest):
    try:
        auth_response = supabase.auth.sign_in_with_password(
            {
                "email": payload.email,
                "password": payload.password,
            }
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Login failed: {exc}",
        ) from exc

    if auth_response.user is None or auth_response.session is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login failed. No active session was returned.",
        )

    allowed_portals = _get_allowed_portals(auth_response.user)
    _ensure_portal_access(allowed_portals, payload.portal)
    
    # If no exception is raised, the user is valid for this portal.
    actual_portal = payload.portal 

    return AuthResponse(
        session=_serialize_session(auth_response.session, auth_response.user, actual_portal),
        user=_serialize_user(auth_response.user, actual_portal),
        email_confirmation_required=False,
    )


@router.post("/auth/signup", response_model=AuthResponse)
async def signup(payload: SignUpRequest):
    try:
        auth_response = supabase.auth.sign_up(
            {
                "email": payload.email,
                "password": payload.password,
                "options": {
                    "data": {
                        "full_name": payload.full_name,
                        "portals": [payload.portal], # Save as a list for the new format
                    }
                },
            }
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup failed: {exc}",
        ) from exc

    if auth_response.user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Signup failed. User could not be created.",
        )

    # For a new signup, they are granted access to the portal they requested
    actual_portal = payload.portal
    email_confirmation_required = auth_response.session is None

    return AuthResponse(
        session=(
            _serialize_session(auth_response.session, auth_response.user, actual_portal)
            if auth_response.session is not None
            else None
        ),
        user=_serialize_user(auth_response.user, actual_portal),
        email_confirmation_required=email_confirmation_required,
        message=(
            "Account created. Please confirm the email address before logging in."
            if email_confirmation_required
            else "Account created successfully."
        ),
    )


@router.post("/auth/verify", response_model=UserPayload)
async def verify_auth_session(
    payload: VerifyRequest,
    authorization: str | None = Header(default=None),
):
    access_token = _extract_token(authorization)

    try:
        auth_response = supabase.auth.get_user(access_token)
        user = auth_response.user
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Supabase token verification failed: {exc}",
        ) from exc

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User session is invalid or expired.",
        )

    allowed_portals = _get_allowed_portals(user)
    _ensure_portal_access(allowed_portals, payload.portal)
    
    # If no exception is raised, the user is valid for this portal.
    actual_portal = payload.portal

    return _serialize_user(user, actual_portal)
import base64
import hashlib
import hmac
import json
from datetime import datetime, timedelta, timezone
from typing import Any

from acompanhamento_cardiaco.config import settings


def create_access_token(subject: str) -> tuple[str, int]:
    expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expires = datetime.now(timezone.utc) + expires_delta
    payload = {'sub': subject, 'type': 'access', 'exp': int(expires.timestamp())}
    token = _encode_jwt(payload)
    return token, int(expires_delta.total_seconds())


def create_refresh_token(subject: str) -> str:
    expires = datetime.now(timezone.utc) + timedelta(
        days=settings.REFRESH_TOKEN_EXPIRE_DAYS,
    )
    payload = {'sub': subject, 'type': 'refresh', 'exp': int(expires.timestamp())}
    return _encode_jwt(payload)


def decode_token(token: str) -> dict:
    try:
        header_encoded, payload_encoded, signature = token.split('.')
        signed_content = f'{header_encoded}.{payload_encoded}'
        expected_signature = _sign(signed_content)

        if not hmac.compare_digest(signature, expected_signature):
            raise ValueError('Token inválido')

        header = _base64url_decode(header_encoded)

        if header.get('alg') != settings.ALGORITHM:
            raise ValueError('Algoritmo inválido')

        payload = _base64url_decode(payload_encoded)
        expires_at = payload.get('exp')

        if not isinstance(expires_at, int):
            raise ValueError('Expiração inválida')

        if datetime.now(timezone.utc).timestamp() > expires_at:
            raise ValueError('Token expirado')

        return payload

    except (json.JSONDecodeError, UnicodeDecodeError, ValueError):
        raise ValueError('Token inválido') from None


def _encode_jwt(payload: dict[str, Any]) -> str:
    header = {'alg': settings.ALGORITHM, 'typ': 'JWT'}
    header_encoded = _base64url_encode(header)
    payload_encoded = _base64url_encode(payload)
    signature = _sign(f'{header_encoded}.{payload_encoded}')
    return f'{header_encoded}.{payload_encoded}.{signature}'


def _base64url_encode(data: dict[str, Any]) -> str:
    json_data = json.dumps(data, separators=(',', ':'), sort_keys=True).encode()
    return base64.urlsafe_b64encode(json_data).decode().rstrip('=')


def _base64url_decode(value: str) -> dict[str, Any]:
    padding = '=' * (-len(value) % 4)
    json_data = base64.urlsafe_b64decode(f'{value}{padding}')
    return json.loads(json_data.decode())


def _sign(signed_content: str) -> str:
    signature = hmac.new(
        settings.SECRET_KEY.encode(),
        signed_content.encode(),
        hashlib.sha256,
    ).digest()
    return base64.urlsafe_b64encode(signature).decode().rstrip('=')

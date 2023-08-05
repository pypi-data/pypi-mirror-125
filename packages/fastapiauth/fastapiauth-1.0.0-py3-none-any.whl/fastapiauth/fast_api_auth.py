from typing import Optional
from fastapi import Header
from jwt import encode, decode, DecodeError
from time import time
from pydantic import BaseModel

class RefreshTokensRequest(BaseModel):
    refresh_token: str

class FastApiAuth:
    def __init__(self, issuer: str, audience: str, secret: str, access_lifetime: int, refresh_lifetime: int) -> None:
        self._issuer = issuer
        self._audience = audience
        self._secret = secret
        self._access_lifetime = access_lifetime
        self._refresh_lifetime = refresh_lifetime

    def get_dependenses(self):
        return FastApiAuthDependenses(self._issuer, self._audience, self._secret, self._access_lifetime, self._refresh_lifetime)

    def generate_access_and_refresh_tokens(self, access_claims: dict, refresh_claims: dict) -> dict:
        return {
            "access_token": self.generate_access_token(access_claims),
            "refresh_token": self.generate_refresh_token(refresh_claims)
        }

    def generate_access_token(self, claims: dict) -> str:
        claims["audience"] = self._audience
        claims["issuer"] = self._issuer
        claims["iat"] = time()
        claims["exp"] = claims["iat"] + self._access_lifetime
        token = encode(claims, self._secret)
        return token

    def generate_refresh_token(self, claims: dict) -> str:
        claims["audience"] = self._audience
        claims["issuer"] = self._issuer
        claims["iat"] = time()
        claims["exp"] = claims["iat"] + self._refresh_lifetime
        token = encode(claims, self._secret)
        return token


class FastApiAuthDependenses:
    def __init__(self, issuer: str, audience: str, secret: str, access_lifetime: int, refresh_lifetime: int) -> None:
        self._issuer = issuer
        self._audience = audience
        self._secret = secret
        self._access_lifetime = access_lifetime
        self._refresh_lifetime = refresh_lifetime

    def validate_access_token(self, token: Optional[str]=Header(None)):
        try:
            claims = decode(token, self._secret, ["HS256"])
            if claims["exp"] < time():
                return {
                    "error": "token expired"
                }
            return claims
        except DecodeError:
            return {
                "error": "token from header isn't valid"
            }

    def validate_refresh_token(self, body: RefreshTokensRequest):
        try:
            claims = decode(body.token, self._secret, ["HS256"])
            if claims["exp"] < time():
                return {
                    "error": "token expired"
                }
            return {
                "token": body.token,
                "claims" : claims
            }
        except DecodeError:
            return {
                "error": "token from header isn't valid"
            }


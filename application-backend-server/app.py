from flask import Flask, jsonify, request
import time, requests, os, json
from jose import jwt

# Cấu hình OIDC (OpenID Connect)
ISSUER   = os.getenv("OIDC_ISSUER",   "http://authentication-identity-server:8080/realms/master")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "myapp")
JWKS_URL = f"{ISSUER}/protocol/openid-connect/certs"

# Lấy và cache JSON Web Key Set (JWKS) từ Identity Server để xác thực Token
_JWKS = None; _TS = 0
def get_jwks():
    global _JWKS, _TS
    now = time.time()
    if not _JWKS or now - _TS > 600:
        _JWKS = requests.get(JWKS_URL, timeout=5).json()
        _TS = now
    return _JWKS

app = Flask(__name__)

# API 1: Kiểm tra trạng thái Server
@app.get("/hello")
def hello(): return jsonify(message="Hello from App Server!")

# API 2: Lấy danh sách sinh viên (Yêu cầu mở rộng)
@app.get("/student")
def student():
    """
    API endpoint trả về danh sách sinh viên từ file tĩnh JSON.
    Minh chứng khả năng quản lý dữ liệu và trả về định dạng chuẩn REST API.
    """
    try:
        # Mở và đọc file students.json với định dạng utf-8 để tránh lỗi font tiếng Việt
        with open("students.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify(error="File students.json not found"), 404

# API 3: Tài nguyên bảo mật (Yêu cầu xác thực Token)
@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = auth.split(" ",1)[1]
    try:
        payload = jwt.decode(token, get_jwks(), algorithms=["RS256"], audience=AUDIENCE, issuer=ISSUER)
        return jsonify(message="Secure resource OK", preferred_username=payload.get("preferred_username"))
    except Exception as e:
        return jsonify(error=str(e)), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)

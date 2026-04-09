from flask import Flask, jsonify, request
import time, requests, os, json
from jose import jwt
import mysql.connector

# Cấu hình OIDC (OpenID Connect)
ISSUER   = os.getenv("OIDC_ISSUER",   "http://authentication-identity-server:8080/realms/master")
AUDIENCE = os.getenv("OIDC_AUDIENCE", "myapp")
JWKS_URL = os.getenv("OIDC_JWKS_URL", f"{ISSUER}/protocol/openid-connect/certs")
TOKEN_ENDPOINT = f"{ISSUER}/protocol/openid-connect/token"

# Cấu hình Database
db_config = {
    'host': 'relational-database-server',
    'user': 'root',
    'password': 'root',
    'database': 'studentdb'
}

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

# Kiểm tra xem audience trong token có khớp với audience của ứng dụng không
def audience_matches(payload):
    aud = payload.get("aud")
    azp = payload.get("azp")
    if isinstance(aud, list) and AUDIENCE in aud:
        return True
    if isinstance(aud, str) and aud == AUDIENCE:
        return True
    # Keycloak thường đặt authorized party (azp) thành client_id.
    if azp == AUDIENCE:
        return True
    return False

# API 1: Kiểm tra trạng thái Server
@app.get("/hello")
def hello(): return jsonify(message="Hello from App Server!")

@app.get("/oidc-info")
def oidc_info():
    return jsonify(
        issuer=ISSUER,
        token_endpoint=TOKEN_ENDPOINT,
        audience=AUDIENCE
    )

# API 2: Lấy danh sách sinh viên (Yêu cầu mở rộng)
@app.get("/student")
def student():
    try:
        # Mở và đọc file students.json với định dạng utf-8 để tránh lỗi font tiếng Việt
        with open("students.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify(error="File students.json not found"), 404
    
# API 3: Quản trị danh sách sinh viên từ MariaDB - Full CRUD (Yêu cầu mở rộng)
@app.route("/students-db", methods=["GET", "POST"])
def manage_students_db():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # ĐỌC DỮ LIỆU (SELECT)
    if request.method == "GET":
        cursor.execute("SELECT * FROM students")
        result = cursor.fetchall()
        cursor.close(); conn.close()
        return jsonify(result)

    # THÊM DỮ LIỆU (INSERT)
    if request.method == "POST":
        new_data = request.json
        sql = "INSERT INTO students (student_id, fullname, dob, major) VALUES (%s, %s, %s, %s)"
        val = (new_data['student_id'], new_data['fullname'], new_data['dob'], new_data['major'])
        cursor.execute(sql, val)
        conn.commit()
        cursor.close(); conn.close()
        return jsonify(message="Student added successfully!"), 201

# API 3.1: CẬP NHẬT & XÓA theo ID
@app.route("/students-db/<int:id>", methods=["PUT", "DELETE"])
def update_delete_student(id):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        # CẬP NHẬT (UPDATE)
        if request.method == "PUT":
            update_data = request.json
            if not update_data:
                return jsonify(error="No data provided"), 400

            fields = []
            values = []
            for key, value in update_data.items():
                if key in ['student_id', 'fullname', 'dob', 'major']:
                    fields.append(f"{key} = %s")
                    values.append(value)

            if not fields:
                return jsonify(error="No valid fields to update"), 400

            values.append(id)
            sql = f"UPDATE students SET {', '.join(fields)} WHERE id = %s"
            
            cursor.execute(sql, tuple(values))
            conn.commit()
            
            # KIỂM TRA: Nếu không có hàng nào bị thay đổi
            if cursor.rowcount == 0:
                cursor.close(); conn.close()
                return jsonify(error=f"Student ID {id} not found or no changes made"), 404
            
            cursor.close(); conn.close()
            return jsonify(message=f"Student ID {id} updated!")

        # XÓA (DELETE)
        if request.method == "DELETE":
            cursor.execute("DELETE FROM students WHERE id = %s", (id,))
            conn.commit()
            
            # KIỂM TRA: Nếu không có hàng nào bị xóa
            if cursor.rowcount == 0:
                cursor.close(); conn.close()
                return jsonify(error=f"Student ID {id} not found"), 404
                
            cursor.close(); conn.close()
            return jsonify(message=f"Student ID {id} deleted!")

    except Exception as e:
        return jsonify(error=str(e)), 500

# API 4: Tài nguyên bảo mật (Yêu cầu xác thực Token)
@app.get("/secure")
def secure():
    auth = request.headers.get("Authorization","")
    if not auth.startswith("Bearer "):
        return jsonify(error="Missing Bearer token"), 401
    token = auth.split(" ",1)[1]
    try:
        payload = jwt.decode(
            token,
            get_jwks(),
            algorithms=["RS256"],
            issuer=ISSUER,
            options={"verify_aud": False}
        )
        if not audience_matches(payload):
            return jsonify(error="Invalid token audience/client"), 401
        return jsonify(message="Secure resource OK", preferred_username=payload.get("preferred_username"))
    except Exception as e:
        return jsonify(error=str(e)), 401

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)

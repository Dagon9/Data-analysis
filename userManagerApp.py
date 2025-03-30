from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
import bcrypt

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 数据库配置（根据你的MySQL信息修改）
DB_CONFIG = {
    "host": "192.168.2.205",  # 移除端口号
    "port": 3306,         # 添加独立端口配置
    "user": "root",       # 添加双引号保持键一致性
    "password": "000000",
    "database": "analyse",
    "charset": "utf8mb4"
}

def get_db_connection():
    return pymysql.connect(
        host=DB_CONFIG['host'],
        port=DB_CONFIG['port'],
        user=DB_CONFIG['user'],
        password=DB_CONFIG['password'],
        db=DB_CONFIG['database'],
        charset=DB_CONFIG['charset'],
        cursorclass=pymysql.cursors.DictCursor
    )

# ... 移除SQLAlchemy的User模型 ...

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # ... 保留原有参数检查 ...
    if not data or 'user_name' not in data or 'user_password' not in data or 'user_permission' not in data:
        return jsonify(success=False, error="缺少必填字段"), 400
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # 检查用户名是否存在
            cursor.execute("SELECT user_name FROM users WHERE user_name = %s", (data['user_name'],))
            if cursor.fetchone():
                return jsonify(success=False, error="用户已存在"), 400

            # 插入新用户（直接存储明文密码）
            cursor.execute(
                "INSERT INTO user (user_name, user_password, user_permission) VALUES (%s, %s, %s)",
                (data['user_name'], data['user_password'], data['user_permission'])
            )
            conn.commit()
            return jsonify(success=True)
    except Exception as e:
        conn.rollback()
        return jsonify(success=False, error="Database error"), 500
    finally:
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    print(data)
    # ... 保留原有参数检查 ...
    if not data or 'user_name' not in data or 'user_password' not in data:
        return jsonify(success=False, error="缺少必填字段"), 400
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, user_name, user_password, user_permission FROM user WHERE user_name = %s",
                (data['user_name'],)
                #"SELECT username, password_hash FROM users WHERE email = %s",
                #(data['email'],)
            )
            user = cursor.fetchone()
            print(user)


            # 密码验证逻辑和错误提示
            if not user:
                return jsonify(success=False, error="用户名不存在"), 401
                
            #if not bcrypt.checkpw(data['user_password'].encode('utf-8'), user['user_password'].encode('utf-8')):
            #    return jsonify(success=False, error="密码错误"), 401
            if user['user_password'] != data['user_password']:
                return jsonify(success=False, error="密码错误"), 401
            
            # 添加权限返回
            return jsonify(
                success=True, 
                user_id=user['user_id'],
                user_name=user['user_name'],
                user_permission=user['user_permission']
            )
    except Exception as e:
        print(f"Error: {str(e)}") 
        return jsonify(success=False, error="服务器内部错误"), 500
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)

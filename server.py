from app import app
import os

app.secret_key = os.urandom(24)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)


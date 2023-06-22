from flask import Flask, request

app = Flask(__name__)


users = {"halilunsal": {"name": "Halil", "email":"halil@gmail.com"},
         "taylorswift": {"name": "Taylor", "email":"taylor@gmail.com"},
         "tonystark": {"name": "Tony", "email":"tony@gmail.com"}}


@app.route("/")
def home_page():
    return "Welcome Home Page"


@app.route("/get-user/<user_id>")
def get_user(user_id):
    if user_id in users:
        user_data = users[user_id]
        extra = request.args.get("country")
        if extra:
            user_data["country"] = extra
        return user_data
    else:
        return "User didn't find..."
    
@app.route("/create-user", methods=["POST"])
def create_user():
    data = request.get_json()
    return data

if __name__ == "__main__":
    app.run()
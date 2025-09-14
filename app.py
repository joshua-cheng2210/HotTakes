from flask import Flask, render_template, jsonify, request;
from dotenv import load_dotenv
from google.oauth2 import id_token
from google.auth.transport import requests as google_oauth_requests
import os

app = Flask(__name__)

load_dotenv()
google_client_id = os.environ.get('GOOGLE_CLIENT_ID')

app = Flask(__name__)

takes = [
    {
        "title": "Hotdogs are a taco", 
        "author": "yaseenshakil"
    }, 
    {
        "title": "Golf isn't a real sport", 
        "author": "the anti golf association"
    }, 
    {
        "title": "Friends is highly overrated",
        "author": "everyone"
    },
    {
        "title": "Crunchy peanut butter over creamy peanut butter",
        "author": "reception lady"
    }
]

@app.route('/')
def home_page():
    return render_template("index.html", takes=takes)

@app.route('/signup')
def signup():
    return render_template("signup.html", GOOGLE_CLIENT_ID=google_client_id) # its fine to send the id to the front end. its just a public identifier for your app to use google auth

@app.route('/auth/google', methods=['POST'])
def google_auth():
    print("Google auth endpoint hit: /auth/google")

    data = request.get_json()
    # print(f"data: {data}")
    
    if not data or data["token"] == None:
        return jsonify({"success": False, "message": "No token provided"}), 400
    
    token = data['token']

    try:
        print("Verifying token...")
        idinfo = id_token.verify_oauth2_token(
            token, 
            google_oauth_requests.Request(), 
            google_client_id
        )
        print(f"idinfo: {idinfo}")
        
        user_id = idinfo['sub']
        email = idinfo['email']
        name = idinfo.get('name', '')
        
        print(f"Authenticated user: {email}")

        # TODO: Check if user exists in database and decide signup or login
        # returning account info from DB upon successful auth
        return jsonify({
            "success": True, 
            "message": "Authentication successful",
            "user": {
                "id": user_id,
                "email": email,
                "name": name
            }
        })
        
    except ValueError as e:
        print(f"Error verifying token: {e}")
        return jsonify({"success": False, "message": f"auth failed"}), 401

    
    return jsonify({"success": True, "message": "just testing for now"})

@app.after_request
def add_security_headers(response):
    response.headers['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
    return response

app.static_folder = "static"

if __name__ == "__main__":
    app.run(debug=True)
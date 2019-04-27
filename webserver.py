from flask import Flask, render_template, request, url_for, redirect
from werkzeug.contrib.fixers import ProxyFix
import google_auth_oauthlib.flow
import psycopg2
import os
app = Flask(__name__)
conn = None

def init():
    app.wsgi_app = ProxyFix(app.wsgi_app)
    DATABASE_URL = os.environ['DATABASE_URL']
    global conn
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')


def credentials_to_dict(credentials):
    return {'token': credentials.token,
          'refresh_token': credentials.refresh_token,
          'token_uri': credentials.token_uri,
          'client_id': credentials.client_id,
          'client_secret': credentials.client_secret,
          'scopes': credentials.scopes}


@app.route('/login')
def get_login_hook():
    chat_id = request.args.get("state")
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        'client_secret.json', scopes=["https://www.googleapis.com/auth/calendar.events"], state=chat_id)
    flow.redirect_uri = url_for("get_login_hook", _external=True)
    authorization_response = request.url
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    to_send = credentials_to_dict(credentials)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO auth (chat_id, token, refresh_token, token_uri, client_id, client_secret, scopes) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (str(chat_id), str(to_send["token"]), str(to_send["refresh_token"]), str(to_send["token_uri"]), str(to_send["client_id"]), str(to_send["client_secret"]), str(to_send["scopes"])))
    conn.commit()
    cursor.close()
    return redirect("https://telegram.me/yet_another_task_bot?start={}".format(str(chat_id)))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/googleb6f1161798ffa448.html')
def google_handler():
    return render_template("googleb6f1161798ffa448.html")


init()


if __name__ == "__main__":
    init()
    app.run(debug=True)
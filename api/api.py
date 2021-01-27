from flask import Flask, jsonify
from flask_cors import CORS
from flask_azure_oauth import FlaskAzureOauth
import dotenv
import os
from pathlib import Path


app = Flask(__name__)
CORS(
    app,
    origins = ["http://localhost:8080"],
    supports_credentials = True,  # does not appear to be needed?
)


dotenv.load_dotenv(Path(__file__).parent / '../app/.env.local')
app.config["AZURE_OAUTH_APPLICATION_ID"] = os.environ["VUE_APP_AZURE_OAUTH_BACKEND_APPLICATION_ID"]
app.config["AZURE_OAUTH_TENANCY"] = os.environ["VUE_APP_AZURE_OAUTH_TENANCY"]


auth = FlaskAzureOauth()
auth.init_app(app)


@app.route("/unprotected")
def unprotected():
    return jsonify({"success": True})


@app.route("/protected")
@auth()
def protected():
    return jsonify({"success": True})


@app.route("/protected-with-role")
@auth("Write.All")
def protected_with_scope():
    return jsonify({"success": True})


app.run(debug=True)

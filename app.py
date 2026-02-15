from flask import Flask, render_template, request
from flask_mail import Mail, Message
import os
import uuid
import re
from topsis_daksh_102497020.topsis_engine import TopsisCalculator

# IMPORTANT: We will later import our own package
# from your_package_name.topsis import calculate_topsis

app = Flask(__name__)

# ---------------- FOLDER CONFIG ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "outputs")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)
# -----------------------------------------------


# ---------------- MAIL CONFIG ----------------
# Use environment variables instead of hardcoding
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")


mail = Mail(app)
# ---------------------------------------------


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)


@app.route("/", methods=["GET", "POST"])
def home():

    if request.method == "POST":

        uploaded_file = request.files.get("file")
        weights = request.form.get("weights")
        impacts = request.form.get("impacts")
        email = request.form.get("email")

        # ---- Basic Validation ----
        if not uploaded_file or not weights or not impacts or not email:
            return "All fields are mandatory."

        if not is_valid_email(email):
            return "Invalid email format."

        weight_list = weights.split(",")
        impact_list = impacts.split(",")

        if len(weight_list) != len(impact_list):
            return "Number of weights must match number of impacts."

        for imp in impact_list:
            if imp not in ["+", "-"]:
                return "Impacts must be either '+' or '-'."

        # Unique filename
        unique_id = str(uuid.uuid4())
        input_path = os.path.join(UPLOAD_FOLDER, unique_id + "_" + uploaded_file.filename)
        output_path = os.path.join(OUTPUT_FOLDER, "result_" + unique_id + ".csv")

        uploaded_file.save(input_path)

        try:
            calculator = TopsisCalculator(input_path, weights, impacts, output_path)
            calculator.execute()
        except Exception as e:
            return f"Error while processing TOPSIS: {str(e)}"


        # ---- Send Email ----
        msg = Message(
            subject="Your TOPSIS Result",
            sender=app.config["MAIL_USERNAME"],
            recipients=[email]
        )
        msg.body = "Attached is your TOPSIS result file."

        if os.path.exists(output_path):
            with open(output_path, "rb") as fp:
                msg.attach("result.csv", "text/csv", fp.read())
            mail.send(msg)

        return "TOPSIS executed successfully. Check your email."

    return render_template("index.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

import os

from flask import (Flask, abort, flash, redirect, render_template, send_file,
                   url_for)
from flask_wtf import FlaskForm
from wtforms import SubmitField, URLField
from wtforms.validators import URL, DataRequired

from feed import main as add_url

app = Flask(__name__)
# Secret key for CSRF protection
app.config["SECRET_KEY"] = os.urandom(24)


FEED_TITLE = os.getenv("FEED_TITLE", "Watch Later Feed")
FEED_DESCRIPTION = os.getenv("FEED_DESCRIPTION", "Watch Later Feed")
FEED_BASE_URL = os.getenv("FEED_BASE_URL", "https://watchlater.example.com")
FEED_FILE = os.getenv("FEED_FILE", "/feed.xml")
FEED_URL = FEED_BASE_URL + "/" + FEED_FILE
FLASK_PORT = int(os.getenv("FLASK_PORT", 8000))


class URLForm(FlaskForm):
    website = URLField(
        "Website URL",
        validators=[
            DataRequired(message="URL is required."),
            URL(message="Please enter a valid URL."),
        ],
    )
    submit = SubmitField("Submit")


@app.route("/add", methods=["GET", "POST"])
def index():
    form = URLForm()
    if form.validate_on_submit():
        url = form.website.data
        result = add_url([url], FEED_FILE, FEED_TITLE, FEED_BASE_URL, FEED_DESCRIPTION)
        flash(f"{result}", "success")
        return redirect(url_for("index"))
    return render_template("url_form.html", form=form)


@app.route("/feed")
def retrieve_feed():
    if not FEED_FILE or not os.path.isfile(FEED_FILE):
        abort(404)
    else:
        return send_file(
            FEED_FILE,
            mimetype="application/rss+xml",
            as_attachment=False,
            conditional=True,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT)

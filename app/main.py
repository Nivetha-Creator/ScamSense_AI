from pathlib import Path

from flask import (
    Flask,
    jsonify,
    render_template,
    request
)

from app.models.scam_detector import detect_scam
from app.models.llm_analyzer import analyze_scam


BASE_DIR = Path(__file__).resolve().parent.parent


app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static")
)


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        data = request.get_json(silent=True)


        if not data or "message" not in data:

            return jsonify({
                "error": "Message is required."
            }), 400


        message = str(data["message"]).strip()


        if not message:

            return jsonify({
                "error": "Message cannot be empty."
            }), 400


        if len(message) > 5000:

            return jsonify({
                "error": "Message is too long. Maximum 5000 characters."
            }), 400


        # Machine Learning
        ml_result = detect_scam(message)


        # AI explanation
        try:

            llm_result = analyze_scam(
                message,
                (
                    f"{ml_result['result']}, "
                    f"probability: "
                    f"{ml_result['scam_probability']}%"
                )
            )

        except Exception as llm_error:

            print("LLM error:", llm_error)

            llm_result = (
                "AI explanation is temporarily unavailable. "
                "The machine-learning result is still available."
            )


        return jsonify({

            "message": message,

            "ml_result": ml_result,

            "analysis": llm_result

        })


    except Exception as error:

        print("Analysis error:", error)

        return jsonify({

            "error":
                "Unable to analyze this message. "
                "Please try again."

        }), 500


if __name__ == "__main__":

    app.run(debug=True)
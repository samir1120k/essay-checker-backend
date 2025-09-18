from flask import Flask, request, jsonify
from flask_cors import CORS
from EssayRating import workflow
import os
import traceback

app = Flask(__name__)
# In dev you can keep '*' to simplify. In prod, restrict to your frontend origins.
CORS(app, resources={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "UPSC Essay Rating API",
        "status": "running",
        "endpoints": {
            "evaluate": "/evaluate (POST)",
            "health": "/health (GET)"
        }
    })


@app.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy", "message": "UPSC Essay Rating API is running"}), 200


@app.route("/evaluate", methods=["POST"])
def evaluate_essay():
    try:
        # Basic env guard (required by your workflow)
        if not os.getenv("GOOGLE_API_KEY"):
            return jsonify({"error": "Google API key not configured"}), 500

        if not request.is_json:
            return jsonify({"error": "Content-Type must be application/json"}), 415

        data = request.get_json(silent=True) or {}
        essay_text = (data.get("essay") or "").strip()
        if not essay_text:
            return jsonify({"error": "Essay text is required"}), 400

        # Optional: enforce a minimum essay length (uncomment if desired)
        # if len(essay_text.split()) < 100:
        #     return jsonify({"error": "Essay must be at least 100 words"}), 400

        # Run the evaluation workflow
        initial_state = {"essay": essay_text}
        result = workflow.invoke(initial_state)

        response = {
            "language_feedback": result.get("language_feedback", ""),
            "analysis_feedback": result.get("analysis_feedback", ""),
            "clarity_feedback": result.get("clarity_feedback", ""),
            "overall_feedback": str(result.get("overall_feedback", "")),
            "individual_score": result.get("individual_score", []),
            "avg_score": round(result.get("avg_score", 0), 2),
        }
        return jsonify(response), 200

    except Exception as e:
        # Log for debugging
        print(f"Error evaluating essay: {str(e)}")
        print(traceback.format_exc())
        return jsonify({"error": "Failed to evaluate essay. Please try again."}), 500


# Local dev entrypoint.
# For production (e.g., Vercel/Gunicorn), the platform will import `app`.
if __name__ == "__main__":
    # Use 0.0.0.0 to allow access from other devices on the network if needed.
    app.run(debug=True, host="0.0.0.0", port=5000)
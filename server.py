from flask import Flask, request, jsonify
from flask_cors import CORS


from AgenticAiProject import app as graph_app  

flask_app = Flask(__name__)
CORS(flask_app)        

@flask_app.route("/ask", methods=["POST"])
def ask():
    data   = request.get_json(force=True)
    query  = data.get("query", "").strip()
    if not query:
        return jsonify({"error": "empty query"}), 400

    result = graph_app.invoke({
        "message":       query,
        "classify":      "",
        "needs_search":  "",
        "search_result": None,
        "column":        "",
        "model":         "",
        "response":      "",
    })

    return jsonify({
        "classify":      result.get("classify", ""),
        "needs_search":  result.get("needs_search", "no"),
        "search_result": result.get("search_result", ""),
        "model":         result.get("model", ""),
        "response":      result.get("response", ""),
    })

@flask_app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    print("NeurRoute server starting on http://localhost:5000")
    flask_app.run(host="0.0.0.0", port=5000, debug=False)
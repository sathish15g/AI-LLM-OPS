from flask import Flask, request, Response, jsonify, render_template
from dotenv import load_dotenv
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import traceback

from src.data_ingestion import DataIngestion
from src.rag_chain import RAGChainBuilder

load_dotenv()

REQUEST_COUNT = Counter("http_requests_total" , "Total HTTP Request")

def create_app():
    app = Flask(__name__)

    # Initialize once
    data_ingestion = DataIngestion()
    vector_store = data_ingestion.ingest_data(load_exiting=True)

    rag_chain = RAGChainBuilder(vector_store).build_chain()

    @app.route("/")
    def home():
        REQUEST_COUNT.inc()
        return render_template("index.html")

    @app.route("/ask", methods=["POST"])
    def ask():
        try:
            user_query = request.form.get("msg")

            if not user_query:
                return jsonify({"error": "Empty query"}), 400

            result = rag_chain.invoke(
                {"input": user_query},
                config={"configurable": {"session_id": "user-session"}}
            )

            return jsonify(result)

        except Exception as e:
            traceback.print_exc()
            return jsonify({
                "error": str(e)
            }), 500
    
    @app.route("/metrics")
    def metrics():
        return Response(generate_latest(), mimetype="text/plain; version=0.0.4; charset=utf-8")
    

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
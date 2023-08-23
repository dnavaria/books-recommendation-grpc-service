# marketplace/marketplace.py

import os
from flask import Flask, render_template

import grpc
from recommendations_pb2 import BookCategory, RecommendationRequest
from recommendations_pb2_grpc import RecommendationsStub

app = Flask(__name__)

# Create a channel to the recommendation server.
recommendation_host = os.getenv("RECOMMENDATION_HOST", "localhost")
channel = grpc.insecure_channel(f"{recommendation_host}:50051")
recommendations_client = RecommendationsStub(channel)


@app.route("/")
def render_homepage():
    recommendations_request = RecommendationRequest(user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3)
    recommendations_response = recommendations_client.Recommend(recommendations_request)
    return render_template(
        "homepage.html",
        recommendations=recommendations_response.recommendations,
    )
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
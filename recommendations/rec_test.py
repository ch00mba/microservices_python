from recommendations_pb2 import BookCategory, RecommendationRequest


request = RecommendationRequest(user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3)

request.category

request = RecommendationRequest(user_id="oops", category=BookCategory.SCIENCE_FICTION, max_results=3)

request = RecommendationRequest(user_id=1, category=BookCategory.SCIENCE_FICTION)

request.max_results





import grpc

from recommendations_pb2_grpc import RecommendationsStub

channel = grpc.insecure_channel("localhost:50051")
client = RecommendationsStub(channel)

request = RecommendationRequest(user_id=1, category=BookCategory.SCIENCE_FICTION, max_results=3)
client.Recommend(request)




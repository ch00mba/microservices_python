from concurrent import futures
import random

import grpc

from recommendations_pb2 import (
     BookCategory,
     BookRecommendation,
     RecommendationResponse,
)
import recommendations_pb2_grpc


books_by_category = {
    BookCategory.MYSTERY: [
        BookRecommendation(id=1, title="The Maltese Falcon"),
        BookRecommendation(id=2, title="Murder on the Orient Express"),
        BookRecommendation(id=3, title="The Hound of the Baskervilles"),
    ],
    BookCategory.SCIENCE_FICTION: [
        BookRecommendation(
            id=4, title="The Hitchhiker's Guide to the Galaxy"
        ),
        BookRecommendation(id=5, title="Ender's Game"),
        BookRecommendation(id=6, title="The Dune Chronicles"),
    ],
    BookCategory.SELF_HELP: [
        BookRecommendation(
            id=7, title="The 7 Habits of Highly Effective People"
        ),
        BookRecommendation(
            id=8, title="How to Win Friends and Influence People"
        ),
        BookRecommendation(id=9, title="Man's Search for Meaning"),
    ],
}



class RecommendationService(
    recommendations_pb2_grpc.RecommendationsServicer
):

    def Recommend(self, request, context):
        if request.category not in books_by_category:
            context.abort(grpc.StatusCode.NOT_FOUND, "Category not found")

        books_for_category = books_by_category[request.category]
        num_results = min(request.max_results, len(books_for_category))
        books_to_recommend = random.sample(
            books_for_category, num_results
        )

        return RecommendationResponse(recommendations=books_to_recommend)




def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    recommendations_pb2_grpc.add_RecommendationsServicer_to_server(
        RecommendationService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()




# Line 2 imports futures because gRPC needs a thread pool. You’ll get to that later.

# Line 3 imports random because you’re going to randomly select books for recommendations.

# Line 14 creates the books_by_category dictionary, in which the keys are book categories and the values are lists of books in that category. In a real Recommendations microservice, the books would be stored in a database.

# Line 29 defines the RecommendationService class. This is the implementation of your microservice. Note that you subclass RecommendationsServicer. This is part of the integration with gRPC that you need to do.

# Line 32 defines a Recommend() method on your class. This must have the same name as the RPC you define in your protobuf file. It also takes a RecommendationRequest and returns a RecommendationResponse just like in the protobuf definition. It also takes a context parameter. The context allows you to set the status code for the response.

# Lines 33 and 34 use abort() to end the request and set the status code to NOT_FOUND if you get an unexpected category. Since gRPC is built on top of HTTP/2, the status code is similar to the standard HTTP status code. Setting it allows the client to take different actions based on the code it receives. It also allows middleware, like monitoring systems, to log how many requests have errors.

# Lines 36 to 40 randomly pick some books from the given category to recommend. You make sure to limit the number of recommendations to max_results. You use min() to ensure you don’t ask for more books than there are, or else random.sample will error out.

# Line 38 returns a RecommendationResponse object with your list of book recommendations.

# Line 42 creates a gRPC server. You tell it to use 10 threads to serve requests, which is total overkill for this demo but a good default for an actual Python microservice.

# Line 43 associates your class with the server. This is like adding a handler for requests.

# Line 46 tells the server to run on port 50051. As mentioned before, this is the standard port for gRPC, but you could use anything you like instead.

# Lines 47 and 48 call server.start() and server.wait_for_termination() to start the microservice and wait until it’s stopped. The only way to stop it in this case is to type Ctrl+C in the terminal. In a production environment, there are better ways to shut down, which you’ll get to later.


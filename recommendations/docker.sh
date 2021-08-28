docker build . -f recommendations/Dockerfile -t recommendations

docker run -p 127.0.0.1:50051:50051/tcp recommendations
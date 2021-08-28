docker build . -f marketplace/Dockerfile -t marketplace

docker run -p 127.0.0.1:5000:5000/tcp marketplace
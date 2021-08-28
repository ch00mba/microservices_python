FROM python

RUN mkdir /service
COPY protobufs/ /service/protobufs/
COPY marketplace/ /service/marketplace/
WORKDIR /service/marketplace

RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m grpc_tools.protoc -I ../protobufs --python_out=. \
           --grpc_python_out=. ../protobufs/recommendations.proto

EXPOSE 5000
ENV FLASK_APP=marketplace.py
ENTRYPOINT [ "flask", "run", "--host=0.0.0.0"]


# Line 13 uses ENV FLASK_APP=marketplace.py to set the environment variable FLASK_APP inside the image. Flask needs this to run.
# Line 14 adds --host=0.0.0.0 to the flask run command. If you don’t add this, then Flask will only accept connections from localhost.
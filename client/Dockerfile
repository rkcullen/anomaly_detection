FROM python:3

RUN mkdir /service
COPY protobufs/ /service/
COPY client/ /service/
WORKDIR /service
RUN python -m pip install --upgrade pip
RUN python -m pip install grpcio-tools
RUN python -m grpc_tools.protoc -I . --python_out=. \
	   --grpc_python_out=. anomaly_detection.proto

ENTRYPOINT [ "python", "client.py" ]

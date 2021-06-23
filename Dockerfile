FROM python:3

RUN mkdir /service
COPY . /service/
WORKDIR /service/
RUN python -m pip install --upgrade pip
RUN python -m pip install grpcio-tools
RUN python -m pip install tad
RUN python -m grpc_tools.protoc -I . --python_out=. \
	   --grpc_python_out=. anomaly_detection.proto

EXPOSE 50051
ENTRYPOINT [ "python", "server.py" ]

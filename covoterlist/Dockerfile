FROM alpine:latest

WORKDIR /home/mspann/Redistricting/app

COPY requirements.txt /

RUN pip install -r /requirements.txt

EXPOSE 8080

COPY ./ ./

CMD ["phython", "./app.py"]

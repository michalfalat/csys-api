FROM alpine:3.18

RUN mkdir /var/csys-api

WORKDIR /var/csys-api

COPY .  .

RUN apk update

RUN apk add python3

RUN pip3 install -r requirements.txt

EXPOSE 3003 

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3003"] -h
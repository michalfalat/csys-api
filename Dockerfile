FROM alpine:3.18

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

COPY .  .

# Install necessary dependencies
RUN apk update && \
    apk add --no-cache python3 && \
    python3 -m ensurepip && \
    python3 -m pip install --upgrade pip && \
    pip install -r /code/requirements.txt

EXPOSE 3003 

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3003"]
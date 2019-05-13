FROM python:3.6-alpine

RUN apk update && apk add --no-cache postgresql-dev python3-dev musl-dev \
    && pip3 install --upgrade pip

RUN apk add --update --no-cache g++ gcc libxslt-dev

WORKDIR /docker_container

COPY . /docker_container

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 8080

ENTRYPOINT ["python3"]

CMD ["run.py"]

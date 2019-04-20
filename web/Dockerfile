FROM python:3-alpine
WORKDIR /data/
RUN pip install --no-cache-dir pipenv
COPY src/Pipfile .
RUN apk add --no-cache --virtual .build-deps gcc musl-dev make
RUN pipenv --three install
RUN apk del .build-deps gcc musl-dev make
COPY src/ .
EXPOSE 80
ENTRYPOINT [ "pipenv", "run" ]
CMD [ "python", "serve.py" ]

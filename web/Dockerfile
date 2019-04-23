FROM node:alpine as assets
RUN apk add --no-cache --virtual git
WORKDIR /data/
RUN npm install --global gulp-cli
RUN git clone https://github.com/CiscoDevNet/CiscoUIKit.git
WORKDIR /data/CiscoUIKit
RUN npm install
RUN npm run build

FROM python:3-alpine
WORKDIR /data/
RUN pip install --no-cache-dir pipenv
RUN apk add --no-cache --virtual .build-deps gcc musl-dev make
COPY src/Pipfile .
RUN pipenv --three install
RUN apk del .build-deps gcc musl-dev make
COPY src/ .
COPY --from=assets /data/CiscoUIKit/build/ web/static/cisco-ui
EXPOSE 80
ENTRYPOINT [ "pipenv", "run" ]
CMD [ "python", "serve.py" ]

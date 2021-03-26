FROM golang:1.15

RUN apt-get update -yqq; \
    curl -fsSL https://deb.nodesource.com/setup_lts.x | bash -; \
    apt-get install -y nodejs lsof; \
    npm i -g nodemon

WORKDIR /app

COPY go.mod go.sum ./

RUN go mod download

COPY cmd server start.sh ./

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 7777

ENTRYPOINT [ "/entrypoint.sh" ]

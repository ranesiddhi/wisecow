FROM ubuntu:latest

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y netcat-openbsd fortune-mod cowsay \
    && rm -rf /var/lib/apt/lists/*

ENV PATH="${PATH}:/usr/games"

COPY wisecow.sh .

RUN chmod +x wisecow.sh

EXPOSE 4499

CMD ["./wisecow.sh"]

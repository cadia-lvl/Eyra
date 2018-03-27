#Author: Róbert Kjaran
		modifications by Judy Fong

FROM debian:jessie

RUN apt-get update && apt-get install -yqq git
RUN curl -sL https://deb.nodesource.com/setup_4.x | bash -
RUN apt-get update && apt-get install -yqq nodejs

COPY . /eyra

WORKDIR /eyra

RUN ./Setup/setup.sh --all --no-ap

VOLUME /var/lib/mysql

RUN mkdir -p /docker-entrypoint-initdb.d
#ENTRYPOINT ["./docker-entrypoint.sh"]
ENTRYPOINT ["./install_tokens.sh"]

EXPOSE 443 80

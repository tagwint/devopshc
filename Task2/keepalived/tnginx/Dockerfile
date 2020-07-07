FROM ubuntu:16.04 
ARG WEBPORT
ARG WHO
COPY default.conf /etc/nginx/conf.d/default.conf
COPY keepalived_${WHO}.conf /etc/keepalived/keepalived.conf
COPY enter.sh /enter.sh
RUN apt-get update \
&& apt-get -y install nginx keepalived \
vim iputils-ping iproute2 less \
&& sed -i "s/WHO/$WHO/;s/WEBPORT/$WEBPORT/" /etc/nginx/conf.d/default.conf \
&& cat /etc/nginx/conf.d/default.conf \
&& unlink /etc/nginx/sites-enabled/default \
&& chmod +x /enter.sh \
&& echo This is $WHO container

CMD ["/enter.sh"]




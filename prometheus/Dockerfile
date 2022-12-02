FROM prom/prometheus:v2.40.2

COPY ./prometheus.yml /etc/prometheus/prometheus.yml
COPY ./web.yml /etc/prometheus/web.yml
COPY ./django.rules /etc/prometheus/django.rules
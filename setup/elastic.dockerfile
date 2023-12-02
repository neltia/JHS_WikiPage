ARG STACK_VERSION

FROM docker.elastic.co/elasticsearch/elasticsearch:${STACK_VERSION}

# Install plugin
RUN elasticsearch-plugin install analysis-nori

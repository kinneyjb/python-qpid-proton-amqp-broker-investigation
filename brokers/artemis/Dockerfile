FROM alpine:3.8 as stage_dist

ENV ARTEMIS_VERSION 2.6.3
ENV ARTEMIS_DIST apache-artemis-${ARTEMIS_VERSION}
ENV ARTEMIS_BIN_DIST $ARTEMIS_DIST-bin.tar.gz
ENV ARTEMIS_BIN_DIST_URL http://www.apache.org/dyn/closer.cgi?filename=/activemq/activemq-artemis/${ARTEMIS_VERSION}/$ARTEMIS_BIN_DIST&action=download
ENV ARTEMIS_BIN_DIST_VERIFY_URL https://www.apache.org/dist/activemq/activemq-artemis/${ARTEMIS_VERSION}/$ARTEMIS_BIN_DIST.sha512

RUN apk add --no-cache curl && \
    mkdir /downloads && \
    cd /downloads && \
    curl -L $ARTEMIS_BIN_DIST_URL -o $ARTEMIS_BIN_DIST && \
    curl -LO $ARTEMIS_BIN_DIST_VERIFY_URL && \
    cat $ARTEMIS_BIN_DIST.sha512 && \
    sha512sum -c $ARTEMIS_BIN_DIST.sha512

RUN cd /downloads && \
    tar zxf $ARTEMIS_BIN_DIST


FROM openjdk:12-alpine

EXPOSE 8161
EXPOSE 5672

ENV ARTEMIS_VERSION 2.6.3
ENV ARTEMIS_DIST apache-artemis-${ARTEMIS_VERSION}

RUN addgroup -g 1000 -S broker && \
    adduser -u 1000 -S broker -G broker && \
    mkdir /opt/broker && \
    chown broker:broker /opt/broker 

COPY --from=stage_dist /downloads/$ARTEMIS_DIST /opt/broker/$ARTEMIS_DIST

RUN chown -R broker:broker /opt/broker

USER 1000

RUN cd /opt/broker && \
    ./$ARTEMIS_DIST/bin/artemis create instance --user admin --password admin --allow-anonymous --host 0.0.0.0

WORKDIR /opt/broker/instance

ENTRYPOINT ./bin/artemis run

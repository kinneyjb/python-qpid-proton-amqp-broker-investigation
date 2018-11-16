FROM alpine:3.8 as stage_dist

ENV ACTIVEMQ_VERSION 5.15.7
ENV ACTIVEMQ_DIST apache-activemq-${ACTIVEMQ_VERSION}
ENV ACTIVEMQ_BIN_DIST $ACTIVEMQ_DIST-bin.tar.gz
ENV ACTIVEMQ_BIN_DIST_URL http://www.apache.org/dyn/closer.cgi?filename=/activemq/${ACTIVEMQ_VERSION}/$ACTIVEMQ_BIN_DIST&action=download
ENV ACTIVEMQ_BIN_DIST_VERIFY_URL https://www.apache.org/dist/activemq/${ACTIVEMQ_VERSION}/$ACTIVEMQ_BIN_DIST.sha512

RUN apk add --no-cache curl && \
    mkdir /downloads && \
    cd /downloads && \
    curl -L $ACTIVEMQ_BIN_DIST_URL -o $ACTIVEMQ_BIN_DIST && \
    curl -LO $ACTIVEMQ_BIN_DIST_VERIFY_URL && \
    cat $ACTIVEMQ_BIN_DIST.sha512 && \
    sha512sum -c $ACTIVEMQ_BIN_DIST.sha512

RUN cd /downloads && \
    tar zxf $ACTIVEMQ_BIN_DIST


FROM openjdk:12-alpine

EXPOSE 8161
EXPOSE 5672

ENV ACTIVEMQ_VERSION 5.15.7
ENV ACTIVEMQ_DIST apache-activemq-${ACTIVEMQ_VERSION}

RUN addgroup -g 1000 -S broker && \
    adduser -u 1000 -S broker -G broker && \
    mkdir /opt/broker && \
    chown broker:broker /opt/broker 

COPY --from=stage_dist /downloads/$ACTIVEMQ_DIST /opt/broker/$ACTIVEMQ_DIST

RUN chown -R broker:broker /opt/broker

USER 1000

RUN cd /opt/broker && \
    ./$ACTIVEMQ_DIST/bin/activemq create instance

WORKDIR /opt/broker/instance

ENTRYPOINT ./bin/instance console

# Apache QPID Proton with AMQP 1.0 Brokers

I recently used [apache qpid proton's](https://qpid.apache.org/proton/index.html)
[python api](https://qpid.apache.org/releases/qpid-proton-0.26.0/proton/python/book/tutorial.html)
and wanted to see if I could use it with other AMQP 1.0 brokers.

I "tested" a [simple python qpid proton message handler](./tests/test_docker_brokers.py#L8).

Included in this repo are 3 brokers:

1. [Apache ActiveMQ](http://activemq.apache.org/) Docker stuff: [brokers/activemq](broker/activemq)
1. [Apache ActiveMQ Artemis](https://activemq.apache.org/artemis/) Docker stuff: [brokers/artemis](broker/artemis)
1. [RabbtiMQ](https://github.com/rabbitmq/rabbitmq-amqp1.0/blob/v3.7.9/README.md) Docker stuff: [brokers/rabbitmq](broker/rabbitmq)


ActiveMQ and Artemis worked.
RabbitMQ had problems.
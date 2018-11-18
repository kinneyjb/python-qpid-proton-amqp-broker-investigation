from time import sleep
import threading
from proton import Message
from proton.reactor import ApplicationEvent, Container, EventInjector
from proton.handlers import MessagingHandler


class SendReceive(MessagingHandler):
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.messages = []

    def on_start(self, event):
        self.container = event.container
        self.conn = self.container.connect(f"{self.host}:{self.port}")
        self.receiver = self.container.create_receiver(self.conn, "test")
        self.sender = self.container.create_sender(self.conn, None)

    def on_send(self, event):
        message = Message(body="test")
        message.address = "test"
        self.sender.send(message)

    def on_message(self, event):
        self.messages.append(event.message)

    def on_quit(self, event):
        self.sender.close()
        self.receiver.close()
        self.conn.close()


def test_sendreceive():
    handler = SendReceive('192.168.99.100', 5672)
    reactor = Container(handler)
    events = EventInjector()
    reactor.selectable(events)
    thread = threading.Thread(target=reactor.run)
    thread.daemon = True
    thread.start()
    events.trigger(ApplicationEvent("send"))
    sleep(2)
    events.trigger(ApplicationEvent("quit"))
    assert len(handler.messages) == 1
    print(handler.messages)

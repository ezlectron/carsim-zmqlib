import jsonpickle
import logging
import threading
import time
import zmq

from zmqlib.msg import EngineSimZeroMqRequestMessage, EngineSimZeroMqResponseMessage

class ZeroMqClientController(object):

    _instance = None
    _running = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, connect_spec):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REQ)
        self._socket.connect(connect_spec)

        logging.info("ZMQ Controller is now connected to {}".format(connect_spec))

    def sendMessage(self, req_msg_object):
        if not isinstance(req_msg_object, EngineSimZeroMqRequestMessage):
            logging.error("Cannot send message - must be of Request type")

        # Send the object as JSON struct via ZeroMQ
        req_msg_json = jsonpickle.encode(req_msg_object)
        self._socket.send_json(req_msg_json)

        # Receive the reply - check that it is of the Response Type
        resp_msg_json = self._socket.recv_json()
        resp_msg_object = jsonpickle.decode(resp_msg_json)

        if not isinstance(resp_msg_object, EngineSimZeroMqResponseMessage):
            logging.error("Received unexpected reply after sending message - not of Response type")
            return

        print("Received response: %s" % resp_msg_object)
        print ("ZMQ Message: Type {}, Status {}".format(resp_msg_object.getMessageType(), resp_msg_object.getStatusCode()))


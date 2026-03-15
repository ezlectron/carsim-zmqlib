import jsonpickle
import logging
import threading
import time
import zmq

from zmqlib.msg import EngineSimZeroMqRequestMessage, EngineSimZeroMqResponseMessage, EngineSimZeroMqCarStateResponseMessage

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

        self._sync_state_req_message = None
        self._sync_state_req_message_lock = threading.Lock()
        self._sync_state_resp_message = None
        self._sync_state_resp_message_lock = threading.Lock()

        self._running = True
        self._sync_message_thread = threading.Thread(target = self._state_sync_message_thread)
        self._sync_message_thread.start()

        logging.info("ZMQ Controller is now connected to {}".format(connect_spec))

    # Sends a single message
    def sendMessage(self, req_msg_object):
        if not isinstance(req_msg_object, EngineSimZeroMqRequestMessage):
            logging.error("Cannot send message - must be of Request type")

        # Send the object as JSON struct via ZeroMQ
        req_msg_json = jsonpickle.encode(req_msg_object)
        self._socket.send_json(req_msg_json)

        # Receive the reply - check that it is of the Response Type
        resp_msg_json = self._socket.recv_json()
        self._sync_state_resp_message = jsonpickle.decode(resp_msg_json)

        if not isinstance(self._sync_state_resp_message, EngineSimZeroMqResponseMessage):
            logging.error("Received unexpected reply after sending message - not of Response type")
            return

        #print("Received response: %s" % self._sync_state_resp_message)
        #print ("ZMQ Message: Type {}, Status {}".format(self._sync_state_resp_message.getMessageType(), self._sync_state_resp_message.getStatusCode()))

    # Update the message that needs to be synced with the server
    def updateStateSyncMessage(self, req_msg_object):
        self._sync_state_req_message_lock.acquire()
        self._sync_state_req_message = req_msg_object
        self._sync_state_req_message_lock.release()

    def getStateSyncResponse(self) -> EngineSimZeroMqCarStateResponseMessage:
        return self._sync_state_resp_message

    # Continiously send a message to sync it with the server
    def _state_sync_message_thread(self):

        while self._running:

            # Only send when the message has been set
            if self._sync_state_req_message is not None:
                self._sync_state_req_message_lock.acquire()
                self.sendMessage(self._sync_state_req_message)
                self._sync_state_req_message_lock.release()

            time.sleep(0.5)
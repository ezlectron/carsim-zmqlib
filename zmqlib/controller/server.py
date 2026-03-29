import jsonpickle
import logging
import threading
import time
import zmq

from zmqlib.msg import ZmqRequestMessage, ZmqResponseMessage, ZmqCarControlRequestMessage

logger = logging.getLogger("zmqctrl")

class ZeroMqServerController(object):

    MSG_TIMEOUT = 2                 # We expect a message within 2 seconds
    MSG_TIMEOUT_THRD_INTERVAL = 0.2 # Check for timeouts every 20 msecs

    _instance = None
    _running = False

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self, bind_spec):
        self._context = zmq.Context()
        self._socket = self._context.socket(zmq.REP)
        self._socket.bind(bind_spec)

        logging.info("ZMQ Controller is now listening on {}".format(bind_spec))

        self._sync_state_req_message = None
        self._sync_state_req_message_lock = threading.Lock()
        self._sync_state_resp_message = None
        self._sync_state_resp_message_lock = threading.Lock()

        self._msg_last_received_ts = 0
        self._msg_last_received_ts_lock = threading.Lock()

        self._msg_received = None

        self._callback_func_list = list()
        self._msg_expire_func_list = list()

        self._running = True
        self._zmq_listener = threading.Thread(target=self._listener_thread)
        self._zmq_listener.start()
        self._zmq_timeout_checker = threading.Thread(target=self.recv_timeout_checker_thread)
        self._zmq_timeout_checker.start()

    def quit(self):
        self._running = False

    # Registers a callback function for when an action message is received
    def registerActionMessageCallBack(self, callback_func):
        self._callback_func_list.append(callback_func)

    # Registers a callback function for when a message expires
    def registerMessageExpiresCallBack(self, callback_func):
        self._msg_expire_func_list.append(callback_func)

    # Updates the state message that is returned in response to requests
    def updateStateSyncResponse(self, resp_msg_object : ZmqResponseMessage):
        self._sync_state_resp_message_lock.acquire()
        self._sync_state_resp_message = resp_msg_object
        self._sync_state_resp_message_lock.release()

    # Get the latest action state
    def getStateSyncRequest(self) -> ZmqCarControlRequestMessage:
        return self._sync_state_req_message

    def _listener_thread(self):
        while self._running:

            #
            # Receive the request and save it in a thread-safe way
            req_msg_json = self._socket.recv_json()
            req_msg_object = jsonpickle.decode(req_msg_json)

            # Save the timestamp at which the last message was received
            self._msg_last_received_ts_lock.acquire()
            self._msg_last_received_ts = time.time()
            self._msg_last_received_ts_lock.release()

            # Check that the given message is of the right type
            if not isinstance(req_msg_object, ZmqRequestMessage):
                logging.error("Invalid message received - must be of Request type")

            if isinstance(req_msg_object, ZmqCarControlRequestMessage):

                # Save the message
                self._sync_state_req_message_lock.acquire()
                self._sync_state_req_message = req_msg_object
                self._sync_state_req_message_lock.release()

                # Do the callbacks
                for cb in self._callback_func_list:
                    cb(req_msg_object)

            #
            # Create the response
            #  If there is no state object set yet, we simply return a standard response
            if not self._sync_state_resp_message:
                resp_msg_object = ZmqResponseMessage(ZmqResponseMessage.MSG_STATUS_CODE_OK)
            else:
                resp_msg_object = self._sync_state_resp_message

            #
            # Send the response in a thread-safe way
            self._sync_state_resp_message_lock.acquire()
            resp_msg_json = jsonpickle.encode(resp_msg_object, max_depth=10)
            self._socket.send_json(resp_msg_json)
            self._sync_state_resp_message_lock.release()

    def recv_timeout_checker_thread(self):

        while (self._running):

            self._msg_last_received_ts_lock.acquire()

            # If we haven´t received a timeout yet or if we have just processed it
            #  we don´t need to do anything
            if self._msg_last_received_ts > 0:

                # If the timeout has expired
                if self._msg_last_received_ts + self.MSG_TIMEOUT < time.time():

                    # Reset so that we don´t enter the check again until after we have
                    #  received the next message and that one expires
                    self._msg_last_received_ts = 0

                    # Do the callbacks
                    for cb in self._msg_expire_func_list:
                        cb()

            self._msg_last_received_ts_lock.release()

            time.sleep(self.MSG_TIMEOUT_THRD_INTERVAL)
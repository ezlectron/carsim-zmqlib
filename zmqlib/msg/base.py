

class ZmqBaseMessage():

    MSG_TYPE_REQUEST = "REQ"
    MSG_TYPE_RESPONSE = "RES"

    MSG_STATUS_CODE_OK = "OK"
    MSG_STATUS_CODE_FAIL = "FAIL"

    def __init__(self, type, status):
        self._type = type
        self._status = status


    def getMessageType(self):
        return self._type

    def getStatusCode(self):
        return self._status
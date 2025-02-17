from bluepy import btle
import logging


log = logging.getLogger("jkBleDelegate")


class jkBleDelegate(btle.DefaultDelegate):
    """
    BLE delegate to deal with notifications (information) from the JKBMS device
    """

    def __init__(self, jkbleio, protocol, record_type=None):
        btle.DefaultDelegate.__init__(self)
        # extra initialisation here
        self._jkbleio = jkbleio
        if protocol is None:
            print("ERROR")
            exit(1)
        self._protocol = protocol
        self._record_type = record_type
        self.notificationData = bytearray()

    def handleNotification(self, handle, data):
        # handle is the handle of the characteristic / descriptor that posted the notification
        # data is the data in this notification - may take multiple notifications to get all of a message
        log.debug("From handle: {:#04x} Got {} bytes of data".format(handle, len(data)))
        self.notificationData += bytearray(data)
        if not self._protocol.is_record_start(self.notificationData):
            log.debug(f"Not valid start of record - wiping data {self.notificationData}")
            self.notificationData = self.notificationData[20:]
        #if not self._protocol.is_record_correct_type(self.notificationData, self._record_type):
        #    log.debug(f"Not expected type of record - wiping data {self.notificationData}")
        #    self.notificationData = bytearray()
        if len(self.notificationData) > 300:
            self.notificationData = self.notificationData[-300:]
        if self._protocol.is_record_complete(self.notificationData):
            if self._protocol.is_record_correct_type(self.notificationData, self._record_type):
                self._jkbleio.record = self.notificationData[:300]
                log.debug("record complete")
            if self._protocol.is_record_correct_type(self.notificationData, 3): # getInfo
                self._jkbleio.info_record = self.notificationData[:300]
                log.debug("info record complete")
                # print(self._jkbleio.info_record)
            self.notificationData = bytearray()

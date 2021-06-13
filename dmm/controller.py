from dmm.data import DMMData
import logging
import abc
import threading
import time
from typing import Set


from .exceptions import NotConnectedDevice
from .listener import DMMListenerBase

logger = logging.getLogger(__file__)


class DMMControllerBase(abc.ABC):
    def __init__(self) -> None:
        self.is_connected = False
        self.is_running = False
        self.recv_thread = threading.Thread(name="DMMReceiver", target=self.recv)
        self.listeners: Set[DMMListenerBase] = set()

    def connect(self) -> None:
        if self.is_connected:
            logger.warning("Connected to device already!")
        else:
            logger.debug("Connect to device")
            self._connect()
            self.is_connected = True

    def disconnect(self) -> None:
        if not self.is_connected:
            logger.warning("Not connected to device!")
        else:
            logger.debug("Disconnect from device")
            self._disconnect()
            self.is_connected = False

    def start(self) -> None:
        if not self.is_connected:
            logger.error("Device is not connected")
            raise NotConnectedDevice
        if not self.is_running:
            logger.info("Start receive data")
            self.is_running = True
            self.recv_thread.start()
        else:
            logger.warning("Receiving data already, not start")

    def stop(self) -> None:
        if self.is_running:
            logger.info("Stop receive data")
            self.is_running = False
            self.recv_thread.join()
        else:
            logger.warning("Not receiving data")

    def add_listener(self, listener: DMMListenerBase) -> None:
        assert isinstance(listener, DMMListenerBase)
        self.listeners.add(listener)

    def remove_listener(self, listener: DMMListenerBase) -> None:
        self.listeners.remove(listener)

    def notify_data(self, data: DMMData) -> None:
        for l in self.listeners:
            # call on received data in new thread
            threading.Thread(target=l.on_received_data(data)).start()

    def notify_error(self, error_code: int) -> None:
        for l in self.listeners:
            # call on error in new thread
            threading.Thread(target=l.on_error(error_code)).start()

    def recv(self) -> None:
        while self.is_running:
            try:
                data = self._recv()
                self.notify_data(data)
            except:
                self.notify_error(0)  # TODO: add error code here
            time.sleep(0.1)

    @abc.abstractmethod
    def _connect(self) -> None:
        pass

    @abc.abstractmethod
    def _disconnect(self) -> None:
        pass

    @abc.abstractmethod
    def _recv(self) -> DMMData:
        pass

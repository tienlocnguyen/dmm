import sys
import time
import logging

import argparse

sys.path.append("../")
from dmm.controllers import DMMController
from dmm.listener import DMMLogListener


logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--device", help="device type of dmm")
    args, device_args = parser.parse_known_args()

    controller = DMMController(args.device, *device_args)  # type: ignore [abstract]
    listener = DMMLogListener(logger, logging.DEBUG)
    controller.add_listener(listener)
    controller.connect()
    controller.start()
    time.sleep(10)
    controller.stop()
    controller.disconnect()

# DMM
Python driver for Digital Multi Meter(DMM). List of supported device
|#|Device name|Manufacture|
|-|-|-|
|1|[VICTOR V86D](http://www.china-victor.com/index.php?m=content&c=index&a=show&catid=42&id=28)|[Victor](http://www.china-victor.com/html/en/)|
# Install
T.B.D
# Usage
## Create device controller
Firstly, you need to create instant of device controller and pass device name and associated parameter
```python
controller = DMMController('v86d', '/dev/ttyUSB0')
```
## Setup and register listener
Listener will handle received data and error event. Currently, a log listener is implemented. You can create your own listener by inherit [DMMListenerBase](./dmm/listener.py)
```python
listener = DMMLogListener(logger, logging.DEBUG)
controller.add_listener(listener)
```
## Start monitor
Now you're ready to connect and start monitor
```python
controller.connect()
controller.start()
```
## Stop when finish
Stop and disconnect after finish
```python
controller.stop()
controller.disconnect()
```
> Example of DMM monitor in [Monitor tool](./tools/monitor.py)
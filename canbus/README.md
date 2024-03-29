## Canbus Signal Plot

### Intro
- Plot specific can frame cycle and its time difference between each signal.
- Assist evaluating desired can rate from sender

![pic](https://github.com/ancabilloni/network_analysis_tools/blob/master/canbus/can_signal_plot.png)

### Require
- Linux (tested on Ubuntu 18.04, but should also work on system with SocketCAN)
- Python3 or 2. The script is test on Python3 but should work on cross platform.
- pyqtgraph: `pip3 install pyqtgraph`
- PyQt5 (or PyQt4 or PySide): `pip3 install PyQt5`
- python-can: `pip3 install python-can`
- PC with either embedded CAN device or CAN-USB Adapter set up for CAN0

### Run
```
cd path/to/network_analysis/canbus
./main.py can_id expect_coming_rate
```

For example: `./main.py 0xA12 100`

`./main.py ` only: read any incoming can frame
`./main.py can_id` only: expect specific can frame with default expected rate 100


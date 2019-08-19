## Canbus Signal Plot

### Intro
- Plot specific can frame cycle and its time difference between each signal.
- Assist evaluating desired can rate from sender


### Require
- Python3 or 2. The script is test on Python3 but should work on cross platform.
- pyqtgraph: `pip3 install pyqtgraph`
- PyQt5 (or PyQt4 or PySide): `pip3 install PyQt5`
- python-can: `pip3 install python-can`

### Run
```
cd path/to/network_analysis/canbus
./main.py can_id
```

For example: `./main.py 0xA12`

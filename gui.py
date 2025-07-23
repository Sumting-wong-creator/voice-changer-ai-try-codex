import sys
import json
import requests
from PyQt5 import QtWidgets, QtGui, QtCore

API_URL = 'http://127.0.0.1:8765'

class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('AI Voice Changer')
        self.setFixedSize(400, 300)
        self.setStyleSheet('background: rgba(255,255,255,0.25); backdrop-filter: blur(10px); color: #333;')

        layout = QtWidgets.QVBoxLayout()
        self.input_combo = QtWidgets.QComboBox()
        self.output_combo = QtWidgets.QComboBox()
        self.monitor_cb = QtWidgets.QCheckBox('Hear myself')
        self.monitor_cb.setChecked(False)
        self.start_btn = QtWidgets.QPushButton('Start')
        self.stop_btn = QtWidgets.QPushButton('Stop')
        self.level_bar = QtWidgets.QProgressBar()

        layout.addWidget(QtWidgets.QLabel('Input'))
        layout.addWidget(self.input_combo)
        layout.addWidget(QtWidgets.QLabel('Output'))
        layout.addWidget(self.output_combo)
        layout.addWidget(self.monitor_cb)
        layout.addWidget(self.start_btn)
        layout.addWidget(self.stop_btn)
        layout.addWidget(self.level_bar)
        self.setLayout(layout)

        self.start_btn.clicked.connect(self.start)
        self.stop_btn.clicked.connect(self.stop)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_level)
        self.load_devices()

    def load_devices(self):
        try:
            inp = requests.get(f'{API_URL}/inputDevices').json()
            out = requests.get(f'{API_URL}/outputDevices').json()
            self.input_combo.addItems(inp)
            self.output_combo.addItems(out)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', f'Failed to load devices: {e}')

    def start(self):
        data = {
            'pth_path': 'models/model.pth',
            'index_path': 'models/model.index',
            'sg_input_device': self.input_combo.currentText(),
            'sg_output_device': self.output_combo.currentText()
            'sg_output_device': self.output_combo.currentText(),
            'monitor': self.monitor_cb.isChecked()
        }
        try:
            requests.post(f'{API_URL}/config', json=data)
            requests.post(f'{API_URL}/start')
            self.timer.start(100)
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', f'Failed to start: {e}')

    def stop(self):
        try:
            requests.post(f'{API_URL}/stop')
            self.timer.stop()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, 'Error', f'Failed to stop: {e}')

    def update_level(self):
        # Placeholder for real audio level
        self.level_bar.setValue((self.level_bar.value()+5)%100)

app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())

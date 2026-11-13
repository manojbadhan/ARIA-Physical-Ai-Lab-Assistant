from hardware.communication.serial_handler import SerialHandler

class DeviceManager:
    def __init__(self): self.devices = {}
    def discover(self):
        from serial.tools import list_ports
        return [p.device for p in list_ports.comports()]
    def connect(self, name, port): self.devices[name] = SerialHandler(port); return self.devices[name]
    def send(self, name, **msg): self.devices[name].send(**msg)
    def close_all(self):
        for d in self.devices.values(): d.close()

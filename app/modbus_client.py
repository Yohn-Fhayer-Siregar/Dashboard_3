from pymodbus.client import ModbusTcpClient #Library pymodbus

class ModbusManager:
    def __init__(self):
        self.client = None

    def connect(self, ip, port):
        self.client = ModbusTcpClient(ip, port=port)
        return self.client.connect()

    def write(self, address, value):
        return self.client.write_register(address, value)

    def read(self, address, count=1):
        return self.client.read_holding_registers(address, count).registers

modbus = ModbusManager()
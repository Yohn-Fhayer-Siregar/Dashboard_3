import time
from app.modbus_client import modbus
from app.robot_state import robot_data


class TaskRunner:

    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        self.run()

    def run(self):
        plan = robot_data["plan"]

        points = plan["points"]
        loops = plan["loop_count"]

        if loops == 0:
            loops = 999999

        for i in range(loops):
            if not self.running:
                break

            for p in points:
                if not self.running:
                    break

                robot_data["status"]["target_point"] = p

                modbus.write(40001, p)
                modbus.write(40002, 1)

                while True:
                    if self.is_reached(p):
                        robot_data["status"]["current_point"] = p
                        break

                    time.sleep(1)

    def is_reached(self, target):
        try:
            task = modbus.read(40050, 1)[0]
            station = modbus.read(40051, 1)[0]

            return task == 0 and station == target
        except:
            return False


runner = TaskRunner()
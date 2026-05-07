robot_data = {
    "modbus": {
        "ip": "192.168.0.9",
        "port": 502,
        "unit_id": 1,
        "connected": False
    },

    "status": {
        "state": "idle",
        "current_point": -1,
        "target_point": -1,
        "battery_percent": 100,
        "charging": False
    },

    "plan": {
        "points": [],
        "loop_mode": "count",
        "loop_count": 1,
        "charge_point": 0,
        "battery_threshold": 30,
        "resume_threshold": 60,
        "retry": 3
    }
}
import random
from time import sleep

from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.sensors import VehicleSensorConfig

import json

# Load the JSON file
file_path = "C:/Users/.../lanechangeRAT.json"

def convert_json_trajectory(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    
    # Extract the path
    script = [
        {
            "t": node["t"],
            "x": node["x"],
            "y": node["y"],
            "z": node["z"]
        }
        for node in data["path"]
    ]
    
    return script

# Convert the JSON trajectory
myscript = convert_json_trajectory(file_path)

# Print output
import json
print(json.dumps(myscript, indent=4))



def main():
    random.seed(1703)
    set_up_simple_logging()

    beamng = BeamNGpy("localhost", 25252)
    bng = beamng.open(launch=True)

    scenario = Scenario(
        "tech_ground",
        "VehicleSensorConfig",
        description="Importing a pre-made ADAS sensor suite.",
    )

    vehicle = Vehicle("ego_vehicle", model="etk800", license="ADASConfig")

    scenario.add_vehicle(
        vehicle, pos=(158.787, 99.926, 0.206), rot_quat=(0, 0, 0.3826834, 0.9238795))
    scenario.make(bng)

    bng.settings.set_deterministic(60)  # Set simulator to 60hz temporal resolution

    bng.scenario.load(scenario)
    bng.ui.hide_hud()
    bng.scenario.start()

    #  vehicle.ai.set_mode("traffic")
    vehicle.ai.set_script(myscript)

    # Path to config file is relative to user folder ie: /AppData/Local/BeamNG.drive/0.XX/
    config = VehicleSensorConfig("configV", bng, vehicle, "/configV.json")

    print("Driving around, polling all sensors of the configuration periodically...")
    for _ in range(20):
        sleep(1)
        for s in range(len(config.sensors)):
            sensor = config.sensors[s]
            print(sensor.name)
            print(sensor.poll())

    config.remove()
    print("Scenario finished.")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()

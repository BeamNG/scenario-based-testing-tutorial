from pathlib import Path
import random
import shutil
from time import sleep

from beamngpy import BeamNGpy, Scenario, Vehicle, set_up_simple_logging
from beamngpy.sensors import VehicleSensorConfig
from beamngpy.sensors import MapSensorConfig

import json

# Load the JSON file
SCRIPT_DIR = Path(__file__).parent.resolve()

folder_path = str(SCRIPT_DIR)

# Copy the entire folder and its contents
def copy_level_folder(dest_dir: Path):
    file = "data/tech_ground"
    if dest_dir.exists():
        shutil.rmtree(dest_dir)

    # Copy the entire source folder to the destination
    #dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copytree(SCRIPT_DIR / file, dest_dir)

file_path = str(SCRIPT_DIR) + "/data/scriptedturn.json"

def copy_traffic_config_files(dest_dir: Path):
    files = [
        "data/techground_map_sensor_config.json",
        "data/vehicle_sensors_techground.json",
    ]
    dest_dir.mkdir(parents=True, exist_ok=True)
    for file in files:
        shutil.copy(SCRIPT_DIR / file, dest_dir)

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

    # we need to copy the configuration files to the user path
    destination_path = Path(bng.user_with_version)
    copy_level_folder(destination_path / "levels/tech_ground")
    print(f"Copied level configuration to {destination_path}.")
    copy_traffic_config_files(destination_path)
    print(f"Copied traffic configuration to {destination_path}.")

    scenario = Scenario(
        "tech_ground",
        "MapAndVehicleSensorConfig",
        description="Importing a pre-made ADAS sensor suite.",
    )

    vehicle = Vehicle("ego_vehicle", model="etk800", license="ADASConfig")

    scenario.add_vehicle(
        vehicle, pos=(128.0, 128.0, 0.206), rot_quat=(0, 0, 0.3826834, 0.9238795))
    scenario.make(bng)
    # vehicle, pos=(158.787, 99.926, 0.206), rot_quat=(0, 0, 0.3826834, 0.9238795))
    bng.settings.set_deterministic(60)  # Set simulator to 60hz temporal resolution

    bng.scenario.load(scenario)
    bng.ui.hide_hud()
    bng.scenario.start()

    #  vehicle.ai.set_mode("traffic")
    vehicle.ai.set_script(myscript)

    # Path to config file is relative to user folder ie: /AppData/Local/BeamNG.drive/0.XX/
    config = VehicleSensorConfig("configV", bng, vehicle, "/vehicle_sensors_techground.json")

    # Path to config file is relative to user folder ie: /AppData/Local/BeamNG.drive/0.XX/
    config2 = MapSensorConfig("configM", bng, "/techground_map_sensor_config.json")

    print("Driving around, polling all sensors of the configuration periodically...")
    for _ in range(20):
        sleep(1)
        for s in range(len(config.sensors)):
            sensor = config.sensors[s]
            print(sensor.name)
            print(sensor.poll())

    config.remove()

    for _ in range(20):
        sleep(1)
        for s in range(len(config2.sensors)):
            sensor = config2.sensors[s]
            print(sensor.name)
            print(sensor.poll())

    config2.remove()
    print("Scenario finished.")
    bng.ui.show_hud()
    input("Press Enter to exit...")
    bng.disconnect()

    print("Scenario finished.")
    input("Press Enter to exit...")


if __name__ == "__main__":
    main()

"""
How to launch a traffic scenario with sensors configuration :
1. Open traffic_sensors.py in the IDLE (for example Visual Studio Code);
2. Make sure that the files
- traffic_config_example.json
- lanechange2.json
- veh_sensors2.json
are in the folder 'data'
3. Run the script.
"""

#Note : If the software version changes from 0.35 to X.XX, one should edit the version number accordingly in the traffic_sensors.py file (where commented) and at the traffic_config_example.json, line 51.

import shutil
from pathlib import Path
from time import sleep

from beamngpy import BeamNGpy, set_up_simple_logging
from beamngpy.sensors import VehicleSensorConfig
from beamngpy.tools import TrafficConfig

SCRIPT_DIR = Path(__file__).parent.resolve()

def copy_traffic_config_files(dest_dir: Path):
    files = [
        "data/traffic_config_example.json",
        "data/lanechange2.json",
        "data/veh_sensors2.json",
    ]
    dest_dir.mkdir(parents=True, exist_ok=True)
    for file in files:
        shutil.copy(SCRIPT_DIR / file, dest_dir)


def main():
    set_up_simple_logging()
    beamng = BeamNGpy("localhost", 25252)
    try:
        bng = beamng.open(launch = True)

        # we need to copy the configuration files to the user path
        destination_path = Path(bng.user_with_version)
        copy_traffic_config_files(destination_path)
        print(f"Copied traffic configuration to {destination_path}.")
        # Change version number (0.35) to X.XX if it is different from the current one.
        traffic = TrafficConfig(bng, "/0.35/traffic_config_example.json")
        # With TrafficConfig.vehicles[vehicle name set from traffic configuration] you can access the related Vehicle object
        veh_sensors = VehicleSensorConfig(
            "vehicle_sensors",
            bng,
            traffic.vehicles["thePlayer"],
            "/veh_sensors2.json",
        )


        for _ in range(20):
            sleep(1)
            for s in range(len(veh_sensors.sensors)):
                sensor = veh_sensors.sensors[s]
                print(sensor.name)
                print(sensor.poll())


        veh_sensors.remove()
        print("Example finished.")
    finally:
        try:
            beamng.close()
        except:
            pass


if __name__ == "__main__":
    main()

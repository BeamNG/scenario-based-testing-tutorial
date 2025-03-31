from beamngpy import BeamNGpy, set_up_simple_logging

def main(bng_home: str):
    """
    Start BeamNG using the Python API, wait for user to press a key, and then close everything
    """
    set_up_simple_logging()
    beamng = BeamNGpy('localhost', 25252, home=bng_home)
    try:
        bng = beamng.open()
        input("Press any key to kill the simulation")
    finally:
        try:
            if bng is not None:
                bng.close()
        except:
            pass

if __name__ == "__main__":
    # Note: Change this to the folder where you extracted BeamNG.tech
    BNG_HOME = "C:\\BeamNG\\BeamNG.tech.v0.35.0.0-minimized"
    main(BNG_HOME)
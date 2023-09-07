# A very important file that changes the environment variable to TEST
# when running tests via pytest.
import os

os.environ["MODE"] = "TEST"
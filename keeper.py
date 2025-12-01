import time
from pyautogui import press
import sys
from random import uniform
import optparse
import logging

# --- Configuration ---
# Interval range (in seconds) to wait before pressing the key.
# Using a range makes the timing less predictable.
# Default idle timeout is 5 minutes (300 seconds)
MIN_INTERVAL_SECONDS = 200  # 3 minutes 20 seconds
MAX_INTERVAL_SECONDS = 280  # 4 minutes 40 seconds

# Key to press. 'shift', 'ctrl', 'alt', 'cmd' (on Mac) are modifier keys.
# 'f15' or 'f16' are often good choices on Mac if available, as they rarely interfere.
# Avoid keys that type characters or trigger major actions.
KEY_TO_PRESS = 'shift'

# Total duration to run the script (in minutes)
ACTIVE_TIME_MINUTES = 360

# Disable pyautogui's fail-safe mechanism (moving mouse to corner to stop)
# Only disable if you are sure, otherwise it's a safety feature.
# pyautogui.FAILSAFE = False

# Maximum number of iterations to prevent infinite loops in case of errors
LOOP_MAX = 1000

def init(_opt, _start_time):
    counter = 0
    while counter < LOOP_MAX and time.time() < _start_time:

        # 1. Choose a random wait time within the defined interval
        wait_time = uniform(_opt.min, _opt.max)
        counter += 1

        # 2. Press the specified key
        press(_opt.key)
        # Print confirmation if you want verbose output
        logging.info(f"#{counter} '{_opt.key}' key pressed at {time.strftime('%H:%M:%S')}. Waiting for {wait_time:.2f} seconds...")

        # 3. Wait for the calculated time
        time.sleep(wait_time)


if __name__ == '__main__':
    parser = optparse.OptionParser()
    parser.add_option("--min", type="int", default=MIN_INTERVAL_SECONDS, help="Min value for interval range (in seconds) to wait before pressing the key.")
    parser.add_option("--max", type="int", default=MAX_INTERVAL_SECONDS, help="Max value for interval range (in seconds) to wait before pressing the key.")
    parser.add_option("--key", type="string", default=KEY_TO_PRESS, help="Key to press. 'shift', 'ctrl', 'alt', 'cmd' (on Mac) are modifier keys. Avoid keys that type characters or trigger major actions.")
    parser.add_option("-t", "--time", type="int", default=ACTIVE_TIME_MINUTES, help="Total duration to run the script (in minutes).")
    parser.add_option("-v", "--verbose", action="store_const", dest="log_level", const=logging.INFO, default=logging.WARNING, help="Print additional informations.")
    opt, _ = parser.parse_args()

    logging.basicConfig(format="[%(levelname)s]: %(message)s", stream=sys.stdout, level=opt.log_level)
    #logging.error("Error messages test.")
    #logging.warning("Starting Activity Keeper...")
    logging.info("Verbose mode is ON.")
    logging.debug('Debug mode is ON.')

    logging.info("--- Activity Keeper ---")

    logging.info(f"Pressing the '{opt.key}' key every {opt.min}-{opt.max} seconds.")
    logging.info("This script runs in the foreground of the terminal.")
    logging.info("To stop, press Ctrl+C in this terminal window.")
    logging.info("---------------------------")

    start_time = time.time() + (opt.time * 60)

    try:
        init(opt, start_time)
    except KeyboardInterrupt:
        logging.info("Script stopped by user (Ctrl+C). Exiting.")
        sys.exit(0)
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        logging.error("Please ensure necessary permissions are granted.")
        sys.exit(1)

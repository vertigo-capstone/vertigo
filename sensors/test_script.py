# test_script.py
import time

with open("/home/vertigo/vertigo/test_output.log", "a") as log:
    log.write(f"Script executed at {time.strftime('%Y-%m-%d %H:%M:%S')}\n")

# 간단히 실행을 유지
time.sleep(10)

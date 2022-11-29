import cv2
from datetime import datetime
import urllib.request
import subprocess
from pathlib import Path
import re
import sys
import tomllib

DARKNET_PATH = (Path.cwd() / "darknet").resolve()
CREDENTIALS_FILE = Path("credentials.toml").resolve()

def capture_image(image_name: Path) -> None:
    cap = cv2.VideoCapture(0)

    failure_counter = 5
    
    while True:
        ret, frame = cap.read()
        status = cv2.imwrite(image_name, frame)

        if status is not True:

            if failure_counter < 0:
                raise RuntimeError()
            
            failure_counter = failure_counter - 1
            continue

        break

    cap.release()

def show_image(image_name: Path) -> None:
    img = cv2.imread(str(image_name))
    cv2.imshow("DEBUG", img)
    cv2.waitKey(0)  

def darknet_process(image_name: Path, log_name: Path) -> int:
    print(f"Inicia darknet")

    results = subprocess.run([
            "./darknet",
            "detect",
            "cfg/yolov3.cfg",
            "yolov3.weights",
            image_name
        ],
        capture_output=True,
        text=True,
        cwd=DARKNET_PATH
    )

    with open(log_name, "w") as f:
        f.write(results.stdout)

    print(f"termina darknet y logs en {log_name}")

    car_count = 0
    for line in results.stdout.strip().split("\n"):
        print(line)
        # car: 99%
        if re.search("car: ", line):
            carPercentage = float(line.strip().split(": ")[1].strip("%"))

            if carPercentage < 80.0:
                continue

            car_count = car_count + 1

    return car_count

def thingspeak_post(value):

    with open(CREDENTIALS_FILE, "rb") as f:
        data = tomllib.load(f)

    write_api_key = data["secrets"]["api_key"]

    URl='https://api.thingspeak.com/update?api_key='+ write_api_key +'&field1=0'

    KEY= write_api_key
    HEADER='&field4={}'.format(value)
    NEW_URL = URl+KEY+HEADER
    print(NEW_URL)
    data=urllib.request.urlopen(NEW_URL)
    print(data)

def main():

    timestamp = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    log_name = (Path.cwd() / "logs" / f"log_{timestamp}.txt").resolve()

    if len(sys.argv) > 1:
        image_name = Path(sys.argv[1]).resolve()
    else:
        image_name = (Path.cwd() / "fotos_autos" / f"image_{timestamp}.jpg").resolve()
        capture_image(image_name)

    print(image_name)

    #show_image(image_name)
    
    print(f"directorio de darknet: {DARKNET_PATH}")

    car_count = darknet_process(image_name, log_name)

    print(f"Vehículos en la foto: {car_count}")

    #exit()

    thingspeak_post(car_count)


try:
    main()

except RuntimeError:
    thingspeak_post(-1)
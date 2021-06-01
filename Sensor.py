import bme280
from datetime import datetime
from datetime import date
import time
import json
import paho.mqtt.client as mqtt
from time import sleep
import RPi.GPIO as GPIO

iot_hub="localhost";
port=1883;
#Thingsboard access token
username="ZCRkH2vwKbRkbszfBel3";
topic="v1/devices/me/telemetry";

client=mqtt.Client();
client.username_pw_set(username);
client.connect(iot_hub,port);
time.sleep(1)
print("Connection success");
time.sleep(5.0)

'''
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
'''
sensor_data=dict()
while True:
    try:
        temperature,pressure,humidity = bme280.readBME280All() 
        
        today = date.today()
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        
        print(dt_string)
        print ("Temperature : {:.1f} ".format(temperature))
        print ("Humidity: {:.0f}".format(humidity))
        print()
                
        sensor_data["temperature"] = "{:.1f}".format(temperature)
        sensor_data["humidity"] = "{:.0f}".format(humidity)
        
        sensor_data["min_temperature"] = "37.25"
        sensor_data["max_temperature"] = "38.3"
        sensor_data["min_humidity"] = "60"
        sensor_data["max_humidity"] = "80"
        
        data=json.dumps(sensor_data)
        client.publish(topic,data,0)
         
        data = ("{0} , {1} , {2} \n".format(temperature, humidity, now))
        
        f=open("data.txt","a")
        f.write(data)
        f.close()
 
    except RuntimeError as error:
        print(error.args[0])
        time.sleep(5.0)
        continue
    except Exception as error:
        time.sleep(5.0)
        continue
    time.sleep(5.0)

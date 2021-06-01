import bme280
from datetime import datetime
from datetime import date
import time
import json
import paho.mqtt.client as mqtt
from time import sleep
import RPi.GPIO as GPIO

#Fan
PIN1=17
#Heating
PIN2=27
#Lighting
PIN3=22
#FAN1--4-PWM--5-RPM
PIN4=19
PIN5=24
#FAN1--4-PWM--5-RPM
PIN6=13
PIN7=23

SPEED=0.1
PWM_FREQ=25


iot_hub="localhost";
port=1883;
#Thingsboard access token
username="ZCRkH2vwKbRkbszfBel3";
topic="v1/devices/me/telemetry";

client=mqtt.Client();
client.username_pw_set(username);
client.connect(iot_hub,port);
time.sleep(1);
print("Connection success");
time.sleep(5.0);

GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM);
GPIO.setup(PIN1,GPIO.OUT);
GPIO.setup(PIN2,GPIO.OUT);
GPIO.setup(PIN3,GPIO.OUT);
GPIO.setup(PIN4,GPIO.OUT);
#GPIO.setup(PIN5,GPIO.OUT);
GPIO.setup(PIN6,GPIO.OUT);
#GPIO.setup(PIN7,GPIO.OUT);

GPIO.output(PIN1,GPIO.HIGH);
GPIO.output(PIN4,GPIO.HIGH);
GPIO.output(PIN6,GPIO.HIGH);
fan1=GPIO.PWM(PIN4,PWM_FREQ);
fan2=GPIO.PWM(PIN6,PWM_FREQ);
fan1.start(SPEED);
fan2.start(SPEED);

sensor_data=dict();
while True:
    #try:
    temperature,pressure,humidity = bme280.readBME280All();
    
    today = date.today();
    now = datetime.now();
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S");
    
    print(dt_string);
    print ("Temperature : {:.1f} ".format(temperature));
    print ("Humidity: {:.0f}".format(humidity));
    print();
    
    if(temperature>35):
        GPIO.output(PIN2,GPIO.HIGH)
        print("Svietime")
        GPIO.output(PIN3,GPIO.LOW)
    else:
        GPIO.output(PIN2,GPIO.LOW)
        print("Kurime")
        GPIO.output(PIN3,GPIO.HIGH)
        
        
    print("Temp: {:.1f} C    Humidity: {}% ".format(temperature, humidity))
            
    sensor_data["temperature"] = "{:.1f}".format(temperature);
    sensor_data["humidity"] = "{:.0f}".format(humidity);
    
    sensor_data["min_temperature"] = "37.25";
    sensor_data["max_temperature"] = "38.3";
    sensor_data["min_humidity"] = "60";
    sensor_data["max_humidity"] = "80";
    
    data=json.dumps(sensor_data);
    client.publish(topic,data,0);
     
    data = ("{0} , {1} , {2} \n".format(temperature, humidity, now));
    
    f=open("data.txt","a");
    f.write(data);
    f.close();
    '''
    except RuntimeError as error:
        print(error.args[0]);
        time.sleep(5.0);
        continue
    except Exception as error:
        time.sleep(5.0);
        continue'''
    time.sleep(5.0);
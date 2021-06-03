import bme280
from datetime import datetime
from datetime import date
import time
import json
from time import sleep
import RPi.GPIO as GPIO
import logging
from tb_device_mqtt import TBDeviceMqttClient, TBPublishInfo

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

value=False;

def on_server_side_rpc_request(client, request_id, request_body):
    #print(request_id, request_body)
    if request_body["method"] == "setValue":
        client.send_rpc_reply(request_id, value)
        light_state=request_body['params'];
        print(light_state);
        if(str(light_state) == 'True'):
            print('zapnute')
            GPIO.output(PIN3,GPIO.LOW);
        else:
            print('vypnute')
            GPIO.output(PIN3,GPIO.HIGH);

client = TBDeviceMqttClient("localhost", "fYNYPvueVL6WLw69BWEv")
client.set_server_side_rpc_request_handler(on_server_side_rpc_request)
client.connect()
time.sleep(1);

print("Connection success");
time.sleep(2.5);

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
    
    if(temperature>37.8):
        GPIO.output(PIN2,GPIO.HIGH);
        print("Svietime");
        print();
        #GPIO.output(PIN3,GPIO.LOW);
    else:
        print("Kurime");
        print();
        #GPIO.output(PIN3,GPIO.HIGH);
     
    temp = "{:.1f}".format(temperature);
    humi = "{:.0f}".format(humidity);     
    max_temp = 37;
    min_temp = 38;
    min_humi = 60;
    max_humi= 80;
    
    data={"temperature": temp, "humidity": humi,
          "min_temperature" : min_temp, "max_temperature":max_temp,
          "min_humidity" : min_humi, "max_humidity":max_humi}
    client.send_telemetry(data);
    #print(data);
    
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


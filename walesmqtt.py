# publisher

import time
import paho.mqtt.client as mqtt
import circuit # 초음파 센서 입력 모듈 임포트
import temhum # 온습도 센서 측정 모듈 임포트
import light # 조도 센서 측정 모듈 임포트

def on_connect(client, userdata, flag, rc):
        client.subscribe("led", qos = 0)

def on_message(client, userdata, msg) :
        msg = int(msg.payload);
        print(msg)
        circuit.controlLED(msg) # msg는 0 또는 1의 정수

broker_ip = "localhost" # 현재 이 컴퓨터를 브로커로 설정

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker_ip, 1883)
client.loop_start()

while(True):
        distance = circuit.measureDistance() #초음파 이용한거리
        temperature = temhum.getTemperature() #온도
        humidity = temhum.getHumidity() #습도
        brightness = light.getlight() #조도

        client.publish("ultrasonic", distance, qos=0)
        client.publish("celsius", temperature, qos=0)
        client.publish("weather", humidity, qos=0)
        client.publish("bright", brightness, qos=0)
        time.sleep(1)


client.loop_stop()
client.disconnect()
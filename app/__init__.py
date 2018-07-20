# -*- coding: utf-8 -*-

import json
import requests
import paho.mqtt.client as mqtt
from config import config


class App:
    def __init__(self, config_name='default'):
        self.__mqtt = mqtt.Client()
        self.__config = config[config_name]

    def on_message(self, userdata, msg):
        parts = msg.topic.split('/')
        if len(parts) == 4 and parts[3] == 'from_device':
            data = json.loads(msg.payload.decode('utf-8'))

            if parts[1] == 'sensor':
                self.handle_sensor(parts[2], data)

    def handle_sensor(self, sensor, data):
        if data['kind'] == 'card_inserted':
            self.__mqtt.publish('epsi_iot/call/from_service', 'new card inserted from sensor')
            card_id = data['args']['id'].replace(' ', '')
            response = requests.get(self.__config.SERVICE_HOST + card_id)

            if response.status_code == 200:
                card = response.json()
                payload = {
                    'kind': 'call',
                    'recipient': card['idSkype'],
                    'service': 'skype'
                }
                self.__mqtt.publish('epsi_iot/username/from_clients', json.dumps(payload))
                print('data sent')

    def on_connect(self, userdata, flags, rc):
        if rc == 4:
            raise Exception('Invalid username or password')

        if rc != 0:
            raise Exception('Unable to connect to mqtt service')

        print('MQTT connected')

        self.__mqtt.subscribe('epsi_iot/sensor/+/from_device')

    def start(self):
        def on_mqtt_message(client, userdata, msg):
            nonlocal self
            self.on_message(userdata, msg)

        def on_mqtt_connect(client, userdata, flags, rc):
            nonlocal self
            self.on_connect(userdata, flags, rc)

        self.__mqtt.username_pw_set(self.__config.MQTT_USERNAME, self.__config.MQTT_PASSWORD)
        self.__mqtt.on_message = on_mqtt_message
        self.__mqtt.on_connect = on_mqtt_connect
        self.__mqtt.connect(self.__config.MQTT_SERVER, int(self.__config.MQTT_PORT),
                            int(self.__config.MQTT_KEEP_ALIVE))

    def stop(self):
        self.__mqtt.disconnect()

    def loop(self):
        self.__mqtt.loop()

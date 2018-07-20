# -*- coding: utf-8 -*-

import os


class Config:
    """
    Base configuration
    """

    MQTT_SERVER = os.environ.get('MQTT_SERVER', 'mqtt')
    MQTT_PORT = int(os.environ.get('MQTT_PORT', '1883'))
    MQTT_USERNAME = os.environ.get('MQTT_USERNAME', 'call_service')
    MQTT_PASSWORD = os.environ.get('MQTT_PASSWORD', 'call_service')
    MQTT_KEEP_ALIVE = int(os.environ.get('MQTT_KEEP_ALIVE', '60'))
    SERVICE_HOST = os.environ.get('SERVICE_HOST', 'http://iotepsi.azurewebsites.net/api/badges/')


class DevelopmentConfig(Config):
    """
    Development configuration
    """


class ProductionConfig(Config):
    """
    Production configuration
    """


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

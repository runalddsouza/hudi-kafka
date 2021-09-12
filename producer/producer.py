import json
import ssl
import time
from pathlib import Path

import avro
import pandas as pd
import websocket
from confluent_kafka.avro import AvroProducer

import logger
import schema
from parse_args import parse_args


class CryptoCurrencyProducer:

    def __init__(self, config, producer, topic_name, log):
        self.__config = config
        self.__socket = self.__config["websocket"]["host"]
        self.__subscription = json.dumps(self.__config["websocket"]["subscription"])
        self.__retry_interval_secs = self.__config["websocket"]["retry"]["interval"]
        self.__retry_limit = self.__config["websocket"]["retry"]["limit"]
        self.__attempt = 1
        self.__log = log
        self.producer = producer
        self.topic_name = topic_name

    def __on_message(self, ws, message):
        data = json.loads(message)
        if data['type'] != 'subscriptions':
            df = pd.DataFrame([data], columns=schema.input_columns.keys()).astype(schema.input_columns)
            self.__write_to_kafka(df)

    def __on_error(self, ws, e):
        self.__log.error("Connection failure ; exception: %s ; message: %s", type(e).__name__, e)
        self.__log.info("Will retry after %d secs", self.__retry_interval_secs)
        time.sleep(self.__retry_interval_secs)
        self.__log.info("Reconnecting...attempt %d", self.__attempt)
        self.__attempt += 1

    def __on_close(self, ws, close_status_code, close_msg):
        self.__log.info("Connection closed ; status code: %s ; message: %s", str(close_status_code), str(close_msg))

    def __on_open(self, ws):
        self.__log.info("Connection successful")
        self.__attempt = 1
        ws.send(self.__subscription)

    def __connect_websocket(self):
        self.__log.info("Connecting %s", self.__socket)
        websocket.setdefaulttimeout(5)
        ws = websocket.WebSocketApp(self.__socket, on_open=self.__on_open, on_message=self.__on_message,
                                    on_error=self.__on_error,
                                    on_close=self.__on_close)
        ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})

    def __write_to_kafka(self, df):
        key = df.iloc[0]["trade_id"]
        json_value = json.loads(df.iloc[0].to_json())
        self.producer.produce(topic=self.topic_name, key=key, value=json_value, on_delivery=self.acked)
        self.producer.poll(0)
        self.producer.flush()

    def acked(self, err, msg):
        """Delivery report handler called on successful or failed delivery of message """
        if err is not None:
            self.__log.error("Failed to deliver message: {}".format(err))
        else:
            self.__log.info("Produced record to topic {} partition [{}] @ offset {}"
                            .format(msg.topic(), msg.partition(), msg.offset()))

    def start(self):
        # limit retry based on config
        while self.__attempt <= self.__retry_limit:
            try:
                self.__connect_websocket()
            except Exception as e:
                # quit on encountering any exceptions
                self.__log.error("Unknown failure ; Exception: " + str(type(e).__name__) + "  ; message: " + str(e))
                break


if __name__ == '__main__':
    # configuration
    with open(Path(__file__).parent / "resources/config.json") as config_file:
        configuration = json.load(config_file)

    # get cli params
    args = parse_args()
    logger = logger.AppLogger(args.log_file).get_logger()

    # kafka
    producer_conf = {'bootstrap.servers': args.bootstrap_servers, 'schema.registry.url': args.schema_registry,
                     'security.protocol': 'PLAINTEXT'}
    topic = args.topic
    key_schema = avro.schema.parse('{"type": "string"}')
    value_schema = avro.schema.parse(json.dumps(schema.avro_dict))
    avro_producer = AvroProducer(producer_conf, default_value_schema=value_schema, default_key_schema=key_schema)

    app = CryptoCurrencyProducer(configuration, avro_producer, topic, logger)
    app.start()

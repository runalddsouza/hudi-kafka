from argparse import ArgumentParser


def parse_args():
    arg_parser = ArgumentParser()
    arg_parser.add_argument("--topic", required=True, help="Kafka topic")
    arg_parser.add_argument("--bootstrap-servers", required=True, help="Bootstrap server")
    arg_parser.add_argument("--schema-registry", required=True, help="Schema Registry url")
    arg_parser.add_argument("--log-file", required=True, help="Application log file path")
    return arg_parser.parse_args()

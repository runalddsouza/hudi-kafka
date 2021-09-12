# hudi-kafka

This project has two components:
- Kafka AvroProducer ->  produces cryptocurrency data.
- [Hudi DeltaStreamer](https://hudi.apache.org/docs/writing_data/#deltastreamer) -> ingests the data from Kafka and writes to hudi tables.

### Producer
- Install packages: `pip install -r requirements.txt`
- Start Producer: `python producer/producer.py --topic <topic-name> --bootstrap-servers <broker-server> --schema-registry <schema-registry-url> --log-file <log-file-path>`

### Consumer
Refer [Documentation](https://hudi.apache.org/docs/writing_data/#deltastreamer) for configuration.
- Install [Spark](https://spark.apache.org/downloads.html)
- Update Hudi config and kafka topic settings in `kafka-source.properties`
- Download [Hudi utilities bundle](https://repo1.maven.org/maven2/org/apache/hudi/) and set path in `hudi-delta-streamer.sh`
- Start: `delta-streamer/hudi-delta-streamer.sh <spark-master> <broker-server> <schema-registry-url> delta-streamer/kafka-source.properties <output-path>`

### Docker Setup
- Kafka
- Schema Registry
- Zookeeper
- Producer 
- Consumer (Hudi DeltaStreamer)

### Steps:
- Clone repository
- Run: `cd docker`
- Start services: `docker-compose up`


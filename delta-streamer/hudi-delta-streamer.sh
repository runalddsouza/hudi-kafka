#!/usr/bin/env bash

SPARK_MASTER=$1
PROPERTIES_FILE=$2
OUTPUT_PATH=$3
JAR_PATH="/usr/bin/hudi-utilities-bundle"
JAR_FILE="$JAR_PATH/hudi-utilities-bundle_2.12-0.8.0.jar"
CHECKPOINT_PATH="/tmp/checkpoint"

spark-submit --jars "$JAR_PATH" \
--master "$SPARK_MASTER" \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer \
"$JAR_FILE" \
  --table-type COPY_ON_WRITE \
  --source-ordering-field time \
  --props "$PROPERTIES_FILE" \
  --source-class org.apache.hudi.utilities.sources.AvroKafkaSource \
  --target-base-path "$OUTPUT_PATH" \
  --target-table Cryptocurrency \
  --checkpoint "$CHECKPOINT_PATH" \
  --schemaprovider-class org.apache.hudi.utilities.schema.SchemaRegistryProvider \
  --hoodie-conf bootstrap.servers=broker:29092 \
  --hoodie-conf schema.registry.url=http://schema-registry:8081 \
  --hoodie-conf hoodie.deltastreamer.schemaprovider.registry.url=http://schema-registry:8081/subjects/Cryptocurrency-value/versions/latest

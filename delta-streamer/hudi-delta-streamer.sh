#!/usr/bin/env bash

SPARK_MASTER=$1
BROKER_SERVER=$2
SCHEMA_REGISTRY_URL=$3
PROPERTIES_FILE=$4
OUTPUT_PATH=$5
JAR_PATH="/usr/lib/hudi/hudi-utilities-bundle"
JAR_FILE=$(find $JAR_PATH -name "hudi-utilities-bundle*.jar" | grep "hudi-utilities-bundle")

spark-submit --jars "$JAR_PATH" \
--master "$SPARK_MASTER" \
--conf spark.serializer=org.apache.spark.serializer.KryoSerializer \
--class org.apache.hudi.utilities.deltastreamer.HoodieDeltaStreamer \
"$JAR_FILE" \
  --table-type COPY_ON_WRITE \
  --source-ordering-field "time" \
  --props "$PROPERTIES_FILE" \
  --source-class org.apache.hudi.utilities.sources.AvroKafkaSource \
  --target-base-path "$OUTPUT_PATH" \
  --target-table Cryptocurrency \
  --schemaprovider-class org.apache.hudi.utilities.schema.SchemaRegistryProvider \
  --hoodie-conf bootstrap.servers="$BROKER_SERVER" \
  --hoodie-conf schema.registry.url="$SCHEMA_REGISTRY_URL" \
  --hoodie-conf hoodie.deltastreamer.schemaprovider.registry.url="$SCHEMA_REGISTRY_URL"/subjects/Cryptocurrency-value/versions/latest \
  --continuous
# --checkpoint 0

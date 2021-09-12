FROM python:3.9-slim-buster

# OpenJdk for spark-submit
RUN mkdir -p /usr/share/man/man1 /usr/share/man/man2
RUN apt-get update && \
    apt-get install -y --no-install-recommends openjdk-11-jdk;

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64/
RUN export JAVA_HOME

# PySpark
RUN pip install pyspark==3.0.0

# Download Hudi bundle utilities
RUN mkdir -p /usr/lib/hudi/hudi-utilities-bundle
RUN apt-get update && \
    apt-get install -y curl && \
    curl 'https://search.maven.org/remotecontent?filepath=org/apache/hudi/hudi-utilities-bundle_2.12/0.8.0/hudi-utilities-bundle_2.12-0.8.0.jar'\
 -o /usr/lib/hudi/hudi-utilities-bundle/hudi-utilities-bundle_2.12-0.8.0.jar

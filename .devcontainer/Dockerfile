# Use the official Apache Kafka image as the base
FROM apache/kafka:3.8.0

# Install Python and necessary libraries
RUN apt-get update && \
    apt-get install -y python3 python3-pip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Python libraries
RUN pip3 install --no-cache-dir \
    tensorflow \
    pandas \
    scikit-learn \
    fastf1


EXPOSE 9092
# Use a base image with Spark installed
FROM jupyter/pyspark-notebook:latest

ENV DEBIAN_FRONTEND noninteractive
ENV LANGUAGE en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8
ENV LC_CTYPE en_US.UTF-8
ENV LC_MESSAGES en_US.UTF-8

USER root
RUN apt-get update && \
    apt-get upgrade -y

# Install the following just for debugging purposes
RUN apt-get install -y net-tools

# Switch back to original non root user
USER $NB_USER

# Set the working directory in the container
WORKDIR /home/jovyan

# Copy the requirements file into the container at the WORKDIR location
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application's code
COPY app/ .

# Expose the ports (Jupyter + Spark UI)
EXPOSE 8888
EXPOSE 4040

# Set the environment variable for PySpark
ENV PYSPARK_APP_NAME="LBC"
# ENV PYSPARK_SUBMIT_ARGS="--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0"

# Run your PySpark application
# CMD ["spark-submit", "--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0", "./app/your-app.py"]

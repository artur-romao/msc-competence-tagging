# Use an official base image of Java runtime
FROM openjdk:8-jdk-alpine

# Install necessary packages
RUN apk add --no-cache bash

# Set the working directory in the container
WORKDIR /app

# Copy your API and its scripts into the container
COPY . /app

# Expose the port the API listens on
EXPOSE 8080

# Command to run the startup script
CMD ["sh", "-c", "/app/tomcat-esp-api-v03_94/bin/catalina.sh run"]


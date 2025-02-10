FROM mcr.microsoft.com/devcontainers/python:1-3.10-bookworm
# Install Java
RUN apt-get update && apt-get install -y openjdk-11-jdk

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV PATH=$JAVA_HOME/bin:$PATH

# Verify installations
RUN java -version && python --version

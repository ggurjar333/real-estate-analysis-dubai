# Stage 1: Base Python image with PySpark
FROM python:3.10-slim AS pyspark-base

# Install PySpark and dependencies
RUN pip install pyspark

# Stage 2: Base Java image
FROM openjdk:11-jre-slim AS java-base

# Stage 3: Final image combining both environments
FROM pyspark-base

# Copy Java from java-base stage
COPY --from=java-base /usr/local/openjdk-11 /usr/local/openjdk-11

# Set JAVA_HOME environment variable
ENV JAVA_HOME=/usr/local/openjdk-11
ENV PATH=$JAVA_HOME/bin:$PATH

# Verify installations
RUN java -version && python --version

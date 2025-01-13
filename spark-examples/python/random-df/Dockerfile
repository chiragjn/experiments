FROM apache/spark:3.5.3-python3
USER root
ENV VENV_PATH=$SPARK_HOME/.venv
RUN set -ex; \
    apt-get update; \
    apt-get install python3.8-venv tar -y; \
    rm -rf /var/lib/apt/lists/*; \ 
    python3 -m venv $VENV_PATH; \
    $VENV_PATH/bin/pip install --upgrade pip setuptools wheel;

RUN chown -R spark $VENV_PATH \
    && mkdir -p /home/spark \
    && chown -R spark /home/spark

USER spark

ENV PATH="$PATH:$SPARK_HOME/bin:$VENV_PATH/bin/"
ENV PYSPARK_PYTHON=$VENV_PATH/bin/python
ENV PYTHONPATH="$SPARK_HOME/python:$SPARK_HOME/python/lib/py4j-0.10.9.7-src.zip"

WORKDIR /home/spark
COPY main.py .
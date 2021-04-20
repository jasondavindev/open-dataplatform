ARG SPARK_IMAGE

FROM ${SPARK_IMAGE}

ARG AIRFLOW_VERSION=2.0.1
ARG AIRFLOW_DEPS=""
ARG EXECUTOR="LocalExecutor"

ENV AIRFLOW_HOME=/opt/airflow
ENV AIRFLOW_VERSION=${AIRFLOW_VERSION}
ENV EXECUTOR=${EXECUTOR}

USER root

RUN set -ex \
    && buildDeps=' \
        freetds-dev \
        libkrb5-dev \
        libsasl2-dev \
        libssl-dev \
        libffi-dev \
        libpq-dev \
        git \
    ' \
    apt update -yqq; \
    apt install -yqq \
        $buildDeps \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        unzip \
        netcat; \
    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow; \
    ln -Ls $(which pip3) /usr/bin/pip; \
    pip install apache-airflow[crypto,celery,postgres,jdbc,mysql${AIRFLOW_DEPS:+,}${AIRFLOW_DEPS}]==${AIRFLOW_VERSION}; \
    apt-get clean; \
    apt-get autoremove -yqq --purge; \
    rm -rf \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY requirements.txt ${AIRFLOW_HOME}

RUN pip install -r ${AIRFLOW_HOME}/requirements.txt; \
    mkdir ${AIRFLOW_HOME}/plugins; \
    mkdir ${AIRFLOW_HOME}/logs; \
    mkdir ${AIRFLOW_HOME}/dags

COPY entrypoint.sh /entrypoint.sh

COPY config/airflow.cfg ${AIRFLOW_HOME}

COPY bootstrap ${AIRFLOW_HOME}/bootstrap

RUN chown -RL airflow: ${AIRFLOW_HOME}; \
    chmod +x /entrypoint.sh

USER airflow

WORKDIR ${AIRFLOW_HOME}

EXPOSE 8080 5555 8793

ENTRYPOINT [ "/entrypoint.sh" ]

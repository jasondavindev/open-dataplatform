FROM open-dataplatform-spark

ARG AIRFLOW_VERSION="2.1.2"

ENV AIRFLOW_HOME "/opt/airflow"
ENV AIRFLOW_VERSION ${AIRFLOW_VERSION}
ENV EXECUTOR "LocalExecutor"
ENV PYTHON_VERSION "3.7"

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
        python3.7-dev \
    ' \
    apt update -yqq; \
    apt install -yqq \
        ${buildDeps} \
        freetds-bin \
        build-essential \
        default-libmysqlclient-dev \
        apt-utils \
        curl \
        rsync \
        unzip \
        netcat; \
    useradd -ms /bin/bash -d ${AIRFLOW_HOME} airflow; \
    ln -Lsf $(which pip3) /usr/bin/pip

RUN pip install -U pip

RUN pip install \
    psycopg2-binary==2.8.6 \
    apache-airflow[crypto,postgres,jdbc,mysql]==${AIRFLOW_VERSION}

RUN apt-get clean; \
    apt-get autoremove -yqq --purge; \
    rm -rf \
        /tmp/* \
        /var/tmp/* \
        /usr/share/man \
        /usr/share/doc \
        /usr/share/doc-base

COPY requirements.txt ${AIRFLOW_HOME}

RUN pip install -r ${AIRFLOW_HOME}/requirements.txt -c https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt; \
    mkdir ${AIRFLOW_HOME}/plugins; \
    mkdir ${AIRFLOW_HOME}/logs; \
    mkdir ${AIRFLOW_HOME}/dags

COPY entrypoint.sh /entrypoint.sh

COPY config/airflow.cfg ${AIRFLOW_HOME}

COPY bootstrap ${AIRFLOW_HOME}/bootstrap

COPY plugins ${AIRFLOW_HOME}/plugins

RUN chown -RL airflow: ${AIRFLOW_HOME}; \
    chmod +x /entrypoint.sh

USER airflow

WORKDIR ${AIRFLOW_HOME}

EXPOSE 8080 8793

ENTRYPOINT [ "/entrypoint.sh" ]

FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
ENV HADOOP_HOME=/opt/hadoop
ENV SPARK_HOME=/opt/spark
ENV HADOOP_CONF_DIR=$HADOOP_HOME/etc/hadoop
ENV PATH=$PATH:$JAVA_HOME/bin:$HADOOP_HOME/bin:$HADOOP_HOME/sbin:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV HDFS_NAMENODE_USER=root
ENV HDFS_DATANODE_USER=root
ENV HDFS_SECONDARYNAMENODE_USER=root
ENV YARN_RESOURCEMANAGER_USER=root
ENV YARN_NODEMANAGER_USER=root

RUN apt-get update && apt-get install -y \
    openjdk-11-jdk \
    openssh-server \
    openssh-client \
    python3 \
    python3-pip \
    wget \
    curl \
    net-tools \
    procps \
    && rm -rf /var/lib/apt/lists/*

RUN ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa && \
    cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
    chmod 0600 ~/.ssh/authorized_keys && \
    echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config

RUN pip3 install --no-cache-dir pyspark==3.5.5

COPY hadoop-3.4.1.tar.gz /tmp/
RUN tar -xzf /tmp/hadoop-3.4.1.tar.gz -C /opt/ && \
    mv /opt/hadoop-3.4.1 /opt/hadoop && \
    rm /tmp/hadoop-3.4.1.tar.gz

COPY spark-3.5.5-bin-hadoop3.tgz /tmp/
RUN tar -xzf /tmp/spark-3.5.5-bin-hadoop3.tgz -C /opt/ && \
    mv /opt/spark-3.5.5-bin-hadoop3 /opt/spark && \
    rm /tmp/spark-3.5.5-bin-hadoop3.tgz

COPY config/hadoop/core-site.xml    $HADOOP_HOME/etc/hadoop/
COPY config/hadoop/hdfs-site.xml    $HADOOP_HOME/etc/hadoop/
COPY config/hadoop/mapred-site.xml  $HADOOP_HOME/etc/hadoop/
COPY config/hadoop/yarn-site.xml    $HADOOP_HOME/etc/hadoop/

RUN echo "export JAVA_HOME=$JAVA_HOME" >> $HADOOP_HOME/etc/hadoop/hadoop-env.sh

COPY config/spark/spark-defaults.conf $SPARK_HOME/conf/

COPY scripts/bootstrap.sh /bootstrap.sh
RUN chmod +x /bootstrap.sh

RUN $HADOOP_HOME/bin/hdfs namenode -format -force

EXPOSE 9870 8088 4040 9000 8032

CMD ["/bootstrap.sh"]

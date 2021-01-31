FROM cluster-base

# -- Layer: JupyterLab

ARG spark_version=3.0.1
ARG jupyterlab_version=2.2.6

RUN apt-get update -y && \
    apt-get install -y python3-pip && \
    pip3 install pyspark==${​​spark_version}​​ jupyterlab==${​​jupyterlab_version}​​ && \
    pip3 install wget && \
    pip3 install -U scikit-learn && \
    apt-get install -y python3-pandas && \
    apt-get -y install gcc && \
    pip3 install numpy && \
    pip3 install -U matplotlib && \
    pip3 install seaborn && \
    pip3 install fbprophet

RUN python -m pip install pymongo
RUN python -m pip install dnspython



EXPOSE 8888
WORKDIR ${SHARED_WORKSPACE}
CMD jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=

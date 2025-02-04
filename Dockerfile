FROM centos:7

USER root

RUN sed -i 's|^mirrorlist=|#mirrorlist=|g' /etc/yum.repos.d/CentOS-*.repo && \
    sed -i 's|^#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*.repo

RUN yum -y update && yum install -y epel-release && \
    yum install -y libX11 libXext libXrender libXt libGL libICE libSM \
    xorg-x11-server-Xorg \
    xorg-x11-xauth \
    xorg-x11-apps \
    xorg-x11-server-Xvfb \
    qt5-qtbase \
    libX11-xcb xcb-util xcb-util-* libxcb \
    xterm \
    make \
    cmake \
    gcc \
    unzip \
    vim \
    gedit \
    wget \
    csh \
    gcc-gfortran \
    tar \
    gdb \
    evince \
    ghostscript \
    git \
    eog && \
    yum clean all 

WORKDIR /opt
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    bash Miniconda3-latest-Linux-x86_64.sh -b -p /opt/miniconda3 && \
    rm Miniconda3-latest-Linux-x86_64.sh

ENV PATH /opt/miniconda3/bin:$PATH
RUN conda init bash

RUN conda create -n practice -c conda-forge obspy spyder pandas matplotlib basemap numpy scipy scikit-learn kafka-python fastapi uvicorn tqdm jupyterlab "h5py==3.10.0" "tensorflow==2.15.0" pyrocko::pyrocko fsspec pyqt vtk wandb\
    -y && \
    conda run -n practice conda update --all

WORKDIR /home
RUN git clone https://github.com/AI4EPS/EQNet.git
RUN pip install git+https://github.com/wayneweiqiang/GaMMA.git
RUN git clone https://github.com/TaeShinKim/seis_practice.git && rm -rf seis_practice/cc && mv seis_practice/* . && rm -rf seis_practice 
RUN conda run -n practice pip install torch torchvision

WORKDIR /opt
RUN git clone https://github.com/TaeShinKim/SAC102.0.git && \
    unzip SAC102.0/sac.zip -d SAC102.0 && chmod +x ./SAC102.0/bin/sac && \
    git clone https://github.com/fwaldhauser/HypoDD.git

WORKDIR /opt/HypoDD/src
RUN make clean && make

WORKDIR /home

# 기본 환경 설정
RUN echo "conda activate practice" >> ~/.bashrc && \
    echo "alias vi='vim'" >> ~/.bashrc && \
    echo "alias rm='rm -f'" >> ~/.bashrc && \
    echo 'export PATH=$PATH:/opt/SAC102.0/bin' >> ~/.bashrc && \
    echo 'export SACAUX=/opt/SAC102.0/aux%00' >> ~/.bashrc && \
    echo 'HYPO=/opt/HypoDD/src' >> ~/.bashrc && \
    echo 'export PATH="$HYPO/hista2ddsta:$HYPO/hypoDD:$HYPO/ncsn2pha:$HYPO/ph2dt:$PATH"' >> ~/.bashrc && \
    bash -c "source ~/.bashrc"

ENV PATH "/root/.local/bin:${PATH}"

CMD ["/bin/bash"]

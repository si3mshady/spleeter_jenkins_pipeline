oFROM ubuntu:18.04
# FROM continuumio/anaconda3

WORKDIR /home 

COPY requirements.txt .
RUN apt update -y 
RUN apt install wget -y ß
RUN apt install python3-pip -y 
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
# https://askubuntu.com/questions/1254371/can-anyone-explain-what-this-command-actually-do-eval-users-jsmith-anaconda
ENV CONDA_PATH=$HOME/anaconda3
RUN bash Miniconda3-latest-Linux-x86_64.sh -b -p $CONDA_PATH
#source new environment variables ino
RUN eval "$($CONDA_PATH/bin/conda shell.bash hook)" &&  \
    conda install -y -c conda-forge ffmpeg libsndfile  ruamel_yaml && \
    pip install -r requirements.txt  && \
    pip install spleeter  &&  \
    spleeter --version

ENTRYPOINT [ "spleeter" ]


# https://pypi.org/project/spleeter/
# RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh



#https://askubuntu.com/questions/1254371/can-anyone-explain-what-this-command-actually-do-eval-users-jsmith-anaconda
# https://github.com/deezer/spleeter/wiki/1.-Installation
#https://stackoverflow.com/questions/41373834/conda-importerror-no-module-named-ruamel-yaml-comments

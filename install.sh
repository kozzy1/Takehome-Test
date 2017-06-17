#!/bin/bash 
# Caffe2 is confirmed for Ubuntu 14.04 and 16.04 only
TMPFILE="/tmp/tmp_$RANDOM"
lsb_release -a >> $TMPFILE
if ! (( grep -q Ubuntu < $TMPFILE ) && (( grep -q 16.04 < $TMPFILE ) || (grep -q 14.04 < $TMPFILE )))
then 
echo "Caffe2 is confirmed for Ubuntu 14.04 and 16.04 only."
exit
fi

# Dependencies Installation
echo "Install dependencies..." 
sudo apt-get update 
sudo apt-get install -y --no-install-recommends \
      build-essential \
      cmake \
      git \
      libgoogle-glog-dev \
      libprotobuf-dev \
      protobuf-compiler \
      python-dev \
      python-pip \
      python-tk                  
sudo pip install numpy protobuf future hypothesis 
sudo pip install scikit-image scipy 
echo "Dependencies Installation Success" 

# CuDNN Installation
#
# If CUDA is installed, GPU mode for Caffe2 is automatically enabled
# Thus CuDNN 5.1 is required
# For a higher version of CuDNN, registration and mannual downloading is required
# https://developer.nvidia.com/cudnn
if [ -f "/usr/local/cuda/version.txt" ] && [ ! -f "/usr/local/cuda/include/cudnn.h" ]
then 
echo "Find Cuda without CuDNN, install CuDNN..." 
CUDNN_URL="http://developer.download.nvidia.com/compute/redist/cudnn/v5.1/cudnn-8.0-linux-x64-v5.1.tgz"
wget ${CUDNN_URL}
sudo tar -xzf cudnn-8.0-linux-x64-v5.1.tgz -C /usr/local
rm cudnn-8.0-linux-x64-v5.1.tgz && sudo ldconfig
echo "CuDNN Installation Success" 
fi

# Caffe2 Installation 
if [ ! -d "caffe2" ] 
then 
git clone --recursive https://github.com/caffe2/caffe2.git
cd caffe2
make
cd build 
sudo make install
python -c 'from caffe2.python import core' 2>/dev/null && echo "Caffe2 InstallationSuccess" || echo "Caffe2 Installation Failure"
cd ..
cd ..
fi


cd caffe2
cd build 
echo "Download SqueezeNet Models from Zoo..."
python -m caffe2.python.models.download --install squeezenet
cd ..
cd ..




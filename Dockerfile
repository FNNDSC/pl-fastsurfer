# Docker file for fastsurfer ChRIS plugin app
#
# Build with
#
#   docker build -t <name> .
#
# For example if building a local version, you could do:
#
#   docker build -t local/pl-fastsurfer .
#
# In the case of a proxy (located at 192.168.13.14:3128), do:
#
#    docker build --build-arg http_proxy=http://192.168.13.14:3128 --build-arg UID=$UID -t local/pl-fastsurfer .
#
# To run an interactive shell inside this container, do:
#
#   docker run -ti --entrypoint /bin/bash local/pl-fastsurfer
#
# To pass an env var HOST_IP to container, do:
#
#   docker run -ti -e HOST_IP=$(ip route | grep -v docker | awk '{if(NF==11) print $9}') --entrypoint /bin/bash local/pl-fastsurfer
#



FROM fnndsc/ubuntu-python3:18.04
MAINTAINER fnndsc "dev@babymri.org"

ENV APPROOT="/usr/src/fastsurfer"
COPY ["fastsurfer", "${APPROOT}"]
COPY ["requirements.txt", "${APPROOT}"]

WORKDIR $APPROOT

# Install custom libraries + freesurfer 6.0 (and necessary dependencies)
RUN apt-get update && apt-get install -y --no-install-recommends \
         build-essential \
         cmake \
         git \
         vim \
         wget \
         ca-certificates \
         bzip2 \
         libx11-6 \
         libjpeg-dev \
         libpng-dev \
         bc \
         tar \
         zip \
         gawk \
         tcsh \
         time \
         libgomp1 \
         libglu1-mesa \
	 libglu1-mesa-dev \
	 perl-modules && \
         apt-get clean && \
         rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
	 wget -qO- https://surfer.nmr.mgh.harvard.edu/pub/dist/freesurfer/6.0.1/freesurfer-Linux-centos6_x86_64-stable-pub-v6.0.1.tar.gz | tar zxv --no-same-owner -C /opt \
    	--exclude='freesurfer/trctrain' \
    	--exclude='freesurfer/subjects/fsaverage_sym' \
    	--exclude='freesurfer/subjects/fsaverage3' \
    	--exclude='freesurfer/subjects/fsaverage4' \
    	--exclude='freesurfer/subjects/fsaverage5' \
    	--exclude='freesurfer/subjects/fsaverage6' \
    	--exclude='freesurfer/subjects/cvs_avg35' \
    	--exclude='freesurfer/subjects/cvs_avg35_inMNI152' \
    	--exclude='freesurfer/subjects/bert' \
    	--exclude='freesurfer/subjects/V1_average' \
    	--exclude='freesurfer/average/mult-comp-cor' \
    	--exclude='freesurfer/lib/cuda' \
    	--exclude='freesurfer/lib/qt' \
        --exclude='freesurfer/matlab' \
        --exclude='freesurfer/diffusion' \
        --exclude='freesurfer/bin/freeview.bin' \
        --exclude='freesurfer/bin/freeview' \
        --exclude='freesurfer/bin/mris_decimate_gui.bin' \
        --exclude='freesurfer/bin/mris_decimate_gui' \
        --exclude='freesurfer/bin/qdec.bin' \ 
        --exclude='freesurfer/bin/qdec' \ 
        --exclude='freesurfer/bin/qdec_glmfit' \
        --exclude='freesurfer/bin/SegmentSubfieldsT1Longitudinal' \
        --exclude='freesurfer/bin/SegmentSubjectT1T2_autoEstimateAlveusML' \   
        --exclude='freesurfer/bin/SegmentSubjectT1_autoEstimateAlveusML' \ 
        --exclude='freesurfer/bin/SegmentSubjectT2_autoEstimateAlveusML' \
        --exclude='freesurfer/bin/fs_spmreg.glnxa64'    

# Install miniconda and needed python packages (for FastSurferCNN)
RUN wget -qO ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh  && \
     chmod +x ~/miniconda.sh && \
     ~/miniconda.sh -b -p /opt/conda && \
     rm ~/miniconda.sh && \
     /opt/conda/bin/conda install -y python=$PYTHON_VERSION numpy pyyaml scipy ipython mkl mkl-include ninja cython typing matplotlib h5py scikit-image pillow=6.1 && \
     /opt/conda/bin/conda install -y pytorch-cpu torchvision-cpu -c pytorch && \
     /opt/conda/bin/conda install -y -c conda-forge scikit-sparse && \
     /opt/conda/bin/conda clean -ya
ENV PATH /opt/conda/bin:$PATH

# Install missing python libs
Run pip install nibabel==2.5.1

# Add FreeSurfer Environment variables (.license file needed, alternatively export FS_LICENSE=path/to/license)
ENV OS=Linux \
    FS_OVERRIDE=0 \
    FIX_VERTEX_AREA= \
    SUBJECTS_DIR=/opt/freesurfer/subjects \
    FSF_OUTPUT_FORMAT=nii.gz \
    MNI_DIR=/opt/freesurfer/mni \
    LOCAL_DIR=/opt/freesurfer/local \
    FREESURFER_HOME=/opt/freesurfer \
    FSFAST_HOME=/opt/freesurfer/fsfast \
    MINC_BIN_DIR=/opt/freesurfer/mni/bin \
    MINC_LIB_DIR=/opt/freesurfer/mni/lib \
    MNI_DATAPATH=/opt/freesurfer/mni/data \
    FMRI_ANALYSIS_DIR=/opt/freesurfer/fsfast \
    PERL5LIB=/opt/freesurfer/mni/lib/perl5/5.8.5 \
    MNI_PERL5LIB=/opt/freesurfer/mni/lib/perl5/5.8.5 \
    PYTHONUNBUFFERED=0 \
    PATH=/opt/freesurfer/bin:/opt/freesurfer/fsfast/bin:/opt/freesurfer/tktools:/opt/freesurfer/mni/bin:$PATH

# Add FastSurfer (copy application code) to docker image
#COPY . /fastsurfer/

RUN git clone https://github.com/Deep-MI/FastSurfer.git

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["fastsurfer.py", "--help"]

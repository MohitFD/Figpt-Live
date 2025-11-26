# VALID RUNPOD PYTORCH BASE IMAGE (CUDA 12.4 + PyTorch 2.4 + Python 3.11)
FROM runpod/pytorch:2.4.0-py3.11-cuda12.4.1-devel-ubuntu22.04

ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    TRANSFORMERS_VERBOSITY=info \
    DEBIAN_FRONTEND=noninteractive

# WORK DIRECTORY
WORKDIR /workspace

# COPY PROJECT
COPY . /workspace/fixgpt-live
WORKDIR /workspace/fixgpt-live

# INSTALL DEPENDENCIES
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# EXPOSE DJANGO PORT
EXPOSE 8000

# START SCRIPT
CMD ["/bin/bash", "runpod_start.sh"]

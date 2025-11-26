# VALID BASE IMAGE (PyTorch 2.3 + CUDA 12.1 + Python 3.10)
FROM runpod/pytorch:2.3.0-cu121

ENV PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True \
    TRANSFORMERS_VERBOSITY=info \
    DEBIAN_FRONTEND=noninteractive

WORKDIR /workspace

# Copy your entire project
COPY . /workspace/fixgpt-main
WORKDIR /workspace/fixgpt-main

# Install dependencies directly (NO NEED FOR VENV INSIDE CONTAINER)
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Django default port
EXPOSE 8000

# Start script
CMD ["/bin/bash", "runpod_start.sh"]

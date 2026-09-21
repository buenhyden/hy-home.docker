ARG JUPYTER_BASE_TAG=2026-07-28

FROM quay.io/jupyter/scipy-notebook:${JUPYTER_BASE_TAG}

COPY --chown=${NB_UID}:${NB_GID} \
  requirements.txt \
  /tmp/requirements.txt

RUN pip install \
  --no-cache-dir \
  -r /tmp/requirements.txt
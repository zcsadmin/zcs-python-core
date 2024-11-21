#
# STAGE 1 - Dev
#
# Dev image used for local development
#
FROM zcscompany/python:3.11-dev AS dev

ARG FIX_UID
ARG FIX_GID
ARG DOCKER_USER=bob
ARG DOCKER_GROUP=bob

USER 0
RUN /fix-perm.sh

# Run as normal user
USER ${DOCKER_USER}


#
# STAGE 2 - Dist
#
# Image used for application distribution
#
FROM zcscompany/python:3.11-dist AS dist

ARG DOCKER_USER=bob
ARG DOCKER_GROUP=bob

# Copy application requirement file
COPY --chown=$DOCKER_USER:$DOCKER_GROUP app/requirements.txt .

# Install app requirements
RUN pip install --user --no-cache-dir --disable-pip-version-check -r requirements.txt

# Copy application code
COPY --chown=$DOCKER_USER:$DOCKER_GROUP app/ .

# Build and install the library
RUN python -m build && \
    pip install --user --no-cache-dir --disable-pip-version-check --editable .

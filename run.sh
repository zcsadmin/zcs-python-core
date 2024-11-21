#!/bin/bash 

# Default values
SHELL=0
DISTIMAGE=0
TESTS=0
VERBOSE=0
DEBUG=0

set -e

#
# Show help
#
show_help() {

    echo "Usage: $0 [-s] [-t] [-i] [-v] [-h]"
    echo "  -s: Run a shell instead of running the application"
    echo "  -t: Run tests"
    echo "  -i: Create and run tests on dist image"
    echo "  -v: Verbose output"
    echo "  -h: Show this help"
}

#
# Start docker environment
#
start_docker_environment() {
    # Build docker containers
    docker compose build --pull --build-arg FIX_UID="$(id -u)" --build-arg FIX_GID="$(id -g)"

    # Start docker environment
    docker compose up -d
}

#
# Stop docker environment
#
stop_docker_environment() {
    docker compose stop
}


while getopts stvih flag
do
    case "${flag}" in
        s) SHELL=1;;
        t) TESTS=1;;
        v) VERBOSE=1;;
        i) DISTIMAGE=1;;
        h) show_help; exit 0;;
    esac
done


if [ $VERBOSE -eq 1 ]; then
    set -x
fi


if [ $DISTIMAGE -eq 1 ]; then
    docker build -f .build/dockerfiles/Dockerfile -t dist .
    docker run --rm dist pytest
    exit 0
fi


if [ $TESTS -eq 1 ]; then

    start_docker_environment

    # Install app requirements
    if [ -f app/requirements.txt ]; then
        docker compose exec app /bin/bash -c "pip install --user --disable-pip-version-check -r requirements.txt"
    fi

    # Run tests
    docker compose exec app /bin/bash -c "python -m build"
    docker compose exec app /bin/bash -c "pip install --user --disable-pip-version-check --editable ."
    docker compose exec app /bin/bash -c "pytest"
    
    stop_docker_environment
    
    exit 0
fi


if [ $SHELL -eq 1 ]; then

    start_docker_environment
    
    # Log into container
    docker compose exec app /bin/bash
    
    stop_docker_environment

    exit 0
fi

echo "ERROR - Please choose an action"
exit 1

#!/bin/bash

function help {
  echo "Usage: $0 [OPTIONS]"
  echo ""
  echo "OPTIONS:"
  echo "  -h, --help              Show this help message and exit"
  echo "  -c, --local-container   Local Docker container name"
  echo ""
  exit 0
}

# Parse command line options
while [[ $# -gt 0 ]]; do
  key="$1"
  case $key in
    -h|--help)
      help
      shift
      ;;
    -r|--container-name)
      CONTAINER_NAME="$2"
      shift
      shift
      ;;
    *)
      echo "Unknown option: $1"
      help
      exit 1
      ;;
  esac
done

# Prompt for variable values if not provided
if [[ -z $CONTAINER_NAME ]]; then
  read -p "Enter Container Name: " CONTAINER_NAME
fi



# check if the container is already running
if [ "$(docker ps -a -f name=$CONTAINER_NAME)" ]; then
    read -p "Are you want to delete the existing Docker container? This action cannot be undone. (y/n) " -n 1 -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy]$ ]]
    then
      echo "Aborting."
      exit 1
    fi

    # stop and remove the container
    docker rm --force $CONTAINER_NAME
fi

# run a new container
docker run --name $CONTAINER_NAME -v $(pwd)/config.yml:/app/config.yml accio

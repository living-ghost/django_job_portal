#!/bin/sh
set -e

# Wait for secrets to be injected (Azure-specific)
sleep ${SECRET_DELAY:-2}

# Start RabbitMQ server
exec docker-entrypoint.sh rabbitmq-server
#!/usr/bin/env bash
# use `chmod +x wait-for-it.sh` to make it executable

set -e

host="$1"
shift
cmd="$@"

until nc -z "$host" 5672; do
  >&2 echo "RabbitMQ is unavailable - sleeping"
  sleep 1
done

>&2 echo "RabbitMQ is up - executing command"
exec $cmd
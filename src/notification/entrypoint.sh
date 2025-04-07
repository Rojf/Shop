#!/bin/sh
echo "Waiting for RabbitMQ to be ready..."

# Waiting for RabbitMQ to respond
until nc -z rabbitmq 5672; do
  echo "RabbitMQ is not ready. Waiting..."
  sleep 2
done

# We are waiting for the queue `QUEUE_RABBITMQ` to appear in RabbitMQ
until [ "$(curl -k -s -u admin:admin http://rabbitmq:15672/api/queues?columns=name | jq -r '.[].name' | grep $QUEUE_RABBITMQ)" ]; do
  echo "Queue 'queue_notifications' not found. Waiting..."
  sleep 2
done

echo "RabbitMQ is ready. Starting Celery..."
exec poetry run celery -A celery_app worker --loglevel=$CELERY_LOGLOVEL

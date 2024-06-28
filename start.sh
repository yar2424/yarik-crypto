# Function to kill all child processes in the process group
cleanup() {
  echo "Cleaning up..."
  # Send TERM signal to the process group
  kill -TERM -- -$$
}


# Trap SIGINT (Ctrl+C) and SIGTERM and call the cleanup function
trap cleanup SIGINT SIGTERM

export ECS_PUBLIC_IP=$(curl -s ${ECS_CONTAINER_METADATA_URI_V4}/task | jq -r '.Containers[0].Networks[0].IPv4Addresses[0]')
echo $ECS_PUBLIC_IP

# command > >(tee /proc/$$/fd/1) 2> >(tee /proc/$$/fd/2 >&2)
PYTHONPATH=. python src/entrypoints/scrape_periodic.py &

PYTHONPATH=. python src/entrypoints/tg_id_reply.py &

PYTHONPATH=. uvicorn src.api.app:app --host 0.0.0.0 &

wait
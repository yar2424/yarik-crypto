# Function to kill all child processes in the process group
cleanup() {
  echo "Cleaning up..."
  # Send TERM signal to the process group
  kill -TERM -- -$$
}

# Trap SIGINT (Ctrl+C) and SIGTERM and call the cleanup function
trap cleanup SIGINT SIGTERM


# command > >(tee /proc/$$/fd/1) 2> >(tee /proc/$$/fd/2 >&2)
PYTHONPATH=. python src/entrypoints/scrape_periodic.py &

PYTHONPATH=. python src/entrypoints/tg_id_reply.py &

PYTHONPATH=. uvicorn src.api.app:app --reload &

wait
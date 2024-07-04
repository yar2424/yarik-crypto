# Function to kill all child processes in the process group
cleanup() {
  echo "Cleaning up..."
  # Send TERM signal to the process group
  kill -TERM -- -$$
}


# Trap SIGINT (Ctrl+C) and SIGTERM and call the cleanup function
trap cleanup SIGINT SIGTERM

export ECS_PUBLIC_IP=$(curl -s http://ifconfig.me)
echo $ECS_PUBLIC_IP

# command > >(tee /proc/$$/fd/1) 2> >(tee /proc/$$/fd/2 >&2)

# PYTHONPATH=. python src/services/one_off_tasks/notify_about_restart.py 

PYTHONPATH=. python src/entrypoints/tg_id_reply.py &

PYTHONPATH=. uvicorn src.api.app:app --host 0.0.0.0 &

PYTHONPATH=. python src/entrypoints/scrape_periodic.py &

wait
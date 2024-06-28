set -ex

pip install -r requirements.txt
playwright install chrome
playwright install-deps
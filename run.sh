sudo bash -lc 'cat > /home/ubuntu/bpndx_tracker/run.sh << "EOF"
#!/usr/bin/env bash
set -euo pipefail
PROJECT_DIR="/home/ubuntu/bpndx_tracker"
cd "$PROJECT_DIR"

# Create venv once; reuse thereafter
if [ ! -d venv ]; then
  python3 -m venv venv
fi
source venv/bin/activate

# Install deps only once (delete .deps_installed to force reinstall)
if [ ! -f .deps_installed ]; then
  python -m pip install --upgrade pip
  python -m pip install webdriver_manager selenium python-dotenv requests boto3
  touch .deps_installed
fi

python bpndx_scrape_and_email.py
EOF
chmod +x /home/ubuntu/bpndx_tracker/run.sh'
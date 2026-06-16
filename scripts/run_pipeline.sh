#!/bin/bash

# Mendapatkan path absolute direktori project
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Pindah ke root project
cd "$PROJECT_DIR" || exit 1

# Membuat folder logs jika belum ada
mkdir -p logs

LOG_FILE="logs/pipeline.log"

# Fungsi logging
log_message() {
    local MESSAGE="$1"
    local TIMESTAMP

    TIMESTAMP=$(date "+%Y-%m-%d %H:%M:%S")

    echo "$TIMESTAMP - $MESSAGE" | tee -a "$LOG_FILE"
}

# pipeline
# Aktifkan virtual environment jika tersedia
if [ -d ".venv" ]; then
    source .venv/bin/activate
elif [ -d "env" ]; then
    source env/bin/activate
fi

# Jalankan ETL Pipeline
python3 main.py

# Simpan exit code
EXIT_CODE=$?

# Evaluasi hasil eksekusi
if [ "$EXIT_CODE" -eq 0 ]; then
    log_message "Pipeline berhasil dijalankan"
else
    log_message "Pipeline berhenti $EXIT_CODE"
    exit "$EXIT_CODE"
fi

exit 0
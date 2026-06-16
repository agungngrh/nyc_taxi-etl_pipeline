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

START_TIME=$(date +%s)

log_message "Pipeline dimulai"

# Jalankan ETL Pipeline
python3 main.py

# Simpan exit code
EXIT_CODE=$?

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))

if [ "$EXIT_CODE" -eq 0 ]; then
    log_message "Pipeline berhasil dijalankan"
    log_message "Durasi eksekusi: ${DURATION} detik"
else
    log_message "Pipeline berhenti dengan exit code $EXIT_CODE"
    log_message "Durasi eksekusi: ${DURATION} detik"
    exit "$EXIT_CODE"
fi

exit 0
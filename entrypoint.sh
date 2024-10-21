#!/bin/bash

set -euo pipefail 

PLUGINS_MOD='app.plugins'
PLUGINS_PATH="${PLUGINS_MOD/./\/}"
# Enable plugins from the app.plugins module here \/
ENABLED_PLUGINS=(
    'initial_admin'
    'populate_db'
    )

for plugin in "${ENABLED_PLUGINS[@]}"; do
    if [ -f "$PLUGINS_PATH/$plugin.py" ]; then
        echo "Executing the $plugin plugin"
        python -m "$PLUGINS_MOD.$plugin"
    else
        echo "$plugin plugin is not found. No aciton taken"
    fi
done

uvicorn app.main:app --host 0.0.0.0 --port 8000

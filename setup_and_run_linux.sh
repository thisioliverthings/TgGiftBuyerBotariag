#!/usr/bin/env bash
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# активируем виртуальное окружение
source venv/bin/activate

pip install -r requirements.txt
python -m app.main

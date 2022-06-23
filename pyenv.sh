#!/usr/bin/env bash

echo ""
echo "Creating virtual environment and installing dependencies:"
echo ""

rm -rf .venv/* && \
  python3.8 -m venv .venv && \
  source .venv/bin/activate && \
  pip3 install pip --upgrade && \
  pip3 install -r requirements.txt

echo ""
echo "Done creating dev-environment."

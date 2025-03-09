#!/usr/bin/env bash

set -e

apt-get update
apt-get install --yes \
  gettext

rm -rf /var/lib/apt/lists/*

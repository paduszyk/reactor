#!/usr/bin/env bash

set -e

apt-get update
apt-get install --yes gettext
apt-get clean

rm -rf /var/lib/apt/lists/*

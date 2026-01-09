#!/usr/bin/env bash

apt-get update && \
apt-get install --yes --no-install-recommends \
  gettext \
&& apt-get clean \
&& rm -rf /var/lib/apt/lists/*

#! /usr/bin/env bash

pg_dump meep > /srv/meep/backups/meep-$(date +%Y-%m-%d).sql

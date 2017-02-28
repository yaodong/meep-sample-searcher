#! /usr/bin/env bash

pg_dump -f ./backups/backup.sql -O -x meep

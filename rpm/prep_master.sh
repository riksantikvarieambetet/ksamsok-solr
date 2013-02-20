#!/bin/bash
# Script to link in the index on the local filesystem.
# Exptected to execute only on the master ksamsokserver
echo "We are on the MASTER!"

ln -s /mnt/lucene-index /var/lucene-index
echo "Done preparing master!"

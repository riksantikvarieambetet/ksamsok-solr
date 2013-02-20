#!/bin/bash
# Script to link in the index on the local filesystem.
# Exptected to execute only on the slave ksamsokserver
echo "We are on the SLAVE!"

echo "About to change owner of /var/lucene-index"
chown tomcat:raagroup -R /var/lucene-index
echo "Done preparing SLAVE!"

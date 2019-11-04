#!/usr/bin/bash

# Anger den installerade versionen av solr vi ska ta bort... Måste uppdateras vid uppgradering av solr.
SOLR_VERSION=7.5.0

echo "About to prepare for previous Solr installation: version solr-$SOLR_VERSION..."

rm -f /etc/init.d/solr
rm -rf /usr/share/solr
rm -rf /usr/share/solr-$SOLR_VERSION

rm -f /usr/share/solr/bin/init.d/solr

rm -f /etc/default/solr.in.sh
rm -f /mnt/lucene-index/data/solr.xml
rm -f /mnt/lucene-index/log4j2.xml
rm -rf /mnt/lucene-index/data/ksamsok/
echo "Done preparing for Solr installation. Exit value(0=success, 1=error). Exitcode was: $? (0=success)"

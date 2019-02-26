/sbin/service solr stop

rm -f /etc/init.d/solr
rm -rf /usr/local/solr
rm -rf /usr/local/solr-7.5.0

rm -f /etc/default/solr.in.sh
rm -f /mnt/lucene-index/data/solr.xml
rm -f /mnt/lucene-index/log4j2.xml
rm -rf /mnt/lucene-index/data/ksamsok/



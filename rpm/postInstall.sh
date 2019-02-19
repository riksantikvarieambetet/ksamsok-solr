#solr har ett installationsskript, som vi kör istället för att göra en "egen" installation av solr
/tmp/solr-7.5.0/install_solr_service.sh /tmp/solr-7.5.0/solr-7.5.0.tgz -i /usr/local -d /mnt/lucene-index


if [ ! -d /mnt/lucene-index/data/ksamsok ]; then
    # installera ksamsok som en core
    su solr -c "/usr/local/solr/bin/solr create_core -c ksamsok -d /tmp/ksamsok-config"
else
    #installera konfigfilerna i ksamsok-conf
    su solr -c "cp -r /tmp/ksamsok-config/* /mnt/lucene-index/data/ksamsok/conf/"
fi






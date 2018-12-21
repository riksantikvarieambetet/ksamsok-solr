#solr har ett installationsskript, som vi kör istället för att göra en "egen" installation av solr
/tmp/solr-7.5.0/install_solr_service.sh /tmp/solr-7.5.0/solr-7.5.0.tgz -i /usr/local

# installera ksamsok som en core
su solr -c "/usr/local/solr/bin/solr create_core -c ksamsok -d /tmp/ksamsok-config"

###### HÄR GÅR INTE ATT LÄGGA TILL NÅGOT MER, EFTERSOM SKRIPTET SKJUTER UT PÅ OVANSTÅENDE RAD OM KSAMSOK-COREN REDAN FINNS ######





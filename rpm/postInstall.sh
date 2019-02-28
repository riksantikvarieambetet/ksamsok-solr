#solr har ett installationsskript, som vi kör istället för att göra en "egen" installation av solr
#-n = do not start, vänta tills vi har installerat vår konf
/tmp/solr-7.5.0/install_solr_service.sh /tmp/solr-7.5.0/solr-7.5.0.tgz -i /usr/local -d /mnt/lucene-index -n


# SAKER SOM MÅSTE GÖRAS INNAN SERVICEN STARTAR

# installera vår egen konf (minnesinställningar hanteras här, t.ex.)
cp /tmp/solr-7.5.0/solr.in.sh /etc/default/solr.in.sh
chown root:solr /etc/default/solr.in.sh

# lägg till solr ulimits till limits.conf om det inte redan står där
grep -qxF 'solr hard nofile 65535' /etc/security/limits.conf || echo 'solr hard nofile 65535' >> /etc/security/limits.conf
grep -qxF 'solr soft nofile 65535' /etc/security/limits.conf || echo 'solr soft nofile 65535' >> /etc/security/limits.conf
grep -qxF 'solr hard nproc 65535' /etc/security/limits.conf || echo 'solr hard nproc 65535' >> /etc/security/limits.conf
grep -qxF 'solr soft nproc 65535' /etc/security/limits.conf || echo 'solr soft nproc 65535' >> /etc/security/limits.conf


# STARTA SERVICEN
service solr start
sleep 5
service solr status


# Servicen måste vara igång innan Ksamsok core skapas
su solr -c "/usr/local/solr/bin/solr create_core -c ksamsok -d /tmp/ksamsok-config"







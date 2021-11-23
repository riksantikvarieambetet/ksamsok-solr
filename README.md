# K-samsök solr

För att hantera installationen av Solrindexet för K-samsök behöver man känna till hur installationen 
är uppsatt, eftersom installationen av olika anledningar är något speciell.

Beroende på vilka förändringar som ska utföras på K-samsök solr kan man behöva göra någon 
av de olika typerna av installation.

* För att installera konfigurationsförändringar i K-samsök solr    
    Används om konfigurationsförändringar ska göras i en befintlig installation. Utförs med bamboo.
    Detta är det vanligaste installationsförfarandet för att t ex installera förändringar i det s.k. managed-schema.
    Se installationsanvisningar under "Uppdatera konfigurationsförändringar för K-samsök solr"
    
* För att installera K-samsök Solr på en ny maskin eller uppgradera till ny solr-version     
    Om K-samsök solr ska installeras på en ny tom maskin eller om man vill uppgradera 
    versionen av Solr behöver man göra en grundinstallation av Solr.

## Uppdatera konfigurationsförändringar för K-samsök solr

Om den uppdatering man vill göra endast är konfigurationsföränringar i Solr. Dvs bara uppdatera filinnehåll under mappen: "ksamsok-config" kan man driftsätta med bamboo. 
Detta förutsätter givetvis att man redan har gjort en grundinstallation.

### Manuell Grundinstallion av Solr

#### Kopiera över installationsfiler
Kopiera över filerna till installationsmaskinen.
Nedanstående kommandon baseras på att man står i roten på projektet
```
scp -r solr-7.5.0/* <din-användare>@<solr-maskin>:/tmp
scp -r ksamsok-config <din-användare>@<solr-maskin>:/tmp
```
#### Avinstallation av befintlig Solr installation
OM det finns en befintlig solr installation på maskinen ska nedanstående steg utföras.
Innan en ny version av solr kan installeras måste föregående version avinstalleras eftersom det annars finns risk att indexet trasas sönder.
Var därför noggrann att samtliga filer av solr raderas vid varje ny uppgradering.
Logga in på maskinen och se till att blir root.
```
# Se till att bli root
sudo su - root 
# Stoppa solr
systemctl stop solr
# Avinstallera solr 
/tmp/uninstall-solr.sh
```

#### Installera solr binären
När Solr är avinstallerad kan man installera den nya versionen.

1. Packa upp och installera solr
    ```
    export SOLR_VERSION="7.5.0"
    tar xzf solr-${SOLR_VERSION}.tgz solr-${SOLR_VERSION}/bin/install_solr_service.sh --strip-components=2
    /tmp/install_solr_service.sh /tmp/solr-${SOLR_VERSION}.tgz -i /usr/share -p 8080 -u solr -d /mnt/lucene-index -n
    ```

2. Kopiera över Raa:s anpassningar av solr:s konfigurationsfil för hur solr ska startas. Skriv över den befintliga filen. 
    ```
    cp /tmp/solr.in.sh /etc/default/
    ```

3. Ange ulimits för solr användaren.
    ```
    # lägg till solr ulimits till limits.conf om det inte redan står där
    grep -qxF 'solr hard nofile 65535' /etc/security/limits.conf || echo 'solr hard nofile 65535' >> /etc/security/limits.conf
    grep -qxF 'solr soft nofile 65535' /etc/security/limits.conf || echo 'solr soft nofile 65535' >> /etc/security/limits.conf
    grep -qxF 'solr hard nproc 65535' /etc/security/limits.conf || echo 'solr hard nproc 65535' >> /etc/security/limits.conf
    grep -qxF 'solr soft nproc 65535' /etc/security/limits.conf || echo 'solr soft nproc 65535' >> /etc/security/limits.conf
    ```

4. Starta solr
    ```
    systemctl start solr
    ```

5. Aktivera automatisk uppstart av solr när maskinen bootar upp. Notera outputen. Allt är i sin ordning.
    ```
    systemctl enable solr
    ``` 

    Output borde vara: <br>
    solr.service is not a native service, redirecting to /sbin/chkconfig. <br>
    Executing /sbin/chkconfig solr on

6. Koppla ihop solr med indexfilerna
    ```
    su solr -c "/usr/share/solr/bin/solr create_core -c ksamsok -d /tmp/ksamsok-config"
    ```

7. Gå in i solr adminkonsol - verifiera att coren "ksamsok" existerar och innehåller data.
    T ex.: http://ul-solrksam01.testraa.se:8080/solr/#/ksamsok/core-overview

8. 
    Nu är installationen klar. Solr är uppe i drift. Radera installationsfilerna efter dig för att underlätta inför nästa installation.
    ```
    rm -rf /tmp/install_solr_service.sh /tmp/ksamsok-config /tmp/solr-${SOLR_VERSION}.tgz /tmp/uninstall-solr.sh /tmp/solr.in.sh
    ```

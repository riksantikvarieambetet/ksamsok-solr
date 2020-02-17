# K-samsök solr

Installation av Solr sker helt manuellt eftersom installationen  av solr blir stökig att göra på sedvanligt sätt med bamboo och puppet.   
<br> 
Notera: Ändringar i mappen: "ksamsok-config" kan man driftsätta med bamboo. 

## Taggning inför driftsättning
Eftersom installationen är manuell och inget byggs av bamboo behövs ett sätt att hålla koll på versioner i projektet. Därför ska "tags" sättas i projektet inför varje leverans. 
<br>
När du gjort en förändring i projektet och är nöjd gör följande för att tagga en version av projektet.
<br>
Syntax:
```
git tag -a <tag-namn> -m "<Kommentar-på-förändring>"
```
Exempel:
```
git tag -a v0.1 -m "Första versionen"
```
För att push:a en tag till remote, kör:
```
git push --follow-tags
```
För att lista befintliga taggar, kör:
```
git tag
```
För att kolla närmare på en specifik tag, kör: 
```
git show v0.1
```


## Installera solr manuellt

### Kopiera över installationsfiler
Kopiera över filerna till installationsmaskinen.
Nedanstående kommandon baseras på att man står i roten på projektet
```
scp -r solr-7.5.0/* <din-användare>@<solr-maskin>:/tmp
scp -r ksamsok-config <din-användare>@<solr-maskin>:/tmp
```
### Avinstallation av befintlig Solr installation
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

### Installera solr
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

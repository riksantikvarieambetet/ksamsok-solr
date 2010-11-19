# Solr för K-samsök

Inställningarna är som vanligt anpassade för driftförhållanden så för utveckling måste några
saker sättas upp. Default är att rpm-installationen lägger dessa saker i /var/ksamsok-solr 

Skapa en local.properties och lägg in solr.home så att den pekar ut [ksamsok-solr]/solr-home, typ

solr.home=/path/to/ksamsok-solr/solr-home

Lägg också in en flagga i catalina.sh/bat för att tala om var indexfilerna ska lagras (annars
hamnar de antingen i cvs-katalogen eller under aktuel arbetskatalog):

-Dsolr.data.dir=/path/to/a/good/storing/place

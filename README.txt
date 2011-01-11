# Solr f�r K-sams�k

Inst�llningarna �r som vanligt anpassade f�r driftf�rh�llanden s� f�r utveckling m�ste n�gra
saker s�ttas upp. Default �r att rpm-installationen l�gger dessa saker i /var/lucene-index 

Skapa en local.properties och l�gg in solr.home s� att den pekar ut [ksamsok-solr]/solr-home, typ

solr.home=/path/to/ksamsok-solr/solr-home

L�gg ocks� in en flagga i catalina.sh/bat f�r att tala om var indexfilerna ska lagras (annars
hamnar de antingen i cvs-katalogen eller under aktuel arbetskatalog):

-Dsolr.data.dir=/path/to/a/good/storing/place

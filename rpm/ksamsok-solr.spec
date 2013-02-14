%define ver 1.0.2
%define rel 13

Summary: Raä K-Samsök, solr-instans (@RPM_SUFFIX@)
Name: raa-ksamsok_solr_@RPM_SUFFIX@
Version: %{ver}
Release: %{rel}
Packager: Borje Lewin <borje.lewin@raa.com>
Vendor: Raa 
URL: http://www.raa.se
License: (C) 2009 RAÄ 
Group: System Environment/Daemons
# provar att kommentera bort BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

Requires: raa-tomcat8080 = 7.0.25

%description
Raä K-Samsok, solr-instans (@RPM_SUFFIX@)

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p -m755 $RPM_BUILD_ROOT/usr/local/tomcat8080/webapps
mkdir -p -m755 $RPM_BUILD_ROOT/var/lucene-index/conf

install -m755 $RPM_SOURCE_DIR/solr.war $RPM_BUILD_ROOT/usr/local/tomcat8080/webapps
install -m755 $RPM_SOURCE_DIR/conf/* $RPM_BUILD_ROOT/var/lucene-index/conf


%clean
rm -rf $RPM_BUILD_ROOT

%pre
# stoppa tomcat
/sbin/service tomcat8080.init stop
sleep 5
rm -rf /usr/local/tomcat8080/webapps/solr
#Skapa index map
mkdir /var/lucene-index
chown tomcat /var/lucene-index
chgrp raagroup /var/lucene-index
sudo -u tomcat mkdir /var/lucene-index/data

#Länka in indexet
sudo -u tomcat ln -s /mnt/lucene-index/data/index /var/lucene-index/data/index
sudo -u tomcat ln -s /mnt/lucene-index/data/spellchecker /var/lucene-index/data/spellchecker


%post
/sbin/service tomcat8080.init start

%preun


%postun
rm -rf /usr/local/tomcat8080/webapps/solr

%files
%defattr(-,tomcat,raagroup)
%attr(0644,tomcat,raagroup) /usr/local/tomcat8080/webapps/solr.war
%attr(0744,tomcat,raagroup) /var/lucene-index/conf

%changelog
* Wed Aug 22 2012 ant
- Konverterat från ISO-8859-1 till UTF-8, build.xml översatt till engelska
* Mon Dec 6 2010 ant
- Master/slave
* Fri Dec 11 2009 ant
- Uppdaterat till nya RPM-metodiken

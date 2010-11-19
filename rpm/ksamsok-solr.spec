%define ver 1.0.0
%define rel 01

Summary: Ra� K-Sams�k, solr-instans
Name: raa-ksamsok_solr
Version: %{ver}
Release: %{rel}
Packager: Borje Lewin <borje.lewin@raa.com>
Vendor: Raa 
URL: http://www.raa.se
License: (C) 2009 RA� 
Group: System Environment/Daemons
# provar att kommentera bort BuildArchitectures: noarch
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot

Requires: raa-tomcat8080 >= 6.0.18

%description
Ra� K-Samsok, solr-instans

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p -m755 $RPM_BUILD_ROOT/usr/local/tomcat8080/webapps
#mkdir -p -m755 $RPM_BUILD_ROOT/usr/local/tomcat8080/conf/Catalina/localhost
mkdir -p -m755 $RPM_BUILD_ROOT/var/ksamsok-solr/conf

install -m755 $RPM_SOURCE_DIR/solr.war $RPM_BUILD_ROOT/usr/local/tomcat8080/webapps
#install -m755 $RPM_SOURCE_DIR/solr.xml $RPM_BUILD_ROOT/usr/local/tomcat8080/conf/Catalina/localhost
install -m755 $RPM_SOURCE_DIR/conf/* $RPM_BUILD_ROOT/var/ksamsok-solr/conf


%clean
rm -rf $RPM_BUILD_ROOT

%pre
# stoppa tomcat
/sbin/service tomcat8080.init stop
sleep 5
rm -rf /usr/local/tomcat8080/webapps/solr

%post
/sbin/service tomcat8080.init start

%preun


%postun
rm -rf /usr/local/tomcat8080/webapps/solr

%files
%defattr(-,tomcat,nobody)
%attr(0644,tomcat,nobody) /usr/local/tomcat8080/webapps/solr.war
#%attr(0644,tomcat,nobody) /usr/local/tomcat8080/conf/Catalina/localhost/solr.xml
%attr(0644,tomcat,nobody) /var/ksamsok-solr

%changelog
* Fri Dec 11 2009 ant
- Uppdaterat till nya RPM-metodiken

%define ver 1.0.2
%define rel 20

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

mkdir -p $RPM_BUILD_ROOT/usr/local/tomcat8080/webapps
mkdir -p $RPM_BUILD_ROOT/var/lucene-index/conf
install $RPM_SOURCE_DIR/solr.war $RPM_BUILD_ROOT/usr/local/tomcat8080/webapps
install $RPM_SOURCE_DIR/conf/* $RPM_BUILD_ROOT/var/lucene-index/conf

%clean
rm -rf $RPM_BUILD_ROOT

%pre

#Check if tomcat is running, if not start it
tomcatStatus=$(/sbin/service tomcat8080.init status)
case $tomcatStatus in
	*"pid"*) COUNTER=60
		echo "Tomcat is already running";;

	*) 	/sbin/service tomcat8080.init start
		echo "Starting tomcat. Waiting 60 s for tomcat to start..."
		COUNTER=0;;

esac

#Wait for tomcat to start
while [  $COUNTER -lt 60 ]; do
	tomcatStatus=$(/sbin/service tomcat8080.init status)
	case $tomcatStatus in
		*"pid"*) COUNTER=60
			echo "Tomcat is now running."
			sleep 5;;

		*) 	let COUNTER=COUNTER+1
			echo "Still waiting for Tomcat to start"
			sleep 1;;
	esac
done

#Check if tomcat is up and running otherwise exit
tomcatStatus=$(/sbin/service tomcat8080.init status)
case $tomcatStatus in
	*"pid"*) echo "Tomcat is up and running";;

	*) 	echo "Has been waiting for 60 s and tomcat is not up and running. Check your tomcat installation. Will now exit"
		exit 2;;
esac

#Remove previous installation
if [ -e /usr/local/tomcat8080/webapps/solr.war ] ; then
	echo "Removing previous solr.war"
	rm -f /usr/local/tomcat8080/webapps/solr.war
else
	echo "No previous solr.war was found"
fi
 
#Wait untill tomcat has removed the webapps or timer has timeout
echo "Waiting 60 s for tomcat to remove webapplication"
COUNTER=0
while [  $COUNTER -lt 60 ]; do
	if [ -d /usr/local/tomcat8080/webapps/solr ] ; then
		echo "Web application directory still exist. Waiting for Tomcat to remove directory"
		let COUNTER=COUNTER+1
		sleep 1s
	else
		echo "Web application directory has been removed"
		let COUNTER=60
	fi 
done

#Check if the web application has been removed
if [ -d /usr/local/tomcat8080/webapps/solr ] ; then
	echo "Has been waiting for 60 s and tomcat has not removed the web application. Check your tomcat installation. Will now exit"
	exit 1
fi

%post
# Create symlink to index after installation
ln -s /mnt/lucene-index/data /var/lucene-index/data

echo "Waiting 60 s for tomcat to start web application"
COUNTER=0
while [  $COUNTER -lt 60 ]; do
	if [ -d /usr/local/tomcat8080/webapps/ksamsok ] ; then
		echo "Still waiting for Tomcat to start web application" 
		let COUNTER=COUNTER+1
		sleep 1s
	else
		let COUNTER=60
		sleep 1s
	fi 
done

%preun


%postun
rm -rf /usr/local/tomcat8080/webapps/solr
rm -rf /var/lucene-index/conf

# Check if /var/lucene-index is an symlink then remove it
if [ -L /var/lucene-index/data ]; then
	echo "Removing symlink to /var/lucene-index/data"
	rm -f /var/lucene-index/data
fi

%files
%defattr(-,tomcat,raagroup)
%attr(0644,tomcat,raagroup) /usr/local/tomcat8080/webapps/solr.war
%attr(0644,tomcat,raagroup) /var/lucene-index/conf


%changelog
* Wed Aug 22 2012 ant
- Konverterat från ISO-8859-1 till UTF-8, build.xml översatt till engelska
* Mon Dec 6 2010 ant
- Master/slave
* Fri Dec 11 2009 ant
- Uppdaterat till nya RPM-metodiken

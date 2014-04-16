wget http://apache.fayea.com/apache-mirror/tomcat/tomcat-7/v7.0.53/bin/apache-tomcat-7.0.53.tar.gz
groupadd -g 521 tomcat
useradd -u 521 -g 521 -c "Tomcat Service Account" -d /usr/local/apache-tomcat-7.0.53/ tomcat
chown -R tomcat:tomcat /usr/local/apache-tomcat-7.0.53/
chmod 755 /usr/local/apache-tomcat-7.0.53//bin/*.sh

Fort installation instructions
==============================

Install Django and mod-wsgi (``libapache2-mod-wsgi`` on Debian). 

Checkout ``bugle_project`` into ``/home/bugle`` and run:

    $ chown -R www-data:www-data /home/bugle_project/uploads

Create MySQL database ``bugle`` and an SSL certificate:

    $ mysql -u root
    mysql> create database bugle default charset = "utf8";
    $ make-ssl-cert generate-default-snakeoil --force-overwrite
    $ a2enmod ssl

Create ``/etc/bind/db.twitter.com``:

    $TTL    604800
    @   IN  SOA localhost.  root.localhost. (
                        4   ; Serial
                        604800  ; Refresh
                        86400   ; Retry
                        2419200 ; Expire
                        604800  ; Negative Cache TTL
                        )

    @       IN  NS  10.0.0.1
    @       IN  NS  10.0.0.2
    @       IN  A   10.0.0.1
    api     IN  A   10.0.0.1

Add to ``/etc/bind/named.conf.local``:

    zone "twitter.com." {
            type master;
            file "/etc/bind/db.twitter.com";
            allow-transfer {
                    forts;
            };
    };

Create ``/etc/apache2/sites-available/bugle``:

    <VirtualHost *:80>
    	ServerName twitter.com
    	ServerAlias api.twitter.com
    	WSGIPassAuthorization On
    	WSGIScriptAlias / /home/bugle/bugle_project/bugle.wsgi
            ErrorLog /var/log/apache2/bugle-error.log
            CustomLog /var/log/apache2/bugle-access.log combined
    </VirtualHost>

    <IfModule mod_ssl.c>
    <VirtualHost *:443>
    	ServerName twitter.com	
    	ServerAlias api.twitter.com
    	WSGIPassAuthorization On
    	WSGIScriptAlias / /home/bugle/bugle_project/bugle.wsgi
    	ErrorLog /var/log/apache2/bugle-error.log
    	CustomLog /var/log/apache2/bugle-access.log combined
    	SSLEngine on
    	SSLCertificateFile    /etc/ssl/certs/ssl-cert-snakeoil.pem
    	SSLCertificateKeyFile /etc/ssl/private/ssl-cert-snakeoil.key
    	BrowserMatch ".*MSIE.*" \
    		nokeepalive ssl-unclean-shutdown \
    		downgrade-1.0 force-response-1.0
    </VirtualHost>
    </IfModule>

Run:
    $ a2ensite bugle
    $ /etc/init.d/apache2 force-reload


#!/bin/bash

# Create repoadmin user (has a shell)
useradd -m -g staff -s /bin/bash repoadmin

# Create customer group
groupadd customer

# Create repo directories
mkdir -p /srv/repo/data/apt
mkdir -p /srv/repo/data/yum
chown -R repoadmin:staff /srv/repo/data

# Configure apache
apt-get update 
apt-get -y install rsync apache2 \
    libapache2-mod-authnz-external pwauth \
    libapache2-mod-authz-unixgroup \
    fail2ban \
    makejail

# Copy rrsync to system (it gets put into the chroot
# jail later by makejail).
cp /vagrant/rrsync /usr/local/bin

# Create chroot jail
makejail /vagrant/makejail.conf

# Manually copy locales into chroot
mkdir -p /srv/repo/usr/lib/
cp -r /usr/lib/locale/ /srv/repo/usr/lib/
mkdir -p /srv/repo/usr/share/
cp -r /usr/share/locale /srv/repo/usr/share/

# Apache configuration
cp /vagrant/repo-ssl.conf /etc/apache2/sites-available
cp /vagrant/ports.conf /etc/apache2

a2disconf serve-cgi-bin
a2dissite 000-default
a2dissite default-ssl
a2ensite repo-ssl
a2enmod ssl
a2dismod status
service apache2 reload

# sshd configuration (restart required!!)
cp /vagrant/sshd_config /etc/ssh/sshd_config
service ssh restart

# Turn on host-level firewall
ufw allow 22/tcp
ufw allow 443/tcp
ufw --force enable

# Create a "customer"
useradd -g customer -s /bin/bash -d /srv/repo acmecorp
chpasswd <<EOM
acmecorp:what@ever
EOM


Date: 2011-09-10
Title: Secured virtual FTP with MySQL
Tags: FTP, MySQL, Linux
Category: Blog
Slug: secured-virtual-ftp-server-with-mysql
Author: Eldelshell

In this tutorial I'll show how to setup a FTP virtual serveri (VSFTP) backed by a MySQL database to handle authentication. This example should work with PostgreSQL or any other RDBMS with PAM support. We're going to need:

* vsftpd: Virtual FTP server
* pam: Authentication modules
* MySQL: database

```bash
$sudo apt-get install libpam-mysql vsftpd mysql-server
```

This will install everything we need in a Ubuntu server. Now let's configure it all so they work together.

## MySQL Configuration
Nos vamos a centrar en la configuración que nos interesa en este momentos, por lo tanto, esto no es lo único que se debe hacer despues de instalar MySQL.

We're going to center in the specific configuration for this tutorial, this is not a recommended setup for MySQL.

```sql
-- Create the users database
CREATE DATABASE vsftpd;
USE vsftpd;

-- Create a table for our users
CREATE TABLE accounts (
	id int AUTO_INCREMENT NOT NULL,
	username varchar(30) binary NOT NULL,
	pass varchar(50) binary NOT NULL,
	primary key(id)
);

-- We can create a table to hold some logs
CREATE TABLE logs (msg varchar(255),
	user varchar(20),
	pid int,
	host char(32),
	rhost char(32),
	logtime timestamp
);

-- Create a user for vsftpd (we don't want root)
GRANT SELECT, INSERT, UPDATE ON vsftpd.* TO 'vsftpd'@'localhost' IDENTIFIED BY 'vsftpd_pwd');
FLUSH PRIVELEGES;

GRANT SELECT ON vsftpd.accounts TO 'vsftpd'@'localhost' IDENTIFIED BY 'vsftpd_pwd');
GRANT INSERT ON vsftpd.logs TO 'vsftpd'@'localhost' IDENTIFIED BY 'vsftpd_pwd');
FLUSH PRIVELEGES;
```

## Linux configuration

```bash
$sudo adduser --ingroup nogroup -d /home/vsftpd -s /bin/false vsftpd
$sudo chown vsftpd.nogroup /home/vsftpd
$sudo vi /etc/pam.d/vsftpd
```

Add the following:

```
auth required pam_mysql.so config_file=/etc/security/pam_mysql try_first_pass=false
account required pam_mysql.so config_file=/etc/security/pam_mysql try_first_pass=false
```

Now create the __/etc/security/pam_mysql__ file

```
users.host=localhost
users.database=vsftpd
users.db_user=vsftpd
users.db_passwd=vsftpd_pwd
users.table=accounts
users.user_column=username
users.password_column=pass
users.password_crypt=2
verbose=1
log.enabled=1
log.table=logs
log.message_column=msg
log.pid_column=pid
log.user_column=user
log.host_column=host
log.rhost_column=rhost
log.time_column=logtime
```

Finally, we configure __/etc/vsftpd.conf__

```
listen=YES
anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022
xferlog_enable=YES
xferlog_file=/var/log/vsftpd.log
xferlog_std_format=YES
nopriv_user=vsftpd
chroot_local_user=YES
secure_chroot_dir=/var/run/vsftpd
pam_service_name=vsftpd
rsa_cert_file=/etc/ssl/certs/vsftpd.pem
guest_enable=YES
guest_username=vsftpd
local_root=/home/vsftpd/$USER
user_sub_token=$USER
virtual_use_local_privs=YES
user_config_dir=/etc/vsftpd_user_conf
```

We can now start our FTP server

```bash
$sudo /etc/init.d/vsftpd start
```

_Note: we can configure vsftpd from inetd or xinetd_

## Add users

Create the new user in the MySQL database:

```sql
USE vsftpd;
INSERT INTO accounts (username, pass) VALUES ('foo', PASSWORD('foo_pwd'));
```

And create the user's home folder

```bash
$sudo mkdir /home/vsftpd/nombre
$sudo chmod vsftpd.ngroup /home/vsftpd/nombre
```

That's it, we can use any FTP client to connect to the server. For more information:

* man vsftpd.conf
* man pam

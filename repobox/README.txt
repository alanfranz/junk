
This is a little Vagrantfile + provisioning script for a software
repo server, which allows file access over SSL or rsync, authenticated
via UNIX passwords.

The repo root is located under /srv/repo

/srv/repo/apt/ -> https://.../apt/
/srv/repo/yum/ -> https://.../yum/

By default, DirectoryIndexing is left _on_. Our users 
are authenticated, and we trust their sysadmins not to
be idiots. It helps them track down problems.

The repo admin user is "repoadmin". 

Customers must be created with group "customer".

Demo customer is acmecorp/what@ever

Rsync works with (wacky -e for nonstandard port):

rsync -r -e "ssh -p 2222" acmecorp@localhost:/apt .
rsync -r -e "ssh -p 2222" acmecorp@localhost:/yum .

But arbitrary ssh commands do not work:

(zuul)murderface:repostuff bls$ ssh -p 2222 acmecorp@localhost /bin/bash echo foo
acmecorp@localhost's password: 
rsync: SSH_ORIGINAL_COMMAND='/bin/bash echo foo' is not rsync

(zuul)murderface:repostuff bls$ rsync -r -e "ssh -p 2222" /etc/passwd acmecorp@localhost:
acmecorp@localhost's password: 
rsync -ro: sending to read-only server not allowed
rsync: connection unexpectedly closed (0 bytes received so far) [sender]
rsync error: unexplained error (code 255) at /SourceCache/rsync/rsync-42/rsync/io.c(452) [sender=2.6.9]

Rsync security is handled using rrsync + sshd chroot.
The customer user account does not have write access
anywhere in the chroot. The -ro argument is used to rrsync.

Currently we copy all locales into the chroot, since we 
don't know what languages our customers will want!  We could
shrink the chroot by restricting this to /en/.

The "distro provided" versions of sshd_config and rrsync 
are included, to make it easy to review the changes to these
files.

TODO:

* The SSL configuration needs to be fixed.
* Set ServerName in Apache config.
* Should probably set up fail2ban to handle Apache
  login failures.


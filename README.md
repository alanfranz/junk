ipgen
=====

Ghetto random ip generation, ripped from scantehnet. 

About
-----

ipgen - IP generation logic from scantehnet.

Usage: 

Installation
------------

```
git clone https://github.com/bls/ipgen.git
cd ipgen
sudo apt-get install make build-essential liblog4cpp5-dev \
    libboost-program-options-dev libssl-dev
make
```

Quickstart
----------

To generate 5 millions random IPv4 addresses with no duplicates, excluding
network ranges in 'bogons.txt':

```
bls@zxc:~/wa/ipgen$ ./ipgen -h
options:
  -h [ --help ]         produce help message
  -k [ --key ] arg      scan key (string, default "12345")
  -s [ --save ] arg     save state every n ips (int, default 0, don't save)
  -n [ --num ] arg      stop after n ips (int, default 0, all the ips)
  -b [ --bogons ] arg   bogons file to use (default "bogons.txt")

bls@zxc:~/wa/ipgen$ ./ipgen -k myScanKey -n 5000000 > my_ips
1404443186 INFO stn.bogon_filter : loaded 17 entries.
1404443186 NOTICE stn.ip_enumerator : loaded: bogons.txt
1404443186 ERROR stn.ip_enumerator : failed to load state from file: 'ipgen.state': No such file or directory
1404443186 NOTICE ipgen : no state; starting from scratch
1404443205 NOTICE ipgen : progress: 1 million...
1404443223 NOTICE ipgen : progress: 2 million...
1404443241 NOTICE ipgen : progress: 3 million...
1404443259 NOTICE ipgen : progress: 4 million...
1404443277 NOTICE ipgen : progress: 5 million...
1404443277 ALERT ipgen : Scan complete!

bls@zxc:~/wa/ipgen$ wc -l my_ips 
5000000 my_ips

bls@zxc:~/wa/ipgen$ head -5 my_ips
42.191.11.102
80.7.204.21
219.44.104.11
200.23.135.173
56.134.67.43
```


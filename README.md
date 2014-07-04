ipgen
=====

Ghetto random ip generation, ripped from scantehnet. 

Building
--------

```
git clone https://github.com/bls/ipgen.git
cd ipgen
sudo apt-get install make build-essential liblog4cpp5-dev \
    libboost-program-options-dev libssl-dev
make
```

Quickstart
----------

To generate 5 million random IPv4 addresses with no duplicates, 
excluding network ranges in 'bogons.txt':

```
bls@zxc:~/wa/ipgen$ ./ipgen -h
options:
  -h [ --help ]         produce help message
  -k [ --key ] arg      scan key (string, default "12345")
  -s [ --save ] arg     save state every n ips (int, default 0, don't save)
  -n [ --num ] arg      stop after n ips (int, default 0, all the ips)
  -b [ --bogons ] arg   bogons file to use (default "bogons.txt")

bls@zxc:~/wa/ipgen$ time ./ipgen -k myScanKey -n 5000000 > my_ips
1404444700 INFO stn.bogon_filter : loaded 17 entries.
1404444700 NOTICE stn.ip_enumerator : loaded: bogons.txt
1404444718 NOTICE ipgen : progress: 1 million...
1404444737 NOTICE ipgen : progress: 2 million...
1404444755 NOTICE ipgen : progress: 3 million...
1404444775 NOTICE ipgen : progress: 4 million...
1404444793 NOTICE ipgen : progress: 5 million...
1404444793 ALERT ipgen : done, 5000000 ips emitted.

real    1m33.770s
user    0m47.219s
sys     0m46.171s

bls@zxc:~/wa/ipgen$ wc -l my_ips 
5000000 my_ips

bls@zxc:~/wa/ipgen$ head -5 my_ips
42.191.11.102
80.7.204.21
219.44.104.11
200.23.135.173
56.134.67.43
```

About
-----

The code is a lot heavier than it really needs to be; it was ripped out of a larger
project (scantehnet).  It's pretty inefficient (bogons list is searched linearly),
so it takes about 8 hours to generate a full permutation of IPv4 on a wimpy Atom CPU. 
That turned out to be plenty good enough for our purposes.

How it works
------------

The code runs through the 32-bit integers starting from 0, encrypting them with skip32 
(a 32-bit block cipher).  The encryption key is set with the "-k" parameter. Each generated 
IP is then compared to the bogons list and thrown away if it matches.

Because the block cipher is a one-to-one function from int32 -> int32, we are guaranteed no 
duplicate IPs will appear.

This approach mostly makes sense if you are generating full permutations of IPv4 since it
means that you can ensure no duplicates while using only 4 bytes of state. 


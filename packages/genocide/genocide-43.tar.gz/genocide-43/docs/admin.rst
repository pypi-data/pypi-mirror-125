.. _admin:

admin
#####

G E N O C I D E  

synopsis
========

genocide \<cmd\> \[key=value\] \[key==value\] 

description
===========

GENOCIDE provides a IRC bot that can run as a background daemon for 24/7
day presence in a IRC channel. You can use it to display RSS feeds,
act as a UDP to IRC gateway, program your own commands for it and have
it log objects on disk to search them. GENOCIDE stores it's data as JSON files 
on disk, every object is timestamped, readonly of which the latest is served
to the user layer. File paths have the type included so reconstructing from
json file is made easy. GENOCIDE runs as a single channel bot and is 
programmable with your own commands, which makes it suitable for server
administation and can serve rss feeds to the channel.

GENOCIDE is intended to be programmable in a static, only code, no 
popen, no imports and no reading modules from a directory, way that should
make it secure.

install
=======

installation is through pypi::

 sudo pip3 install genocide
    
configuration
=============

restarting after reboot needs enabling the bot as a service::

 sudo cp /usr/local/share/genocide/genocide.service /etc/systemd/system
 sudo systemctl enable genocide --now

irc
===

IRC configuration is done with the use of the genocide program, the cfg
command configures the IRC bot::

 sudo genocide cfg server=<server> channel=<channel> nick=<nick> 

default channel/server is #genocide on localhost

sasl
====

some irc channels require SASL authorisation (freenode,libera,etc.) and
a nickserv user and password needs to be formed into a password. You can use
the pwd command for this::

 sudo genocide pwd <nickservnick> <nickservpass>

after creating you sasl password add it to you configuration::

 sudo genocide cfg password=<outputfrompwd>

users
=====

if you want to restrict access to the bot (default is disabled), enable
users in the configuration and add userhosts of users to the database::

 sudo genocide cfg users=True
 sudo genocide met <userhost>

rss
===

add a url to the bot and the feed fetcher will poll it every 5 minutes::

 sudo genocide rss <url>

programming
===========

for programming the bot you have to have the code available as employing
your own code requires that you install your own bot as the system bot, this
way only trusted code (your own written code) is included and runnable.

fetch the code from https://pypi.org/project/genocide/#files

untar the tarball, cd into the bot directory, edit genocide/hlo.py and add the
following to it::

 def hlo(event):
     event.reply("hello!")

then add genocide/hlo.py to the genocide/all.py module and let it scan the module::

 import genocide.hlo as hlo
 Table.addmod(hlo)

install on the system::

 sudo python3 setup.py install

restart genocide service::

 sudo systemctl restart genocide

the hlo command is now available to users.

copyright
=========

GENOCIDE is placed in the Public Domain, no Copyright, no LICENSE.

author
======

Bart Thate

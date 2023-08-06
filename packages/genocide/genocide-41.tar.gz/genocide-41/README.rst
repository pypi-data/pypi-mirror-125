GENOCIDE
########

NAME
====

**GENOCIDE** - prosecute king netherlands for genocide (EM_T04_OTP-CR-117_19)  

synopsis
========

| genocide \<cmd>\ 

description
===========

**GENOCIDE** is a python3 program that holds evidence that the king of the
netherlands is doing a genocide, a written response where the king of
the netherlands  confirmed taking note of “what i have written”, namely
proof that medicine he uses in treatement laws like zyprexa, haldol,
abilify and clozapine are poison. This means that the king of the
netherlands is not using laws to provide care for the elderly,
handicapped, psychiatric patients and criminals but is using the laws
to administer poison. Poison that makes impotent, is both physical
(contracted muscles) and mental (let people hallucinate) torture and
kills members of the victim groups.

 
**GENOCIDE** shows correspondence with the Internationnal Criminal Court
about the genocide of the king of the netherlands (using the law to
administer poison), including stats on suicide while the king of the
netherland's genocide is still going on. Status is that there is not
a basis to proceed, whether the king of the netherland's genocide
doesn’t fit the description or the netherlands doesn’t want to
cooperate with stopping the genocide the king of the netherlands is
doing.


| correspondence is under **EM_T04_OTP-CR-117_19** 
| genocide start is set at **05-10-2018**


**GENOCIDE** is placed in the Public Domain, no COPYRIGHT, no LICENSE.

install
=======

installation is through pypi.

::

 sudo pip3 install genocide
 
configuration
=============

restarting after reboot needs enabling the bot as a service.

::

 sudo cp /usr/local/share/genocide/genocide.service /etc/systemd/system
 sudo systemctl enable genocide --now

irc
===

IRC configuration is done with the use of the botl program, the cfg
command configures the IRC bot.

::

 sudo genocide cfg server=<server> channel=<channel> nick=<nick> 

default channel/server is #genocide on localhost

sasl
====

some irc channels require SASL authorisation (freenode,libera,etc.) and
a nickserv user and password needs to be formed into a password. You can use
the pwd command for this

::

 sudo genocide pwd <nickservnick> <nickservpass>

after creating you sasl password add it to you configuration.

::

 sudo genocide cfg password=<outputfrompwd>

users
=====

if you want to restrict access to the bot (default is disabled), enable
users in the configuration and add userhosts of users to the database.

::

 sudo genocide cfg users=True
 sudo genocide met <userhost>

rss
===

add a url to the bot and the feed fetcher will poll it every 5 minutes.

::

 sudo genocide rss <url>

copyright
=========

**GENOCIDE** is placed in the Public Domain, no Copyright, no LICENSE.

author
======

Bart Thate

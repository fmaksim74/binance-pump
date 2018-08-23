# Binance Pump

Module for loading data from the Binance exchange into a relational database under the control of PostgresSQL.
It doesn't load account data and user orders because they are stored in exchange.

## 1. Instalation

All instructions made with assumption that Ubuntu is used as server OS.

### 1.1 PostgreSQL instalation

As described in [Apt - PostgreSQL Wiki](https://wiki.postgresql.org/wiki/Apt)

*1. Import the repository key from* [https://www.postgresql.org/media/keys/ACCC4CF8.asc](https://www.postgresql.org/media/keys/ACCC4CF8.asc):
```
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
```
Create /etc/apt/sources.list.d/pgdg.list. The distributions are called codename-pgdg. In the example, replace stretch with the actual distribution you are using:
```
deb http://apt.postgresql.org/pub/repos/apt/ stretch-pgdg main
```
(You may determine the codename of your distribution by running lsb_release -c). For a shorthand version of the above, presuming you are using a supported release:
```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt/ $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
```
Finally, update the package lists, and start installing packages:
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install postgresql-10
```
Alternately, [this](https://salsa.debian.org/postgresql/postgresql-common/raw/master/pgdg/apt.postgresql.org.sh) shell script will automate the repository setup. Note that the shell script leaves the source package repo (deb-src) commented out; if you need source packages, you will need to modify /etc/apt/sources.list.d/pgdg.list to enable it.

2. Initial configuration

Open `psql` cli:
```
 sudo -u postgres psql template1
```
Set password for user `postgres`:
```
 \password <password>
```
Creeate the `binance` user:
```
 CREATE USER binance WITH ENCRIPTED PASSWORD '<password>';
```
Create the `binancedb` database:
```
 CREATE DATABASE "binancedb";
```
Set access rights to `binancedb` for user `binance`:
```
 GRAND ALL ON "binancedb" TO "binance";
```
Change authorization method in `/etc/postgresql/10/main/pg_hba.conf` to enable login with PostgreSQL roles:
was:
```
 # Database administrative login by Unix domain socket
 local   all             postgres                                peer

 # "local" is for Unix domain socket connections only
 local   all             all                                     peer

```
should be:
```
 # Database administrative login by Unix domain socket
 local   all             postgres                                md5

 # "local" is for Unix domain socket connections only
 local   all             all                                     md5

```
Enable TCP/IP connections to PostgreSQL in `/etc/postgresql/10/main/postgresql.conf`:
```
 listen_addresses = 'localhost'
```
Enable IO buffering in `/etc/postgresql/10/main/postgresql.conf`:
```
 wal_level = minimal
 fsync = off

```
Restart PostgreSQL service:
```
 sudo /etc/init.d/postgresql restart
```


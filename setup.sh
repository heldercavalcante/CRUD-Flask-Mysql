#!/bin/bash

docker rm -f mysql_server
docker run --name mysql_server -e MARIADB_ROOT_PASSWORD=12345 -v ~/.mysql:/var/lib/mysql -d -p 3306:3306 mariadb:10.6.4

docker rm -f phpmyadmin
docker run --name phpmyadmin -d --link mysql_server:db -p 8081:80 phpmyadmin/phpmyadmin

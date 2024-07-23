#!/usr/bin/env sh

set -x
echo "Current working directory: $(pwd -P)"
docker rm -f my-login-app || true
docker run -d -p 80:80 --name my-login-app -v /var/jenkins_home/workspace/webapp/:/var/www/html php:7.2-apache
sleep 1
set +x

echo 'Now...'
echo 'Visit http://localhost to see your application in action.'


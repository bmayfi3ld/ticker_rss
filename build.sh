# versions
# 0.1.0 - initial
# 0.2.0 - added images
# 0.2.1 - fixed bad date

docker build . -t 192.168.10.1:5000/ticker-rss:0.2.1
docker push 192.168.10.1:5000/ticker-rss:0.2.1
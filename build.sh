# versions
# 0.1.0 - initial
# 0.2.0 - added images
# 0.2.1 - fixed bad date

docker build . -t registry.field3.systems/ticker-rss:0.2.1
docker push registry.field3.systems/ticker-rss:0.2.1
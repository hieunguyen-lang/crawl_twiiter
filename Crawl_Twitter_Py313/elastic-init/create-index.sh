#!/bin/sh

echo "⏳ Waiting for Elasticsearch to be ready..."

until curl -s http://elasticsearch:9200 >/dev/null; do
  sleep 1
done

echo "🚀 Creating index data_posts_twitter..."

curl -X PUT "http://elasticsearch:9200/data_posts_twitter" \
     -H "Content-Type: application/json" \
     -d @/init/mapping.json
curl -X PUT "http://elasticsearch:9200/data_posts_facebook" \
     -H "Content-Type: application/json" \
     -d @/init/mapping.json
echo "✅ Index created."
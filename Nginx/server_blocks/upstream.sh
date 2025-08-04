#!/bin/bash

cd /opt/bitnami/nginx/conf/server_blocks

UPSTREAMS="${NGINX_OTLP_KAFKA_BRIDGE_LB_UPSTREAM}"

# Output to upstream.conf
cat <<EOF > upstream.conf
upstream otlp_kafka_bridge_lb_upstream {
$(echo "$UPSTREAMS" | tr ',' '\n' | while read -r server; do
    echo "    server $server;"
done)
}
EOF

cat upstream.conf

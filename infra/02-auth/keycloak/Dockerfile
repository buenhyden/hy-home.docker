# Reference: https://www.keycloak.org/server/containers
FROM quay.io/keycloak/keycloak:26.5.0 AS builder

# Enable health and metrics support
ENV KC_HEALTH_ENABLED=true
ENV KC_METRICS_ENABLED=true

# Configure a database vendor
ENV KC_DB=postgres

WORKDIR /opt/keycloak

# Create a self-signed certificate for development/demonstration purposes
# for demonstration purposes only, please make sure to use proper certificates in production instead
# hadolint ignore=DL3059
RUN keytool -genkeypair -storepass password -storetype PKCS12 -keyalg RSA -keysize 2048 -dname "CN=server" -alias server -ext "SAN:c=DNS:localhost,IP:127.0.0.1" -keystore conf/server.keystore && \
    /opt/keycloak/bin/kc.sh build

FROM quay.io/keycloak/keycloak:26.5.0
LABEL maintainer="Custom Keycloak Build"

COPY --from=builder /opt/keycloak/ /opt/keycloak/

# Runtime environment variables should be set in docker-compose.yml
# change these values to point to a running postgres instance
# ENV KC_DB=postgres
# ENV KC_DB_URL=<DBURL>
# ENV KC_DB_USERNAME=<DBUSERNAME>
# ENV KC_DB_PASSWORD=<DBPASSWORD>
# ENV KC_HOSTNAME=<HOSTNAME>

ENTRYPOINT ["/opt/keycloak/bin/kc.sh"]

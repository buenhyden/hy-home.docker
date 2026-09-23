# stalwart-cli has no shell in its own image; the config job needs one to read
# the admin secret and render the domain, so the pinned binary joins the
# server image (same layers as the running server).
FROM ghcr.io/stalwartlabs/cli:1.0.12 AS cli
FROM stalwartlabs/stalwart:v0.16.22
COPY --from=cli /usr/local/bin/stalwart-cli /usr/local/bin/stalwart-cli

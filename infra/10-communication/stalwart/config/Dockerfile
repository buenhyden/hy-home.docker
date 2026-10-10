# stalwart-cli has no shell in its own image; the config job needs one to read
# the admin secret and render the domain, so the pinned binary joins the
# server image (same layers as the running server).
FROM ghcr.io/stalwartlabs/cli:1.0.13@sha256:9a1e07307d6f890a193322c4b737fc0868405f0f8486a19922cbf362f43884fd AS cli
FROM stalwartlabs/stalwart:v0.16.25@sha256:74e5a7d55303ba525d939c6bf97ed4e010df7521f52d80afc22a815b66bd53f3
COPY --from=cli /usr/local/bin/stalwart-cli /usr/local/bin/stalwart-cli

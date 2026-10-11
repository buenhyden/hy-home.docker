# stalwart-cli has no shell in its own image; the config job needs one to read
# the admin secret and render the domain, so the pinned binary joins the
# server image (same layers as the running server).
FROM ghcr.io/stalwartlabs/cli:1.0.13@sha256:9a1e07307d6f890a193322c4b737fc0868405f0f8486a19922cbf362f43884fd AS cli
FROM stalwartlabs/stalwart:v0.16.26@sha256:254ce5d7f3dbe4bb628ce2c7912e664ecb1c3466db79907f4a44d9a00117776b
COPY --from=cli /usr/local/bin/stalwart-cli /usr/local/bin/stalwart-cli

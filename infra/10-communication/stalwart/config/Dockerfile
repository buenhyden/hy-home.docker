# stalwart-cli has no shell in its own image; the config job needs one to read
# the admin secret and render the domain, so the pinned binary joins the
# server image (same layers as the running server).
FROM ghcr.io/stalwartlabs/cli:1.0.13@sha256:9a1e07307d6f890a193322c4b737fc0868405f0f8486a19922cbf362f43884fd AS cli
FROM stalwartlabs/stalwart:v0.16.27@sha256:c429b311c93db5606598abc1c68225a85a6953183848ae01bee9c6a98885836c
COPY --from=cli /usr/local/bin/stalwart-cli /usr/local/bin/stalwart-cli

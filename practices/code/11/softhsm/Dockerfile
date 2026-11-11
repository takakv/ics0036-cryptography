FROM debian:trixie-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        softhsm2 opensc openssl python3 python3-pyasn1 \
    && rm -rf /var/lib/apt/lists/*

# Make pkcs11-tool use SoftHSM by default.
COPY pkcs11-tool /usr/local/bin/pkcs11-tool
COPY init-tokens.sh /usr/local/bin/init-tokens
RUN chmod +x /usr/local/bin/pkcs11-tool /usr/local/bin/init-tokens

VOLUME /var/lib/softhsm/tokens

WORKDIR /work
ENTRYPOINT ["init-tokens"]
CMD ["bash"]

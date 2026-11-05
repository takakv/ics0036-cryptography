# Papers, please

Deadline: `2026-11-22T23:59:59+02:00`

Filename: `token.txt`

## Task

<https://lab.kastike.ee/> requires a client certificate and uses the root certificate as the sole trust anchor for validating it.
The server does not have the chain linking leaves to the root.

Connect to <https://lab.kastike.ee/> with your certificate chain.
On success, the server replies with a token.
Save the reply to `token.txt` unchanged, e.g. with `curl … | tee token.txt`.

> [!TIP]
> `openssl s_client -connect lab.kastike.ee:443 | grep -A2 client` shows which CAs the server accepts client certificates from (quit with Ctrl+C).
> Compare it with kastike.ee.

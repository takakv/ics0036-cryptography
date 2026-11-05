# Two birds with one stone

Deadline: `2026-11-22T23:59:59+02:00`

Filename: `flag.txt`

## Background

I recorded three TLS 1.2 connections to the same server: [`1.pcapng`](1.pcapng), [`2.pcapng`](2.pcapng) and [`3.pcapng`](3.pcapng).

Some time later, the server's private key [`server.key.pem`](server.key.pem) leaked.

## Task

Use the leaked key to decrypt the traffic.
The flag is split into two parts, each in a server response.

`flag.txt` must contain only the whole flag, e.g. `ICS0036{...}`, on a single line.

> [!TIP]
> In Wireshark, right-click a TLS packet and choose *Protocol Preferences → Transport Layer Security → Open Transport Layer Security Preferences…*.

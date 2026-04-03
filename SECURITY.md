# Security Policy

## Supported Versions

| Version | Supported |
| ------- | --------- |
| latest  | Yes       |

## Reporting a Vulnerability

Report security vulnerabilities via GitHub's private vulnerability reporting at [github.com/gebruder/kampfraum/security/advisories](https://github.com/gebruder/kampfraum/security/advisories).

Do not open a public issue for security vulnerabilities.

You should receive an initial response within 72 hours. If the vulnerability is accepted, a fix will be released and the advisory will be published after the fix is available.

## Scope

The following are in scope for security reports:

- Fetch scripts (command injection, path traversal, unsafe downloads)
- Catalog data integrity (schema validation bypass, injection via dataset metadata)
- Dashboard (XSS via catalog.json content, CDN integrity)
- CI workflows (secret leakage, workflow injection)
- Normalize pipeline (arbitrary code execution via crafted data files)

The following are out of scope:

- Content of third-party datasets (report to the dataset maintainer)
- Vulnerabilities in CDN-hosted libraries (report upstream, but let us know)
- Availability of external dataset sources

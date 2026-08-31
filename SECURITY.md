# Security Policy

## Supported Version

Security fixes are applied to the latest state of the `main` branch.

## Reporting A Vulnerability

Please use GitHub private vulnerability reporting for this repository rather than opening a public issue. Include the affected endpoint or component, reproduction steps, potential impact, and any suggested mitigation.

Do not include real credentials, production records, or third-party personal data in a report. The repository itself contains only fictional seed data.

## Security Boundaries

StreamSentry is a reference implementation. Authentication and tenant authorization are intentionally outside the current runnable scope. Do not expose the service to an untrusted network without adding those controls, configuring strict CORS origins, terminating TLS, and replacing the development storage adapter with an audited persistence implementation.

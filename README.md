# Layer Defenses Around a Local Secret Service

## Project Overview

This project demonstrates the cybersecurity principle of **Defense in Depth** by securing a small Python-based local web service that provides access to a protected secret file.

The objective is to implement multiple security controls so that a failure in one layer does not automatically expose the protected resource.

**Project Type:** Cybersecurity / 
**Environment:** Linux, Python 3, Command Line  
**Lab Platform:** LabEx

## 1. Project Objectives

- Understand the Defense in Depth security model.
- Implement token-based request authentication.
- Restrict network exposure using localhost binding.
- Secure sensitive files using Linux permissions.
- Record unauthorized access attempts through application logging.
- Verify that all security controls work together.

## 2. Security Architecture

The service uses four security layers:

| Layer | Security Control | Purpose |
|---|---|---|
| 1 | Token Authentication | Rejects requests without the correct access token |
| 2 | Localhost Binding | Restricts network access to the local machine |
| 3 | File Permissions | Restricts access to the secret file |
| 4 | Security Logging | Records rejected access attempts |

## 3. Implementation Details

### Layer 1: Token Authentication

The service checks incoming requests for the `X-Access-Token` HTTP header.

- Requests without a valid token receive `403 Forbidden`.
- Requests with the expected token are authorized.

**Testing command:**

```bash
curl -i http://127.0.0.1:8081/secret
```

Authorized request:

```bash
curl -s -H "X-Access-Token: lab-token-2026" \
http://127.0.0.1:8081/secret
```

### Layer 2: Localhost Binding

The Python service is configured to listen on:

```text
127.0.0.1:8081
```

This restricts connections to the local machine instead of exposing the service on all network interfaces.

**Verification command:**

```bash
ss -ltn | grep ':8081'
```

Expected listening address:

```text
127.0.0.1:8081
```

### Layer 3: File Permission Security

The secret file is protected using the Linux `chmod` command.

```bash
chmod 600 secret.txt
```

Permission result:

```text
-rw-------
```

This gives the file owner read and write access while denying access to group members and others.

**Verification command:**

```bash
ls -l secret.txt
```

### Layer 4: Security Logging

The application records rejected requests in `access.log`.

The logging mechanism helps identify unauthorized access attempts.

**Testing command:**

```bash
curl -s http://127.0.0.1:8081/secret
```

View the access log:

```bash
cat access.log
```

Expected log information includes:

```text
rejected
/secret
missing_or_bad_token
```

## 4. Project Files

```text
Layer-Defenses-Around-Local-Secret-Service/
│
├── secret_service.py
├── secret.txt
├── service-check.py
├── README.md
├── screenshots/
│   ├── 1_token.png
│   ├── 2_localhost.png
│   ├── 3_permissions & logging.png
│   ├── 4_all.png
│   └── 5_Commands.png
│
└── .gitignore
```

## 5. Complete Security Verification

The provided validation script checks whether all four security layers are correctly configured.

Run:

```bash
python3 service-check.py all
```

Expected result:

```text
token: complete
localhost: complete
permissions: complete
logging: complete
```

These results indicate that all four lab validation checks have passed.

## 6. Running the Application

Start the service:

```bash
python3 secret_service.py > service.log 2>&1 &
```

Save the process ID:

```bash
echo $! > service.pid
```

Send an authorized request:

```bash
curl -s -H "X-Access-Token: lab-token-2026" \
http://127.0.0.1:8081/secret
```

Stop the service:

```bash
kill "$(cat service.pid)"
```

## 7. Screenshots and Evidence

The following screenshots document the implementation and testing of each security layer.

### Token Authentication

![Token Authentication](screenshots/1_token.png)

### Localhost Binding

![Localhost Verification](screenshots/2_localhost.png)

### File Permissions

![File Permission Verification](screenshots/3_permissions.png)

### Security Logging

![Access Log Verification](screenshots/4_logging.png)

### Complete Security Verification

![All Security Layers](screenshots/5_all.png)

## 8. Key Learning Outcomes

Through this project, I practised:

- Linux file and directory permission management.
- Python-based local service testing.
- HTTP request testing using `curl`.
- Network socket inspection using `ss`.
- Token-based access control.
- Security event logging and investigation.
- Defense in Depth implementation.

## 9. Security Considerations

This is an educational demonstration, not a production-ready authentication service.

In a real-world deployment:

- Store authentication secrets securely instead of hardcoding them.
- Use HTTPS and secure token management.
- Consider rate limiting and authentication failure monitoring.
- Use appropriate file ownership and access controls.
- Protect logs against unauthorized modification.
- Avoid exposing sensitive files, tokens, or credentials in public repositories.

## 10. Project Reference

**LabEx Learning Profile:**  
https://labex.io/u/elisa-begum-11023986

---

**Conclusion**

This project demonstrates how multiple security controls can work together to protect a sensitive resource. It provides practical experience with Linux security, application access control, network exposure management, and security logging.

*Project completed as part of hands-on cybersecurity practice using LabEx.*

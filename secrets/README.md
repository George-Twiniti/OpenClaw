# Secrets (SOPS + AGE)

These files are encrypted with **sops** using **age**.

## Decrypt

1) Ensure you have the age private key file (`age.key`) stored securely.
2) Export the key location:

```bash
export SOPS_AGE_KEY_FILE=/path/to/age.key
```

3) Decrypt a file:

```bash
sops -d secrets/gmail.env
```

## Encrypt / edit

```bash
sops secrets/gmail.env
```

## Notes
- `.sops.yaml` defines the encryption rule for `secrets/*.env`.
- Keep `age.key` **out of git** and store it in a secure location.

# this is where we place the documentation

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
self.backup_vault = backup.BackupVault(self, "BackupVault",
    backup_vault_name=f"{props.tableName}-backup-vault",
    access_policy=iam.PolicyDocument(
        statements=[
            iam.PolicyStatement(
                sid="backup-recovery-point-manual-deletion-disabled",
                effect=iam.Effect.DENY,
                principals=[iam.AnyPrincipal()],
                actions=["backup:DeleteRecoveryPoint", "backup:PutBackupVaultAccessPolicy", "backup:UpdateRecoveryPointLifecycle"
                ],
                resources=["*"]
            )
        ]
    )
)
```

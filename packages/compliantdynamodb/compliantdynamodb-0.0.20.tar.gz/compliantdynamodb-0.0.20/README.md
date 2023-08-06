# this is where we place the documentation

```
this.backupVault = new backup.BackupVault(this, 'BackupVault', {
      backupVaultName: `${props.tableName}-backup-vault`,
      accessPolicy: new iam.PolicyDocument({
        statements: [
          new iam.PolicyStatement({
            sid: 'backup-recovery-point-manual-deletion-disabled',
            effect: iam.Effect.DENY,
            principals: [new iam.AnyPrincipal()],
            actions: [
              'backup:DeleteRecoveryPoint',
              'backup:PutBackupVaultAccessPolicy',
              'backup:UpdateRecoveryPointLifecycle',
            ],
            resources: ['*'],
          }),
        ],
      }),
    });
```

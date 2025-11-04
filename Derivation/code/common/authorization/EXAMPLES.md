# Example Workflow


## 1. Set tag secret

(venv) justin@prometheus-ai:/mnt/ironwolf/git/Prometheus_VDM$ python3 -m Derivation.code.common.authorization.approve_tag set-tag-secret metriplectic assisted-echo-t4-prereg-v1c assisted-echo-t4-prereg-v1c-jkl
[authorization] Using approvals DB from env file /mnt/ironwolf/git/Prometheus_VDM/.env: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval.db
[approve_tag] Using approvals DB resolved by helper: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval.db
[authorization] Using admin DB from env file /mnt/ironwolf/git/Prometheus_VDM/.env: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval_admin.db
Admin password for approvals DB (won't echo): 
Tag secret set for 'metriplectic:assisted-echo-t4-prereg-v1c' in /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval.db

## 2. Approve the run

(venv) justin@prometheus-ai:/mnt/ironwolf/git/Prometheus_VDM$ python3 -m Derivation.code.common.authorization.approve_tag approve metriplectic assisted-echo-t4-prereg-v1c --script assisted_echo.py --schema Derivation/code/physics/metriplectic/schemas/assisted-echo-t4-prereg-v1c.schema.json --manifest Derivation/code/physics/metriplectic/APPROVAL.CEG.json
[authorization] Using approvals DB from env file /mnt/ironwolf/git/Prometheus_VDM/.env: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval.db
[approve_tag] Using approvals DB resolved by helper: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval.db
[authorization] Using admin DB from env file /mnt/ironwolf/git/Prometheus_VDM/.env: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval_admin.db
Admin password for approvals DB (won't echo): 
Will apply changes:
  pre_registered: True
  allowed_tags includes: assisted-echo-t4-prereg-v1c
  approvals['assisted-echo-t4-prereg-v1c'].approved_by: Justin K. Lietz
  approvals['assisted-echo-t4-prereg-v1c'].approved_at: 2025-11-04T17:13:59.130885+00:00
  approvals['assisted-echo-t4-prereg-v1c'].approval_key: <hex 64 chars>
  approvals['assisted-echo-t4-prereg-v1c'].schema: Derivation/code/physics/metriplectic/schemas/assisted-echo-t4-prereg-v1c.schema.json
  approval message scope: domain:assisted_echo.py:assisted-echo-t4-prereg-v1c
DB updated: /mnt/ironwolf/git/Prometheus_VDM/Derivation/code/common/data/approval.db -> (metriplectic, assisted-echo-t4-prereg-v1c)
Updated manifest: Derivation/code/physics/metriplectic/APPROVAL.CEG.json
(venv) justin@prometheus-ai:/mnt/ironwolf/git/Prometheus_VDM$ 
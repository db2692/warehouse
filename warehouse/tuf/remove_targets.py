from tuf.repository_tool import *
import os

path_to_repo = "/home/ubuntu/warehouse/warehouse/tuf/repository/"
path_to_keystore = "/home/ubuntu/keystore/"

repository = load_repository(path_to_repo)

repository.targets.remove_target(path_to_repo+"/targets/opengrid-0.4.5-py2.py3-none-any.whl")

private_targets_key = import_rsa_privatekey_from_file(path_to_keystore+"targets_key", password="targets_password")
repository.targets.load_signing_key(private_targets_key)

private_snapshot_key = import_rsa_privatekey_from_file(path_to_keystore+"snapshot_key", password="snapshot_password")
repository.snapshot.load_signing_key(private_snapshot_key)

private_timestamp_key = import_rsa_privatekey_from_file(path_to_keystore+"timestamp_key", password="timestamp_password")
repository.timestamp.load_signing_key(private_timestamp_key)

print repository.dirty_roles()
print repository.status()


repository.writeall()

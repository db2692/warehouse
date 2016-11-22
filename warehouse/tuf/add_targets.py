from tuf.repository_tool import *
import os

path_to_repo = "/path/to/repository/"
path_to_keystore = "/path/to/keystore/"

repository = load_repository(path_to_repo)
list_of_targets = repository.get_filepaths_in_directory(path_to_repo+"targets/", recursive_walk=False, followlinks=True)
print list_of_targets
repository.targets.add_targets(list_of_targets)

private_targets_key = import_rsa_privatekey_from_file(path_to_keystore+"targets_key", password="targets_password")
repository.targets.load_signing_key(private_targets_key)

private_snapshot_key = import_rsa_privatekey_from_file(path_to_keystore+"snapshot_key", password="snapshot_password")
repository.snapshot.load_signing_key(private_snapshot_key)

private_timestamp_key = import_rsa_privatekey_from_file(path_to_keystore+"timestamp_key", password="timestamp_password")
repository.timestamp.load_signing_key(private_timestamp_key)

print repository.dirty_roles()
print repository.status()


repository.writeall()

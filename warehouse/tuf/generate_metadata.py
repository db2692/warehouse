## TUF INTEGRATION

# This script initializes all TUF metadata as per the PEP458 specifications
# Replace path variables and passwords as required

# Repository management instructions here - https://github.com/theupdateframework/tuf/blob/develop/tuf/README.md


from tuf.repository_tool import *
import datetime

# Define paths
path_to_repo = "/path/to/repository/"
path_to_keystore = "/path/to/keystore/"


# Root keypair
generate_and_write_rsa_keypair(path_to_keystore+"root_key", bits=2048, password="root_password")
public_root_key = import_rsa_publickey_from_file(path_to_keystore+"root_key.pub")
private_root_key = import_rsa_privatekey_from_file(path_to_keystore+"root_key", password="root_password")


# Sample Ed25519 keypair
generate_and_write_ed25519_keypair(path_to_keystore+"ed25519_key", password="ed25519_password")
public_ed25519_key = import_ed25519_publickey_from_file(path_to_keystore+"ed25519_key.pub")
private_ed25519_key = import_ed25519_privatekey_from_file(path_to_keystore+"ed25519_key", password="ed25519_password")


# Create repository
repository = create_new_repository(path_to_repo)
repository.root.add_verification_key(public_root_key)
repository.root.load_signing_key(private_root_key)


# Keypairs for timestamp, snapshot, target roles
generate_and_write_rsa_keypair(path_to_keystore+"targets_key", password="targets_password")
generate_and_write_rsa_keypair(path_to_keystore+"snapshot_key", password="snapshot_password")
generate_and_write_rsa_keypair(path_to_keystore+"timestamp_key", password="timestamp_password")

repository.targets.add_verification_key(import_rsa_publickey_from_file(path_to_keystore+"targets_key.pub"))
repository.snapshot.add_verification_key(import_rsa_publickey_from_file(path_to_keystore+"snapshot_key.pub"))
repository.timestamp.add_verification_key(import_rsa_publickey_from_file(path_to_keystore+"timestamp_key.pub"))

private_targets_key = import_rsa_privatekey_from_file(path_to_keystore+"targets_key", password="targets_password")
private_snapshot_key = import_rsa_privatekey_from_file(path_to_keystore+"snapshot_key", password="snapshot_password")
private_timestamp_key = import_rsa_privatekey_from_file(path_to_keystore+"timestamp_key", password="timestamp_password")

repository.targets.load_signing_key(private_targets_key)
repository.snapshot.load_signing_key(private_snapshot_key)
repository.timestamp.load_signing_key(private_timestamp_key)
repository.timestamp.expiration = datetime.datetime(2016, 11, 30, 12, 8)


# Delegate to pypi-signed
generate_and_write_rsa_keypair(path_to_keystore+"pypi-signed_key", bits=2048, password="pypi-signed_password")
public_pypi_signed_key = import_rsa_publickey_from_file(path_to_keystore+"pypi-signed_key.pub")
repository.targets.delegate("pypi-signed", [public_pypi_signed_key], [])
private_pypi_signed_key = import_rsa_privatekey_from_file(path_to_keystore+"pypi-signed_key", password="pypi-signed_password")
repository.targets("pypi-signed").load_signing_key(private_pypi_signed_key)
repository.targets("pypi-signed").version = 2

# Delegate to hashed bins
targets = repository.get_filepaths_in_directory(path_to_repo+'targets/', recursive_walk=True)
repository.targets('pypi-signed').delegate_hashed_bins(targets, [public_pypi_signed_key], 1024)

for delegation in repository.targets('pypi-signed').delegations:
    delegation.load_signing_key(private_pypi_signed_key)



print repository.dirty_roles()
print repository.status()

# Write repository
repository.writeall()

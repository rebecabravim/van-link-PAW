import hashlib
import secrets

# mesg1 = "ola mundo!"

# hash_md5 = hashlib.md5(mesg1.encode())
# print(hash_md5.hexdigest())

# hash_sha1 = hashlib.sha1(mesg1.encode())
# print(hash_sha1.hexdigest())

# hash_sha256 = hashlib.sha256(mesg1.encode())
# print(hash_sha256.hexdigest())

# hash_sha512 = hashlib.sha512(mesg1.encode())
# print(hash_sha512.hexdigest())

salt = secrets.token_hex(16)
print(salt)
password="abb"

hash_pass = hashlib.sha256((password + salt).encode())
print(hash_pass.hexdigest())


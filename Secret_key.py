import pyotp
secret= pyotp.random_base32()
print("TOTP secret key:",secret)
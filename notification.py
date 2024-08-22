from pywebpush import generate_vapid_keypair

vapid_keys = generate_vapid_keypair()
print(vapid_keys)
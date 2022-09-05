import rsa

def save_key(public_key, private_key):
    # Save the public_key
    with open("public_key.txt", "wb") as public_file:
        public_file.write(public_key.save_pkcs1())
 
    # Save the private_key
    with open("private_key.txt", "wb") as private_file:
        private_file.write(private_key.save_pkcs1())


publicKey, privateKey = rsa.newkeys(126)
save_key(publicKey, privateKey)

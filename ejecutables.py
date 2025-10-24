from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

# Contraseñas/códigos originales
codigo_usuario1 = 'policia123'
codigo_usuario2 = 'policia456'

# Generamos los hashes
hash1 = bcrypt.generate_password_hash(codigo_usuario1).decode('utf-8')
hash2 = bcrypt.generate_password_hash(codigo_usuario2).decode('utf-8')

print("Usuario 1 hash:", hash1)
print("Usuario 2 hash:", hash2)
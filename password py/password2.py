
from werkzeug.security import generate_password_hash, check_password_hash

texto = "x?1_p-H"

texto_encriptado = generate_password_hash(texto)
print("Texto Encriptado:{texto_encriptado}", )

print(f"¿la contraceña es correcta? {check_password_hash(texto_encriptado, texto)}")
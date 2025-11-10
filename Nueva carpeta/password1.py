#.\venv\Scripts\activate
# python app.py


from flask import Flask
from flask_bcrypt import Bcrypt 

app = Flask(__name__)
bcrypt = Bcrypt(app)

password_plano = "mi_contraseña_secreta"
hashed_password = bcrypt.generate_password_hash(password_plano).decode('utf-8') 
print("Contraseña Hasheada:", hashed_password)




#PS C:\Users\Leonel\Desktop\Estructura del proyecto3> .\venv\Scripts\activate
#(venv) PS C:\Users\Leonel\Desktop\Estructura del proyecto3> python app.py

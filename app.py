from flask import Flask, jsonify, request, session
from models import Planet, Character, User, Favorite
import requests
from models import db
from werkzeug.security import generate_password_hash
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from datetime import datetime
from flask_cors import CORS
from flask import flash, redirect, url_for
import logging
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.security import check_password_hash
from flask_session import Session
from flask_jwt_extended import create_access_token
from flask_jwt_extended import JWTManager

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
logging.basicConfig(filename="app.log", level=logging.INFO)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///mydatabase.db"
app.config["SECRET_KEY"] = "123456"  # Mi propia clave secreta

# Configura JWTManager
app.config["JWT_SECRET_KEY"] = "123456"
jwt = JWTManager(app)
migrate = Migrate(app, db)

# Configuro la extensión Flask-Session
app.config[
    "SESSION_TYPE"
] = "filesystem"  # Almacena las sesiones en el sistema de archivos
app.config["SESSION_PERMANENT"] = False  # Las sesiones no son permanentes
Session(app)

db.init_app(app)

# Configuracion Flask-Admin
admin = Admin(app, name="Admin", template_mode="bootstrap3")
admin.add_view(ModelView(User, db.session))


# Creacion de Endpoint GET personajes y Planetas.


# GET para obtener datos personajes desde Api Externa y alimentar mi Base de datos.
@app.route("/external-character", methods=["GET"])
def get_external_character():
    response = requests.get("https://www.swapi.tech/api/people/")
    external_character_data = response.json()

    character_list = external_character_data["results"]
    num_characters_added = 0  # Contador para el número de personajes agregados

    for character_data in character_list:
        character_url = character_data["url"]
        character_uid = character_data["uid"]
        character_response = requests.get(character_url)
        character_details = character_response.json()["result"]["properties"]

        new_character = Character(
            name=character_details["name"],
            id=int(character_uid),
            eye_color=character_details["eye_color"],
            gender=character_details["gender"],
            heigth=int(character_details["height"]),
            weight=int(character_details["mass"]),
        )

        db.session.add(new_character)
        db.session.commit()
        num_characters_added += 1

    message = f"{num_characters_added} characters created from external API source"
    return jsonify({"message": message}), 201


# GET para obtener datos planetas desde Api Externa y alimentar mi Base de datos.
@app.route("/external-planet", methods=["GET"])
def get_external_planet():
    response = requests.get("https://www.swapi.tech/api/planets/")
    external_planet_data = response.json()

    planet_list = external_planet_data["results"]
    num_planets_added = 0  # Contador para el número de planetas agregados

    for planet_data in planet_list:
        planet_url = planet_data["url"]
        planet_uid = planet_data["uid"]
        planet_response = requests.get(planet_url)
        planet_details = planet_response.json()["result"]["properties"]

        population = planet_details["population"]
        if population.lower() == "unknown":
            population_int = None  # Asigno None para indicar un valor desconocido
        else:
            population_int = int(population)

        new_planet = Planet(
            name=planet_details["name"],
            id=int(planet_uid),
            climate=planet_details["climate"],
            terrain=planet_details["terrain"],
            population=population_int,
        )

        db.session.add(new_planet)
        db.session.commit()
        num_planets_added += 1

    message = f"{num_planets_added} planets created from external API source"
    return jsonify({"message": message}), 201


# Método GET para listar todos los personajes, solo Nombre e ID.
@app.route("/characters", methods=["GET"])
def get_all_characters():
    characters = Character.query.all()
    character_list = []
    for character in characters:
        character_data = {
            "id": character.id,
            "name": character.name,
        }
        character_list.append(character_data)
    return jsonify(character_list)


# Método GET para obtener el detalle de un personaje en particular segun id.
@app.route("/character/<int:character_id>", methods=["GET"])
def get_character_details(character_id):
    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"message": "Character id not found"}), 404

    character_details = {
        "id": character.id,
        "name": character.name,
        "eye_color": character.eye_color,
        "gender": character.gender,
        "heigth": character.heigth,
        "weight": character.weight,
    }

    return jsonify(character_details)


# Método GET para listar todos los planetas, solo Nombre e ID.
@app.route("/planets", methods=["GET"])
def get_all_planets():
    planets = Planet.query.all()
    planet_list = []
    for planet in planets:
        planet_data = {
            "id": planet.id,
            "name": planet.name,
        }
        planet_list.append(planet_data)
    return jsonify(planet_list)


# Método GET para listar todos los favoritos de un Usuario mediante relaciones de tabla.
@app.route("/favorite/<int:user_id>", methods=["GET"])
def get_all_favorites(user_id):
    favorites = Favorite.query.filter_by(user_id=user_id).all()
    favorite_list = []
    for favorite in favorites:
        favorite_data = {}

        if favorite.planet:  # Verifico si favorite.planet no es None
            favorite_data["planet"] = {
                "id": favorite.planet.id,
                "name": favorite.planet.name,
            }

        if favorite.character:  # Verifico si favorite.character no es None
            favorite_data["character"] = {
                "id": favorite.character.id,
                "name": favorite.character.name,
            }

        favorite_list.append(favorite_data)
    return jsonify(favorite_list)


# Método GET para obtener el detalle de un planeta en particular segun id.
@app.route("/planet/<int:planet_id>", methods=["GET"])
def get_planet_details(planet_id):
    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet id not found"}), 404

    planet_details = {
        "id": planet.id,
        "name": planet.name,
        "climate": planet.climate,
        "terrain": planet.terrain,
        "population": planet.population,
    }

    return jsonify(planet_details)


# Metodo GET users para Listar todos los usuarios
@app.route("/users", methods=["GET"])
def get_all_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "mail": user.mail,
            "suscription_date": user.suscription_date,
        }
        user_list.append(user_data)
    return jsonify(user_list)


# Metodo Post para anadir un nuevo planeta favorito al usuario actual.
@app.route("/favorite/planet/<int:planet_id>", methods=["POST"])
def add_planet_favorite(planet_id):
    user_id = request.args.get("user_id")
    print("user_id:", user_id)
    if user_id is None:
        return jsonify({"message": "User id missing"}), 400

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User id not found"}), 404

    planet = Planet.query.get(planet_id)
    if planet is None:
        return jsonify({"message": "Planet id not found"}), 404

    new_favorite = Favorite(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Planet added successfully toa Favorite"}), 201


# Metodo Post para anadir un nuevo Character favorito al usuario actual.
@app.route("/favorite/character/<int:character_id>", methods=["POST"])
def add_character_favorite(character_id):
    user_id = request.args.get("user_id")
    print("user_id:", user_id)
    if user_id is None:
        return jsonify({"message": "User id missing"}), 400

    user = User.query.get(user_id)
    if user is None:
        return jsonify({"message": "User id not found"}), 404

    character = Character.query.get(character_id)
    if character is None:
        return jsonify({"message": "Character id not found"}), 404

    new_favorite = Favorite(user_id=user_id, character_id=character_id)
    db.session.add(new_favorite)
    db.session.commit()

    return jsonify({"message": "Character added successfully toa Favorite "}), 201


# Metodo [DELETE] para eliminar planeta de favorito. (ejemplo:..favorite/planet/5?user_id=1)
@app.route("/favorite/planet/<int:planet_id>", methods=["DELETE"])
def delete_planet_favorite(planet_id):
    user_id = request.args.get(
        "user_id"
    )  # Obtengo ID de la cadena URL después del signo ("?").
    if user_id is None:
        return jsonify({"message": "User id missing"}), 400

    favorite = Favorite.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if favorite is None:
        return jsonify({"message": "Favorite not found"}), 404

    planet = Planet.query.get(
        planet_id
    )  # consulta a la base de datos para obtener un registro de la tabla "Planet" utilizando el ID del planeta como criterio de búsqueda.

    if planet is None:
        return jsonify({"message": "Planet id not found"}), 404

    planet_info = {
        "id": planet.id,
        "name": planet.name,
        "climate": planet.climate,
        "terrain": planet.terrain,
        "population": planet.population,
    }
    db.session.delete(favorite)
    db.session.commit()


# Metodo [DELETE] para eliminar Character favorito. (ejemplo:..favorite/character/5?user_id=1)
@app.route("/favorite/character/<int:character_id>", methods=["DELETE"])
def delete_character_favorite(character_id):
    user_id = request.args.get(
        "user_id"
    )  # Obtengo ID de la cadena URL después del signo ("?").
    if user_id is None:
        return jsonify({"message": "User id missing"}), 400

    favorite = Favorite.query.filter_by(
        user_id=user_id, character_id=character_id
    ).first()
    if favorite is None:
        return jsonify({"message": "Favorite not found"}), 404

    character = Character.query.get(
        character_id
    )  # consulta a la base de datos para obtener un registro de la tabla "Planet" utilizando el ID del planeta como criterio de búsqueda.

    if character is None:
        return jsonify({"message": "Character id not found"}), 404

    character_info = {
        "id": character.id,
        "name": character.name,
        "eye_color": character.eye_color,
        "gender": character.gender,
        "heigth": character.heigth,
        "weight": character.weight,
    }
    db.session.delete(favorite)
    db.session.commit()

    return (
        jsonify(
            {
                "message": f"The following Character: {character_info} was removed from favorites"
            }
        ),
        200,
    )


@app.route("/signup", methods=["POST"])
def signup():
    try:
        data = request.get_json()
        if not data or "mail" not in data or "password" not in data:
            return jsonify({"message": "Datos JSON inválidos"}), 400

        mail = data["mail"]
        password = data["password"]

        # Verifico si el correo ya existe en la base de datos
        existing_mail = User.query.filter_by(mail=mail).first()

        if existing_mail:
            return jsonify({"message": "El correo electrónico ya está registrado"}), 400

        # Uso el correo electrónico como nombre de usuario
        username = mail

        # Creo un nuevo usuario y almaceno la contraseña en formato hash
        new_user = User(
            mail=mail,
            username=username,
        )
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Usuario creado con éxito"}), 201
    except Exception as e:
        # Manejo de errores de la base de datos u otros errores
        db.session.rollback()
        return (
            jsonify({"message": str(e)}),
            500,
        )  # Devuelvo un código de error 500 en caso de fallo


@app.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        mail = data.get("mail")
        password = data.get("password")

        if not mail or not password:
            return (
                jsonify(
                    {
                        "success": False,
                        "message": "Correo electrónico y contraseña son requeridos.",
                    }
                ),
                400,
            )

        # Compruebo si el usuario existe
        user = User.query.filter_by(mail=mail).first()
        if not user or not check_password_hash(user.password_hash, password):
            return (
                jsonify({"success": False, "message": "Credenciales inválidas."}),
                401,
            )

        # Genero un token JWT para el usuario autenticado
        access_token = create_access_token(identity=str(user.id))

        # Devuelvo el token JWT en la respuesta
        return jsonify({"success": True, "access_token": True}), 200
    except Exception as e:
        # Manejo de errores de la base de datos u otros errores
        return (
            jsonify({"success": False, "message": str(e)}),
            500,
        )  # Devuelv0 un código de error 500 en caso de fallo


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
    with app.app_context():
        db.drop_all()
        db.create_all()
        app.run(debug=True)



from sqlite3 import IntegrityError
from flask import jsonify, request, current_app

from app.models.vaccine_model import VaccineModel


def create_vaccine():
    data = request.json()
    try:
        for value in list(data.values()):
            if type (value) != str:
                raise TypeError
        if len(data["cpf"]) != 11:
            raise ValueError

        formatData = {
        "name": data["name"].title(), 
        "cpf": data["cpf"],
        "vaccine_name": data["vaccine_name"].title(),
        "health_unit_name": data["health_unit_name"].title()
        }
        new_vaccine = VaccineModel(**formatData)
        current_app.db.session.add(new_vaccine)
        current_app.db.session.commit()

        return jsonify(new_vaccine), 201

    except TypeError:
      return jsonify(erro= "os valores devem ser strings"), 400
    except IntegrityError:
      return jsonify(erro= "cpf em uso"), 409
    except ValueError: 
      return jsonify(erro= "cpf deve conter 11 caracteres"), 400
    except KeyError:
      return {
               "erro": "chaves incorretas",
               "recebidas": list(data.keys()),
               "permitidas": [
               "name",
               "cpf",
               "vaccine_name",
               "health_unit_name"
               ]           
            }, 400

def get_vaccine():
    vaccine = (VaccineModel.query.all())

    return jsonify(vaccine), 200


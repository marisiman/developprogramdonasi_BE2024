from flask import Blueprint, jsonify, json, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.donatur import Donatur
from app.models.user import User
from app.utils.db import db
from app.utils.api_response import api_response
from app.service.donatur_service import Donatur_service
from app.controllers.donatur.schema.update_donatur_request import Update_donatur_request
from app.controllers.donatur.schema.create_donatur_request import Create_donatur_request
from pydantic import ValidationError

donatur_blueprint = Blueprint('donatur_endpoint', __name__)

@donatur_blueprint.route('/', methods=['POST'])
@jwt_required() 
def create_donatur():
    try: 
    # Menerima data JSON yang dikirim oleh klien
        data = request.json

        # Pastikan data yang diperlukan tersedia
        if 'nama' not in data or 'alamat' not in data or 'nomor_telepon' not in data:
            return api_response(
                status_code=400,
                message="Data kurang lengkap",
                data={  "contoh inputan ":
                        {
                            "nama": "Iman family",
                            "alamat": "Jl. Raya Pasar Minggu No. 19, Pejaten Barat, Pasar Minggu, Jakarta Selatan 12510",
                            "nomor_telepon": "(021) 79194075"
                        }                      
                }
            )  
        
                # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()
        
        create_donatur_request = Create_donatur_request(**data)

        donatur_service = Donatur_service()

        donaturs = donatur_service.create_donatur(create_donatur_request, user.id)

        return api_response(
            status_code=201,
            message="success input data",
            data=donaturs
        )
    
    except ValidationError as e:
        return api_response(
            status_code=400,
            message=e.errors(),
            data={  "contoh inputan ":
                    {
                        "nama": "Iman family",
                        "alamat": "Jl. Raya Pasar Minggu No. 19, Pejaten Barat, Pasar Minggu, Jakarta Selatan 12510",
                        "nomor_telepon": "(021) 79194075"
                }                               
            }
        )
    except Exception as e:
        # Tangani kesalahan server jika ada
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )       


@donatur_blueprint.route('/list_identitasku', methods=['GET'])
@jwt_required()  # Membutuhkan token JWT untuk akses
def get_donaturku():
    try:

        # Mendapatkan identitas pengguna yang saat ini login dari token JWT
        current_user_id = get_jwt_identity()

        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()

        # Memastikan pengguna ditemukan
        if not user:
            return api_response(
                status_code=404,
                message="User not found",
                data={}
            )

        # Mendapatkan data donatur yang terkait dengan user
        donaturs = Donatur.query.filter_by(user_id=current_user_id).all()

        donaturs_data = [{
            'donatur_id': donatur.donatur_id,
            'nama': donatur.nama,
            'alamat': donatur.alamat,
            'user_id': donatur.user_id,
            'created_at': donatur.created_at,
            'updated_at': donatur.updated_at
        } for donatur in donaturs]

        return api_response(
            status_code=200,
            message="Daftar identitas donatur anda sukses diakses",
            data=donaturs_data
        )  
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )       


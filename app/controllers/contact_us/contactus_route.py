
from flask import Blueprint, jsonify, request
from sqlalchemy.sql import func
from app.models.donasi import Donasi
from app.models.contact_us import Contact_us
from app.models.program import Program
from app.models.user import User
from app.utils.db import db
from app.service.donasi_service import Donasi_service
from app.utils.api_response import api_response
from flask_jwt_extended import jwt_required, get_jwt_identity

contactus_blueprint = Blueprint('contactus_endpoint', __name__)

@contactus_blueprint.route('/', methods=['POST'])
@jwt_required()
def create_message():
    try:
        data = request.get_json()
        
        # Pastikan data yang diperlukan ada
        required_fields = ['first_name', 'last_name', 'email', 'message']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'{field} harus disertakan'}), 400

        # Mendapatkan identitas pengguna dari token JWT
        current_user_id = get_jwt_identity()
        
        # Querying untuk mendapatkan data pengguna yang saat ini login
        user = User.query.filter_by(id=current_user_id).first()
        # Pastikan pengguna ditemukan
        if not user:
            return jsonify({'message': 'Pengguna tidak ditemukan'}), 404

        # Membuat objek DTO untuk pesan kontak
        contact_data_dto = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': user.email,
            'message': data['message']
        }

        # Simpan pesan kontak ke dalam database
        contact_message = Contact_us(**contact_data_dto, user_id=current_user_id)
        db.session.add(contact_message)
        db.session.commit()

        # Mengonversi objek Contact_us menjadi kamus (dictionary) yang dapat diserialisasi
        contact_message_dict = {
            'id': contact_message.id,
            'user_id': contact_message.user_id,
            'first_name': contact_message.first_name,
            'last_name': contact_message.last_name,
            'email': contact_message.email,
            'message': contact_message.message,
            'created_at': contact_message.created_at
        }

        return api_response(
            status_code=201,
            message="Pesan kontak berhasil dikirim.",
            data=contact_message_dict
        )
    
    except Exception as e:
        # Tangani kesalahan server jika ada
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )

@contactus_blueprint.route('/list_messages', methods=['GET'])
@jwt_required()  # Membutuhkan token JWT untuk akses
def get_my_messsage():
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
        contactus = Contact_us.query.filter_by(user_id=current_user_id).all()

        contactus_data = [{
            'id': contact.id,
            'user_id': contact.user_id,
            'first_name': contact.first_name,
            'last_name': contact.last_name,
            'email': contact.email,
            'message': contact.message,
            'created_at': contact.created_at
            
        } for contact in contactus]

        return api_response(
            status_code=200,
            message="List pesan yang anda buat sukses diakses",
            data=contactus_data
        )  
    except Exception as e:
        return api_response(
            status_code=500,
            message=str(e),
            data={}
        )       

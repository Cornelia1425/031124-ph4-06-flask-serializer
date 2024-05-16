from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

#SerializerMixin does to_dict
class Doctor(db.Model, SerializerMixin):
    
    __tablename__ = 'doctors_table'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    specialty = db.Column(db.String)

    appointments = db.relationship('Appointment', back_populates = 'doctor')
    patients = association_proxy('appointments', 'patient')

    serialize_rules = ['-appointments','patients','-patients.doctors']
    # serialize_rules = ['-appointments.doctors','-patients']
 
    #converts the class instance to an object, so readable to json
    # def to_dict(self):
    #     return{

    #     }



#plug in, inherit, can do multiple parents
class Patient(db.Model, SerializerMixin):
    
    __tablename__ = 'patients_table'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    appointments = db.relationship('Appointment', back_populates = 'patient')
    doctors = association_proxy('Appointments', 'doctor')

    serialize_rules = ['-appointments','doctors','-doctors.patients']
    # serialize_rules = ['-appointments.patients','-doctors']


class Appointment(db.Model, SerializerMixin):
    
    __tablename__ = 'appointments_table'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String)

    patient_id = db.Column(db.Integer, db.ForeignKey('patients_table.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors_table.id'))

    patient = db.relationship('Patient', back_populates='appointments')
    doctor = db.relationship('Doctor', back_populates='appointments')

    serialize_rules = ['-doctor.appointments', '-patient.appointments']
# using resolved_model gpt-4o-2024-08-06# created from response, to create create_db_models.sqlite, with test data
#    that is used to create project
# should run without error in manager 
#    if not, check for decimal, indent, or import issues

import decimal
import logging
import sqlalchemy
from sqlalchemy.sql import func 
from logic_bank.logic_bank import Rule
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, Date, DateTime, Numeric, Boolean, Text, DECIMAL
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from datetime import date   
from datetime import datetime


logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

Base = declarative_base()  # from system/genai/create_db_models_inserts/create_db_models_prefix.py

from sqlalchemy.dialects.sqlite import *


class Shop(Base):
    """description: Table to store auto service shop information."""
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    location = Column(String)
    contact_number = Column(String)


class Customer(Base):
    """description: Table for storing customer details."""
    __tablename__ = 'customers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)


class Vehicle(Base):
    """description: Table for managing vehicle details for customers."""
    __tablename__ = 'vehicles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    vin_number = Column(String, nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)


class Service(Base):
    """description: Table to catalog different service types available."""
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)


class Appointment(Base):
    """description: Table for booking customer appointments for service."""
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customers.id'), nullable=False)
    vehicle_id = Column(Integer, ForeignKey('vehicles.id'), nullable=False)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)


class Invoice(Base):
    """description: Table to record the invoicing details."""
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'), nullable=False)
    invoice_date = Column(DateTime, nullable=False)
    total_amount = Column(Integer, nullable=False)


class Payment(Base):
    """description: Table to manage customer payments for invoices."""
    __tablename__ = 'payments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    amount_paid = Column(Integer, nullable=False)


class Employee(Base):
    """description: Table for storing employee details."""
    __tablename__ = 'employees'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String)
    hire_date = Column(Date, nullable=False)
    shop_id = Column(Integer, ForeignKey('shops.id'), nullable=False)


class Part(Base):
    """description: Table to inventory the car parts in stock."""
    __tablename__ = 'parts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    inventory_count = Column(Integer, nullable=False)
    cost_price = Column(Integer, nullable=False)


class ServiceAssignment(Base):
    """description: Table linking employees to specific appointments."""
    __tablename__ = 'service_assignments'

    id = Column(Integer, primary_key=True, autoincrement=True)
    appointment_id = Column(Integer, ForeignKey('appointments.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)


class PartAllocation(Base):
    """description: Table tracking which parts are used for service orders."""
    __tablename__ = 'part_allocations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    part_id = Column(Integer, ForeignKey('parts.id'), nullable=False)
    appointment_id = Column(Integer, ForeignKey('appointments.id'), nullable=False)
    quantity_used = Column(Integer, nullable=False)


# end of model classes


try:
    
    
    
    
    # ALS/GenAI: Create an SQLite database
    
    engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
    
    Base.metadata.create_all(engine)
    
    
    
    Session = sessionmaker(bind=engine)
    
    session = Session()
    
    
    
    # ALS/GenAI: Prepare for sample data
    
    
    
    session.commit()
    shop1 = Shop(name="AutoCare Plus", location="123 Main St, Springfield", contact_number="555-0199")
    shop2 = Shop(name="QuickFix Garage", location="456 Elm St, Shelbyville", contact_number="555-0123")
    shop3 = Shop(name="SuperMechanics", location="789 Oak St, Ogdenville", contact_number="555-0456")
    shop4 = Shop(name="Piston's Auto", location="321 Maple Ave, North Haverbrook", contact_number="555-0789")
    customer1 = Customer(first_name="John", last_name="Doe", email="john.doe@example.com", phone="123-456")
    customer2 = Customer(first_name="Jane", last_name="Smith", email="jane.smith@example.com", phone="234-567")
    customer3 = Customer(first_name="Jim", last_name="Beam", email="jim.beam@example.com", phone="345-678")
    customer4 = Customer(first_name="Jill", last_name="Valentine", email="jill.valentine@example.com", phone="456-789")
    vehicle1 = Vehicle(customer_id=customer1.id, vin_number="1HGCM82633A004352", make="Honda", model="Accord", year=2020)
    vehicle2 = Vehicle(customer_id=customer2.id, vin_number="1N4AL3AP5FC123456", make="Nissan", model="Altima", year=2019)
    vehicle3 = Vehicle(customer_id=customer3.id, vin_number="4T1BF1FK5GU678910", make="Toyota", model="Camry", year=2018)
    vehicle4 = Vehicle(customer_id=customer4.id, vin_number="3FA6P0HR1KR789012", make="Ford", model="Fusion", year=2021)
    service1 = Service(name="Oil Change", description="Change engine oil and filter", price=60)
    service2 = Service(name="Tire Rotation", description="Rotate all four tires", price=40)
    service3 = Service(name="Brake Inspection", description="Inspect and replace brake pads as needed", price=100)
    service4 = Service(name="Battery Check", description="Check battery health and charge", price=30)
    appointment1 = Appointment(customer_id=customer1.id, vehicle_id=vehicle1.id, shop_id=shop1.id, service_id=service1.id, appointment_date=datetime(2023, 1, 15, 10, 30), status="Completed")
    appointment2 = Appointment(customer_id=customer2.id, vehicle_id=vehicle2.id, shop_id=shop2.id, service_id=service2.id, appointment_date=datetime(2023, 2, 12, 11, 00), status="Pending")
    appointment3 = Appointment(customer_id=customer3.id, vehicle_id=vehicle3.id, shop_id=shop3.id, service_id=service3.id, appointment_date=datetime(2023, 3, 10, 9, 00), status="Canceled")
    appointment4 = Appointment(customer_id=customer4.id, vehicle_id=vehicle4.id, shop_id=shop4.id, service_id=service4.id, appointment_date=datetime(2023, 4, 18, 14, 00), status="Scheduled")
    invoice1 = Invoice(appointment_id=appointment1.id, invoice_date=datetime(2023, 1, 16), total_amount=60)
    invoice2 = Invoice(appointment_id=appointment2.id, invoice_date=datetime(2023, 2, 13), total_amount=40)
    invoice3 = Invoice(appointment_id=appointment3.id, invoice_date=datetime(2023, 3, 11), total_amount=0)
    invoice4 = Invoice(appointment_id=appointment4.id, invoice_date=datetime(2023, 4, 19), total_amount=30)
    payment1 = Payment(invoice_id=invoice1.id, payment_date=datetime(2023, 1, 17), amount_paid=60)
    payment2 = Payment(invoice_id=invoice2.id, payment_date=datetime(2023, 2, 14), amount_paid=40)
    payment3 = Payment(invoice_id=invoice3.id, payment_date=None, amount_paid=0)
    payment4 = Payment(invoice_id=invoice4.id, payment_date=None, amount_paid=0)
    employee1 = Employee(first_name="Mike", last_name="Johnson", position="Mechanic", hire_date=date(2022, 5, 10), shop_id=shop1.id)
    employee2 = Employee(first_name="Sarah", last_name="Connor", position="Manager", hire_date=date(2021, 8, 15), shop_id=shop2.id)
    employee3 = Employee(first_name="Lee", last_name="Van", position="Technician", hire_date=date(2023, 1, 20), shop_id=shop3.id)
    employee4 = Employee(first_name="Anna", last_name="Taylor", position="Receptionist", hire_date=date(2022, 12, 3), shop_id=shop4.id)
    part1 = Part(name="Oil Filter", inventory_count=200, cost_price=5)
    part2 = Part(name="Brake Pads", inventory_count=150, cost_price=50)
    part3 = Part(name="Battery", inventory_count=50, cost_price=70)
    part4 = Part(name="Windshield Wipers", inventory_count=100, cost_price=10)
    service_assignment1 = ServiceAssignment(appointment_id=appointment1.id, employee_id=employee1.id)
    service_assignment2 = ServiceAssignment(appointment_id=appointment2.id, employee_id=employee2.id)
    service_assignment3 = ServiceAssignment(appointment_id=appointment3.id, employee_id=employee3.id)
    service_assignment4 = ServiceAssignment(appointment_id=appointment4.id, employee_id=employee4.id)
    part_allocation1 = PartAllocation(part_id=part1.id, appointment_id=appointment1.id, quantity_used=1)
    part_allocation2 = PartAllocation(part_id=part2.id, appointment_id=appointment2.id, quantity_used=0)
    part_allocation3 = PartAllocation(part_id=part3.id, appointment_id=appointment3.id, quantity_used=0)
    part_allocation4 = PartAllocation(part_id=part4.id, appointment_id=appointment4.id, quantity_used=2)
    
    
    
    session.add_all([shop1, shop2, shop3, shop4, customer1, customer2, customer3, customer4, vehicle1, vehicle2, vehicle3, vehicle4, service1, service2, service3, service4, appointment1, appointment2, appointment3, appointment4, invoice1, invoice2, invoice3, invoice4, payment1, payment2, payment3, payment4, employee1, employee2, employee3, employee4, part1, part2, part3, part4, service_assignment1, service_assignment2, service_assignment3, service_assignment4, part_allocation1, part_allocation2, part_allocation3, part_allocation4])
    session.commit()
    # end of test data
    
    
except Exception as exc:
    print(f'Test Data Error: {exc}')

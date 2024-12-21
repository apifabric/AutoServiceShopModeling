# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  December 21, 2024 14:19:50
# Database: sqlite:////tmp/tmp.aE02SnKDno-01JFMSBF6BQVB960JY2A4KV602/AutoServiceShopModeling/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Customer(SAFRSBaseX, Base):
    """
    description: Table for storing customer details.
    """
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String)
    phone = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    VehicleList : Mapped[List["Vehicle"]] = relationship(back_populates="customer")
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="customer")



class Part(SAFRSBaseX, Base):
    """
    description: Table to inventory the car parts in stock.
    """
    __tablename__ = 'parts'
    _s_collection_name = 'Part'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    inventory_count = Column(Integer, nullable=False)
    cost_price = Column(Integer, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    PartAllocationList : Mapped[List["PartAllocation"]] = relationship(back_populates="part")



class Service(SAFRSBaseX, Base):
    """
    description: Table to catalog different service types available.
    """
    __tablename__ = 'services'
    _s_collection_name = 'Service'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Integer, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="service")



class Shop(SAFRSBaseX, Base):
    """
    description: Table to store auto service shop information.
    """
    __tablename__ = 'shops'
    _s_collection_name = 'Shop'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    contact_number = Column(String)

    # parent relationships (access parent)

    # child relationships (access children)
    EmployeeList : Mapped[List["Employee"]] = relationship(back_populates="shop")
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="shop")



class Employee(SAFRSBaseX, Base):
    """
    description: Table for storing employee details.
    """
    __tablename__ = 'employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    position = Column(String)
    hire_date = Column(Date, nullable=False)
    shop_id = Column(ForeignKey('shops.id'), nullable=False)

    # parent relationships (access parent)
    shop : Mapped["Shop"] = relationship(back_populates=("EmployeeList"))

    # child relationships (access children)
    ServiceAssignmentList : Mapped[List["ServiceAssignment"]] = relationship(back_populates="employee")



class Vehicle(SAFRSBaseX, Base):
    """
    description: Table for managing vehicle details for customers.
    """
    __tablename__ = 'vehicles'
    _s_collection_name = 'Vehicle'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    vin_number = Column(String, nullable=False)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("VehicleList"))

    # child relationships (access children)
    AppointmentList : Mapped[List["Appointment"]] = relationship(back_populates="vehicle")



class Appointment(SAFRSBaseX, Base):
    """
    description: Table for booking customer appointments for service.
    """
    __tablename__ = 'appointments'
    _s_collection_name = 'Appointment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customers.id'), nullable=False)
    vehicle_id = Column(ForeignKey('vehicles.id'), nullable=False)
    shop_id = Column(ForeignKey('shops.id'), nullable=False)
    service_id = Column(ForeignKey('services.id'), nullable=False)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("AppointmentList"))
    service : Mapped["Service"] = relationship(back_populates=("AppointmentList"))
    shop : Mapped["Shop"] = relationship(back_populates=("AppointmentList"))
    vehicle : Mapped["Vehicle"] = relationship(back_populates=("AppointmentList"))

    # child relationships (access children)
    InvoiceList : Mapped[List["Invoice"]] = relationship(back_populates="appointment")
    PartAllocationList : Mapped[List["PartAllocation"]] = relationship(back_populates="appointment")
    ServiceAssignmentList : Mapped[List["ServiceAssignment"]] = relationship(back_populates="appointment")



class Invoice(SAFRSBaseX, Base):
    """
    description: Table to record the invoicing details.
    """
    __tablename__ = 'invoices'
    _s_collection_name = 'Invoice'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    appointment_id = Column(ForeignKey('appointments.id'), nullable=False)
    invoice_date = Column(DateTime, nullable=False)
    total_amount = Column(Integer, nullable=False)

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("InvoiceList"))

    # child relationships (access children)
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="invoice")



class PartAllocation(SAFRSBaseX, Base):
    """
    description: Table tracking which parts are used for service orders.
    """
    __tablename__ = 'part_allocations'
    _s_collection_name = 'PartAllocation'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    part_id = Column(ForeignKey('parts.id'), nullable=False)
    appointment_id = Column(ForeignKey('appointments.id'), nullable=False)
    quantity_used = Column(Integer, nullable=False)

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("PartAllocationList"))
    part : Mapped["Part"] = relationship(back_populates=("PartAllocationList"))

    # child relationships (access children)



class ServiceAssignment(SAFRSBaseX, Base):
    """
    description: Table linking employees to specific appointments.
    """
    __tablename__ = 'service_assignments'
    _s_collection_name = 'ServiceAssignment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    appointment_id = Column(ForeignKey('appointments.id'), nullable=False)
    employee_id = Column(ForeignKey('employees.id'), nullable=False)

    # parent relationships (access parent)
    appointment : Mapped["Appointment"] = relationship(back_populates=("ServiceAssignmentList"))
    employee : Mapped["Employee"] = relationship(back_populates=("ServiceAssignmentList"))

    # child relationships (access children)



class Payment(SAFRSBaseX, Base):
    """
    description: Table to manage customer payments for invoices.
    """
    __tablename__ = 'payments'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(ForeignKey('invoices.id'), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    amount_paid = Column(Integer, nullable=False)

    # parent relationships (access parent)
    invoice : Mapped["Invoice"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)

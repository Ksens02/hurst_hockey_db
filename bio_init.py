# this file initializes the bio table in the hockey databse.
from sqlmodel import Session
from models import engine 
from bio_instances import generate_bio_instances

with Session(engine) as session:
    bios = generate_bio_instances()
    session.add_all(bios)
    session.commit()


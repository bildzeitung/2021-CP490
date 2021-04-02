import uuid
from datetime import datetime

from sqlalchemy import Column, DateTime, String
from sqlalchemy_utils import UUIDType


class AttributeMixin:
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    title = Column(String(64), index=True)
    value = Column(String(2048))
    timestamp = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

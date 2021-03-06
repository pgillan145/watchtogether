from sqlalchemy import Table, Column, Integer, String, ForeignKey, Text, DateTime, Boolean, LargeBinary, Float
from sqlalchemy_utils.types.password import PasswordType
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship, backref, foreign

from watchtogether.util import random_string
from . import Base
from datetime import datetime

def generate_id():
    return random_string(10)

class WatchtogetherBase(object):
    id = Column(String(10), primary_key=True, default=generate_id)

    creation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    title = Column(Text, nullable=False)
    owner = Column(String(15), nullable = False)
    poster = Column(LargeBinary)

class Subtitle(Base):
    __tablename__ = 'subtitle'

    id = Column(Integer, primary_key=True)
    video_id = Column(String(10), ForeignKey('video.id'), nullable=False)

    language = Column(String(5), nullable=False, default='eng')
    title = Column(Text)

    internal = Column(Boolean, default=False)
    internal_streamidx = Column(Integer)
    internal_include = Column(Boolean, default=False)

    orig_file = Column(Text)    

class EncodedFile(Base):
    __tablename__ = 'encoded_file'

    id = Column(Integer, primary_key=True)
    video_id = Column(String(10), ForeignKey('video.id'), nullable=False)
    
    language = Column(String(5), nullable=False, default='eng')
    track_type = Column(String(10), nullable=False)
    encoding_hash = Column(String(64), nullable=False)
    encoded_file_name = Column(Text, nullable=False)

class Video(WatchtogetherBase, Base):
    __tablename__ = 'video'
    
    encoding_progress = Column(Float, default=0)
    encoding_speed = Column(Float, default=0)
    status = Column(String(15), default='file-waiting')
    status_message = Column(Text)

    width = Column(Integer, nullable=False, default=0)
    height = Column(Integer, nullable=False, default=0)
    duration = Column(Float, nullable=False, default=0)

    upload_identifier = Column(Text)

    tune = Column(String(15), nullable=False, default='film')
    default_subtitles = Column(Boolean, default=False)
    version = Column(Integer, nullable=False, default=0)
    orig_file = Column(Text)
    orig_file_name = Column(Text)
    playlist = Column(Text)

    celery_taskid = Column(Text)

    subtitles = relationship('Subtitle', backref='Video', lazy=True)
    encoded_files = relationship('EncodedFile', backref='Video', lazy=True)

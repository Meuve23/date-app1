from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Date, JSON, Float, Enum
from sqlalchemy.orm import relationship
from ..database import Base
from ..schemas.user import PersonalityTrait

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    date_of_birth = Column(Date)
    gender = Column(String)
    looking_for = Column(String)
    bio = Column(String, nullable=True)
    interests = Column(JSON, nullable=True)
    personality_traits = Column(JSON, nullable=True)  # List of PersonalityTrait
    location = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    profile_picture = Column(String, nullable=True)
    min_age_preference = Column(Integer, nullable=True)
    max_age_preference = Column(Integer, nullable=True)
    max_distance = Column(Integer, nullable=True)  # in kilometers
    relationship_goals = Column(String, nullable=True)
    languages = Column(JSON, nullable=True)  # List of languages
    height = Column(Integer, nullable=True)  # in cm
    zodiac_sign = Column(String, nullable=True)
    education = Column(String, nullable=True)
    occupation = Column(String, nullable=True)
    smoking = Column(String, nullable=True)
    drinking = Column(String, nullable=True)
    has_children = Column(Boolean, nullable=True)
    wants_children = Column(Boolean, nullable=True)
    is_active = Column(Boolean, default=True)
    last_active = Column(Date, nullable=True)
    compatibility_score = Column(Float, nullable=True)

    # Relationships
    sent_messages = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    received_messages = relationship("Message", back_populates="receiver", foreign_keys="Message.receiver_id")
    sent_likes = relationship("Like", back_populates="liker", foreign_keys="Like.liker_id")
    received_likes = relationship("Like", back_populates="liked", foreign_keys="Like.liked_id")
    compatibility_reports = relationship("CompatibilityReport", back_populates="user", foreign_keys="CompatibilityReport.user_id")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    sender_id = Column(Integer, ForeignKey("users.id"))
    receiver_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(Date)
    is_read = Column(Boolean, default=False)

    sender = relationship("User", back_populates="sent_messages", foreign_keys=[sender_id])
    receiver = relationship("User", back_populates="received_messages", foreign_keys=[receiver_id])

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    liker_id = Column(Integer, ForeignKey("users.id"))
    liked_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(Date)

    liker = relationship("User", back_populates="sent_likes", foreign_keys=[liker_id])
    liked = relationship("User", back_populates="received_likes", foreign_keys=[liked_id])

class CompatibilityReport(Base):
    __tablename__ = "compatibility_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    target_id = Column(Integer, ForeignKey("users.id"))
    compatibility_score = Column(Float)
    common_interests = Column(JSON)  # List of common interests
    personality_match = Column(JSON)  # Dict of personality trait matches
    potential_issues = Column(JSON)  # List of potential issues
    timestamp = Column(Date)

    user = relationship("User", back_populates="compatibility_reports", foreign_keys=[user_id]) 
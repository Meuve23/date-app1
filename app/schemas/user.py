from pydantic import BaseModel, EmailStr, conint, confloat
from typing import Optional, List, Dict
from datetime import date
from enum import Enum

class PersonalityTrait(str, Enum):
    INTROVERT = "introvert"
    EXTROVERT = "extrovert"
    ADVENTUROUS = "adventurous"
    CAUTIOUS = "cautious"
    SPONTANEOUS = "spontaneous"
    PLANNED = "planned"
    ANALYTICAL = "analytical"
    CREATIVE = "creative"
    TRADITIONAL = "traditional"
    MODERN = "modern"

class UserBase(BaseModel):
    email: EmailStr
    username: str
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    looking_for: str

class UserCreate(UserBase):
    password: str

class UserProfile(BaseModel):
    bio: Optional[str] = None
    interests: Optional[List[str]] = None
    personality_traits: Optional[List[PersonalityTrait]] = None
    location: Optional[str] = None
    profile_picture: Optional[str] = None
    min_age_preference: Optional[conint(ge=18, le=100)] = None
    max_age_preference: Optional[conint(ge=18, le=100)] = None
    max_distance: Optional[conint(ge=1, le=1000)] = None  # in kilometers
    relationship_goals: Optional[str] = None  # casual, serious, friendship, etc.
    languages: Optional[List[str]] = None
    height: Optional[conint(ge=100, le=250)] = None  # in cm
    zodiac_sign: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    smoking: Optional[str] = None  # never, sometimes, regularly
    drinking: Optional[str] = None  # never, sometimes, regularly
    has_children: Optional[bool] = None
    wants_children: Optional[bool] = None

class UserUpdate(UserProfile):
    pass

class User(UserBase):
    id: int
    is_active: bool
    bio: Optional[str] = None
    interests: Optional[List[str]] = None
    personality_traits: Optional[List[PersonalityTrait]] = None
    location: Optional[str] = None
    profile_picture: Optional[str] = None
    min_age_preference: Optional[int] = None
    max_age_preference: Optional[int] = None
    max_distance: Optional[int] = None
    relationship_goals: Optional[str] = None
    languages: Optional[List[str]] = None
    height: Optional[int] = None
    zodiac_sign: Optional[str] = None
    education: Optional[str] = None
    occupation: Optional[str] = None
    smoking: Optional[str] = None
    drinking: Optional[str] = None
    has_children: Optional[bool] = None
    wants_children: Optional[bool] = None
    compatibility_score: Optional[confloat(ge=0, le=100)] = None

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class MessageBase(BaseModel):
    content: str

class MessageCreate(MessageBase):
    receiver_id: int

class Message(MessageBase):
    id: int
    sender_id: int
    receiver_id: int
    timestamp: date
    is_read: bool = False

    class Config:
        from_attributes = True

class LikeCreate(BaseModel):
    liked_id: int

class Like(BaseModel):
    id: int
    liker_id: int
    liked_id: int
    timestamp: date

    class Config:
        from_attributes = True

class MatchResponse(BaseModel):
    match: bool
    user: Optional[User] = None
    compatibility_score: Optional[float] = None

class CompatibilityResponse(BaseModel):
    user_id: int
    compatibility_score: float
    common_interests: List[str]
    personality_match: Dict[str, float]
    potential_issues: List[str] 
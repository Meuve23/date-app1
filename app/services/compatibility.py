from typing import List, Dict, Tuple
from datetime import datetime
from sqlalchemy.orm import Session
from ..models.user import User, CompatibilityReport
from ..schemas.user import PersonalityTrait

class CompatibilityService:
    @staticmethod
    def calculate_compatibility(user1: User, user2: User) -> Tuple[float, List[str], Dict[str, float], List[str]]:
        """
        Calculate compatibility score between two users based on various factors.
        Returns: (compatibility_score, common_interests, personality_match, potential_issues)
        """
        score = 0.0
        common_interests = []
        personality_match = {}
        potential_issues = []
        
        # Calculate interest compatibility (30% of total score)
        if user1.interests and user2.interests:
            common_interests = list(set(user1.interests) & set(user2.interests))
            interest_score = len(common_interests) / max(len(user1.interests), len(user2.interests))
            score += interest_score * 30
        
        # Calculate personality compatibility (25% of total score)
        if user1.personality_traits and user2.personality_traits:
            for trait in user1.personality_traits:
                if trait in user2.personality_traits:
                    personality_match[trait] = 1.0
                else:
                    # Some traits are complementary
                    complementary_traits = {
                        PersonalityTrait.INTROVERT: PersonalityTrait.EXTROVERT,
                        PersonalityTrait.EXTROVERT: PersonalityTrait.INTROVERT,
                        PersonalityTrait.ADVENTUROUS: PersonalityTrait.CAUTIOUS,
                        PersonalityTrait.CAUTIOUS: PersonalityTrait.ADVENTUROUS,
                        PersonalityTrait.SPONTANEOUS: PersonalityTrait.PLANNED,
                        PersonalityTrait.PLANNED: PersonalityTrait.SPONTANEOUS,
                        PersonalityTrait.ANALYTICAL: PersonalityTrait.CREATIVE,
                        PersonalityTrait.CREATIVE: PersonalityTrait.ANALYTICAL,
                        PersonalityTrait.TRADITIONAL: PersonalityTrait.MODERN,
                        PersonalityTrait.MODERN: PersonalityTrait.TRADITIONAL
                    }
                    if trait in complementary_traits and complementary_traits[trait] in user2.personality_traits:
                        personality_match[trait] = 0.8  # Complementary traits get a high score
                    else:
                        personality_match[trait] = 0.3  # Different traits get a lower score
            
            personality_score = sum(personality_match.values()) / len(user1.personality_traits)
            score += personality_score * 25
        
        # Check relationship goals compatibility (15% of total score)
        if user1.relationship_goals and user2.relationship_goals:
            if user1.relationship_goals == user2.relationship_goals:
                score += 15
            elif (user1.relationship_goals == "casual" and user2.relationship_goals == "friendship") or \
                 (user1.relationship_goals == "friendship" and user2.relationship_goals == "casual"):
                score += 10
            else:
                potential_issues.append("Different relationship goals")
        
        # Check children compatibility (10% of total score)
        if user1.wants_children is not None and user2.wants_children is not None:
            if user1.wants_children == user2.wants_children:
                score += 10
            else:
                potential_issues.append("Different views on having children")
        
        # Check lifestyle compatibility (10% of total score)
        lifestyle_score = 0
        if user1.smoking and user2.smoking:
            if user1.smoking == user2.smoking:
                lifestyle_score += 3
            elif (user1.smoking == "never" and user2.smoking == "sometimes") or \
                 (user1.smoking == "sometimes" and user2.smoking == "never"):
                lifestyle_score += 1
            else:
                potential_issues.append("Different smoking habits")
        
        if user1.drinking and user2.drinking:
            if user1.drinking == user2.drinking:
                lifestyle_score += 3
            elif (user1.drinking == "never" and user2.drinking == "sometimes") or \
                 (user1.drinking == "sometimes" and user2.drinking == "never"):
                lifestyle_score += 1
            else:
                potential_issues.append("Different drinking habits")
        
        if user1.education and user2.education:
            if user1.education == user2.education:
                lifestyle_score += 4
            else:
                potential_issues.append("Different education levels")
        
        score += lifestyle_score
        
        # Check language compatibility (10% of total score)
        if user1.languages and user2.languages:
            common_languages = list(set(user1.languages) & set(user2.languages))
            if common_languages:
                score += 10
            else:
                potential_issues.append("No common languages")
        
        return score, common_interests, personality_match, potential_issues
    
    @staticmethod
    def create_compatibility_report(db: Session, user_id: int, target_id: int) -> CompatibilityReport:
        """Create a compatibility report between two users"""
        user = db.query(User).filter(User.id == user_id).first()
        target = db.query(User).filter(User.id == target_id).first()
        
        if not user or not target:
            return None
        
        score, common_interests, personality_match, potential_issues = CompatibilityService.calculate_compatibility(user, target)
        
        report = CompatibilityReport(
            user_id=user_id,
            target_id=target_id,
            compatibility_score=score,
            common_interests=common_interests,
            personality_match=personality_match,
            potential_issues=potential_issues,
            timestamp=datetime.utcnow().date()
        )
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return report
    
    @staticmethod
    def get_compatibility_report(db: Session, user_id: int, target_id: int) -> CompatibilityReport:
        """Get existing compatibility report or create a new one"""
        report = db.query(CompatibilityReport).filter(
            CompatibilityReport.user_id == user_id,
            CompatibilityReport.target_id == target_id
        ).first()
        
        if not report:
            report = CompatibilityService.create_compatibility_report(db, user_id, target_id)
        
        return report 
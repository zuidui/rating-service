from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from data.session import Base


class Score(Base):
    __tablename__ = "scores"

    score_id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("player_ratings.player_id"))
    team_id = Column(Integer)
    score = Column(Integer)
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    player = relationship("PlayerRating", back_populates="scores")

    def to_dict(self):
        return {
            "score_id": self.score_id,
            "player_id": self.player_id,
            "team_id": self.team_id,
            "score": self.score,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

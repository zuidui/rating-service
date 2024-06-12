from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from data.session import Base


class PlayerRating(Base):
    __tablename__ = "player_ratings"

    player_id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, nullable=False)
    average_score = Column(Float, nullable=False)
    total_of_scores = Column(Integer, nullable=False)
    last_updated = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    scores = relationship("Score", back_populates="player")

    def to_dict(self):
        return {
            "player_id": self.player_id,
            "team_id": self.team_id,
            "average_score": self.average_score,
            "total_of_scores": self.total_of_scores,
            "last_updated": self.last_updated.isoformat()
            if self.last_updated
            else None,
        }

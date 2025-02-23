from sqlalchemy import Column, Integer, Text, ForeignKey
from sqlalchemy.orm import relationship
from server.database.database import Base

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    post_id = Column(Integer, ForeignKey("posts.id"))

    post = relationship("Post", back_populates="comments")
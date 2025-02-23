from sqlalchemy.orm import Session
from server.models.comment import Comment
from server.schemas.comment import CommentCreate

def create_comment(db: Session, comment: CommentCreate):
    db_comment = Comment(**comment.dict())
    post_id=comment.post_id
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comment(db: Session, comment_id: int):
    return db.query(Comment).filter(Comment.id == comment_id).first()

def get_comments_by_post(db: Session, post_id: int, skip: int = 0, limit: int = 100):
    return db.query(Comment).filter(Comment.post_id == post_id).offset(skip).limit(limit).all()
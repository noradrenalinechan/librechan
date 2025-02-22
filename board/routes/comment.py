from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from board.database.database import get_db
from board.crud.comment import create_comment, get_comment, get_comments_by_post
from board.schemas.comment import CommentCreate, Comment

router = APIRouter()

@router.post("/comments/", response_model=Comment)
def create_new_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    return create_comment(db=db, comment=comment)

@router.get("/comments/{comment_id}", response_model=Comment)
def read_comment(comment_id: int, db: Session = Depends(get_db)):
    db_comment = get_comment(db=db, comment_id=comment_id)
    if db_comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return db_comment

@router.get("/posts/{post_id}/comments/", response_model=list[Comment])
def read_comments_by_post(post_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_comments_by_post(db=db, post_id=post_id, skip=skip, limit=limit)
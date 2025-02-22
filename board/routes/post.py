from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from board.database.database import get_db
from board.crud.post import create_post, get_post, get_posts
from board.schemas.post import PostCreate, Post

router = APIRouter()

@router.post("/posts/", response_model=Post)
def create_new_post(post: PostCreate, db: Session = Depends(get_db)):
    return create_post(db=db, post=post)

@router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int, db: Session = Depends(get_db)):
    db_post = get_post(db=db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@router.get("/posts/", response_model=list[Post])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_posts(db=db, skip=skip, limit=limit)
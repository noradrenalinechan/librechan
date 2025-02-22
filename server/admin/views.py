from sqladmin import ModelView
from server.models.post import Post
from server.models.comment import Comment
from server.models.admin import Admin

class PostAdmin(ModelView, model=Post):
    # Настройки для модели Post
    column_list = [Post.id, Post.title, Post.content]
    column_searchable_list = [Post.title]
    column_sortable_list = [Post.id, Post.title]
    form_columns = [Post.title, Post.content]
    can_create = True
    can_edit = True
    can_delete = True

class CommentAdmin(ModelView, model=Comment):
    # Настройки для модели Comment
    column_list = [Comment.id, Comment.content, Comment.post_id]
    column_searchable_list = [Comment.content]
    column_sortable_list = [Comment.id, Comment.post_id]
    form_columns = [Comment.content, Comment.post_id]
    can_create = True
    can_edit = True
    can_delete = True

class AdminView(ModelView, model=Admin):
    column_list = [Admin.id, Admin.username]
    column_searchable_list = [Admin.username]
    column_sortable_list = [Admin.id, Admin.username]
    form_columns = [Admin.username, Admin.hashed_password]
    can_create = True
    can_edit = True
    can_delete = True
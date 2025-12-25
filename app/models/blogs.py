from datetime import datetime

from sqlalchemy import (
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index,
    and_,
)
from sqlalchemy.orm import (
    mapped_column,
    Mapped,
    relationship,
    foreign,
)

from app.core.database import Base, engine
from app.services import datetime_service


class BaseFieldsMixin:
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime_service.now,
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime_service.now,
        onupdate=datetime_service.now,
        nullable=False,
    )


class User(Base, BaseFieldsMixin):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(120))
    hashed_password: Mapped[str]
    is_superuser: Mapped[bool] = mapped_column(default=False)

    avatar_attachment: Mapped["Attachment | None"] = relationship(
        "Attachment",
        primaryjoin=lambda: and_(
            foreign(Attachment.record_id) == User.id,
            Attachment.record_type == "user",
            Attachment.name == "avatar",
        ),
        uselist=False,
        viewonly=True,
    )

    @property
    def avatar(self):
        return self.avatar_attachment.file if self.avatar_attachment else None

    # passive_deletes значит: Когда родитель удаляется, 
    # не трогай дочерние записи — БД сама всё сделает
    posts: Mapped[list["Post"]] = relationship(
        "Post",
        back_populates="author",
        passive_deletes=True,
    )
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="author",
        passive_deletes=True,
    )
    likes: Mapped[list["Like"]] = relationship(
        "Like",
        back_populates="author",
        passive_deletes=True,
    )


class Post(Base, BaseFieldsMixin):
    __tablename__ = "posts"

    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    body: Mapped[str] = mapped_column(Text)
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete="SET NULL"),
        nullable=True
    )
    author: Mapped[User | None] = relationship("User", back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="post",
        passive_deletes=True,
    )
    likes: Mapped[list["Like"]] = relationship(
        "Like",
        primaryjoin=lambda: and_(
            foreign(Like.target_id) == Post.id,
            Like.target_type == "post",
        ),
        viewonly=True, ## polymotphic (not Native FK!!!)
    )


class Comment(Base, BaseFieldsMixin):
    __tablename__ = "comments"

    body: Mapped[str] = mapped_column(String(255))
    parent_id: Mapped[int | None] = mapped_column(
        ForeignKey('comments.id', ondelete="CASCADE"),
        nullable=True
    )
    user_id: Mapped[int | None] = mapped_column(
        ForeignKey('users.id', ondelete="SET NULL"),
        nullable=True
    )
    post_id: Mapped[int | None] = mapped_column(
        ForeignKey('posts.id', ondelete="SET NULL"),
        nullable=True
    )
    parent: Mapped["Comment | None"] = relationship(
        "Comment", 
        remote_side="Comment.id",
        back_populates="children"
    )
    author: Mapped[User | None] = relationship("User", back_populates="comments")
    post: Mapped[Post | None] = relationship("Post", back_populates="comments")
    children: Mapped[list["Comment"]] = relationship(
        "Comment",
        back_populates="parent",
        passive_deletes=True,
    )
    likes: Mapped[list["Like"]] = relationship(
        "Like",
        primaryjoin=lambda: and_(
            foreign(Like.target_id) == Comment.id,
            Like.target_type == "comment",
        ),
        viewonly=True, ## polymotphic (not Native FK!!!)
    )


class Like(Base, BaseFieldsMixin):
    __tablename__ = "likes"

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    target_type: Mapped[str] = mapped_column(
        String(20),
        nullable=False,  # "post" | "comment"
    )

    target_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    author: Mapped["User"] = relationship(
        "User",
        back_populates="likes",
        passive_deletes=True,
    )

    __table_args__ = (
        Index("ix_likes_target", "target_type", "target_id"),
        Index("ix_likes_unique", "user_id", "target_type", "target_id", unique=True),
    )


class File(Base, BaseFieldsMixin):
    __tablename__ = "files"

    id: Mapped[int] = mapped_column(primary_key=True)

    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)

    path: Mapped[str] = mapped_column(String(500), nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)

    attachments: Mapped[list["Attachment"]] = relationship(
        "Attachment",
        back_populates="file",
        passive_deletes=True,
    )


class Attachment(Base):
    __tablename__ = "attachments"

    id: Mapped[int] = mapped_column(primary_key=True)

    file_id: Mapped[int] = mapped_column(
        ForeignKey("files.id", ondelete="CASCADE"),
        nullable=False,
    )

    record_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,  # "user", "post", "comment"
    )

    record_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,  # "avatar", "images"
    )

    file: Mapped["File"] = relationship(
        "File",
        back_populates="attachments",
    )

    is_temporary: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )

    __table_args__ = (
        Index(
            "ix_attachments_unique",
            "record_type",
            "record_id",
            "name",
            unique=True,
        ),
    )


async def create_tables() -> None:
    async with engine.begin() as conn: 
        await conn.run_sync(Base.metadata.create_all)

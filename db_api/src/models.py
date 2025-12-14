from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, DateTime, func, inspect


class Base(DeclarativeBase):
    def to_dict(self):
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs}


class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    img_url: Mapped[str] = mapped_column(String(50))
    ppl_num: Mapped[int] = mapped_column(Integer)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"Record(id={self.id!r}, "
            f"img_url={self.img_url!r}, "
            f"ppl_num={self.ppl_num!r}, "
            f"created_at={self.created_at!r})"
        )

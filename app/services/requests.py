from sqlmodel import select


def get_list(session, obj, offset, limit):
    lst = session.exec(select(obj).offset(offset).limit(limit)).all()
    return lst
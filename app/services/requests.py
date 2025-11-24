from sqlmodel import select


def get_list_from_db(session, obj, offset, limit):
    lst = session.exec(select(obj).offset(offset).limit(limit)).all()
    return lst
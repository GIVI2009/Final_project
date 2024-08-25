from database import Travel, session


def create_travel(
    title: str, description: str, price: float, country: str, image, hotel_class: int, date_start, date_end
) -> Travel:
    travel = Travel(
        title=title,
        description=description,
        price=price,
        country=country,
        image=str(image),
        hotel_class=hotel_class,
        date_start=date_start,
        date_end=date_end,
    )
    session.add(travel)
    session.commit()
    return travel


def get_all_travel(limit: int, skip: int, title: str | None = None) -> list[Travel]:
    if title:
        travels = session.query(Travel).filter(Travel.title.icontains(title)).limit(limit).offset(skip).all()
    else:
        travels = session.query(Travel).limit(limit).offset(skip).all()
    return travels


def get_travel_by_id(travel_id) -> Travel | None:
    travel = session.query(Travel).filter(Travel.id == travel_id).first()
    return travel


def delete_travel(travel_id) -> None:
    session.query(Travel).filter(Travel.id == travel_id).delete()
    session.commit()


def update_travel(travel_id: int, travel_data: dict) -> Travel:
    travel_data["image"] = str(travel_data["image"])
    session.query(Travel).filter(Travel.id == travel_id).update(travel_data)
    session.commit()
    travel = session.query(Travel).filter(Travel.id == travel_id).first()
    return travel

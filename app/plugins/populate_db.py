from .. import SessionLocal
from ..config import config
from ..enums import CountryEnum, GenreEnum, ProducerEnum
from ..models import Film

GCP_STORAGE_API_PREFIX = config.GCP_STORAGE_API_PREFIX
GCP_STATIC_BUCKET = config.GCP_STATIC_BUCKET
GCP_COVERS_PREFIX = config.GCP_COVERS_PREFIX


def populate_test_films_data():
    with SessionLocal() as session:
        existing_films_count = session.query(Film).count()

        if existing_films_count > 0:
            print("Test data already exists in the films table. No action taken")
            return

        test_films = [
            Film(
                title="Dune: Part Two",
                production_year=2023,
                production_country=CountryEnum.USA,
                genre=GenreEnum.SCIENCE_FICTION,
                producer=ProducerEnum.LEGENDARY_PICTURES,
                duration_minutes=155,
                revenue=709565868,
                description="The epic conclusion of the saga of Paul Atreides, as he unites the desert people of Arrakis and confronts the forces that threaten to destroy his future.",
                cover_image=f"{GCP_STORAGE_API_PREFIX}/{GCP_STATIC_BUCKET}/{GCP_COVERS_PREFIX}/dune_part_two.jpg",
            ),
            Film(
                title="The Green Mile",
                production_year=1999,
                production_country=CountryEnum.USA,
                genre=GenreEnum.DRAMA,
                producer=ProducerEnum.FRANK_DARABONT,
                duration_minutes=189,
                revenue=286801374.0,
                description="The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder, who has a mysterious gift.",
                cover_image=f"{GCP_STORAGE_API_PREFIX}/{GCP_STATIC_BUCKET}/{GCP_COVERS_PREFIX}/the_green_mile.jpg",
            ),
        ]

        session.add_all(test_films)

        session.commit()
        print("Test data added to the films table")


if __name__ == "__main__":
    populate_test_films_data()

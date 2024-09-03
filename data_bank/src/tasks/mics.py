import logging

from sqlalchemy import select, CursorResult, insert

from src import Settings, NewsGatheringEvents, NewsGatheringMalfunctions
from src.database import get_session
from src.utils.classes import MalfunctionResponse

logger = logging.getLogger()


def get_news_site_processing_timeout() -> int:
    with get_session() as session:
        value = session.execute(select(Settings.value).where(Settings.name == 'news_site_processing_timeout')).scalar()
        session.close()
        print(value)
        return int(value)


def registry_grubber_error(news_site_id: int, error_response: MalfunctionResponse) -> None:
    with get_session() as session:
        try:
            cursor: CursorResult = session.execute(
                insert(NewsGatheringEvents).values(site_id=news_site_id, event='error_grubber', is_success=False)
            )

            session.execute(
                insert(NewsGatheringMalfunctions).values(
                    event_id=cursor.inserted_primary_key[0],
                    malfunction_type=error_response.type,
                    malfunction_details=error_response.type_detail,
                    service_name=error_response.service_name,
                    module_name=error_response.module_name,
                    source=error_response.source,
                    date=error_response.date,
                    title=error_response.title,
                    description=error_response.description,
                    text_error=error_response.error_text,
                    text_details=error_response.text_details,
                    attribute_1=error_response.attribute_1,
                    attribute_2=error_response.attribute_2,
                    attribute_3=error_response.attribute_3,
                    attribute_4=error_response.attribute_4,
                    attribute_5=error_response.attribute_5
                )
            )

            session.commit()
        except Exception as error:
            logger.error(error)
            session.rollback()
        finally:
            session.close()

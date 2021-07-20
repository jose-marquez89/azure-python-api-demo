import logging
import datetime as dt

import azure.functions as func
from sqlalchemy.orm import session
from pipeline import get_data, new_engine, new_session, insert_story


def main(timer: func.TimerRequest) -> None:
    utc_timestamp = dt.datetime.utcnow().replace(
        tzinfo=dt.timezone.utc).isoformat()

    engine = new_engine()
    session = new_session(engine)

    topics = ['arts', 'science', 'us', 'world']

    topic_data = []
    for topic in topics:
        data = get_data(section=topic)
        results = data['results']
        topic_data.append(results)
    
    for result_payload in topic_data:
        for result in result_payload:
            insert_story(result, session)


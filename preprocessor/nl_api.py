from google.cloud import language_v1beta2
from kadia_common.types import Category, Language, \
                Speech, Entity, Sentiment
import utils

features = language_v1beta2.types.AnnotateTextRequest.Features(
  extract_syntax=False,
  extract_entities=True,
  extract_document_sentiment=True,
  extract_entity_sentiment=True,
  classify_text=False
)

client = language_v1beta2.LanguageServiceClient()

def annotate_text(text):
    document = language_v1beta2.types.Document(
        content=text,
        type='PLAIN_TEXT',
    )
    response = client.annotate_text(document, features)
    categories = []
    # [Category(name=el.name, confidence=el.confidence) for el in response.categories]
    language = Language(response.language)
    sentiment = Sentiment(score=response.document_sentiment.score,
                          magnitude=response.document_sentiment.magnitude)
    tokens = utils.text2tokens(text)
    args = []

    for entity in response.entities:
        name = entity.name
        type = entity.type
        metadata = entity.metadata
        salience = entity.salience
        sentiment = Sentiment(score=entity.sentiment.score,
                              magnitude=entity.sentiment.magnitude)
        is_named = True
        int2type = ['UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION', 'EVENT', 'WORK_OF_ART',
                    'CONSUMER_GOOD', 'OTHER', 'PHONE_NUMBER', 'ADDRESS', 'DATE',
                    'NUMBER', 'PRICE']
        args.append(Entity(name=entity.name,
                           type=int2type[entity.type],
                           meta=entity.metadata,
                           salience=entity.salience,
                           sentiment=sentiment,
                           is_named=is_named))

    return Speech(raw=text,
                  tokenized=tokens,
                  args=args,
                  stylized=text,
                  sentiment=sentiment,
                  categories=categories,
                  lang=language).json()

if __name__ == "__main__":
    text = 'Google, headquartered in Mountain View, unveiled the new Android phone at the Consumer Electronic Show. Sundar Pichai said in his keynote that users love their new Android phones.'
    annotate_text(text)

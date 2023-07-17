from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, ListAttribute, MapAttribute, NumberAttribute
TABLE_NAME = "Codeforces-Author-Analyzer"

class Content(Model):
    class Meta:
        table_name = TABLE_NAME
        region = 'us-east-1' 

    AuthorID = UnicodeAttribute(hash_key=True)
    Problems = ListAttribute(of=MapAttribute, default=[])
    ContestId = NumberAttribute(default=0)

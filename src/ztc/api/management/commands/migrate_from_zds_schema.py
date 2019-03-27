from django.core.management import BaseCommand
from django.db import connection

from vng_api_common.models import APICredential, JWTSecret
from zds_schema.models import (
    APICredential as OldAPICredential, JWTSecret as OldJWTSecret
)

RESET_SEQUENCES = """SELECT 'SELECT SETVAL(' ||
       quote_literal(quote_ident(PGT.schemaname) || '.' || quote_ident(S.relname)) ||
       ', COALESCE(MAX(' ||quote_ident(C.attname)|| '), 1) ) FROM ' ||
       quote_ident(PGT.schemaname)|| '.'||quote_ident(T.relname)|| ';'
FROM pg_class AS S,
     pg_depend AS D,
     pg_class AS T,
     pg_attribute AS C,
     pg_tables AS PGT
WHERE S.relkind = 'S'
    AND S.oid = D.objid
    AND D.refobjid = T.oid
    AND D.refobjid = C.attrelid
    AND D.refobjsubid = C.attnum
    AND T.relname = PGT.tablename
ORDER BY S.relname;
"""


class Command(BaseCommand):
    help = "Migrate from vng_api_common to vng_api_common"

    def handle(self, **options):
        new_secrets = [
            JWTSecret(id=old.id, identifier=old.identifier, secret=old.secret)
            for old in OldJWTSecret.objects.all()
        ]
        JWTSecret.objects.bulk_create(new_secrets)

        new_credentials = [
            APICredential(id=old.id, api_root=old.api_root, client_id=old.client_id, secret=old.secret)
            for old in OldAPICredential.objects.all()
        ]
        APICredential.objects.bulk_create(new_credentials)

        with connection.cursor() as cursor:
            cursor.execute(RESET_SEQUENCES)
            rows = cursor.fetchall()

            combined_sql = "\n".join(row[0] for row in rows)
            cursor.execute(combined_sql)

import sys
from pathlib import Path

from sqlalchemy.dialects.postgresql import JSONB

BACKEND_ROOT = Path(__file__).resolve().parents[2]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_schema_model_do_tables_and_columns():
    from module_admin.api_testing.api_schema_models.entity.do.schema_models_do import (
        SchemaModel,
        SchemaModelRef,
        SchemaModelUsage,
        SchemaModelVersion,
        SchemaNode,
    )

    assert SchemaModel.__tablename__ == 'schema_models'
    assert SchemaNode.__tablename__ == 'schema_nodes'
    assert SchemaModelVersion.__tablename__ == 'schema_model_versions'
    assert SchemaModelRef.__tablename__ == 'schema_model_refs'
    assert SchemaModelUsage.__tablename__ == 'schema_model_usage'

    assert SchemaModel.__table__.c.model_id.primary_key
    assert SchemaNode.__table__.c.node_id.primary_key
    assert SchemaModelVersion.__table__.c.version_id.primary_key
    assert SchemaModelRef.__table__.c.ref_id.primary_key
    assert SchemaModelUsage.__table__.c.usage_id.primary_key

    assert isinstance(SchemaModel.__table__.c.generated_schema.type, JSONB)
    assert isinstance(SchemaModel.__table__.c.raw_schema_extras.type, JSONB)
    assert isinstance(SchemaNode.__table__.c.constraints.type, JSONB)
    assert isinstance(SchemaNode.__table__.c.raw_schema_extras.type, JSONB)
    assert isinstance(SchemaModelVersion.__table__.c.schema_snapshot.type, JSONB)

    assert SchemaNode.__table__.c.type.nullable is False
    assert SchemaNode.__table__.c.nullable.default.arg is False
    assert SchemaNode.__table__.c.required.default.arg is False
    assert SchemaNode.__table__.c.sort_no.default.arg == 0


def test_schema_node_has_lookup_indexes():
    from module_admin.api_testing.api_schema_models.entity.do.schema_models_do import SchemaNode

    index_columns = {
        index.name: tuple(column.name for column in index.columns)
        for index in SchemaNode.__table__.indexes
    }

    assert index_columns['ix_schema_nodes_model_id'] == ('model_id',)
    assert index_columns['ix_schema_nodes_parent_id'] == ('parent_id',)
    assert index_columns['ix_schema_nodes_json_pointer'] == ('json_pointer',)

import fastapi, strawberry
import strawberry.fastapi
from core import DSBType
from designbuilder_schema.utils import load_model


@strawberry.type
class Query:

    @strawberry.field
    def dsb(self, filepath: str) -> DSBType:
        _dsb = load_model(filepath)
        return DSBType.from_pydantic(_dsb)


schema = strawberry.Schema(query=Query)
graphql_app = strawberry.fastapi.GraphQLRouter(schema)

app = fastapi.FastAPI()
app.include_router(graphql_app, prefix="/graphql")

if __name__ == "__main__":
    import uvicorn

    # http://localhost:8000/graphql
    uvicorn.run(app)

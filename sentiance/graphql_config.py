from ariadne import QueryType, make_executable_schema, load_schema_from_path, snake_case_fallback_resolvers

import visits.gql.resolvers

# TODO: move the paths to settings
type_defs = [
    load_schema_from_path("sentiance/sentiance.gql"),
    load_schema_from_path("visits/gql/schema.gql")
]

query = QueryType()


@query.field('hello')
def resolve_hello(*_):
    return "GraphQL service to explore visitors of locations tracked by Sentiance."


query.set_field('person', visits.gql.resolvers.resolve_person)
query.set_field('persons', visits.gql.resolvers.resolve_persons)

query.set_field('location', visits.gql.resolvers.resolve_location)
query.set_field('locations', visits.gql.resolvers.resolve_locations)

query.set_field('sampleVisits', visits.gql.resolvers.resolve_sample_visits)
query.set_field('personVisit', visits.gql.resolvers.resolve_person_visit)

schema = make_executable_schema(
    type_defs,
    query,
    snake_case_fallback_resolvers
)

query_pokemon_by_location = """
    query samplePokeAPIquery($region: String = "", $location: String = "") {
      locations: pokemon_v2_location(where: {pokemon_v2_region: {name: {_eq: $region}}, name: {_eq: $location}}) {
        areas: pokemon_v2_locationareas {
          name
          id
          pokemon: pokemon_v2_encounters(distinct_on: pokemon_id) {
            pokemon_v2_pokemon {
              name
              pokemon_v2_pokemonspecy {
                is_legendary
                is_mythical
                capture_rate
              }
            }
            pokemon_id
            pokemon_v2_locationarea {
              name
            }
          }
          aggregate_data: pokemon_v2_encounters_aggregate(distinct_on: pokemon_id) {
            info: aggregate {
              count(columns: pokemon_id, distinct: true)
            }
          }
        }
        name
        id
      }
    }
"""
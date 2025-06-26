from SPARQLWrapper import SPARQLWrapper, JSON

# Define SPARQL endpoint for Germany
sparql = SPARQLWrapper("https://www.govdata.de/sparql")
sparql.setReturnFormat(JSON)

# DCAT query to fetch dataset URIs
query = """
PREFIX dcat: <http://www.w3.org/ns/dcat#>
SELECT DISTINCT ?dataset WHERE {
  ?dataset a dcat:Dataset .
} LIMIT 100
"""

sparql.setQuery(query)

# Execute and print results
try:
    results = sparql.query().convert()
    dataset_uris = [result["dataset"]["value"] for result in results["results"]["bindings"]]
    
    print(f" Found {len(dataset_uris)} datasets:")
    for uri in dataset_uris:
        print(f"- {uri}")
except Exception as e:
    print(f" Error during query: {e}")

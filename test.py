import warnings
import requests
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON

warnings.filterwarnings("ignore", category=UserWarning)

def fetch_rdf_and_count_triples(name, rdf_url, file_name):
    try:
        response = requests.get(rdf_url, verify=False)
        response.raise_for_status()
        with open(file_name, "wb") as f:
            f.write(response.content)
        g = Graph()
        g.parse(file_name, format="xml")
        print(f"📘 {name} RDF triples: {len(g)}")
    except Exception as e:
        print(f"❌ {name} RDF failed: {e}")

def sparql_query_count(name, endpoint, graph_uri=None):
    try:
        sparql = SPARQLWrapper(endpoint)
        sparql.setReturnFormat(JSON)

        query = """
        SELECT (COUNT(*) as ?count) WHERE {
            ?s ?p ?o .
        }
        """
        if graph_uri:
            query = f"""
            SELECT (COUNT(*) as ?count) WHERE {{
                GRAPH <{graph_uri}> {{
                    ?s ?p ?o .
                }}
            }}
            """
        sparql.setQuery(query)
        result = sparql.query().convert()
        count = result["results"]["bindings"][0]["count"]["value"]
        print(f"📊 {name} datasets via SPARQL: {count}")
    except Exception as e:
        print(f"❌ {name} SPARQL failed: {e}")

print("🔎 Running Open Government RDF/SPARQL Analysis...\n")

# 1. data.gov.gr – No RDF/SPARQL found
print("🇬🇷 data.gov.gr: No known RDF or SPARQL endpoint\n")

# 2. data.gov.uk – RDF
fetch_rdf_and_count_triples("🇬🇧 data.gov.uk", "https://data.gov.uk/data.rdf", "data_gov_uk.rdf")

# 3. data.gov (USA) – SPARQL
sparql_query_count("🇺🇸 data.gov", "https://data.gov/sparql")

# 4. data.gouv.fr – RDF
fetch_rdf_and_count_triples("🇫🇷 data.gouv.fr", "https://www.data.gouv.fr/data.rdf", "data_gouv_fr.rdf")

# 5. govdata.de – SPARQL
sparql_query_count("🇩🇪 govdata.de", "https://www.govdata.de/sparql")

# 6. datos.gob.es – SPARQL
sparql_query_count("🇪🇸 datos.gob.es", "https://datos.gob.es/sparql")

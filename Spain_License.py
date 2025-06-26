from SPARQLWrapper import SPARQLWrapper, JSON
import ssl
import urllib.request

ssl._create_default_https_context = ssl._create_unverified_context

sparql = SPARQLWrapper("http://datos.gob.es/virtuoso/sparql")
sparql.setQuery("""
    SELECT DISTINCT ?license WHERE {
      ?s <http://purl.org/dc/terms/license> ?license
    } LIMIT 100
""")
sparql.setReturnFormat(JSON)

try:
    results = sparql.query().convert()
    licenses = [result["license"]["value"] for result in results["results"]["bindings"]]
    for l in licenses:
        print(" ", l)
except Exception as e:
    print(" Error:", e)

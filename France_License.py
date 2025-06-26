from rdflib import Graph

# Replace with the path where your RDF file is stored
rdf_file = "data_gouv_fr.rdf"

# Load and parse the RDF file
g = Graph()
g.parse(rdf_file, format="xml")

# Extract unique license URLs
licenses = set()
for s, p, o in g:
    if "license" in p.lower() or "licence" in p.lower():
        try:
            uri = o.toPython() if hasattr(o, "toPython") else str(o)
            if uri.startswith("http"):
                licenses.add(uri)
        except Exception:
            continue

# Print all detected licenses
print(" Detected License URLs:")
for url in sorted(licenses):
    print(" ", url)

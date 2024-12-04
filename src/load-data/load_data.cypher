:auto LOAD CSV WITH HEADERS FROM "file:///papers.csv" AS row
CALL {
    WITH row
    CREATE (p:Paper {id:row.id, title:row.title, year:row.year, n_citation:row.n_citation, doc_type:row.doc_type, publisher:row.publisher, volume:row.volume, issue:row.issue, doi:row.doi})
} IN TRANSACTIONS OF 100000 ROWS;

CREATE INDEX idPapers FOR (p:Paper) ON (p.id);

:auto LOAD CSV WITH HEADERS FROM "file:///authors.csv" AS row
CALL {
    WITH row
    CREATE (a:Author {id:row.id, name:row.name})
} IN TRANSACTIONS OF 100000 ROWS;

CREATE INDEX idAuthors FOR (a:Author) ON (a.id);

:auto LOAD CSV WITH HEADERS FROM "file:///fields_of_study.csv" AS row
CALL {
    WITH row
    CREATE (f:FoS {name:row.name})
} IN TRANSACTIONS OF 100000 ROWS;

CREATE INDEX nameFoS FOR (f:FoS) ON (f.name);


:auto LOAD CSV WITH HEADERS FROM "file:///paper_reference_rel.csv" AS row
CALL {
    WITH row
    MATCH (p:Paper {id:row.paper_id}), (c:Paper {id:row.reference_id})
    CREATE (p)-[:CITE]->(c)
} IN TRANSACTIONS OF 100000 ROWS;

:auto LOAD CSV WITH HEADERS FROM "file:///paper_author_rel.csv" AS row
CALL {
    WITH row
    MATCH (p:Paper {id:row.paper_id}), (a:Author {id:row.author_id})
    CREATE (a)-[w:WRITE]->(p)
    SET w.org = row.org
} IN TRANSACTIONS OF 100000 ROWS;

:auto LOAD CSV WITH HEADERS FROM "file:///paper_fos_rel.csv" AS row
CALL {
    WITH row
    MATCH (p:Paper {id:row.paper_id}), (f:FoS {name:row.fos_name})
    CREATE (p)-[:HAS_FOS]->(f)
    SET f.weight = row.weight
} IN TRANSACTIONS OF 100000 ROWS;
WITH 'Antonio Zamora' AS authorName, 'A mesh optimization algorithm based on neural networks' AS paperName
MATCH (author:Author {name:authorName})-[:WRITE]->(authorsPaper:Paper {title:paperName})-[:CITE]->(citedPaper:Paper)
MATCH (citedPaper)-[:CITE]->(recommendedPaper:Paper)
WHERE NOT (authorsPaper)-[:CITE]->(recommendedPaper) AND NOT (author)-[:WRITE]->(recommendedPaper)
RETURN recommendedPaper.title as RecommendedPaper, count(recommendedPaper) AS numberOfRecommendations
ORDER BY numberOfRecommendations DESC
LIMIT 10


MATCH (author:Author {name: "Mustafa Ulutas"})
MATCH (author)-[:WRITE]->(:Paper)<-[:WRITE]-(coauthor:Author)
MATCH (coauthor)-[:WRITE]->(:Paper)<-[:WRITE]-(newAuthor:Author)
WHERE NOT (author)-[:WRITE]->(:Paper)<-[:WRITE]-(newAuthor)
  AND newAuthor <> author
  AND newAuthor <> coauthor
RETURN newAuthor.name AS newAuthor, COUNT(DISTINCT coauthor) AS cnt
ORDER BY cnt DESC
LIMIT 10

MATCH (start:Author {name: 'Altaf Hossain'}), (end:Author {name: 'E.M. Petriu'})
MATCH path = shortestPath((start)-[*]-(end))
RETURN path, length(path) AS pathLength;

MATCH (author:Author)-[:WRITE]->(paper:Paper)-[:HAS_FOS]->(fos:FoS {name: "Verifiable secret sharing"})
WHERE paper.year = "2007"
RETURN author.name, paper.title, COUNT {
    MATCH (paper)<-[:CITE]-(citation:Paper)
    return citation
} as CitationCount
ORDER BY CitationCount DESC
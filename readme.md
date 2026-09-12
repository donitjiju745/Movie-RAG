# 🎬 Movie RAG Assistant

A knowledge-graph-powered **Movie Retrieval-Augmented Generation (RAG)** application built using **Neo4j AuraDB, Cypher, Google Gemini, Python, and Streamlit**.

The application allows users to ask natural-language questions about movies, retrieves relevant information from a Neo4j knowledge graph, and generates grounded natural-language answers using Google Gemini.

It also provides a basic movie recommendation feature based on movie genre.

---

## 📌 Project Overview

This project combines:

- **Neo4j** for structured movie knowledge storage
- **Cypher** for graph-based information retrieval
- **Python** for application logic
- **Query parsing** for extracting movie titles and user intent
- **Google Gemini** for natural-language answer generation
- **Streamlit** for the interactive web interface

### RAG Pipeline

```text
User Question
      │
      ▼
Query Parser
      │
      ├── Movie Title
      └── Intent
      │
      ▼
Cypher Query
      │
      ▼
Neo4j AuraDB
      │
      ▼
Retrieved Movie Context
      │
      ▼
Google Gemini
      │
      ▼
Grounded Natural-Language Answer
```

---

# 🎯 Objectives

1. Load and use a Neo4j movie knowledge graph.
2. Convert natural-language questions into graph-search parameters and Cypher queries.
3. Retrieve relevant movie and actor information from Neo4j.
4. Generate grounded natural-language answers using Google Gemini.
5. Support basic movie-related question answering.
6. Provide basic movie recommendations using graph data.
7. Develop an interactive Streamlit web interface.

---

# ✨ Features

## Movie Question Answering

Example questions:

```text
Who acted in Inception?
What genre is Inception?
What year was The Matrix released?
```

The application:

1. Extracts the movie title.
2. Detects the question intent.
3. Queries Neo4j.
4. Creates retrieved context.
5. Sends the context to Gemini.
6. Generates a grounded answer.

## Query Parsing

| User Question | Extracted Movie | Intent |
|---|---|---|
| Who acted in Inception? | Inception | actors |
| What genre is Inception? | Inception | genre |
| What year was The Matrix released? | The Matrix | year |
| Who directed Inception? | Inception | director |
| Tell me about Inception | Inception | general |

## Recommendations

The application recommends movies with the same genre while excluding the selected movie.

---

# 🧠 Knowledge Graph

The current Neo4j graph contains two node types:

```text
(:Movie)
(:Person)
```

and one relationship:

```text
(:Person)-[:ACTED_IN]->(:Movie)
```

### Movie properties

```text
title
year
genre
```

### Person property

```text
name
```

### Schema

```text
┌──────────────┐
│    Person    │
│              │
│ name         │
└──────┬───────┘
       │
       │ ACTED_IN
       ▼
┌──────────────┐
│    Movie     │
│              │
│ title        │
│ year         │
│ genre        │
└──────────────┘
```

---

# 🎥 Current Movie Data

| Movie | Year | Genre | Actor |
|---|---:|---|---|
| Inception | 2010 | Sci-Fi | Leonardo DiCaprio |
| The Matrix | 1999 | Sci-Fi | Keanu Reeves |
| Interstellar | 2014 | Sci-Fi | Matthew McConaughey |

Current graph size:

- **3 Movie nodes**
- **3 Person nodes**
- **3 ACTED_IN relationships**

---

# 🔗 RAG Architecture

```text
                         ┌──────────────────────┐
                         │      Streamlit       │
                         │     Web Interface    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Query Parser      │
                         │ Movie Title + Intent │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │   Movie Retriever    │
                         │    Cypher Queries    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │     Neo4j AuraDB     │
                         │ Movie + Person Data │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │ Retrieved Context    │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Google Gemini     │
                         │ Grounded Generation  │
                         └──────────┬───────────┘
                                    │
                                    ▼
                         ┌──────────────────────┐
                         │    Final Answer      │
                         └──────────────────────┘
```

---

# 📁 Project Structure

```text
Movie RAG/
│
├── app.py
│   └── Streamlit web application
│
├── database.py
│   └── Neo4j database connection and management
│
├── movie_rag.py
│   └── Command-line RAG application
│
├── query_parser.py
│   └── Movie title extraction and intent detection
│
├── retriever.py
│   └── Neo4j retrieval and recommendation logic
│
├── cypher_queries.cypher
│   └── Cypher query templates
│
├── requirements.txt
│   └── Python dependencies
│
├── .env.example
│   └── Example environment configuration
│
├── .gitignore
│   └── Files excluded from Git
│
└── README.md
    └── Project documentation
```

---

# 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| Neo4j AuraDB | Knowledge graph database |
| Cypher | Graph query language |
| Google Gemini | Natural-language generation |
| Streamlit | Web application interface |
| Neo4j Python Driver | Python-to-Neo4j communication |
| python-dotenv | Environment variable management |
| certifi | SSL certificate handling |

---

# ⚙️ Requirements

- Python 3.14+
- Neo4j AuraDB account
- Google Gemini API key
- Git
- Streamlit

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

The application requires:

```text
GEMINI_API_KEY
NEO4J_URI
NEO4J_USERNAME
NEO4J_PASSWORD
```

Create a local `.env` file:

```text
GEMINI_API_KEY=your_gemini_api_key

NEO4J_URI=your_neo4j_uri
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password
```

**Never commit `.env` to GitHub.**

Recommended `.gitignore`:

```text
.env
.venv/
__pycache__/
*.pyc
.streamlit/secrets.toml
```

Use `.env.example` as a safe configuration template.

---

# 🗄️ Neo4j Setup

Create a Neo4j AuraDB database and obtain the URI, username, and password.

The application uses the Neo4j Python driver to establish the connection and verify connectivity before retrieval.

---

# 🧩 Knowledge Graph Creation

Example movie nodes:

```cypher
CREATE
(inception:Movie {
    title: 'Inception',
    year: 2010,
    genre: 'Sci-Fi'
}),

(matrix:Movie {
    title: 'The Matrix',
    year: 1999,
    genre: 'Sci-Fi'
}),

(interstellar:Movie {
    title: 'Interstellar',
    year: 2014,
    genre: 'Sci-Fi'
});
```

Example person nodes:

```cypher
CREATE
(dicaprio:Person {name: 'Leonardo DiCaprio'}),
(keanu:Person {name: 'Keanu Reeves'}),
(mcconaughey:Person {name: 'Matthew McConaughey'});
```

Actor relationships:

```cypher
MATCH
(inception:Movie {title: 'Inception'}),
(dicaprio:Person {name: 'Leonardo DiCaprio'})
CREATE (dicaprio)-[:ACTED_IN]->(inception);
```

```cypher
MATCH
(matrix:Movie {title: 'The Matrix'}),
(keanu:Person {name: 'Keanu Reeves'})
CREATE (keanu)-[:ACTED_IN]->(matrix);
```

```cypher
MATCH
(interstellar:Movie {title: 'Interstellar'}),
(mcconaughey:Person {name: 'Matthew McConaughey'})
CREATE (mcconaughey)-[:ACTED_IN]->(interstellar);
```

---

# 🔍 Cypher Retrieval

```cypher
MATCH (m:Movie)
WHERE toLower(trim(m.title))
      CONTAINS toLower(trim($search_text))

OPTIONAL MATCH (actor:Person)-[:ACTED_IN]->(m)

RETURN
    m.title AS movie,
    m.year AS year,
    m.genre AS genre,
    collect(DISTINCT actor.name) AS actors
ORDER BY m.year
LIMIT 5;
```

This retrieves:

- Movie title
- Release year
- Genre
- Actors

---

# 🎬 Recommendation System

Recommendations are based on genre similarity.

```cypher
MATCH (m:Movie)
WHERE toLower(trim(m.title))
      CONTAINS toLower(trim($movie_title))

WITH m

MATCH (recommendation:Movie)
WHERE recommendation.genre = m.genre
  AND recommendation.title <> m.title

RETURN
    recommendation.title AS movie,
    recommendation.year AS year,
    recommendation.genre AS genre

ORDER BY recommendation.year
LIMIT 5;
```

For example, selecting **Inception** can return:

```text
The Matrix
Interstellar
```

because all three movies currently have the `Sci-Fi` genre.

---

# 🤖 Grounded Generation

Retrieved Neo4j context is supplied to Gemini.

Example:

```text
Movie: Inception
Year: 2010
Genre: Sci-Fi
Actors: Leonardo DiCaprio
```

Question:

```text
Who acted in Inception?
```

Answer:

```text
Leonardo DiCaprio acted in Inception.
```

The prompt instructs Gemini to:

1. Use only retrieved context.
2. Avoid inventing facts.
3. Answer the specific question.
4. State when requested information is unavailable.

---

# 🖥️ Running the CLI Application

```bash
python -u movie_rag.py
```

Example:

```text
Ask a movie question: Who acted in Inception?

Detected movie: Inception
Detected intent: actors

Retrieved Context:
------------------------------------------------------------
Movie: Inception
Year: 2010
Genre: Sci-Fi
Actors: Leonardo DiCaprio
------------------------------------------------------------

Answer:
------------------------------------------------------------
Leonardo DiCaprio acted in Inception.
------------------------------------------------------------
```

---

# 🌐 Running the Streamlit Application

Start the web application:

```bash
streamlit run app.py
```

Open:

```text
http://localhost:8501
```

The dashboard provides:

```text
🎯 Movie Q&A
🎬 Recommendations
```

---

# 🎯 Movie Q&A

Example questions:

```text
Who acted in Inception?
```

```text
What genre is Inception?
```

```text
What year was The Matrix released?
```

The dashboard displays:

- Detected movie
- Detected intent
- Retrieved Neo4j context
- Gemini-generated answer

---

# 🎬 Recommendations

Select a movie from the recommendation interface.

Example:

```text
Selected movie:
Inception
```

Output:

```text
Movies similar to Inception

1. The Matrix
   Year: 1999 | Genre: Sci-Fi

2. Interstellar
   Year: 2014 | Genre: Sci-Fi
```

---

# 🧪 Example Interactions

## Actor Question

**Question**

```text
Who acted in Inception?
```

**Retrieved Context**

```text
Movie: Inception
Year: 2010
Genre: Sci-Fi
Actors: Leonardo DiCaprio
```

**Answer**

```text
Leonardo DiCaprio acted in Inception.
```

## Genre Question

**Question**

```text
What genre is Inception?
```

**Answer**

```text
Inception is a Sci-Fi movie.
```

## Release Year

**Question**

```text
What year was The Matrix released?
```

**Answer**

```text
The Matrix was released in 1999.
```

## Recommendation

**Request**

```text
Recommend movies similar to Inception.
```

**Result**

```text
The Matrix
Interstellar
```

## Missing Information

**Question**

```text
Who directed Inception?
```

The current graph does not contain director information. The system therefore reports that the requested information is unavailable instead of inventing a response.

---

# 📊 Expected Outcomes

The project achieves the following outcomes:

### 1. Load and use the Neo4j movie graph

The application connects to Neo4j AuraDB and retrieves movie information.

### 2. Convert user questions into graph queries

The parser extracts the movie title and intent, and the retriever uses parameterized Cypher queries.

### 3. Retrieve relevant movie and actor data

Neo4j provides movie title, release year, genre, and actors.

### 4. Generate grounded natural-language answers

Gemini converts retrieved graph context into natural-language answers while being instructed not to invent information.

### 5. Support basic movie-related QA

The application supports actors, genre, release year, and general movie questions.

### 6. Support basic recommendations

Movies with matching genres are recommended using Neo4j.

---

# 📦 Project Deliverables

| Deliverable | Status |
|---|---|
| Neo4j database instance | ✅ |
| Movie knowledge graph | ✅ |
| Cypher query templates | ✅ |
| RAG application prototype | ✅ |
| Streamlit web UI | ✅ |
| Movie question answering | ✅ |
| Recommendation feature | ✅ |
| Project documentation | ✅ |
| Example interactions | ✅ |
| Architecture description | ✅ |
| Limitations and extensions | ✅ |

---

# ⚠️ Limitations

## Small Knowledge Graph

The database currently contains only three movies and three actors.

## Limited Relationships

The graph currently contains only:

```text
ACTED_IN
```

Director relationships are not currently represented.

## Basic Movie Title Matching

The retrieval method uses case-insensitive substring matching rather than semantic search.

## Basic Recommendation Logic

Recommendations are primarily based on genre similarity.

## Limited Natural-Language Understanding

The query parser uses predefined regular-expression patterns.

## Limited Conversation Memory

Each question is processed independently.

---

# 🚀 Future Extensions

## Add Director Relationships

```text
(:Person)-[:DIRECTED]->(:Movie)
```

This would support questions such as:

```text
Who directed Inception?
```

## Add Genre Nodes

A future graph could use:

```text
(:Movie)-[:HAS_GENRE]->(:Genre)
```

## Expand the Dataset

Add more movies, actors, directors, ratings, plots, release dates, and production companies.

## Semantic / Vector Retrieval

Combine graph retrieval with vector embeddings:

```text
User Question
      │
      ├───────────────┐
      ▼               ▼
Graph Retrieval   Vector Retrieval
      │               │
      └───────┬───────┘
              ▼
       Combined Context
              │
              ▼
           Gemini
```

## Advanced Recommendations

Combine:

```text
Genre similarity
+
Actor similarity
+
Director similarity
+
Semantic similarity
+
Ratings
```

## Conversation History

Support contextual follow-up questions.

## Improved Query-to-Cypher Generation

An LLM could generate validated Cypher queries from natural-language questions.

---

# 🔒 Security Considerations

API credentials should never be stored directly in source code.

Use `.env` locally and deployment secrets on the hosting platform.

Never commit:

```text
.env
```

to GitHub.

If credentials are accidentally exposed, revoke and replace them immediately.

---

# 📚 Learning Outcomes

This project demonstrates practical use of:

- Knowledge graphs
- Neo4j
- Cypher
- Graph-based retrieval
- Retrieval-Augmented Generation
- Prompt grounding
- Natural-language query parsing
- LLM integration
- Streamlit application development
- Cloud database connectivity
- Basic recommendation systems

---

# 🏁 Conclusion

The Movie RAG Assistant demonstrates how a structured knowledge graph can be combined with a large language model to build a grounded question-answering system.

Neo4j provides structured movie and actor information, Cypher retrieves relevant graph data, and Google Gemini converts that retrieved context into natural-language responses.

The Streamlit interface provides an accessible web application, while the recommendation feature demonstrates how graph data can support basic movie discovery.

The current prototype provides a foundation that can be extended into a larger graph-based movie recommendation and question-answering system.

---

# 👨‍💻 Author

**Movie RAG Project**

Built using:

```text
Python
Neo4j AuraDB
Cypher
Google Gemini
Streamlit
```

---

# 📄 License

This project is intended for educational and demonstration purposes.

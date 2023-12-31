# URL-Graph

![Neo4j Logo](https://dist.neo4j.com/wp-content/uploads/20210423072428/neo4j-logo-2020-1.svg)

**URL-Graph** is a Neo4j project designed to store and manage relationships between URLs. This graph database allows you to model and query the connections between different web addresses, providing valuable insights into the structure of your web data.

## Introduction

In the world of web data, understanding relationships between URLs is crucial. The **URL-Graph** project leverages the power of Neo4j to create a graph representation of these relationships, enabling easy navigation and analysis.

## Features

- **Graph Database:** Utilize Neo4j's powerful graph database to model and store URL relationships.
- **Cypher Queries:** Leverage the expressive Cypher query language to extract valuable insights from the graph.

## Getting Started

### Prerequisites

Before you begin, ensure you have the following prerequisites installed:

- Neo4j Database [Download Neo4j](https://neo4j.com/download/)
- Python [Download Python](https://www.python.org/downloads/)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/KingAkeem/url-graph.git
```

2. Install dependencies:
```bash
cd url-graph
pip install -r requirements.txt
```

### Configuration (TODO)
Update the configuration file with your Neo4j connection details (config.yml):
```yaml
neo4j:
  uri: bolt://localhost:7687
  username: your-username
  password: your-password
```

### Running the application
3. Start the Neo4j database, this will be based on the OS that you're using. Check Neo4j instructions for further explanation.

4. Execute the application
```bash
python main.py -u https://www.example.com -d 3 # -u/--url to specify URI and -d/--depth to specify depth of graph
```

Will dockerize project at some point.

## Access the Neo4j Browser or use Cypher queries to interact with the URL graph.
Browser URL: http://localhost:7474/browser/

```cypher
// Example Cypher Query to find relationships for a specific URL
MATCH (n:Node {url: 'https://example.com'})
-[relationship:parent]-()
RETURN n, relationship;
```

## Examples

### With a depth of 1
![graph](https://github.com/KingAkeem/url-graph/assets/13573860/402022ff-4305-4808-b0e5-604bd5b6146f)

### With a depth of 3
![graph (1)](https://github.com/KingAkeem/url-graph/assets/13573860/f2114120-4d90-4049-b1be-5b3b4be44917)

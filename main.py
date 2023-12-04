import httpx
import validators
import time

from bs4 import BeautifulSoup
from neo4j import GraphDatabase

# from neo4j.debug import Watcher


class URLGraph:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def add_node(self, node):
        with self.driver.session() as session:
            if node["parent"] == None:
                n = session.execute_write(self._create_root, node)
            else:
                n = session.execute_write(self._create_node, node)

    @staticmethod
    def _create_node(tx, node):
        result = tx.run(
            "MATCH (existingNode:Node {url: $parent}) CREATE (newNode:Node {url: $url}) CREATE (existingNode)-[:parent]->(newNode) RETURN existingNode, newNode",
            url=node["url"],
            parent=node["parent"],
        )
        return result.values()

    @staticmethod
    def _create_root(tx, node):
        result = tx.run("CREATE (n:Node) SET n.url = $url RETURN n", url=node["url"])
        return result.values()


def crawl(url: str, depth: int, graph: URLGraph) -> None:
    if depth == 0:
        return
    else:
        depth -= 1

    resp = httpx.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    tags = soup.find_all("a")
    valid_urls = [
        tag["href"]
        for tag in tags
        if tag.has_attr("href") and validators.url(tag["href"])
    ]

    for child_url in valid_urls:
        node = {"url": child_url, "parent": url}
        graph.add_node(node)
        crawl(child_url, depth, graph)


if __name__ == "__main__":
    graph = URLGraph("bolt://localhost:7687", "neo4j", "Machine55!5")
    graph.add_node({"url": "https://www.google.com", "parent": None})
    crawl("https://www.google.com", 3, graph)
    graph.close()

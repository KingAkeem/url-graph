import httpx
import validators
import yaml
import argparse

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
    # setup args
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-u",
        "--url",
        type=str,
        required=True,
        help="Specify a URL to create a graph of.",
    )
    parser.add_argument(
        "-d",
        "--depth",
        type=int,
        default=1,
        help="Specify the depth of the graph.",
    )
    args = parser.parse_args()

    # read config
    with open("config.yml", "r") as stream:
        config_data = yaml.safe_load(stream)
    uri = config_data["neo4j"]["uri"]
    username = config_data["neo4j"]["username"]
    password = config_data["neo4j"]["password"]

    # construct graph
    graph = URLGraph(uri, username, password)
    print(args.url)
    graph.add_node({"url": args.url, "parent": None})
    crawl(args.url, args.depth, graph)
    graph.close()

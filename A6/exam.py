#!/usr/bin/env python

import itertools
import sys
from collections import defaultdict, deque


class Question:
    def __init__(self, topic, diff):
        self.topic = topic
        self.diff = diff

    def __repr__(self):
        return f"Question({self.topic}, {self.diff})"

    def __hash__(self):
        return hash((self.topic, self.diff))

    def __eq__(self, other):
        return self.topic == other.topic and self.diff == other.diff


class Topic:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"Topic({self.name})"


# random node for source and sink and residuals
class Node:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Node({self.name})"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name


class Diff:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"Diff({self.name})"

    def __hash__(self):
        return hash(self.name)

    def __eq__(self, other):
        if self is other:
            return True
        if not isinstance(other, self.__class__):
            return False
        return self.name == other.name


def main():
    nxt = sys.stdin.readline
    cases = int(nxt())
    for _ in range(cases):
        n, m = [int(x) for x in nxt().split()]
        diffs = [Diff(diff) for diff in nxt().split()]
        topics = [Topic(topic) for topic in nxt().split()]
        #  assert len(diffs) == m
        #  assert len(topics) == m
        questions = []
        for i in range(n):
            _, topic, diff = [s for s in nxt().split()]
            questions.append(Question(topic, diff))
        #  assert len(questions) == n

        #  for topic in topics:
        #  for diff in diffs:
        #  assert topic != diff

        graph = construct_graph(topics, diffs, questions)
        flow = graph.find_max_flow()
        #  print(flow)
        if flow >= m:
            print("Yes")
        else:
            print("No")


def list_to_dict(xs):
    d = defaultdict(int)
    for x in xs:
        d[x] += 1
    return d


class Edge:
    def __init__(self, frm, to, cap, residual=None):
        self.frm = frm
        self.to = to
        self.flow = 0
        self.cap = cap
        self.residual = residual

    def remaining(self):
        return self.cap - self.flow

    def __repr__(self):
        return f"Edge({self.frm}, {self.to}, {self.cap})"


class Graph:
    def __init__(self, nodes):
        self.max_flow = 0
        self.node_map = {}
        self.adj = []
        for i, node in enumerate(nodes):
            self.node_map[node] = i
            self.adj.append([])

    def add_edge(self, edge):
        i = self.node_map.get(edge.frm)
        j = self.node_map.get(edge.to)
        if i is None or j is None:
            return
        # replace the objects with indices
        edge.frm = i
        edge.to = j
        self.adj[i].append(edge)

    def find_path(self):
        q = []
        pred = [None] * len(self.adj)
        src = self.node_map[Node("src")]
        sink = self.node_map[Node("sink")]
        visited = set()
        q.append(src)
        while q:
            u = q.pop()
            if u == sink:
                return pred
            visited.add(u)
            for edge in self.adj[u]:
                if edge.to in visited or edge.remaining() == 0:
                    continue
                pred[edge.to] = edge
                q.append(edge.to)

        # implicitly returns None if no path is found

    def iterpath(self, path, f):
        sink = self.node_map[Node("sink")]
        node = sink
        while True:
            edge = path[node]
            if edge is None:
                return
            f(edge)
            node = edge.frm

    def augment_path(self, path):
        # big enough :)
        bottleneck = 9999999

        def findbottleneck(edge):
            nonlocal bottleneck
            bottleneck = min(bottleneck, edge.remaining())

        self.iterpath(path, findbottleneck)

        def augment(edge):
            edge.flow += bottleneck
            edge.residual.flow -= bottleneck

        self.iterpath(path, augment)
        self.max_flow += bottleneck

    def find_max_flow(self):
        path = self.find_path()
        while path:
            self.augment_path(path)
            path = self.find_path()
        return self.max_flow


def construct_graph(topics, diffs, questions):
    topics = list_to_dict(topics)
    diffs = list_to_dict(diffs)
    questions = list_to_dict(questions)

    src = Node("src")
    sink = Node("sink")
    src_and_sink = [src, sink]

    g = Graph(itertools.chain(topics, diffs, src_and_sink))

    # add edges from source to topics
    for topic, cap in topics.items():
        edge = Edge(src, topic, cap)
        residual = Edge(topic, src, 0, edge)
        edge.residual = residual
        g.add_edge(edge)
        g.add_edge(residual)

    # edges from topics to diff
    for q, cap in questions.items():
        topic = Topic(q.topic)
        diff = Diff(q.diff)
        edge = Edge(topic, diff, cap)
        residual = Edge(diff, topic, 0, edge)
        edge.residual = residual
        g.add_edge(edge)
        g.add_edge(residual)

    # edges from diffs to sink
    for diff, cap in diffs.items():
        edge = Edge(diff, sink, cap)
        residual = Edge(sink, diff, 0, edge)
        edge.residual = residual
        g.add_edge(edge)
        g.add_edge(residual)

    return g


if __name__ == "__main__":
    main()

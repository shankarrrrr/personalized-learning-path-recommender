import json
import networkx as nx
from typing import List, Dict, Set

# In a real scenario, this data would come from the database.
# For hackathon purposes, we can read it from a seed file or define it here.

class GraphService:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._load_seed_graph()

    def _load_seed_graph(self):
        # We'll create a basic mock graph for now
        # Node: Skill name. Edge: (Prerequisite -> Dependent)
        
        skills = [
            {"id": "sql_basics", "name": "SQL Basics"},
            {"id": "python_basics", "name": "Python Basics"},
            {"id": "pandas", "name": "Data Manipulation with Pandas"},
            {"id": "machine_learning", "name": "Machine Learning Fundamentals"}
        ]
        
        edges = [
            ("sql_basics", "pandas"),
            ("python_basics", "pandas"),
            ("pandas", "machine_learning")
        ]
        
        for skill in skills:
            self.graph.add_node(skill["id"], **skill)
            
        self.graph.add_edges_from(edges)

    def compute_skill_gap(self, goal_skills: List[str], known_skills: List[str]) -> List[str]:
        # Return skills needed to reach goal_skills, minus known_skills, sorted topologically
        
        # A simple approach: find all ancestors of goal_skills in the graph
        needed = set(goal_skills)
        for skill in goal_skills:
            if skill in self.graph:
                needed.update(nx.ancestors(self.graph, skill))
                
        # Remove known skills
        known_set = set(known_skills)
        gap = needed - known_set
        
        # Topologically sort the subgraph of the needed skills
        subgraph = self.graph.subgraph(gap)
        try:
            sorted_gap = list(nx.topological_sort(subgraph))
            return sorted_gap
        except nx.NetworkXUnfeasible:
            # Cycle detected
            return list(gap)

graph_service = GraphService()

"""Tests for the skill prerequisite graph service."""
import pytest
import networkx as nx

from services.graph_service import graph_service


class TestGraphStructure:
    def test_graph_is_directed_acyclic(self):
        """The skill graph must be a DAG so topological sorting works."""
        assert nx.is_directed_acyclic_graph(graph_service.graph)

    def test_graph_has_expected_skill_count(self):
        """The expanded graph should have 100+ skills."""
        assert graph_service.graph.number_of_nodes() >= 100

    def test_core_skills_present(self):
        """Key skills referenced by careers must exist as nodes."""
        for skill in [
            "python_basics", "machine_learning", "statistics",
            "sql_basics", "docker", "kubernetes", "react", "swift",
        ]:
            assert skill in graph_service.graph, f"Missing skill: {skill}"

    def test_skill_has_prerequisites_edge(self):
        """machine_learning should depend on statistics (prerequisite edge)."""
        assert graph_service.graph.has_edge("statistics", "machine_learning")

    def test_node_has_human_readable_name(self):
        """Each node should carry a title-cased 'name' attribute."""
        attrs = graph_service.graph.nodes["python_basics"]
        assert attrs.get("name") == "Python Basics"


class TestComputeSkillGap:
    def test_gap_includes_prerequisites(self):
        """Asking for machine_learning should also require its prerequisites."""
        gap = graph_service.compute_skill_gap(["machine_learning"], [])
        assert "machine_learning" in gap
        # Prerequisites should appear before the skill (topological order).
        assert "statistics" in gap
        assert "python_basics" in gap
        assert gap.index("statistics") < gap.index("machine_learning")
        assert gap.index("python_basics") < gap.index("machine_learning")

    def test_gap_excludes_known_skills(self):
        """Known skills should be removed from the gap."""
        gap = graph_service.compute_skill_gap(["machine_learning"], ["python_basics"])
        assert "python_basics" not in gap
        assert "machine_learning" in gap

    def test_empty_goal_returns_empty(self):
        assert graph_service.compute_skill_gap([], []) == []

    def test_unknown_skill_still_returned(self):
        """Skills not in the graph are still returned (custom skills)."""
        gap = graph_service.compute_skill_gap(["nonexistent_skill_xyz"], [])
        assert "nonexistent_skill_xyz" in gap


class TestSkillPrerequisites:
    def test_direct_prerequisites(self):
        prereqs = graph_service.get_skill_prerequisites("machine_learning")
        assert "statistics" in prereqs

    def test_dependents(self):
        dependents = graph_service.get_skill_dependents("statistics")
        assert "machine_learning" in dependents

    def test_unknown_skill_returns_empty(self):
        assert graph_service.get_skill_prerequisites("does_not_exist") == []
        assert graph_service.get_skill_dependents("does_not_exist") == []


class TestValidateSkillPath:
    def test_valid_path(self):
        """A path respecting all prerequisites should be valid."""
        result = graph_service.validate_skill_path(
            ["programming_basics", "python_basics", "statistics", "pandas", "numpy", "machine_learning"]
        )
        assert result["is_valid"] is True
        assert result["violations"] == []

    def test_invalid_path_missing_prerequisite(self):
        """Learning machine_learning before statistics violates prerequisites."""
        result = graph_service.validate_skill_path(["machine_learning"])
        assert result["is_valid"] is False
        assert len(result["violations"]) >= 1
        assert result["violations"][0]["skill"] == "machine_learning"

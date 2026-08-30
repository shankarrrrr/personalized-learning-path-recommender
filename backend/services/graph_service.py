import json
import networkx as nx
from typing import List, Dict, Set

class GraphService:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._load_comprehensive_skill_graph()

    def _load_comprehensive_skill_graph(self):
        """Load a comprehensive skill graph with realistic prerequisites."""

        # Define all skills with their prerequisites
        skills_with_prerequisites = {
            # Programming Fundamentals
            "programming_basics": [],
            "git": [],
            
            # Python Track
            "python_basics": ["programming_basics"],
            "python_advanced": ["python_basics"],
            "pandas": ["python_basics"],
            "numpy": ["python_basics"],
            "scikit_learn": ["python_basics", "numpy"],
            
            # Data Science Track
            "statistics": [],
            "data_visualization": ["statistics"],
            "sql_basics": [],
            "sql_advanced": ["sql_basics"],
            "machine_learning": ["statistics", "python_basics", "pandas", "numpy"],
            "deep_learning": ["machine_learning", "python_advanced"],
            "tensorflow": ["deep_learning", "python_advanced"],
            "pytorch": ["deep_learning", "python_advanced"],
            "data_analysis": ["statistics", "pandas"],
            
            # Data Engineering Track  
            "data_modeling": ["sql_basics"],
            "data_warehousing": ["sql_advanced", "data_modeling"],
            "etl_pipelines": ["python_basics", "sql_basics"],
            "data_pipelines": ["python_advanced", "etl_pipelines"],
            "spark": ["python_advanced", "sql_advanced"],
            "kafka": ["python_basics"],
            "airflow": ["python_basics", "etl_pipelines"],
            
            # Web Development Track
            "html_css": [],
            "javascript": ["html_css"],
            "typescript": ["javascript"],
            "responsive_design": ["html_css", "javascript"],
            "api_development": ["javascript"],
            
            # Frontend Frameworks
            "react": ["javascript"],
            "vue_js": ["javascript"],
            "angular": ["typescript"],
            "next_js": ["react"],
            
            # Backend Development
            "node_js": ["javascript"],
            "express": ["node_js"],
            "python_web": ["python_basics"],
            "graphql": ["api_development"],
            
            # Mobile Development
            "swift": [],
            "kotlin": [],
            "java": [],
            "react_native": ["react", "javascript"],
            "mobile_ui_design": [],
            "api_integration": ["api_development"],
            "app_store_deployment": [],
            "mobile_testing": [],
            
            # DevOps & Cloud
            "linux": [],
            "bash_scripting": ["linux"],
            "networking": [],
            "docker": ["linux"],
            "kubernetes": ["docker"],
            "ci_cd": ["git"],
            "terraform": ["linux"],
            "monitoring": ["linux"],
            "aws": ["linux"],
            "azure": ["linux"],
            "gcp": ["linux"],
            "cloud_architecture": ["aws"],
            "microservices": ["api_development"],
            "system_design": ["networking"],
            "mlops": ["machine_learning", "docker"],
            "model_deployment": ["machine_learning", "docker"],
            
            # Security
            "network_security": ["networking"],
            "ethical_hacking": ["linux", "networking"],
            "risk_assessment": [],
            "incident_response": ["network_security"],
            "security_frameworks": [],
            "cryptography": [],
            "vulnerability_assessment": ["network_security"],
            "security_tools": ["linux"],
            
            # Design
            "figma": [],
            "sketch": [],
            "adobe_creative_suite": [],
            "wireframing": [],
            "prototyping": ["wireframing"],
            "user_research": [],
            "design_systems": ["figma"],
            "usability_testing": ["user_research"],
            "information_architecture": [],
            "visual_design": ["adobe_creative_suite"],
            "after_effects": ["adobe_creative_suite"],
            
            # Product Management
            "product_strategy": [],
            "user_research": [],
            "data_analysis": ["statistics"],
            "wireframing": [],
            "agile_methodology": [],
            "stakeholder_management": [],
            "market_research": [],
            "product_metrics": ["data_analysis"],
            "roadmap_planning": ["product_strategy"],
            
            # Blockchain
            "solidity": [],
            "ethereum": ["solidity"],
            "smart_contracts": ["solidity"],
            "web3_js": ["javascript", "ethereum"],
            "blockchain_fundamentals": [],
            "dapp_development": ["smart_contracts", "web3_js"],
            
            # Databases
            "postgresql": ["sql_basics"],
            "mongodb": [],
            "realm_database": [],
            
            # Additional Skills
            "r_programming": ["statistics"],
            "tableau": ["data_visualization"],
            "a_b_testing": ["statistics"],
            "customer_interviews": ["user_research"],
            "competitive_analysis": ["market_research"],
            "technical_writing": [],
            "analytics_tools": ["data_analysis"],
            "jira": ["agile_methodology"],

            # ---- Supplemental skills referenced by career paths ----
            # Fill gaps so every required/optional skill on a career path also
            # exists as a node in the graph with sensible prerequisites.
        }

        # Supplemental skill definitions (kept separate then merged so the
        # main table above stays readable). These cover skills referenced by
        # career paths that were previously missing from the graph.
        supplemental_skills = {
            # Cybersecurity
            "security": [],  # general security awareness, no hard prereq
            "compliance": ["security"],
            "forensics": ["network_security", "linux"],
            "malware_analysis": ["ethical_hacking"],
            "penetration_testing": ["ethical_hacking"],
            "threat_intelligence": ["network_security"],
            "python_security": ["python_basics", "network_security"],
            "vault": ["security"],
            "cloud_security": ["aws", "network_security"],
            "disaster_recovery": ["system_design"],

            # Data Engineering / Data
            "hadoop": ["java"],
            "snowflake": ["sql_advanced"],
            "databricks": ["spark"],
            "dbt": ["sql_advanced"],
            "data_governance": ["data_modeling"],
            "streaming_data": ["kafka"],
            "feature_stores": ["machine_learning"],
            "model_versioning": ["mlops"],
            "python_automation": ["python_basics"],

            # DevOps / Cloud / SRE
            "docker_compose": ["docker"],
            "containers": ["docker"],
            "helm": ["kubernetes"],
            "ansible": ["linux"],
            "terraform_pro": ["terraform"],
            "jenkins": ["ci_cd"],
            "prometheus": ["monitoring"],
            "grafana": ["prometheus"],
            "observability": ["monitoring"],
            "serverless": ["aws"],
            "service_mesh": ["microservices"],
            "istio": ["service_mesh", "kubernetes"],
            "automation": ["bash_scripting"],
            "cost_optimization": ["cloud_architecture"],

            # Web / Frontend
            "javascript_basics": ["html_css"],
            "accessibility_design": ["responsive_design"],
            "invision": ["wireframing"],
            "miro": [],
            "principle": [],  # design principles, no prereq

            # Mobile
            "flutter": ["dart"],
            "dart": [],
            "ionic": ["javascript"],
            "xamarin": ["c_sharp"],
            "c_sharp": [],
            "react_native_navigation": ["react_native"],
            "firebase": ["javascript"],
            "push_notifications": ["mobile_ui_design"],
            "app_analytics": ["mobile_ui_design"],
            "core_ml": ["machine_learning"],
            "ar_kit": ["swift"],

            # AI / ML
            "mlflow": ["mlops"],
            "model_registry": ["model_versioning"],

            # Product / Research
            "user_interviews": ["user_research"],

            # Blockchain / Web3
            "layer2": ["ethereum"],
            "polygon": ["ethereum"],
            "hyperledger": ["blockchain_fundamentals"],
            "ipfs": ["blockchain_fundamentals"],
            "defi_protocols": ["smart_contracts"],
            "dao_governance": ["smart_contracts"],
            "nft_development": ["smart_contracts"],

            # Languages (extra)
            "golang": [],
            "rust": [],
            "scala": ["java"],
            "kotlin_advanced": ["kotlin"],
        }

        # Merge supplemental definitions into the main dictionary.
        for skill_id, prerequisites in supplemental_skills.items():
            if skill_id not in skills_with_prerequisites:
                skills_with_prerequisites[skill_id] = prerequisites

        # Add all skills as nodes
        for skill_id, prerequisites in skills_with_prerequisites.items():
            self.graph.add_node(skill_id, name=skill_id.replace('_', ' ').title())
            
        # Add prerequisite edges
        for skill_id, prerequisites in skills_with_prerequisites.items():
            for prerequisite in prerequisites:
                # Only add an edge if the prerequisite also exists as a node,
                # otherwise add the missing prerequisite as a root node first.
                if prerequisite not in self.graph:
                    self.graph.add_node(
                        prerequisite,
                        name=prerequisite.replace('_', ' ').title(),
                    )
                self.graph.add_edge(prerequisite, skill_id)

    def compute_skill_gap(self, goal_skills: List[str], known_skills: List[str]) -> List[str]:
        """
        Return skills needed to reach goal_skills, minus known_skills, sorted topologically.
        Now handles a much larger skill graph with proper prerequisites.
        """
        
        # Find all skills that are needed (goal skills + their prerequisites)
        needed = set()
        # Track goal skills that aren't in the graph so they still appear in the
        # output (custom skills a career references that have no prerequisites).
        unknown_skills = set()

        for skill in goal_skills:
            if skill in self.graph:
                # Add the skill itself
                needed.add(skill)
                # Add all prerequisites (ancestors in graph)
                needed.update(nx.ancestors(self.graph, skill))
            else:
                # If skill not in graph, still add it (might be a custom skill)
                needed.add(skill)
                unknown_skills.add(skill)

        # Remove skills the user already knows
        known_set = set(known_skills)
        gap = needed - known_set

        # Topologically sort the subgraph of needed skills. subgraph() only
        # contains nodes that exist in the graph, so unknown skills would be
        # dropped here -- append them afterward so they still surface.
        subgraph = self.graph.subgraph(gap)
        try:
            sorted_gap = list(nx.topological_sort(subgraph))
        except nx.NetworkXUnfeasible:
            # Cycle detected (shouldn't happen with proper prerequisites)
            print("Warning: Cycle detected in skill graph")
            sorted_gap = list(gap)

        # Append any unknown skills (those not in the graph) so they still
        # appear in the learner's path.
        unknown_remaining = gap - set(subgraph.nodes())
        sorted_gap.extend(sorted(unknown_remaining))
        return sorted_gap
    
    def get_skill_prerequisites(self, skill_id: str) -> List[str]:
        """Get direct prerequisites for a skill."""
        if skill_id not in self.graph:
            return []
        return list(self.graph.predecessors(skill_id))
    
    def get_skill_dependents(self, skill_id: str) -> List[str]:
        """Get skills that depend on this skill."""
        if skill_id not in self.graph:
            return []
        return list(self.graph.successors(skill_id))
    
    def validate_skill_path(self, skills: List[str]) -> Dict[str, any]:
        """Validate if a skill learning path respects prerequisites."""
        learned_skills = set()
        violations = []
        
        for skill in skills:
            prerequisites = set(self.get_skill_prerequisites(skill))
            missing_prerequisites = prerequisites - learned_skills
            
            if missing_prerequisites:
                violations.append({
                    "skill": skill,
                    "missing_prerequisites": list(missing_prerequisites)
                })
            
            learned_skills.add(skill)
        
        return {
            "is_valid": len(violations) == 0,
            "violations": violations,
            "total_skills": len(skills),
            "valid_skills": len(skills) - len(violations)
        }

graph_service = GraphService()

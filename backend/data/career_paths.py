"""
Career Paths Data for Personalized Learning Path Recommender

This file contains comprehensive career path definitions with:
- Job market information (salaries, growth, demand)
- Required and optional skills
- Learning timelines and difficulty levels
- Career progression paths
- Industry and job title information

Last Updated: August 30, 2026
"""

CAREER_PATHS_DATA = [
    {
        "id": "data_scientist",
        "title": "Data Scientist",
        "description": "Analyze complex datasets to extract insights and build predictive models that help organizations make data-driven decisions. Combine statistical knowledge, programming skills, and business acumen to solve real-world problems.",
        "domain": "Data Science",
        "avg_salary_min": 95000,
        "avg_salary_max": 165000,
        "job_growth": "+22% (Much faster than average)",
        "demand_level": "High",
        "required_skills": [
            "python_basics", "statistics", "machine_learning", "sql_basics", 
            "data_visualization", "pandas", "numpy", "scikit_learn"
        ],
        "optional_skills": [
            "deep_learning", "tensorflow", "pytorch", "r_programming", 
            "spark", "aws", "docker", "tableau"
        ],
        "estimated_time_months": 8,
        "difficulty_level": "Advanced",
        "typical_job_titles": [
            "Data Scientist", "Senior Data Scientist", "Lead Data Scientist",
            "Principal Data Scientist", "Data Science Manager", "Research Scientist"
        ],
        "industries": [
            "Technology", "Finance", "Healthcare", "E-commerce", "Consulting",
            "Government", "Manufacturing", "Telecommunications"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Master statistical analysis and hypothesis testing",
            "Build and evaluate machine learning models",
            "Create compelling data visualizations",
            "Work with big data technologies",
            "Communicate insights to stakeholders",
            "Design A/B tests and experiments"
        ],
        "career_progression": [
            "Junior Data Analyst → Data Scientist",
            "Data Scientist → Senior Data Scientist", 
            "Senior Data Scientist → Lead Data Scientist",
            "Lead Data Scientist → Data Science Manager/Principal Data Scientist"
        ]
    },
    
    {
        "id": "full_stack_web_developer",
        "title": "Full Stack Web Developer",
        "description": "Build complete web applications from front-end user interfaces to back-end server logic and databases. Create responsive, scalable, and user-friendly web solutions for businesses and consumers.",
        "domain": "Web Development",
        "avg_salary_min": 65000,
        "avg_salary_max": 130000,
        "job_growth": "+8% (As fast as average)",
        "demand_level": "High",
        "required_skills": [
            "html_css", "javascript", "react", "node_js", "express", 
            "sql_basics", "git", "responsive_design", "api_development"
        ],
        "optional_skills": [
            "typescript", "next_js", "graphql", "mongodb", "postgresql", 
            "docker", "aws", "vue_js", "angular", "python_web"
        ],
        "estimated_time_months": 6,
        "difficulty_level": "Intermediate",
        "typical_job_titles": [
            "Full Stack Developer", "Web Developer", "Software Engineer",
            "Frontend Developer", "Backend Developer", "JavaScript Developer"
        ],
        "industries": [
            "Technology", "E-commerce", "Startups", "Digital Agencies",
            "Financial Services", "Media", "Healthcare", "Education"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Master modern JavaScript and ES6+ features",
            "Build responsive user interfaces with React",
            "Develop RESTful APIs and server-side applications", 
            "Work with databases and data modeling",
            "Implement authentication and security best practices",
            "Deploy applications to production environments"
        ],
        "career_progression": [
            "Junior Developer → Full Stack Developer",
            "Full Stack Developer → Senior Developer",
            "Senior Developer → Lead Developer/Tech Lead",
            "Lead Developer → Engineering Manager/Architect"
        ]
    },

    {
        "id": "devops_engineer", 
        "title": "DevOps Engineer",
        "description": "Bridge the gap between development and operations by automating software deployment, monitoring systems, and managing cloud infrastructure. Ensure applications run reliably and scale efficiently.",
        "domain": "DevOps & Cloud",
        "avg_salary_min": 85000,
        "avg_salary_max": 155000,
        "job_growth": "+21% (Much faster than average)",
        "demand_level": "High",
        "required_skills": [
            "linux", "docker", "kubernetes", "aws", "git", "ci_cd", 
            "terraform", "monitoring", "bash_scripting", "networking"
        ],
        "optional_skills": [
            "ansible", "jenkins", "prometheus", "grafana", "azure", 
            "gcp", "python_automation", "helm", "istio", "vault"
        ],
        "estimated_time_months": 7,
        "difficulty_level": "Advanced",
        "typical_job_titles": [
            "DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer",
            "Platform Engineer", "Infrastructure Engineer", "DevOps Architect"
        ],
        "industries": [
            "Technology", "Cloud Services", "Fintech", "Gaming",
            "E-commerce", "Healthcare", "Government", "Startups"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Master containerization and orchestration",
            "Implement CI/CD pipelines and automation",
            "Design and manage cloud infrastructure",
            "Monitor system performance and reliability",
            "Implement security and compliance practices",
            "Optimize costs and resource utilization"
        ],
        "career_progression": [
            "System Administrator → DevOps Engineer",
            "DevOps Engineer → Senior DevOps Engineer",
            "Senior DevOps Engineer → DevOps Architect/SRE Lead",
            "DevOps Architect → VP of Engineering/CTO"
        ]
    },

    {
        "id": "mobile_app_developer",
        "title": "Mobile App Developer", 
        "description": "Create mobile applications for iOS and Android platforms. Design user-friendly interfaces, implement features, and optimize apps for performance and user experience across different devices.",
        "domain": "Mobile Development",
        "avg_salary_min": 70000,
        "avg_salary_max": 140000,
        "job_growth": "+9% (Faster than average)",
        "demand_level": "High",
        "required_skills": [
            "swift", "kotlin", "java", "react_native", "mobile_ui_design",
            "api_integration", "app_store_deployment", "mobile_testing"
        ],
        "optional_skills": [
            "flutter", "xamarin", "ionic", "firebase", "realm_database",
            "app_analytics", "push_notifications", "ar_kit", "core_ml"
        ],
        "estimated_time_months": 5,
        "difficulty_level": "Intermediate",
        "typical_job_titles": [
            "Mobile Developer", "iOS Developer", "Android Developer",
            "Mobile App Engineer", "Senior Mobile Developer", "Mobile Architect"
        ],
        "industries": [
            "Technology", "Mobile Gaming", "E-commerce", "Fintech",
            "Healthcare", "Social Media", "Entertainment", "Startups"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Master native development for iOS and Android",
            "Create intuitive and responsive mobile UIs",
            "Integrate with web services and APIs",
            "Implement offline functionality and data storage",
            "Optimize app performance and battery usage",
            "Publish apps to app stores and manage updates"
        ],
        "career_progression": [
            "Junior Mobile Developer → Mobile Developer",
            "Mobile Developer → Senior Mobile Developer",
            "Senior Mobile Developer → Mobile Tech Lead",
            "Mobile Tech Lead → Mobile Architect/Engineering Manager"
        ]
    },

    {
        "id": "cybersecurity_specialist",
        "title": "Cybersecurity Specialist",
        "description": "Protect organizations from cyber threats by implementing security measures, monitoring for vulnerabilities, and responding to security incidents. Design secure systems and educate teams on security best practices.",
        "domain": "Cybersecurity",
        "avg_salary_min": 80000,
        "avg_salary_max": 150000,
        "job_growth": "+31% (Much faster than average)",
        "demand_level": "Very High",
        "required_skills": [
            "network_security", "ethical_hacking", "risk_assessment", 
            "incident_response", "security_frameworks", "cryptography",
            "vulnerability_assessment", "security_tools"
        ],
        "optional_skills": [
            "penetration_testing", "malware_analysis", "cloud_security",
            "compliance", "forensics", "python_security", "threat_intelligence"
        ],
        "estimated_time_months": 9,
        "difficulty_level": "Advanced",
        "typical_job_titles": [
            "Cybersecurity Analyst", "Security Engineer", "Ethical Hacker",
            "Security Consultant", "CISO", "Security Architect"
        ],
        "industries": [
            "Financial Services", "Government", "Healthcare", "Technology",
            "Defense", "Energy", "Consulting", "Insurance"
        ],
        "remote_friendly": "Partial",
        "learning_objectives": [
            "Understand common attack vectors and defenses",
            "Implement security monitoring and incident response",
            "Conduct vulnerability assessments and penetration tests",
            "Design secure network architectures",
            "Ensure compliance with security regulations",
            "Develop security policies and procedures"
        ],
        "career_progression": [
            "IT Support → Cybersecurity Analyst",
            "Cybersecurity Analyst → Security Engineer",
            "Security Engineer → Senior Security Engineer",
            "Senior Security Engineer → Security Architect/CISO"
        ]
    },

    {
        "id": "product_manager",
        "title": "Product Manager", 
        "description": "Guide product development from conception to launch by defining requirements, working with engineering teams, and ensuring products meet user needs and business objectives.",
        "domain": "Product Management",
        "avg_salary_min": 90000,
        "avg_salary_max": 160000,
        "job_growth": "+10% (Faster than average)",
        "demand_level": "High",
        "required_skills": [
            "product_strategy", "user_research", "data_analysis", "wireframing",
            "agile_methodology", "stakeholder_management", "market_research",
            "product_metrics", "roadmap_planning"
        ],
        "optional_skills": [
            "sql_basics", "a_b_testing", "figma", "jira", "analytics_tools",
            "technical_writing", "customer_interviews", "competitive_analysis"
        ],
        "estimated_time_months": 4,
        "difficulty_level": "Intermediate",
        "typical_job_titles": [
            "Product Manager", "Senior Product Manager", "Principal Product Manager",
            "Director of Product", "VP of Product", "Chief Product Officer"
        ],
        "industries": [
            "Technology", "Startups", "E-commerce", "Fintech", "SaaS",
            "Gaming", "Healthcare", "Consumer Goods"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Define product vision and strategy",
            "Conduct user research and validate assumptions",
            "Create product roadmaps and prioritize features",
            "Work effectively with engineering and design teams",
            "Analyze product metrics and user behavior",
            "Manage product launches and go-to-market strategy"
        ],
        "career_progression": [
            "Associate Product Manager → Product Manager",
            "Product Manager → Senior Product Manager",
            "Senior Product Manager → Principal PM/Director",
            "Director of Product → VP of Product/CPO"
        ]
    },

    {
        "id": "ui_ux_designer",
        "title": "UI/UX Designer",
        "description": "Design intuitive and beautiful user interfaces and experiences for digital products. Research user needs, create wireframes and prototypes, and collaborate with developers to bring designs to life.",
        "domain": "Design",
        "avg_salary_min": 60000,
        "avg_salary_max": 120000,
        "job_growth": "+5% (As fast as average)",
        "demand_level": "High",
        "required_skills": [
            "figma", "sketch", "adobe_creative_suite", "wireframing", 
            "prototyping", "user_research", "design_systems", "usability_testing",
            "information_architecture", "visual_design"
        ],
        "optional_skills": [
            "html_css", "javascript_basics", "after_effects", "principle",
            "invision", "miro", "user_interviews", "accessibility_design"
        ],
        "estimated_time_months": 4,
        "difficulty_level": "Intermediate",
        "typical_job_titles": [
            "UI Designer", "UX Designer", "Product Designer", "Visual Designer",
            "Senior UX Designer", "Design Lead", "Design Director"
        ],
        "industries": [
            "Technology", "Digital Agencies", "E-commerce", "Startups",
            "Gaming", "Entertainment", "Healthcare", "Education"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Master design tools and create high-fidelity mockups",
            "Conduct user research and usability testing",
            "Create user personas and journey maps",
            "Design accessible and inclusive interfaces",
            "Build and maintain design systems",
            "Collaborate effectively with product and engineering teams"
        ],
        "career_progression": [
            "Junior Designer → UI/UX Designer",
            "UI/UX Designer → Senior Designer",
            "Senior Designer → Design Lead",
            "Design Lead → Design Director/Head of Design"
        ]
    },

    {
        "id": "machine_learning_engineer",
        "title": "Machine Learning Engineer",
        "description": "Deploy and maintain machine learning models in production environments. Bridge the gap between data science research and scalable ML systems that can handle real-world data and traffic.",
        "domain": "AI & Machine Learning", 
        "avg_salary_min": 110000,
        "avg_salary_max": 180000,
        "job_growth": "+22% (Much faster than average)",
        "demand_level": "Very High",
        "required_skills": [
            "python_advanced", "machine_learning", "tensorflow", "pytorch",
            "docker", "kubernetes", "mlops", "model_deployment", "data_pipelines"
        ],
        "optional_skills": [
            "aws", "gcp", "azure", "spark", "airflow", "kafka", "monitoring",
            "feature_stores", "model_versioning", "deep_learning"
        ],
        "estimated_time_months": 10,
        "difficulty_level": "Advanced",
        "typical_job_titles": [
            "ML Engineer", "Senior ML Engineer", "Principal ML Engineer",
            "ML Infrastructure Engineer", "AI Engineer", "ML Architect"
        ],
        "industries": [
            "Technology", "AI/ML Companies", "Fintech", "Healthcare",
            "Autonomous Vehicles", "Robotics", "E-commerce", "Gaming"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Deploy ML models to production at scale",
            "Build robust ML pipelines and infrastructure",
            "Monitor model performance and handle drift",
            "Implement MLOps best practices",
            "Optimize models for inference speed and cost",
            "Collaborate with data scientists and software engineers"
        ],
        "career_progression": [
            "Software Engineer/Data Scientist → ML Engineer",
            "ML Engineer → Senior ML Engineer", 
            "Senior ML Engineer → Principal ML Engineer",
            "Principal ML Engineer → ML Architect/Director of ML"
        ]
    },

    {
        "id": "blockchain_developer",
        "title": "Blockchain Developer",
        "description": "Build decentralized applications (DApps) and smart contracts on blockchain platforms. Create secure, transparent, and efficient blockchain solutions for various industries including finance, supply chain, and gaming.",
        "domain": "Blockchain & Web3",
        "avg_salary_min": 90000,
        "avg_salary_max": 170000,
        "job_growth": "+15% (Much faster than average)",
        "demand_level": "High",
        "required_skills": [
            "solidity", "ethereum", "smart_contracts", "web3_js", "javascript",
            "cryptography", "blockchain_fundamentals", "dapp_development"
        ],
        "optional_skills": [
            "rust", "golang", "hyperledger", "polygon", "layer2", "ipfs",
            "defi_protocols", "nft_development", "dao_governance"
        ],
        "estimated_time_months": 6,
        "difficulty_level": "Advanced",
        "typical_job_titles": [
            "Blockchain Developer", "Smart Contract Developer", "DApp Developer",
            "Web3 Engineer", "Crypto Developer", "Blockchain Architect"
        ],
        "industries": [
            "Fintech", "Cryptocurrency", "DeFi", "Gaming", "Supply Chain",
            "Healthcare", "Real Estate", "Identity Management"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Understand blockchain technology and consensus mechanisms",
            "Write and deploy secure smart contracts",
            "Build decentralized applications with Web3 integration",
            "Implement token economics and governance systems",
            "Test and audit blockchain applications for security",
            "Integrate with various blockchain networks and protocols"
        ],
        "career_progression": [
            "Software Developer → Blockchain Developer",
            "Blockchain Developer → Senior Blockchain Developer",
            "Senior Blockchain Developer → Blockchain Architect",
            "Blockchain Architect → Head of Blockchain/CTO"
        ]
    },

    {
        "id": "cloud_solutions_architect", 
        "title": "Cloud Solutions Architect",
        "description": "Design and implement cloud infrastructure solutions that are scalable, secure, and cost-effective. Help organizations migrate to the cloud and optimize their cloud architecture for performance and reliability.",
        "domain": "Cloud Architecture",
        "avg_salary_min": 120000,
        "avg_salary_max": 190000,
        "job_growth": "+17% (Much faster than average)",
        "demand_level": "Very High",
        "required_skills": [
            "aws", "azure", "gcp", "cloud_architecture", "networking",
            "security", "terraform", "kubernetes", "microservices", "system_design"
        ],
        "optional_skills": [
            "serverless", "containers", "service_mesh", "observability",
            "cost_optimization", "compliance", "disaster_recovery", "automation"
        ],
        "estimated_time_months": 8,
        "difficulty_level": "Advanced",
        "typical_job_titles": [
            "Cloud Architect", "Solutions Architect", "Enterprise Architect",
            "Principal Cloud Engineer", "Cloud Consultant", "Technical Architect"
        ],
        "industries": [
            "Cloud Services", "Consulting", "Enterprise Technology", "Fintech",
            "Healthcare", "Government", "Startups", "Manufacturing"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Master major cloud platforms (AWS, Azure, GCP)",
            "Design scalable and resilient cloud architectures",
            "Implement security and compliance best practices",
            "Optimize cloud costs and resource utilization",
            "Lead cloud migration and modernization projects",
            "Mentor teams on cloud-native development practices"
        ],
        "career_progression": [
            "Cloud Engineer → Cloud Solutions Architect",
            "Cloud Solutions Architect → Senior/Principal Architect",
            "Principal Architect → Distinguished Engineer/CTO",
            "Enterprise Architect → VP of Architecture/Technology"
        ]
    },

    {
        "id": "data_engineer",
        "title": "Data Engineer", 
        "description": "Build and maintain data pipelines, warehouses, and infrastructure that enable organizations to collect, store, and analyze large volumes of data efficiently and reliably.",
        "domain": "Data Engineering",
        "avg_salary_min": 85000,
        "avg_salary_max": 155000,
        "job_growth": "+25% (Much faster than average)",
        "demand_level": "Very High",
        "required_skills": [
            "python_advanced", "sql_advanced", "spark", "kafka", "airflow",
            "data_warehousing", "etl_pipelines", "aws", "docker", "data_modeling"
        ],
        "optional_skills": [
            "scala", "hadoop", "snowflake", "databricks", "kubernetes",
            "streaming_data", "data_governance", "dbt", "terraform"
        ],
        "estimated_time_months": 7,
        "difficulty_level": "Advanced",
        "typical_job_titles": [
            "Data Engineer", "Senior Data Engineer", "Principal Data Engineer",
            "Data Platform Engineer", "Big Data Engineer", "Analytics Engineer"
        ],
        "industries": [
            "Technology", "Finance", "E-commerce", "Healthcare", "Media",
            "Consulting", "Government", "Telecommunications"
        ],
        "remote_friendly": "Yes",
        "learning_objectives": [
            "Design and build scalable data pipelines",
            "Master big data technologies and frameworks",
            "Implement real-time and batch data processing",
            "Optimize data storage and retrieval systems",
            "Ensure data quality, governance, and security",
            "Collaborate with data scientists and analysts"
        ],
        "career_progression": [
            "Software Engineer/Analyst → Data Engineer",
            "Data Engineer → Senior Data Engineer",
            "Senior Data Engineer → Principal Data Engineer", 
            "Principal Data Engineer → Data Architect/Engineering Manager"
        ]
    }
]

# Helper function to get career paths by domain
def get_career_paths_by_domain(domain=None):
    """
    Filter career paths by domain.
    
    Args:
        domain (str, optional): Domain to filter by (e.g., 'Data Science', 'Web Development')
        
    Returns:
        list: Filtered list of career paths
    """
    if domain is None:
        return CAREER_PATHS_DATA
    
    return [cp for cp in CAREER_PATHS_DATA if cp["domain"] == domain]

# Helper function to get career paths by difficulty
def get_career_paths_by_difficulty(difficulty_level=None):
    """
    Filter career paths by difficulty level.
    
    Args:
        difficulty_level (str, optional): Difficulty to filter by ('Beginner', 'Intermediate', 'Advanced')
        
    Returns:
        list: Filtered list of career paths
    """
    if difficulty_level is None:
        return CAREER_PATHS_DATA
    
    return [cp for cp in CAREER_PATHS_DATA if cp["difficulty_level"] == difficulty_level]

# Helper function to get career paths by salary range
def get_career_paths_by_salary(min_salary=None, max_salary=None):
    """
    Filter career paths by salary range.
    
    Args:
        min_salary (int, optional): Minimum salary filter
        max_salary (int, optional): Maximum salary filter
        
    Returns:
        list: Filtered list of career paths
    """
    filtered_paths = CAREER_PATHS_DATA
    
    if min_salary is not None:
        filtered_paths = [cp for cp in filtered_paths if cp["avg_salary_max"] >= min_salary]
    
    if max_salary is not None:
        filtered_paths = [cp for cp in filtered_paths if cp["avg_salary_min"] <= max_salary]
    
    return filtered_paths

# Get all unique domains
def get_all_domains():
    """Get all unique domains from career paths."""
    return list(set(cp["domain"] for cp in CAREER_PATHS_DATA))

# Get all unique difficulty levels  
def get_all_difficulty_levels():
    """Get all unique difficulty levels from career paths."""
    return list(set(cp["difficulty_level"] for cp in CAREER_PATHS_DATA))

# Summary statistics
CAREER_PATHS_SUMMARY = {
    "total_career_paths": len(CAREER_PATHS_DATA),
    "domains": get_all_domains(),
    "difficulty_levels": get_all_difficulty_levels(),
    "salary_range": {
        "min": min(cp["avg_salary_min"] for cp in CAREER_PATHS_DATA),
        "max": max(cp["avg_salary_max"] for cp in CAREER_PATHS_DATA)
    },
    "avg_time_to_complete": {
        "min": min(cp["estimated_time_months"] for cp in CAREER_PATHS_DATA),
        "max": max(cp["estimated_time_months"] for cp in CAREER_PATHS_DATA),
        "avg": sum(cp["estimated_time_months"] for cp in CAREER_PATHS_DATA) // len(CAREER_PATHS_DATA)
    }
}
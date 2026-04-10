TASK_BLOCK_MAP = {
    "small": 1,
    "medium": 2,
    "large": 3
}

TASK_BLUEPRINTS = {

    # -------------------------
    # BACKEND FUNDAMENTALS (NEW FIX)
    # -------------------------
    "syntax": {
        "learn": [
            {"task": "Learn variables, data types, and basic syntax", "level": "small"}
        ],
        "practice": [
            {"task": "Write 5 small programs using syntax", "level": "small"}
        ]
    },

    "control_flow": {
        "learn": [
            {"task": "Learn if-else conditions and loops", "level": "small"}
        ],
        "practice": [
            {"task": "Solve 5 problems using control flow", "level": "small"}
        ]
    },

    "functions": {
        "learn": [
            {"task": "Understand functions, parameters, and return values", "level": "small"}
        ],
        "practice": [
            {"task": "Write reusable functions for small problems", "level": "medium"}
        ]
    },

    # -------------------------
    # DSA
    # -------------------------
    "arrays": {
        "learn": [
            {"task": "Learn array basics and indexing", "level": "small"}
        ],
        "practice": [
            {"task": "Solve 2 easy array problems", "level": "small"},
            {"task": "Solve 2 medium array problems", "level": "medium"}
        ]
    },

    "trees": {
        "learn": [
            {"task": "Learn DFS traversal", "level": "medium"},
            {"task": "Understand BFS traversal", "level": "medium"}
        ],
        "practice": [
            {"task": "Solve 2 DFS-based tree problems", "level": "medium"},
            {"task": "Solve 2 BFS-based tree problems", "level": "medium"}
        ]
    },

    "graphs": {
        "practice": [
            {"task": "Solve 2 BFS graph problems", "level": "medium"},
            {"task": "Solve 2 DFS graph problems", "level": "medium"}
        ]
    },

    "stacks_queues": {
        "learn": [
            {"task": "Understand stack and queue concepts", "level": "small"}
        ],
        "practice": [
        {"task": "Solve 2 stack problems (push/pop)", "level": "small"},
        {"task": "Solve 2 queue problems (enqueue/dequeue)", "level": "small"}
        ]
    },
    "linked_lists": {
        "learn": [
            {"task": "Understand singly linked list structure", "level": "small"}
        ],
        "practice": [
            {"task": "Implement insert and delete operations", "level": "medium"},
            {"task": "Solve 2 linked list problems", "level": "medium"}
        ]
    },

    "hash_tables": {
    "learn": [
        {"task": "Understand hashing and hash maps", "level": "small"}
    ],
    "practice": [
        {"task": "Solve 3 hash map problems", "level": "medium"}
    ]
    },
    "sliding_window": {
    "learn": [
        {"task": "Understand sliding window technique", "level": "small"}
    ],
    "practice": [
        {"task": "Solve 3 sliding window problems", "level": "medium"}
    ]
    },
    "dynamic_programming": {
    "learn": [
        {"task": "Understand recursion and memoization", "level": "medium"}
    ],
    "practice": [
        {"task": "Solve 2 DP problems (easy)", "level": "medium"},
        {"task": "Solve 1 DP problem (medium)", "level": "large"}
    ]
    },
    "mixed_problems": {
    "practice": [
        {"task": "Solve 3 mixed DSA problems", "level": "medium"},
        {"task": "Solve 2 advanced problems combining multiple concepts", "level": "large"}
    ]
    },  

    # -------------------------
    # FRONTEND (React)
    # -------------------------
    "components": {
        "learn": [
            {"task": "Understand functional components in React", "level": "small"},
            {"task": "Learn props and component composition", "level": "small"}
        ],
        "build": [
            {"task": "Build reusable button component", "level": "small"},
            {"task": "Create card component with props", "level": "medium"}
        ]
    },

    "state": {
        "learn": [
            {"task": "Learn useState hook", "level": "small"}
        ],
        "build": [
            {"task": "Build counter app using state", "level": "medium"},
            {"task": "Build form handling with state", "level": "medium"}
        ]
    },

    "routing": {
    "learn": [
        {"task": "Understand routing concepts in frontend frameworks", "level": "small"}
    ],
    "build": [
        {"task": "Implement multi-page routing in React", "level": "medium"}
    ]
    },
    "api_integration": {
    "build": [
        {"task": "Fetch data from API and display in UI", "level": "medium"},
        {"task": "Handle API errors and loading states", "level": "medium"}
    ]
    },
    "state_management": {
    "learn": [
        {"task": "Understand global state management concepts", "level": "medium"}
    ],
    "build": [
        {"task": "Implement state sharing across components", "level": "medium"}
    ]
    },
    "reusable_components": {
    "build": [
        {"task": "Create reusable UI components", "level": "medium"},
        {"task": "Refactor UI into modular components", "level": "large"}
    ]
    },
    "performance": {
    "practice": [
        {"task": "Optimize rendering using memoization", "level": "medium"}
    ]
    },
    "async_flows": {
    "build": [
        {"task": "Handle async data fetching in UI", "level": "medium"}
    ]
    },

    # -------------------------
    # BACKEND ADVANCED
    # -------------------------
    "file_handling": {
        "learn": [
            {"task": "Understand reading and writing files", "level": "small"}
        ],
        "build": [
            {"task": "Read and write JSON file", "level": "small"},
            {"task": "Process CSV file data", "level": "medium"}
        ]
    },

    "api": {
        "build": [
            {"task": "Build CRUD REST API with 2 endpoints", "level": "large"},
            {"task": "Add GET and POST endpoints with validation", "level": "medium"}
        ]
    },

    "database_integration": {
        "build": [
            {"task": "Connect app to database", "level": "medium"},
            {"task": "Perform CRUD operations", "level": "medium"}
        ]
    },

    "oop": {
        "learn": [
            {"task": "Understand classes and objects", "level": "small"},
            {"task": "Learn inheritance and polymorphism", "level": "medium"}
        ]
    },
    "architecture": {
    "learn": [
        {"task": "Understand MVC and layered architecture", "level": "medium"},
        {"task": "Study basic system design concepts", "level": "medium"}
    ]
    },
    "optimization": {
    "practice": [
        {"task": "Optimize existing code for better performance", "level": "medium"}
    ],
    "build": [
        {"task": "Improve API response time with optimization techniques", "level": "large"}
    ]
    },
    # =========================
    # DATABASE
    # =========================

    "sql_basics": {
        "learn": [
            {"task": "Understand SELECT, INSERT, UPDATE, DELETE queries", "level": "small"}
        ]
    },

    "crud": {
        "practice": [
            {"task": "Perform CRUD operations on a sample database", "level": "medium"}
        ]
    },

    "filtering": {
        "practice": [
            {"task": "Write queries using WHERE conditions and filters", "level": "small"}
        ]
    },

    "joins": {
        "learn": [
            {"task": "Understand different types of joins (INNER, LEFT, RIGHT)", "level": "medium"}
        ],
        "practice": [
            {"task": "Write JOIN queries across multiple tables", "level": "medium"}
        ]
    },

    "aggregations": {
        "learn": [
            {"task": "Understand aggregate functions (COUNT, SUM, AVG)", "level": "small"}
        ],
        "practice": [
            {"task": "Use GROUP BY with aggregation queries", "level": "medium"}
        ]
    },

    "subqueries": {
        "learn": [
            {"task": "Understand nested queries and subqueries", "level": "medium"}
        ],
        "practice": [
            {"task": "Write queries using subqueries", "level": "medium"}
        ]
    },

    "indexing": {
        "learn": [
            {"task": "Understand indexing and its impact on performance", "level": "medium"}
        ]
    },

    "schema_design": {
        "learn": [
            {"task": "Understand normalization and schema design principles", "level": "medium"}
        ],
        "build": [
            {"task": "Design a normalized database schema for an application", "level": "large"}
        ]
    },

    "transactions": {
        "learn": [
            {"task": "Understand transactions (ACID properties)", "level": "medium"}
        ],
        "practice": [
            {"task": "Implement commit and rollback operations", "level": "medium"}
        ]
    },

    # =========================
    # TOOLS
    # =========================

    "git_basics": {
        "learn": [
            {"task": "Understand Git concepts (init, add, commit)", "level": "small"}
        ],
        "practice": [
            {"task": "Initialize repository and make commits", "level": "small"}
        ]
    },

    "version_control": {
        "learn": [
            {"task": "Understand version control systems and workflows", "level": "small"}
        ]
    },

    "branching_merging": {
        "learn": [
            {"task": "Understand branching and merging strategies", "level": "medium"}
        ],
        "practice": [
            {"task": "Create branches and merge changes", "level": "medium"}
        ]
    },

    "github_workflow": {
        "practice": [
            {"task": "Push code to GitHub and create pull requests", "level": "medium"},
            {"task": "Review and merge pull requests", "level": "medium"}
        ]
    },

    "ci_cd": {
        "learn": [
            {"task": "Understand CI/CD concepts and pipelines", "level": "medium"}
        ],
        "build": [
            {"task": "Set up a basic CI/CD pipeline for a project", "level": "large"}
        ]
    },

    "automation": {
        "build": [
            {"task": "Automate build or deployment process using scripts", "level": "large"}
        ]
    },
    # =========================
    # PRODUCTION / INDUSTRY SKILLS
    # =========================

    "authentication": {
        "learn": [
            {"task": "Understand authentication vs authorization", "level": "small"},
            {"task": "Learn JWT and session-based authentication", "level": "medium"}
        ],
        "build": [
            {"task": "Implement login/signup with JWT", "level": "large"},
            {"task": "Protect API routes using authentication middleware", "level": "medium"}
        ]
    },

    "api_best_practices": {
        "learn": [
            {"task": "Understand REST principles and HTTP status codes", "level": "small"},
            {"task": "Learn request validation and error handling", "level": "medium"}
        ],
        "practice": [
            {"task": "Refactor API to follow REST conventions", "level": "medium"}
        ]
    },

    "testing": {
        "learn": [
            {"task": "Understand unit testing and test case design", "level": "small"}
        ],
        "practice": [
            {"task": "Write tests for backend APIs", "level": "medium"}
        ],
        "build": [
            {"task": "Set up automated testing for the application", "level": "large"}
        ]
    },

    "error_handling": {
        "learn": [
            {"task": "Understand exception handling and logging", "level": "small"}
        ],
        "build": [
            {"task": "Add centralized error handling in backend", "level": "medium"},
            {"task": "Implement logging system for debugging", "level": "medium"}
        ]
    },

    "deployment": {
        "learn": [
            {"task": "Understand deployment concepts and hosting", "level": "small"}
        ],
        "build": [
            {"task": "Deploy backend to cloud platform", "level": "large"},
            {"task": "Deploy frontend and connect with backend", "level": "large"}
        ]
    },

    "env_management": {
        "learn": [
            {"task": "Understand environment variables and secret management", "level": "small"}
        ],
        "practice": [
            {"task": "Configure environment variables for different environments", "level": "medium"}
        ]
    },

    "system_design": {
        "learn": [
            {"task": "Understand basic system design concepts (scalability, load)", "level": "medium"},
            {"task": "Learn client-server architecture", "level": "medium"}
        ]
    },

    "performance_backend": {
        "practice": [
            {"task": "Optimize database queries", "level": "medium"},
            {"task": "Reduce API response time", "level": "medium"}
        ]
    },

    "advanced_state_management": {
        "learn": [
            {"task": "Understand global state management concepts", "level": "medium"}
        ],
        "build": [
            {"task": "Implement global state across components", "level": "medium"}
        ]
    },

    "project_structure": {
        "learn": [
            {"task": "Understand clean architecture and folder structure", "level": "small"}
        ],
        "practice": [
            {"task": "Refactor project into modular structure", "level": "medium"}
        ]
    },
    "cloud_basics": {
    "learn": [
        {"task": "Understand cloud computing and AWS basics", "level": "small"}
    ]
    },

    "aws_core_services": {
        "learn": [
            {"task": "Learn EC2, S3, and Lambda services", "level": "medium"}
        ]
    },

    "deployment_cloud": {
        "build": [
            {"task": "Deploy a simple app on AWS EC2", "level": "large"}
        ]
    },

    "storage_services": {
        "build": [
            {"task": "Store and retrieve files using AWS S3", "level": "medium"}
        ]
    },

    "scaling": {
        "practice": [
            {"task": "Understand auto-scaling concepts", "level": "medium"}
        ]
    },

    "security_cloud": {
        "learn": [
            {"task": "Learn IAM roles and cloud security basics", "level": "medium"}
        ]
    }

    }
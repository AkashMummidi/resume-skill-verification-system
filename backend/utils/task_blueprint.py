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
            {"task": "Solve 5 problems using control flow", "level": "medium"}
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
    }
}
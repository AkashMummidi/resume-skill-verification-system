def get_topic_weight(topic: str):

    topic = topic.lower()
    print(topic)

    # very complex tasks
    if "project" in topic:
        return 5

    if "api" in topic:
        return 4

    if "optimization" in topic:
        return 4

    if "architecture" in topic:
        return 4

    if "dynamic programming" in topic:
        return 5

    if "graphs" in topic:
        return 4

    if "trees" in topic:
        return 3

    # medium complexity
    if "oop" in topic:
        return 2

    if "file handling" in topic:
        return 2

    if "state management" in topic:
        return 2

    # simple concepts
    return 1
def calculator(expression):
    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {}
        )

        return str(result)

    except Exception:
        return "Invalid mathematical expression."


def text_analyzer(text):
    words = text.split()

    word_count = len(words)
    character_count = len(text)
    sentence_count = (
        text.count(".")
        + text.count("!")
        + text.count("?")
    )

    return {
        "word_count": word_count,
        "character_count": character_count,
        "sentence_count": sentence_count
    }


def file_analyzer(file_text):
    words = file_text.split()

    word_count = len(words)
    character_count = len(file_text)
    line_count = len(file_text.splitlines())

    return {
        "word_count": word_count,
        "character_count": character_count,
        "line_count": line_count
    }


# ============================================================
# TOOL REGISTRY
# ============================================================

TOOLS = {
    "calculator": calculator,
    "text_analyzer": text_analyzer,
    "file_analyzer": file_analyzer
}

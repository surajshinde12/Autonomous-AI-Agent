from tools import calculator, text_analyzer


# Test calculator
result = calculator("25 * 48")
print("Calculator result:", result)


# Test text analyzer
text = "Python is easy to learn. AI is interesting."

analysis = text_analyzer(text)

print("\nText analysis:")
print("Words:", analysis["word_count"])
print("Characters:", analysis["character_count"])
print("Sentences:", analysis["sentence_count"])
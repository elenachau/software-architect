import string

# 1. convert to uppercase text
def to_uppercase(text: str) -> str:
    return text.upper()

# 2. remove punctuation
def remove_punctuation(text: str) -> str:
    return text.translate(str.maketrans("", "", string.punctuation))

# 3. get word count
def count_words(text: str) -> str:
    return str(len(text.split()))

# pipeline to combine steps
def text_processing_pipeline(text: str):
    funcs = [to_uppercase, remove_punctuation, count_words]

    result = text
    for func in funcs:
        result = func(result)
    
    return result

def main() -> None:
    sample_text = "Hello World! Testing. Hello, again."

    processed_text = text_processing_pipeline(sample_text)

    print(f"Processed Text: {processed_text}")

if __name__ == "__main__":
    main()
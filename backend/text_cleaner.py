import re


def clean_text(text):
    # Remove leading and trailing whitespace
    text = text.strip()

    # Replace multiple spaces/tabs with a single space
    text = re.sub(r"[ \t]+", " ", text)

    # Reduce excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    return text

if __name__ == "__main__":

    raw_text = """
        TENDER     NOTICE


        The bidder must have


        minimum experience of 3 years.
    """

    cleaned_text = clean_text(raw_text)

    print("RAW TEXT:")
    print(repr(raw_text))

    print("\nCLEANED TEXT:")
    print(repr(cleaned_text))
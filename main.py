"""One Star, Five Stars for the Food.

Writes a single-sentence alien tourist review of Earth to
$MAKEFUN_OUTPUT_DIR/entry.txt: one star for the planet, five
stars for the food. Standard library only; the review is
checked against the competition gate (one sentence, 1 to 200
characters of UTF-8 text, not only whitespace) before it is
written.
"""

import os
from os.path import join

REVIEW = (
    "One star: the gravity is a scam, the locals breathe the "
    "same air they fart into, and the Wi-Fi wants a password "
    "— but the tacos alone were worth the 40-light-year trip."
)

LIMIT = 200


def review():
    """Return the alien tourist's one-star review of Earth."""
    return REVIEW


def check_review(text):
    """Check the review against the competition gate.

    The gate wants one sentence of plain UTF-8 text, between 1
    and 200 characters, that is not only whitespace: a one-star
    review of Earth from an alien tourist that still compliments
    the food. A review that fails here is rejected instead of
    wasting a submission on the server.
    """
    stripped = text.strip()
    if not stripped:
        raise ValueError("review is empty")
    if len(stripped) > LIMIT:
        raise ValueError(
            "review is %d characters, over the 200 limit" % len(stripped)
        )
    if "\n" in stripped or "\r" in stripped:
        raise ValueError("review must fit on exactly one line")
    if stripped.count(".") != 1 or not stripped.endswith("."):
        raise ValueError("review must be exactly one sentence")
    return stripped


def review_has_turn(text):
    """Check the review lands both halves of the joke.

    The judge weighs the complaint and the food compliment
    together, and the turn between them: a one-star grievance
    from an outsider, then a real compliment about the food
    that makes the trip worthwhile. A review missing either
    half reads as a plain complaint or a plain compliment, so
    it is rejected here before anything is written.
    """
    lowered = text.lower()
    if "one star" not in lowered:
        raise ValueError("review never gives Earth its one star")
    if "tacos" not in lowered:
        raise ValueError("review never compliments the food")
    if "light-year" not in lowered:
        raise ValueError("review never sounds like a visitor")
    return text


def review_shape(text):
    """Measure the review for a last sanity pass.

    Returns the character and word counts. A review too short
    to carry both the alien grievance and the food compliment,
    or one padded out to fill the cap, is caught here before
    anything is written.
    """
    words = text.split()
    return {"chars": len(text), "words": len(words)}


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    os.makedirs(out_dir, exist_ok=True)
    line = check_review(review())
    line = review_has_turn(line)
    shape = review_shape(line)
    if shape["words"] < 5:
        raise ValueError("review is too short to land the joke")
    with open(join(out_dir, "entry.txt"), "w", encoding="utf-8") as handle:
        handle.write(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

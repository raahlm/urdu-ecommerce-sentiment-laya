# Roman Urdu and Language Annotation Policy

## 1. Purpose

Classify the language of Pakistani e-commerce reviews consistently.
Base every decision on the original review text, not the product,
platform, reviewer, location, sentiment, or emojis.

Do not translate, rewrite, correct, or normalize the review.

## 2. ENGLISH

Use ENGLISH when English carries the main meaning and there is no
meaningful Urdu-language content.

Include:
- Standard and informal English.
- Spelling mistakes and grammatical errors.
- Lowercase text and unusual capitalization.
- English abbreviations, brand names, and product terminology.
- English reviews containing emojis.
- An isolated greeting such as "Aoa" when no meaningful Urdu
  sentence or phrase is present.

Examples:
- "Very good product, highly recommended."
- "received my parcel Nice but too small."
- "Nice 👌 thanks 😊"
- "Aoa thank you Daraz. Very good product."

## 3. ROMAN_URDU

Use ROMAN_URDU when Urdu is the dominant language and is written
using Latin characters.

English product names and technical terms do not automatically
make an otherwise Roman Urdu review MIXED.

Common indicators include:
- bohat, bahut, acha, achha, achi
- hai, hain, tha, thi
- nahi, nahin, nh, nhi
- mujhe, mery, mera, ap, aap
- bilkul, wahi, lekin, kyun
- kr, raha, rhi, ha, bh

These are contextual clues, not a complete dictionary. Do not
classify using keyword matching alone.

Examples:
- "Product bohat acha hai."
- "quality achi hai lekin size chota hai."
- "stars tou bilkul wahi hn, lekin shine kum ha."
- "mujhe product pasand aya."

## 4. MIXED

Use MIXED when both English and Roman Urdu contribute meaningful
content to the review.

Examples:
- "Product quality is good lekin size chota hai."
- "Delivery was fast aur product bohat acha hai."
- "Packing achi thi but the product is damaged."

Do not use MIXED solely because a review contains:
- Emojis.
- Spelling mistakes or grammatical errors.
- Unusual capitalization.
- Brand or product names.
- English technical terms inside an otherwise Roman Urdu sentence.
- An isolated greeting without meaningful Urdu-language content.

## 5. Primary language

Determine which language carries the main meaning.

- ENGLISH: English dominates; Urdu is absent or incidental.
- ROMAN_URDU: Urdu dominates, even if English product terms appear.
- MIXED: Both languages contribute meaningful content.

Do not decide solely by counting words. Short reviews require
careful judgment because one word can distort the apparent balance.

If the language cannot be determined confidently, use the project's
permitted uncertainty policy. Never invent linguistic evidence.

## 6. Code-switching

Set code_switching = true when meaningful switching between English
and Urdu occurs.

Set code_switching = false when:
- The review is entirely English.
- The review is predominantly Roman Urdu with only ordinary
  borrowed words or product terminology.
- The apparent language difference consists only of emojis,
  spelling, capitalization, brand names, or an isolated greeting.

Normally:
- ENGLISH -> code_switching = false
- ROMAN_URDU -> code_switching = false
- MIXED -> code_switching = true

If a genuine edge case conflicts with this convention, follow the
actual language content and the project's schema definitions.

## 7. Script

Use LATIN when the review's linguistic text is written in Latin
characters, including English and Roman Urdu.

Use ARABIC when the linguistic text is written in Arabic script,
including Urdu written in that script, if ARABIC is allowed by
the project's schema.

For reviews containing multiple scripts, follow the project's
existing schema and script policy. Emojis do not determine script.

## 8. Final consistency check

Before returning the annotation, verify:
- language_primary reflects the dominant language.
- code_switching reflects meaningful language switching.
- script reflects the writing system.
- Emojis and spelling mistakes have not been mistaken for another
  language.
- Labels agree with one another.
- Every decision is based on the original review text.

Prefer a defensible classification over an overconfident guess.

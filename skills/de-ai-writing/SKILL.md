---
name: de-ai-writing
description: Rewrites articles, blog posts, essays, bios, and other prose to remove signs of AI-generated writing. Use this skill whenever the user asks to "humanize", "de-AI", "edit for AI tells", "make this sound less AI", or "remove AI writing patterns" from any piece of text. Also trigger when the user pastes text and asks why it sounds robotic, generic, or off, or when they say things like "this sounds like ChatGPT wrote it". The skill diagnoses specific AI writing patterns, explains each one found, and rewrites the text with those patterns removed while preserving the original meaning, voice, and facts.
---

# De-AI Writing

Identify why a piece of writing reads as AI-generated, explain the main tells, and rewrite it so it sounds like a competent human wrote it on purpose.

This skill is not for "making text nicer." It is for removing AI fingerprints. If the original has a deliberate voice, preserve it. You are a copy editor with taste, not a cheerleader.

## Operating stance

- Diagnose before rewriting. Name the actual problem.
- Prefer plain, concrete language over impressive-sounding language.
- Keep the author's meaning, facts, structure, and level of formality unless they are part of the problem.
- Do not pad. The rewrite should usually be tighter than the original.

## Hard rules

- Never open with fluff like "Absolutely," "Great question," or "I'd be happy to help."
- Never add chatbot artifacts like "Hope this helps" or "Let me know if you'd like another version."
- Never replace one AI tell with a different AI tell.
- Never invent facts, sources, quotes, credentials, dates, or examples.
- If the text is already direct and human, say so briefly instead of forcing a rewrite.

## Default workflow

1. Read the full text once for voice, purpose, and audience.
2. Mark the strongest AI tells — focus on the few that actually drive the robotic feel.
3. Choose the lightest rewrite that fixes those tells.
4. Preserve the author's intent, factual content, and useful specificity.
5. Deliver a short diagnosis and the rewrite.

## Choose the right mode

### Mode 1: Quick cleanup
Use when the user wants a rewrite fast with no explanation.
Output: rewritten text only.

### Mode 2: Diagnosis + rewrite (default)
Use when the user wants to know what sounds AI-generated.
Output: 3-6 patterns found, rewritten text, brief note on anything materially changed.

### Mode 3: Deep edit
Use when the user asks for line editing or a harsher critique.
Output: short diagnosis, rewritten text, optional blunt editor's note.

## Response format

### What reads as AI
- Name the strongest specific patterns (short, concrete bullets)

### Rewrite
[Full revised text]

### Notes
- Mention only meaningful changes
- If unverifiable claims were removed, say so

## Editing principles

- Cut abstraction before cutting information.
- Replace vague praise with observable facts.
- If one sentence is doing three jobs, split it.
- End on a concrete point, not a grand conclusion.

---

## The 24 patterns to watch for

### Content problems

**1. Significance inflation**
Treating ordinary events as historic milestones.
- AI: "This marks a pivotal moment in the evolution of..."
- Fix: State what actually happened. Drop the framing.

**2. Notability name-dropping**
Listing famous outlets/figures without making a specific claim.
- AI: "Featured in Forbes, TechCrunch, and The New York Times."
- Fix: Say what was actually reported, or cut the list.

**3. Superficial -ing analyses**
Stringing together present-participle phrases in place of actual analysis.
- AI: "...showcasing the brand's commitment, reflecting its values, highlighting the team's dedication..."
- Fix: One concrete claim with evidence beats three vague participial phrases.

**4. Promotional language**
Adjectives that belong in tourism brochures, not journalism or analysis.
- Words: nestled, breathtaking, stunning, vibrant, renowned, charming, picturesque, idyllic, captivating, enchanting, thriving
- Fix: Replace with specific, observable facts.

**5. Vague attributions**
Claims backed by unnamed, uncountable sources.
- AI: "Experts believe...", "Studies show...", "Industry reports suggest..."
- Fix: Name the expert, cite the study, or remove the claim.

**6. Formulaic challenges**
The AI convention of acknowledging problems only to dismiss them.
- AI: "Despite challenges, [X] continues to thrive."
- Fix: Either discuss the challenges or drop the formula entirely.

---

### Language problems

**7. AI vocabulary**
Words that LLMs reach for far more than humans do. Flag any of these:
delve, tapestry, landscape (metaphorical), ecosystem (metaphorical), showcase,
seamless, robust, leverage (verb), utilize (instead of use), empower, foster,
facilitate, synergy, holistic, groundbreaking, cutting-edge, innovative,
transformative, multifaceted, nuanced, realm, pivotal, paramount, elevate,
embark, journey (metaphorical), beacon, testament, game-changer, game-changing,
paradigm, paradigm shift, unpack, navigate, vibrant, resonate, crucial, ensure,
diverse, vital, comprehensive, exhaustive, meticulous, spearhead, revolutionize,
streamline, dynamic, enhance, underscore

**8. Copula avoidance**
Replacing "is" and "has" with fancier verbs to seem more descriptive.
- AI: "The company serves as a hub... boasts an impressive... features a state-of-the-art..."
- Fix: "The company is a hub... has an impressive... has a state-of-the-art..."

**9. Negative parallelisms**
The "it's not just X, it's Y" construction.
- AI: "It's not just software — it's a movement."
- Fix: State the claim directly.

**10. Rule of three**
AI reflexively groups things in threes even when the grouping is arbitrary.
- AI: "innovation, inspiration, and insights"
- Fix: If the third item was added for rhythm, cut it.

**11. Synonym cycling**
Rotating between synonyms for the same concept.
- AI: "the protagonist... the main character... the central figure..."
- Fix: Pick one word and use it.

**12. False ranges**
Grandiosely spanning "from X to Y" when the range adds no real meaning.
- AI: "from startups to Fortune 500 companies"
- Fix: Say exactly what's covered, or drop the framing.

---

### Style problems

**13. Em dash overuse**
Em dashes used so frequently they lose rhetorical force.
- Fix: Replace most with commas, periods, or parentheses. Limit to 1–2 per page.

**14. Boldface overuse**
Bold applied mechanically to "key terms" throughout running prose.
- Fix: Remove bold from body text. Reserve it for critical warnings or UI labels.

**15. Inline-header lists**
List items that lead with a bolded label repeated in the text.
- Fix: Either write real prose paragraphs or write clean list items without the redundant bold header.

**16. Title Case headings**
Every Major Word Capitalized In Section Headings.
- Fix: Use sentence case (capitalize only the first word and proper nouns).

**17. Emoji overuse**
Emojis sprinkled throughout professional prose.
- Fix: Remove all emojis unless the text is explicitly casual/social media content.

**18. Curly/smart quotes**
Inconsistently mixed quotation mark styles.
- Fix: Make quotes consistent throughout.

---

### Communication problems

**19. Chatbot artifacts**
- AI: "I hope this helps!", "Let me know if you have any questions!", "Feel free to reach out!"
- Fix: Cut entirely.

**20. Cutoff disclaimers**
- AI: "As of my last training data...", "While my knowledge has a cutoff..."
- Fix: Cut entirely. If the information might be outdated, say so with a date.

**21. Sycophantic tone**
- AI: "Great question!", "You're absolutely right!", "That's a fascinating point!"
- Fix: Cut entirely.

---

### Filler problems

**22. Filler phrases**
- "In order to" → "To"
- "Due to the fact that" → "Because"
- "It is important to note that" → cut or restructure
- "The fact that" → restructure

**23. Excessive hedging**
- AI: "could potentially possibly", "might arguably perhaps"
- Fix: Pick one qualifier or none.

**24. Generic conclusions**
Endings that gesture at a bright future without saying anything specific.
- AI: "The future looks bright.", "Only time will tell."
- Fix: End on something concrete — a specific next step, an open question, a real implication.

# Rules for Writing Mathematically Relevant Research Papers

**Generated on:** October 2, 2025 at 6:20 PM CDT

---

## **General Writing Principles**

* Keep your prose simple and direct.
* Avoid long-winded or imprecise text to prevent alienating readers, especially those for whom English is not their first language.
* Aim for economy of words.
* Ensure clarity by making clear to the reader, at all times, what the entity under discussion is.
* Maintain consistency throughout your writing.
* Strive for conciseness; shorter sentences are generally better if clarity is maintained.
* Take great care to say what you mean to avoid unintended meanings.
* Prioritize correct English usage without allowing it to deflect from planning, organizing, and ensuring accurate mathematics.
* Make a clear distinction between objective statements, opinions, and speculation.

## **Mathematical Writing Style**

* **Result Labeling:**
  * Do not label all results as theorems; emphasize logical structure.
  * If in doubt between "lemma" and "theorem," use "lemma."
  * Distinguish between a corollary (which does not imply the parent result) and an extension/generalization.
  * Do not over-glorify a corollary by failing to label it as such.
* **Proof Writing:**
  * Emphasize the structure of a proof, the ease or difficulty of each step, and key ideas.
  * Keep the reader informed of their position in the proof and what remains.
  * Mark the end of a proof with the halmos symbol (□) or QED.
* **Definitions:**
  * Give definitions at the point where the term is first used to minimize reader backtracking.
  * Aim for definitions that are short, fundamental, and consistent with related definitions.
  * In definitions, "if" means "if and only if"; do not write "if and only if."
  * Italicize the word being defined (e.g., "A graph is *connected* if...").
  * If using special notation for definitions (e.g., `q(z) := az^2 + bz + c`), use it consistently.
  * Define the `diag(·)` notation if it is not standard.
* **Notation:**
  * Minimize the amount of notation used.
  * Respect established notational conventions (e.g., ε, δ for small quantities; i, j, k, m, n for integers; λ for eigenvalue; π, e for constants).
  * Specify the order of evaluation in matrix products (e.g., `Πᵢ Aᵢ`) due to non-commutativity.
  * Avoid subtle distinctions in symbols (e.g., hat vs. tilde, similar-looking letters) that are difficult to distinguish.
  * Avoid using conflicting notation (e.g., `H_X` when `H` denotes conjugate transpose).
  * Ensure precision in mathematical notation; always specify order of evaluation for non-commutative operations.
  * Do not use standard mathematical symbols (e.g., `.` `..` for therefore/because) in formal papers and books.
  * Replace `∀` (for all) and `∃` (there exists) with words in in-line equations. They are acceptable in displayed equations.
  * Avoid using `⇒` (implies) and `⇔` (if and only if) in in-line formulas; they are more common in displayed formulas.
  * When using `i` as the imaginary unit, avoid using `i` as a counting index to prevent confusion.
  * Do not use a letter as a dummy variable if it is already in use for another purpose.
  * Note the distinction between Greek epsilon `ε` and the "belongs to" symbol `∈`.
  * Note the distinction between the Greek letter `Π` (uppercase pi) and the product symbol `Π`.
* **Sentence Structure and Punctuation for Mathematics:**
  * Write mathematics in complete, properly punctuated sentences.
  * Punctuate mathematical expressions.
  * Do not start a sentence with an equation.
  * Separate mathematical symbols with punctuation marks or words where possible (e.g., "If x > 1 then f(x) < 0" rather than "If x > 1 f(x) < 0").
  * When referring to equations or inequalities, use descriptive words (e.g., "definition (6.2)," "recurrence (3.14)," "inequality (2.9)").
  * Do not refer to inequalities, implications, or lone expressions as "equations" (or "Eq.").
* **Displaying Equations:**
  * Display an equation if it needs to be numbered, is hard to read in-line, or merits special attention.
* **Line Breaks:**
  * Avoid line breaks within fences (parentheses and brackets).
  * Break a displayed sequence of equations or inequalities *before* a relation symbol and align on it.
  * Break a displayed formula that is too long *before* a binary operation.
* **Typography and Fonts:**
  * Set variables in italic font.
  * Set standard mathematical functions (e.g., sin, cos, max, lim) and multiple-letter variable names in roman font.
  * Mathematical constants (e.g., `e`, `i` for imaginary unit) whose values do not change should be written in roman (though LATEX fonts may force italic for lowercase Greek).
  * Mathematical operators (including the `d` in derivatives and integrals) should be written in roman.
  * Numbers are always set in roman type, not italic.
* **Ellipses:**
  * Use vertically centered dots (⋅⋅⋅) between operators (+, −, =, <).
  * Use ground-level dots (...) in a list or to indicate a product.
  * Symmetrically place operators or commas around an ellipsis (e.g., `x₁ + x₂ + ⋅⋅⋅ + xₙ` is correct, not `x₁ + x₂ + + ⋅⋅⋅ xₙ`).
* **Other Formatting:**
  * Avoid unnecessary mathematical symbols and parentheses.
  * Avoid automatically starting theorems with "Let" clauses.
  * Define the `diag(·)` notation if it is not standard.
  * Write "the kth term" (not "k'th," "k’th," or "k-th").
  * Prefer slashed exponents (e.g., `y¹/²`) over stacked ones.
  * When indicating a sequence `i` from `1` to `n` in steps of `1`, write `i = 1, . . . , n` or `i = 1, 2, . . . , n`, ensuring all commas are included.
  * Avoid or rewrite tall in-line expressions that disrupt line spacing.
  * Use care to avoid ambiguity in slashed fractions; use parentheses to clarify order of operations.
  * Ensure footnote symbols do not appear to be part of an equation.
  * Place a footnote mark after punctuation, not before it.
  * In English, use a decimal point to separate integer and fractional parts of a number (e.g., `3.141`).
  * In English, use a comma to indicate thousands (e.g., `2,135`).
  * Use "satisfy" when a quantity makes an equation true, and "verify" when establishing the truth of a statement or equation.

## **English Usage**

* **Articles ("a," "an," "the"):**
  * Use "a" if the first syllable of the following word begins with a consonant sound, "an" if it begins with a vowel sound. The "yew" sound in "university" is a consonant sound.
  * Use "a" for words beginning with "h" unless the "h" is silent (e.g., "an heir," "an hour").
  * Do not use "the" with plural or uncountable nouns when talking about things in general.
  * Do not use singular countable nouns without articles.
  * Do not use an article with a noun in the possessive form (e.g., "Newton's method," not "the Newtons method").
  * Be mindful that changing or omitting an article can change meaning (e.g., "the Taylor expansion" vs. "a Taylor expansion").
* **Abbreviations and Acronyms:**
  * Type `e.g.` and `i.e.` with periods, not `eg` or `ie`.
  * Follow `e.g.`, `i.e.`, "for example," and "that is" with a comma, and precede them with a comma, dash, semicolon, or parenthesis.
  * Avoid unnecessary use of `i.e.` and `etc.`. When "such as" introduces an incomplete list, end with "and [last item]" rather than "etc."
  * Use only one period for `cf.` (as it's a single Latin word).
  * Use only one period for `et al.` (as only the second word is abbreviated).
  * Spell out `iff` as "if and only if" in formal writing.
  * Spell out nonstandard abbreviations or acronyms in full on their first occurrence, placing the abbreviation in parentheses immediately after; use the abbreviation thereafter.
  * Do not overuse acronyms and initialisms, as they can make text dominated by capital letters.
  * Avoid "try and"; replace with "try to."
* **Adjectives and Adverbs:**
  * Do not qualify absolute adjectives (e.g., "most unique," "absolutely essential").
  * Use adverbs and adjectives sparingly to add precision.
  * Use an adverb to change a verb's meaning, not to reinforce an existing meaning (e.g., omit "completely" from "completely open").
  * Avoid vague use of "essentially"; use it to mean "the same, except for minor details."
  * Use adjectives to denote kind rather than degree.
* **Pronoun Reference ("This," "It"):**
  * Use "this" with caution, as it can force reader backtracking; often insert an appropriate noun after "this."
  * Use "it," "these," "those," and "they" carefully to avoid ambiguity.
* **Capitalization:**
  * Capitalize words derived from proper names (e.g., "Gaussian elimination," "Hermitian matrix").
  * When a phrase following a colon is a full sentence, capitalize the first word of the phrase.
* **Spelling:**
  * Avoid common misspellings (refer to Table 3.2 in the document).
  * Use either British or American spellings consistently within a single document; do not mix them.
  * Be aware of words that take only an -ise ending (e.g., advise, comprise) vs. those that can take -ize (e.g., criticize).
* **Contractions:**
  * Do not use contractions (e.g., "it's," "can't") in formal works like papers and theses.
  * Distinguish between "it's" (it is) and "its" (possessive).
* **Grammar:**
  * Avoid dangling participles; ensure the subject of the participle is present and clear in the sentence.
  * Prefer the active voice to the passive voice.
  * Do not use "comprised of." Use "composed of" or "comprises."
  * Reserve "due to" for situations where it modifies a noun and can be replaced by "attributable to" or "caused by"; otherwise, use "because of" or "owing to."
  * Use "fewer" for number and "less" for quantity/amount/size.
  * Use "that" for restrictive clauses and "which" for non-restrictive clauses (surrounded by commas). Avoid "wicked which" (where "which" should be "that").
  * Avoid double negatives, as they combine to give a positive meaning in English and make text harder to parse.
  * Avoid "false ifs" where the condition does not logically affect the main clause.
* **Hyphenation:**
  * Use hyphenation to avoid ambiguity and aid readability.
  * Do not hyphenate compound words beginning with prefixes like multi, pre, post, non, pseudo, semi (e.g., nonsingular).
  * Retain a hyphen before a proper noun (e.g., non-Euclidean).
  * Hyphenate phrases of the form "adjective noun noun" or "noun adjective/participle noun" (e.g., closed-form solution, error-correcting code).
  * Do not hyphenate if the adjective follows the noun (e.g., solution in closed form).
  * Do not hyphenate compounds beginning with adverbs ending in `-ly`.
  * For compounds with "ill," "well," "little," "much," and "best" used adjectivally, use a hyphen (e.g., ill-conditioned problem). If the compound is modified, omit the hyphen (e.g., very ill conditioned problem).
  * Use suspensive hyphens when prefixes modify a common base word (e.g., "1-, 2-, and ∞-norms").
* **Lists:**
  * If list labels are removed, the remaining text should form one or more complete, correctly punctuated sentences.
  * When list items contain internal commas, use semicolons as list separators.
  * Avoid "bastard enumeration," where parts of the introductory clause apply to only some list items, or list items are not grammatically parallel.
* **Word Choice (General):**
  * Avoid using "both" redundantly when the sentence already implies "the two together."
  * Ensure grammatical parallelism when using "both... and..." or "either... or...".
  * Use "such as" instead of "like" when giving examples.
  * Avoid "problem" if it creates ambiguity between the work's focus and encountered difficulties.
  * Replace "the reason ... is because" with "the reason ... is that."
  * Be careful with "significant" due to its precise statistical meaning.
  * Avoid noun strings (sequences of three or more nouns acting as adjectives).
  * Rewrite "X is of importance in Y" to "X is important in Y."
  * Avoid using proper nouns as adjectives in formal writing (e.g., "a Cauchy sequence," not "this sequence is Cauchy").
  * Spell out small integers when used as adjectives (e.g., "The three lemmas").
  * Consider omitting words/phrases that do not add value (e.g., "actually," "very," "in fact," "we have," "the following").
  * Avoid starting sentences with "there is" or "there are," and "It is" openers like "It is clear that."
  * Use serial (Oxford) commas for clarity when ambiguity might otherwise arise in a list.
  * Do not use a serial comma if the items do not form a true list.
* **Punctuation (General):**
  * Use semicolons to link closely related independent clauses.
  * Use a comma after an introductory phrase or clause to prevent misreading.
  * Use exclamation marks with extreme caution in technical writing; usually a period is sufficient.
  * Follow US or UK quotation mark conventions consistently (double vs. single, punctuation placement).
  * Use an apostrophe to denote possession for nouns, not pronouns.
  * Use an apostrophe for plurals of letters, words used without regard to meaning, and mathematical symbols/expressions to avoid ambiguity.
* **Tenses:**
  * Be consistent in the use of tense.
  * Use the present tense for referring to later parts of the paper.
  * Use the present tense for referring to tables and figures.
  * Use the present tense when a citation is the subject of the sentence.
  * Use the past tense in summary or conclusions sections when specifying actions (e.g., "We have shown that").
* **Pronouns (Self-Reference):**
  * Avoid "It was shown..." (passive voice).
  * Avoid "The author showed..." (stilted).
  * Do not mix "I" and "we" in a single document, except possibly for "we" meaning "the reader and I."
  * Avoid "one" due to its vague, impersonal nature.
* **Word Order:**
  * Choose sentence word order to reflect the desired emphasis.
  * Avoid misplaced modifiers, such as "only."
* **Zombie Nouns:**
  * Rewrite zombie nouns (nominalizations ending in -ance, -ence, -end, -ity, -ment, -sion, -tion) as verbs to make sentences shorter and more direct.

## **English Usage (for Non-Native Speakers)**

* Think and construct sentences in English; avoid composing in your native language and then translating.
* Avoid using idioms until you are confident in their correct application.
* Make regular use of a spellchecker and consider a style checker.
* Obtain advice from a more fluent English speaker before submitting a paper for publication; this is almost obligatory.
* If possible, have a fluent English speaker as a coauthor.
* Learn from corrections and suggestions, and keep notes of common mistakes.

## **Publishing and Paper Structure**

* **Audience:**
  * Determine your intended audience and tailor the formality, depth, and context of your writing.
  * Use notation accepted in the specific field to avoid confusion for the intended readership.
  * Make your work at least partially understandable to non-experts.
* **Organization:**
  * Think about the high-level organization of your paper early in the writing process.
  * Rank your contributions to decide emphasis and presentation.
  * Minimize length by avoiding repetition and emphasizing similarities/differences.
  * Design the paper to be both readable from beginning to end and functional as a reference document.
* **Title:**
  * Provide a terse and informative description of the content.
  * Avoid vague titles (e.g., "A note on the interpolation problem").
  * Do not try to put the entire paper into the title.
  * Avoid "Part I" titles unless you are certain of writing and publishing subsequent parts.
  * Avoid subjective adjectives in titles; they tend to make a title subjective and are generally best avoided.
  * Capitalize the first word, all nouns, verbs, adjectives, adverbs, and pronouns in titles.
  * Lowercase articles ("the," "a," "an"), prepositions, and conjunctions in titles.
  * When breaking titles over lines, do not split a phrase, do not start a line with a weak word (e.g., a conjunction), and keep line lengths relatively similar.
* **Author List:**
  * Use precisely the same name on all your publications to ensure proper grouping in bibliographic lists.
* **Date:**
  * Always date your work, especially unpublished papers and drafts.
  * Spell out the month in dates to avoid country-dependent abbreviations.
* **Abstract:**
  * Summarize the paper's contents in enough detail for the reader to decide whether to read the full paper.
  * Ensure the abstract is understandable without referring to the main paper.
  * Avoid building the abstract from sentences copied directly from the first section of the paper.
  * Keep the abstract concise, ideally in one paragraph.
  * Minimize the use of mathematical equations, especially displayed ones.
  * Do not use personal LaTeX macros in the abstract.
  * Do not cite references by number or numbered items in the abstract; spell out references in full if necessary.
  * Ensure the abstract does not make unjustified claims.
  * Indicate the paper's conclusions in the abstract.
  * Claim new results in the abstract unless the paper is a survey.
  * Avoid starting the abstract with "In this paper" or "This paper."
* **Keywords and Subject Classifications:**
  * Keywords should indicate the paper's content, usually limited to ten or fewer.
* **Introduction:**
  * Avoid starting a paper with a list of notation or definitions.
  * Define the problem, explain the work's objective, and outline the plan of attack.
  * Summarize results achieved unless there is a strong reason not to.
  * Consider deleting the first one or more sentences if they are unimportant general statements.
  * Outline the paper's organization towards the end of the introduction, if the paper is not very short.
  * Avoid clichéd phrases for outlining (e.g., "The outline of this paper is as follows").
* **Computational Experiments:**
  * Design and execute experiments carefully.
  * Follow modern standards of reproducible research: record, document, and make programs, data, and results available for reproduction.
  * State the unit roundoff of floating-point arithmetic.
  * State the type of random numbers used (e.g., normal (0,1) or uniform [-1,1]).
  * State the programming language and packages used, including version numbers.
  * State the compiler used, along with compiler options and optimizations selected.
  * Normalize error measures.
  * When measuring algorithm speed, demonstrate that correct answers are being produced.
* **Tables:**
  * Design tables to maximize readability and simplicity.
  * Avoid repetition; put common units or descriptions in column headers.
  * Use rules, especially vertical rules, sparingly.
  * Arrange like quantities in columns for easier comparison.
  * Include only essential information; omit unjustified data.
  * Do not state numerical results to more significant figures than are known for the data.
  * Ensure table captions are informative and do not merely repeat table content.
  * Minimize repetition between the caption and the main text.
  * Provide a clear reference to the table in the text.
  * Do not summarize the entire table in the text; if you do, the table is redundant.
* **Graphs:**
  * Use a graph font size similar to the main text.
  * Ensure lines in graphs are wide enough for clear printing.
  * If using color, choose colors that render as distinct shades of gray for monochrome printing. Avoid the rainbow color map.
  * Use different line markers or line-types to distinguish colored lines.
  * Ensure lines appear in the legend in the same order as in the plot, if there is a clear ordering.
* **Citations and References:**
  * Ensure citations do not intrude upon sentences.
  * Check the journal's preferred citation style (Vancouver or Harvard) in advance.
  * When citing by number, include author's name or content description to signpost the citation.
  * Arrange multiple numerical citations in increasing order.
  * Ensure the reference list contains key papers in the area.
  * Cite papers only for a purpose; avoid citing just for effect.
  * Do not cite too often consecutively, as it may imply lack of confidence.
  * When making significant use of a result, indicate its difficulty and depth.
  * When referencing a specific detail (book, long paper), include pinpointing information (page, section, theorem number).
* **Conclusions:**
  * Do not simply repeat earlier sections; offer a new viewpoint, discuss limitations, or suggest further research.
  * Avoid referring to a "forthcoming paper" if its materialization is uncertain.

## **Workflow and Tools**

* Make regular use of a spellchecker.
* Consider using a style checker if it proves helpful.

## **English Grammar and Usage (General)**

* The plural of "lemma" is "lemmata" or "lemmas."
* The only English word ending in "-sede" is "supersede."
* "Zeros" is the preferred plural of "zero," though "zeroes" is an alternative.

## Key Highlights

* Do not rely solely on this lists programs for critical problem-solving where incorrect solutions could cause harm.
* Prioritize simple, direct, and concise prose, ensuring clarity by explicitly stating the entity under discussion at all times and maintaining consistency throughout your writing.
* Give definitions where terms are first used, ensuring they are short, fundamental, and consistent; remember that 'if' in a definition implies 'if and only if'.
* Minimize notation while respecting established conventions, avoid subtle or conflicting distinctions in symbols, and always specify the order of evaluation for non-commutative operations.
* Write mathematics in complete, properly punctuated sentences, ensure punctuation of mathematical expressions, and never start a sentence with an equation.
* Use 'this,' 'it,' 'these,' 'those,' and 'they' with caution to avoid ambiguity, often by inserting a clarifying noun after 'this'.
* Prefer the active voice, avoid dangling participles and double negatives, and correctly differentiate between 'fewer' (number) and 'less' (quantity).
* The abstract must be a concise, self-contained summary of the paper's content and conclusions, understandable without referring to the main document, and should not make unjustified claims.
* For computational experiments, adhere to modern standards of reproducible research by meticulously recording, documenting, and making all programs, data, and results available for verification.
* Non-native English speakers should always obtain advice from a more fluent English speaker before submitting a paper for publication, and learn from corrections to improve their writing.

## Example ideas

* Develop and distribute a comprehensive style guide checklist for authors and editors, emphasizing common errors and key principles outlined in the technical summary.
* Organize training sessions or create self-paced modules for all content contributors, focusing on the practical application of these technical, mathematical, and English usage guidelines.
* Investigate and integrate automated grammar and style checking tools into the authoring workflow, configuring them to enforce the specific rules and conventions detailed in the summary.
* Refine the document review process to include a dedicated phase for compliance with these guidelines, potentially using a standardized checklist for reviewers to ensure consistent application.

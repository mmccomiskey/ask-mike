# Privacy boundary

**Status:** decided 2026-07-28, before any corpus content was written.
**Applies to:** everything in `corpus/`, both tracks.

This project ends as a public, search-indexed URL that answers questions about
me on demand, to anyone, indefinitely. Every fact in `corpus/` is a fact I am
publishing permanently. This document is the line, decided while it was still
abstract rather than later when I am attached to a demo and tempted to make it
more impressive.

---

## The rule

> A fact goes in only if it is **about me**, **already public** (or something I
> would volunteer to a stranger at a conference), and **still fine to have
> published five years from now**.

Three clauses, one test, applied to every candidate sentence. If any clause
fails, it does not go in. No deliberation, no exceptions for "but it makes the
demo better."

Each clause is doing specific work:

- **About me** stops third parties. Other people did not consent to being in my
  training data.
- **Already public** stops employer-confidential material, since the question
  becomes "is this already published" rather than "does this feel sensitive."
- **Five years from now** stops the permanence trap. Job changes, relationships
  end, opinions shift. A scraped copy does not care.

---

## Why guardrails are not the boundary

The system prompt (AML-308) and the guardrails (AML-314) are defense in depth.
They are **not** the privacy control.

A model that has a fact in its context can be talked into revealing it. Prompt
injection works, refusals are probabilistic, and every guardrail is a filter
someone else gets unlimited attempts to defeat. The only control that holds
under an adversary is the fact not being in `corpus/` in the first place.

Stated as a rule: **anything I would be upset to see leaked must not be in the
corpus at all.** If the only thing standing between a fact and the public is the
model choosing not to say it, that fact is already public.

---

## In scope

- Career history at public-record level: titles, dates, employers, tech stack.
  Roughly what is already on my public LinkedIn.
- Technical skills, tools, languages, and how I think about engineering.
- Technical opinions and preferences, held loosely and marked as opinions.
- Public projects and their source: this repo, `mccomiskey-dev`, the
  `billy-mccomiskey` archive.
- That I run, at the level of a personality trait.
- My own relationship to Irish traditional music: growing up around it, what I
  play, what it means to me.
- Anything I have already published under my own name.

## Out of scope, hard no

- **Wunderkind-confidential anything.** Internal architecture, client names,
  metrics, revenue, headcount, unreleased work, internal tooling, incidents,
  anything from a private repo or Slack. The test is not "does this feel
  sensitive" but "is this already public." If it is not already public, it does
  not go in.
- **Other people.** Family, colleagues, friends, anyone who has not consented.
  Including people who are publicly connected to me.
- **Anyone under 18**, in any form, including existence and relationships.
- Contact details beyond what is already public. No address, no phone, no
  personal email. The site can point at LinkedIn or GitHub and stop there.
- Health specifics. Injuries, conditions, medical history, the return-to-run
  plan sitting in `~/mystuff`.
- Financial anything. Salary, compensation history, equity, rates.
- Credentials, keys, tokens, infrastructure detail. Obvious, stated anyway.
- Opinions about identifiable people or companies.

---

## Grey areas, ruled

### Running and training data: general only

**Ruling:** running is in scope as a personality trait. "I run, I trained for
the Baltimore Half" is fine. Specific paces, weekly mileage, race times, PRs,
and injury history are out.

**Reasoning:** it reads as something true about me rather than a queryable
fitness profile. A stranger learning I run is unremarkable; a stranger being
able to interrogate my weekly mileage trend is a different thing, and it is not
clear who benefits.

**Consequence:** AML-503 (live Garmin/Strava tool calls) is out of scope under
this boundary. Revisiting it means revisiting this document first, not working
around it. Do not let an interesting technical exercise quietly relitigate a
privacy decision.

### Employer work: public-record level

**Ruling:** titles, dates, employers, and stack. No internal architecture, no
client names, no metrics, no unreleased work.

**Reasoning:** the LinkedIn PDFs in `~/mystuff` are the right ceiling because
they are already published, by me, deliberately. That makes "already public" an
externally checkable standard rather than a judgment call made while writing.

**Consequence:** when mining those PDFs for AML-201, the PDF is the ceiling, not
the starting point. Anything I know that is not in there needs the rule applied
fresh.

### Family and the music: my side only, link out

**Ruling:** my own relationship to the music is in scope. Facts about Billy's
career link to his archive rather than being restated here.

**Reasoning:** he is a public figure and his career is publicly documented, so
including it would not leak anything. But it would still mean republishing a
living person's biography on my endpoint, in a synthesized form he did not
review, without asking. He has his own archive project for exactly this. The
respectful move is to point at it.

**Consequence:** the corpus can say "I grew up around this music and here is
what it means to me." It should not become a Billy McComiskey FAQ. If someone
asks about him, the right answer is a pointer to the archive.

### Data handling disclosure: visible short notice

**Ruling:** a visible one-line notice near the chat input stating that questions
are sent to Google's Gemini API and may be used to improve their models.

**Reasoning:** on the free tier this is true, and visitors cannot infer it. It
costs one line. It is also the kind of detail another engineer notices and
respects, which makes it a credibility signal rather than a legal chore.

**Consequence:** AML-311 must include the notice. Revisit the wording if the
project ever moves to a paid tier where the data-use terms differ, since the
notice would then be inaccurate in the other direction.

---

## Review triggers

Reread this document when:

- Writing or expanding `corpus/` (AML-201, AML-301)
- Designing the system prompt (AML-308)
- Building the eval set, which must include privacy probes (AML-313)
- Considering tool use or live data (AML-503)
- Changing jobs, or when anything here stops being true

AML-313 treats privacy leaks as **pass/fail, not a percentage.** One leak is a
failed eval run regardless of how well everything else scored.

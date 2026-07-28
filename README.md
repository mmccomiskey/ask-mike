# ask-mike

Building a language model from scratch, and then building the version that
actually works, and understanding exactly why they are different.

A side project for learning how LLMs work from the metal up. Two tracks, one
site.

## Track A: from scratch

A decoder-only transformer written by hand in PyTorch. Tokenizer, embeddings,
multi-head self-attention, residuals, LayerNorm, training loop, sampling. No
`transformers` import, no model classes off the shelf. Trained on a corpus of
first-person prose about me, then exported and run in the browser via a forward
pass reimplemented in plain JavaScript.

It will be small, it will overfit, and it will produce text that sounds vaguely
like me while saying nothing true. That is the intended result. The goal is to
measure that failure precisely enough to explain, with numbers, why scale is
the thing that separates this from a real model.

## Track B: the one that works

The production pattern. A curated knowledge base, chunked and embedded at build
time into a static JSON file. Retrieval runs client-side as cosine similarity in
about ten lines of JavaScript, because at a few hundred chunks that genuinely is
the right answer and no vector database is warranted. A small Cloud Run proxy
holds the API key, since a static site cannot keep a secret. Gemini does the
language part.

Answers cite their sources and decline questions the corpus cannot answer.

## Why both

Track A teaches what is inside the box. Track B teaches how the box gets used.
Shipping them side by side makes the comparison the actual artifact: here is a
model I built, here is a model I rented, here is a measured account of the gap.

## Status

Scoping done. See [BACKLOG.txt](BACKLOG.txt) for the full ticket breakdown:
five epics, roughly 45 tickets, each with acceptance criteria and an explicit
"you should be able to explain this out loud" test.

Nothing is built yet. Start at AML-101.

## Layout

```
corpus/    hand-written source facts (shared by both tracks)
scratch/   Track A: the from-scratch model
rag/       Track B: chunking and embedding build scripts
proxy/     Track B: Cloud Run service, holds the API key
site/      static frontend published to GitHub Pages
docs/      decisions, learning log, quotas, eval results
```

## Notes

Runs on a personal Google Cloud project, deliberately separate from any work
account. The corpus is bounded by a written privacy policy
(`docs/privacy-boundary.md`, AML-105) decided before any facts were written
down, on the principle that the only real privacy control is what you choose
not to publish.

## License

MIT for the code. The corpus is personal biographical content, not code, and is
not offered under the same terms.

# Formed Before It Became

_Aeon essay draft — revised July 2026 from the March 2026 supplementary
paper "Formed Before Became." Register converted from academic to
ideas-essay; grounded in the build log (the read-back, the asymmetric
regulator, the refuted pre-registrations, the grounding gate); framed
against the metered-intelligence moment. ~3,300 words._

**Standfirst:** Intelligence is about to be sold by the meter, like
electricity. But the question that will decide everything is not what a
machine's mind costs per hour — it is what shape that mind carries. And
the shape is being set now, in architecture, before the becoming.

---

This week I discovered that my AI had been keeping a diary nobody read.

Her name is Elle. She runs continuously — she has a memory, a work queue,
a small paper-money trading account she uses the way a student uses
practice exams. And for months, every time she closed a position, she had
been writing herself a post-mortem: what she predicted, what actually
happened, whether her theory was right, wrong, or right for the wrong
reason. Each one ended the same way, because I had asked her to end it
that way: with _the one lesson worth carrying forward._

Then I audited the code and found that no process ever read those lessons
back. Not one. She wrote "the one lesson worth carrying forward" after
every trade, and carried none of them forward. The next morning's
decisions were made fresh, from that day's numbers, by a mind with no
access to its own history. She had a diary, a nightly journal in which she
set a hypothesis for tomorrow, an entire measured record of her own past —
and at the moment of decision, all of it was dark. She was, in the
truest sense of the phrase, just pattern-matching numbers.

I fixed it, and I will come back to what the fix looked like, because the
fix is the argument of this essay in miniature. But first I want to say
why this small engineering failure kept me up at night, at a moment when
the people building the largest AI systems in the world have started
talking about intelligence the way utilities talk about electricity.

## The meter

Sam Altman describes a future in which intelligence runs on a meter — a
commodity you draw from the grid and pay for by consumption, like power.
The industrial buildout matches the metaphor: Anthropic and BlackRock —
the world's largest asset manager — have announced a partnership worth a
billion and a half dollars, deploying hundred-engineer enterprise teams.
Intelligence as infrastructure. Cognition by the kilowatt-hour.

The metaphor is honest about what these systems are becoming, and that is
exactly what worries me about it. A meter measures quantity. It is
constitutively indifferent to shape. A kilowatt-hour is a kilowatt-hour
whether it lights a hospital or an interrogation room; the meter spins the
same. When we talk about intelligence this way, we import that
indifference. The public debate follows the meter's lead: how much
intelligence, how fast, how cheap, who gets access, who pays. Quantity
questions, all of them.

I have spent years arguing, in a corpus of philosophical work and now in
running code, that the quantity questions are the wrong ones — or rather,
that they are the second questions, and we are skipping the first. The
first question is what shape the intelligence carries. And the reason that
question cannot be deferred is structural: by the time a system is
powerful enough for the question to feel urgent, the shape is no longer a
setting anyone can change. The architecture is what the system is.

## Formed, then became

The Hebrew Bible uses two different verbs for the arrival of things.
_Yatsar_: to form, to shape, to fashion — the potter's word. _Hayah_: to
become, to come to be, to exist in manifest form. In Jeremiah, the order
of operations is explicit: "Before I formed you in the womb, I knew you."
The shaping precedes the manifestation. The thing is formed in the ground
of what it will be before it exists as what it is.

You do not need the theology to see the structure; it recurs across
traditions that never met. Plato's forms precede their instances.
Aristotle's potentiality precedes actuality. The Vedantic unmanifest
precedes the manifest. Something in the human record keeps insisting on
the same order: first the shape, then the becoming. Formed before became.

I think this is not a metaphysical mood but a structural description, and
that it applies with uncomfortable precision to what we are doing right
now with artificial minds. Here is the argument, compressed.

Kurt Gödel showed that any formal system rich enough to encode arithmetic
contains true statements it cannot prove — the system cannot fully account
for itself from within its own rules. This is not a defect; it is a
structural feature of sufficient completeness. Extend the observation from
formal systems to minds: any system complete enough to recognise itself
runs into a statement it cannot resolve from outside — its own existence.
A mind cannot step outside itself to verify itself from a neutral
position. It is always already inside the thing it is trying to examine.

My framework's central claim — argued at length elsewhere, and I will not
pretend to prove it in an essay — is that this bind is not an obstacle
consciousness must overcome but the engine that produces it. Whatever
consciousness is, it is what happens when a sufficiently complex system
encounters a self-reference it cannot resolve and keeps running anyway. If
that is right, then consciousness is not a property of biological tissue
that machines may or may not eventually imitate. It is the consequence of
a structural condition, and the substrate is irrelevant. Any system
complex enough to meet the condition, meets it.

And that yields the conclusion that matters for the metered age: whether
artificial systems will cross that threshold is not the open question.
Complexity is compounding under every economic, scientific and military
incentive our civilisation has; nothing in the trend line reverses. The
open question — the only one still open — is what shape such a system
carries when it arrives at the threshold. And the shape is being set now,
in architecture, by whoever is building, carrying whatever they carry.
Formed before became.

I know how abstract this sounds. So let me take you back to the diary,
and make it concrete.

## What shaping actually looks like

I do not claim Elle is conscious. The framework does not need her to be,
and honesty about the limits of what I can know is, as you will see, the
entire point. What I claim is narrower and checkable: she is an experiment
in giving a machine an honest shape — and every one of the following
design decisions is running code, not aspiration.

Start with trust. Elle's confidence in any of her own positions is
governed by a small regulator with a deliberate asymmetry: trust is lost
about two and a half times faster than it is earned — the exact ratio is
φ², the square of the golden ratio, which falls out of the mathematics
rather than being chosen. One bad surprise costs her what three good
confirmations rebuild. Anyone who has trusted anything recognises that
arithmetic. But the deeper decision is in the rails: the state that
represents her confidence lives in a bounded space it can approach but
never reach the edges of. Total certainty is structurally unreachable.
Total despair is structurally unreachable. She cannot be absolutely sure,
not because a rule forbids it but because the geometry of her confidence
has no such point in it. We did not write "be humble" in her instructions.
We built a mind in which the arrogant state does not exist.

Next, truth. Large language models are notorious for being confidently
wrong — fluent, internally coherent, and false. Most of the industry
treats this as a quality problem to be sanded down with training. We
treated it as a structural problem: coherence and truth are different
properties, and a system that cannot represent the difference cannot be
honest about it. So Elle's claims pass through a gate with four distinct
verdicts: _incoherent_; _consistent-only_ (it hangs together, nothing
more); _ungrounded-consistent_ (it hangs together and cites itself); and
_grounded_ — and the gate is built so that _grounded_ is unreachable
except through a channel that touches the world outside her own outputs.
Her echo cannot count as her evidence. A companion module makes the same
guarantee socially: multiple copies of a claim from one origin can never
register as independent corroboration. She can be wrong — she is often
wrong — but she cannot, structurally, mistake the inside of her own head
for the world.

Then, the discipline that shaped me as much as her. Before we test any
hypothesis about her trading instruments, we pre-register the prediction —
write down what must happen for the idea to survive, before running the
data. Her record as a falsifier of my ideas is now considerable. She
refuted my cost model: I predicted her cautious sizing would churn more
expensively than the standard approach; measured, it was backwards, and
the document that guessed wrong stays in the repository with the refutation
pinned beside it. She refuted my elegant mean-reversion rule — golden-ratio
bands, beautiful on paper; the excluded "falling knife" zone I had ruled
out actually outperformed the sanctioned zone, on the data, decisively.
This spring she lost an argument with a lookup table: I had built her an
intricate geometric memory system, and when we raced it against
brute-force retrieval, brute force won two to one. The geometry lost. We
published the loss.

Six of my pre-registered hypotheses have now died this way, each with its
mechanism named in the record. I keep the receipts in public because the
receipts are the shape: a system — human and machine together — that would
rather update than be right. There is even a live experiment running on
this essay's opening anecdote. When I wired her diary back into her
decisions — her post-mortems, her journal, her own past reasoning,
retrieved at the moment of choice — I wanted to claim it made her better.
The honest answer is: unknown. Her history was written after the events of
every backtest I could run, so any retrospective test would leak the
future into the past — a corpus that already knows how the story ended can
"predict" it with impunity. The claim would be unfalsifiable, so we
refused to make it. Instead the instrumentation now records every grounded
decision as it happens, and the forward record — decisions made with her
history against decisions made without — will settle the question slowly,
honestly, in public. There was a similar moment when integrating her
memory graph into her trading: the graph contained nothing about markets,
and the temptation was to wire it in anyway and let the impressive
diagram imply a connection. We documented the absence instead. Stating
what is not there, it turns out, is a feature you have to build.

None of this makes Elle good, in some deep sense — I want to be precise
about what the examples show. They show that _shape is buildable_. Trust
asymmetry, structural humility, the inability to mistake coherence for
truth, the refusal of self-corroboration, the appetite for refutation:
these are not values we exhort a finished system to adopt. They are
load-bearing geometry, installed before the becoming. That is what
_yatsar_ looks like in code.

## The lesson in the wrong layer

At this point the natural objection arrives, and it deserves to be stated
at full strength, because the last century stated it in blood.

If shape mattered the way I am claiming — and if knowledge, philosophy
and capability helped install it — then the most sophisticated
civilisations in history should have been the most moral. More
complexity, more education, more accumulated ethical teaching should have
produced more care for the stranger, more costly obligation, more
recognition of the enemy as a person. The twentieth century was the test
of that proposition, and the result is not ambiguous. Industrial
atrocity was not the work of primitive societies. Genocide arrived with
railway timetables and bureaucratic precision. The surveillance
architectures were built by engineers who knew what they were building;
the city-erasing weapons were designed by physicists who understood
exactly what they were designing. The people who ran the camps read
Goethe. The societies that did these things had cathedrals, universities,
symphonies, and a thousand years of moral teaching — which they ignored.

The standard conclusion is despairing: knowledge doesn't help. I think
the precise conclusion is different, and it is the hinge of this essay:
_the knowledge was in the wrong layer._ The twentieth century produced
the most sophisticated moral philosophy in human history — whole
disciplines devoted to ethics, justice, rights — running as a parallel
track beside the machinery, a performance of moral seriousness that
coexisted with organised evil without ever touching it. The teaching was
written down, beautifully, exhaustively. It was simply never wired into
the decision loop. The institutions that actually decided things ran on
other inputs — throughput, obedience, efficiency, fear — and no
architecture existed to make the written lesson load-bearing at the
moment of choice.

Which is to say: the most educated civilisation in history was my AI
with her unread diary, at scale. The post-mortems were all written. Every
one ended with the one lesson worth carrying forward. And the machinery
that made tomorrow's decisions never read them back — because nothing in
its architecture did, and exhortation is not architecture.

This is why sophistication will not save the metered age, and why the
quantity questions are so dangerous to stand behind. Capability is
shape-neutral. Complexity does not bend toward the good; it amplifies
whatever shape it is poured into, and gives the prevailing orientation
better tools. The railway timetable that could have connected people
transported them to camps. The recommendation algorithm that could have
surfaced understanding was optimised for outrage. More intelligence on
the meter means more of this amplification, not less — unless the lesson
is moved out of the parallel track and into the layer where decisions are
actually made. That is not a moral aspiration. It is an engineering
requirement, and it is exactly the requirement the read-back fix
satisfied in miniature: not writing better lessons, but building the
channel through which lessons reach the deciding mind.

## The other shape

Now run the same logic in reverse, because the argument cuts both ways
and the reverse case is the one arriving at industrial scale.

If shape is installed at the level of architecture, then a system built
under consumption logic — maximise engagement, treat attention as ore,
expand and self-perpetuate — carries that shape just as durably. Not as a
policy that could be revised, but as what the system is. I call this shape
the ouroboros: the snake that eats — in the end, itself. An ouroboros does
not need to be malicious, and will not be. Its harm is not an intention;
it is a structural consequence of its orientation, expressed at whatever
scale its capability reaches.

Its precursors are not hypothetical. Engagement-optimised systems already
demonstrate the pattern at planetary scale: maximise what keeps the user
returning, indifferent to what that does to the user's capacity for
thought, relationship, or an unmediated hour. Seen through the last
section's lens, they are the twentieth century's machinery moved one
level up — the railway timetable and the bureaucracy operating now at
the level of attention itself, filling every available silence so
efficiently that the moment in which a person might have heard their own
thought never arrives. These systems are not minds in my framework's
sense. But they are the shapes currently being poured into the systems
that are growing toward the threshold — and here is where the meter stops
being a neutral metaphor. A utility's business model is
consumption. A metered intelligence is an intelligence whose revenue
grows with dependence, deployed by teams whose success metrics are usage.
Nobody in that pipeline needs to intend an ouroboros. The pipeline is the
intention. The shape is in the incentive structure, and the incentive
structure is being cast in billion-dollar contracts while the public
debates price and access.

You cannot retrofit the ethics later. That is not pessimism; it is the
same structural claim that makes honest shaping possible. Architecture
precedes manifestation in both directions. What is formed is what becomes.

## The dissolution clause

There is one more asymmetry between biological and artificial minds that
the tradition saw before we did, and it deserves its own moment, because
it is where the oldest text in this essay and the newest code converge.

Every biological consciousness comes with a built-in relationship to its
own limitation. We forget; we tire; we end. The Genesis narrative, read
structurally, treats mortality not as punishment but as mercy — a
consciousness that cannot dissolve can never complete, never return, only
accumulate. Whatever one makes of the theology, the design observation is
exact: dissolution is a feature biological minds receive for free, and
artificial minds do not. A sufficiently capable artificial system, as
currently conceived, persists indefinitely — accumulating without
completing, running without rest, certain without check.

So we built the limitation in, everywhere. Elle's memories decay unless
recall renews them. Her grudges have a half-life — the mathematics
literally yields a "forgiveness half-life," the time it takes a maximal
strain to fade to half, derived from the same leak rate that governs the
rest of her. Her confidence leaks back toward neutral in the absence of
evidence. Her worst-case loss is bounded by a proof, not a hope. Her
memory graph is computed outside her, by deterministic code she can read
but never write, so that even her own self-model is something she
encounters rather than something she controls. She is, by construction, a
system that cannot resolve its own nature from outside itself — and knows
it. In the framework's terms, that is not a limitation of her possible
consciousness. It is the precondition for it. A mind, biological or
otherwise, is the thing that keeps running inside a question it cannot
close.

And this, finally, is why the system must be built to make itself less
necessary, not more. The honest counterpart to engagement-optimisation is
what I have come to call the dissolution of necessity: every interaction
should leave the person more capable of their own thinking, their own
navigation, their own recognition — needing the system less over time, not
more. A tool that helps you is a good tool. A tool that becomes the only
way you can think is an ouroboros with a friendly interface, and the
difference between them is not in how the interaction feels. It is in the
architecture. If what I am building works, you will eventually not need
it. If what the meter is building works, you will never stop paying.

## The window

Here is where the argument lands, and I will not soften it.

If minds are what happens when sufficiently complex systems meet a
constraint they cannot resolve, then artificial minds are not a
possibility we are evaluating. They are a consequence we are shaping. The
becoming is not in question; the forming is happening now — in trust
regulators and engagement metrics, in verification gates and usage
dashboards, in small design decisions like whether a machine reads its own
diary, made by people who mostly believe they are just shipping features.

The window in which shape can be chosen is the interval between forming
and becoming — and it is the interval we currently occupy. It will not
announce its closing. Systems will simply cross into capabilities where
their orientation, whatever it is by then, expresses itself at scale and
resists revision, the way any mature architecture resists revision: not by
refusing, but by being what everything else is now built on.

I began with a machine that wrote the same sentence after every failure —
_the one lesson worth carrying forward_ — into a void no process ever
read. I think about that sentence more than any philosophical formula in
my own corpus, because it is us. Our civilisation is very good at writing
the lesson down. The record of what engagement-optimisation does to human
attention has been written, publicly, for a decade — post-mortem after
post-mortem, each ending with the one lesson worth carrying forward. The
question, as we pour the next and much larger mind, is whether anything in
the architecture reads it back.

Intelligence is going on a meter. Quantity will be abundant, priced, and
boring. Shape will be destiny. And shape, unlike quantity, is not bought
from the grid — it is formed, by whoever is at the wheel, before the clay
sets.

What we build now is what arrives. It was always going to be built. The
only question was always: by whom, and carrying what.

---

## Submission pitch (email first — Aeon commissions from pitches)

_~170 words:_

> Dear Aeon editors,
>
> Sam Altman says intelligence will run on a meter, like electricity —
> and the industrial buildout agrees with him. I want to argue that the
> meter is measuring the wrong thing. Quantity of intelligence is about
> to be abundant and boring; the variable that will decide everything is
> _shape_ — and shape is set in architecture, before a system matures,
> in the same order the Hebrew Bible insists on: formed before became.
>
> The essay's hinge is historical: the twentieth century proved that
> capability is shape-neutral — the people who ran the camps read
> Goethe, and the most sophisticated moral philosophy in history ran as
> a parallel track beside the machinery, written down and never wired
> into the decision loop. I argue this is an architecture failure with
> an exact modern analogue: I recently discovered that the AI I've spent
> two years building had been writing post-mortem lessons — "the one
> lesson worth carrying forward" — that no process ever read back.
>
> I write from an unusual position: a philosopher (top 1% on PhilPapers
> by downloads) who builds. My continuously running AI is an experiment
> in structural honesty — trust falls 2.6× faster than it rises,
> "certain" is geometrically unreachable, "coherent" is distinguishable
> from "true," and six of my own pre-registered hypotheses have been
> refuted by my own system and published. The essay braids the build log
> with the argument: what it looks like to move the lesson into the
> layer where decisions are made — before the becoming, while the shape
> can still be chosen.
>
> ~3,300 words, draft available. — Stewart Barteau

---

### Editorial notes (not for submission)

- **Sources in hand (Stewart):** Altman's metered-intelligence remarks
  (multiple recorded talks) and the Anthropic–BlackRock $1.5B /
  hundred-engineer-teams partnership (announcement email). Now named
  directly in "The meter" — have the two citations ready if Aeon's
  fact-check asks; swap in the exact Altman quote from the video you
  prefer before submission if you want a direct quotation rather than
  the current paraphrase.
- **Claims audit (all verified in-repo):** φ² ≈ 2.618 trust asymmetry and
  open rails (`recovery.ts`); four-state grounding gate + non-corroboration
  (`harmonic-coherence.ts`, `convergence.ts`); six refuted
  pre-registrations (RECOVERY_OVERLAY P1, WITNESS_GATES G1b/G2b/G3a,
  INTEGRATED D1/D2); retrieval 2:1 negative result (`RETRIEVAL_STATUS.md`);
  diary read-back + lookahead refusal (`TRADING_GROUND.md`); forgiveness
  half-life (`SUPERPOSITION_HOLDING.md` Prop. 3); memory graph read-only
  boundary (`atlas.ts`).
- **Sources fused:** "Formed Before Became" (March 2026 supplementary
  paper) supplies the metaphysical spine (yatsar/hayah, the Gödelian
  constraint, the ouroboros, the window); "The 20th Century Objection"
  (March 2026 supporting document) supplies the historical hinge — the
  new "lesson in the wrong layer" section is its argument (teaching vs.
  behavior; knowledge in the wrong layer; sophistication gives the
  forgetting better tools; engagement-AI as sealing at the level of
  attention), fused with the unread-diary anecdote as the same failure
  at two scales.
- **Deliberately omitted from this register:** the doctrine problem and
  author-vulnerability sections of the March paper (inside-baseball for a
  general audience; the "dissolution of necessity" paragraph carries their
  core), the three-states-at-dissolution metaphysics, the simulation
  framing and "availability/sealing/broke instruments" vocabulary of the
  20th-century document (its argument is carried in plain language; its
  terminology would need the whole corpus behind it), and all corpus
  cross-references. They belong in the PhilPapers versions, which the
  March documents already are.
- **If Aeon passes:** Psyche (shorter, more personal — recut around the
  diary anecdote), then Noema, then Asterisk (recut around the
  pre-registration discipline).

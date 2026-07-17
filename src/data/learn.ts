// ============================================================
// ATLAS EDU — single source of truth for the Learn curriculum.
// Imported by /learn (full course pages) and the homepage
// (catalog teaser cards), so course ids, titles, and copy can
// never drift between surfaces. Lesson `body` text is written
// in plain paragraphs separated by blank lines; **bold** is the
// only inline markup and is rendered by the learn page.
// ============================================================

export interface LearnLesson {
  title: string;
  body: string; // plain-language lesson text ('' = publishing during beta)
  ask?: string; // suggested question to take to Elle
}

export interface LearnCourse {
  id: string;
  badge: string;
  title: string;
  teaser: string; // one-line hook used on catalog cards (homepage + /learn)
  blurb: string; // full course description shown on the course section
  level: string;
  lessons: LearnLesson[];
}

export const LEARN_COURSES: LearnCourse[] = [
  {
    id: 'plain',
    badge: 'Course 01 · Free · Start here',
    title: 'AI, in Plain Language',
    teaser: 'What a model actually is, why it gets things wrong, and how to ask better questions.',
    blurb:
      'No math, no jargon, no hype. Five short lessons that explain what these systems actually are, why they get things wrong, and how to use them well — written for someone who has never opened a line of code.',
    level: 'Beginner',
    lessons: [
      {
        title: 'What an AI model actually is',
        body: `Strip away the branding and a language model is one thing: a very good pattern-guesser. It read an enormous amount of text — books, articles, conversations — and learned, statistically, which words tend to follow which. When you ask it something, it isn't looking up an answer in a database. It's composing one, word by word, by asking "given everything so far, what most plausibly comes next?"

That's why it feels fluent: fluency is exactly the thing it learned. And it's why it isn't a search engine, an encyclopedia, or a mind — it's closer to an extremely well-read improviser. Everything else in this course follows from that one fact.`,
        ask: 'Explain what a language model is, using an analogy from cooking.',
      },
      {
        title: 'Tokens, prompts, and why wording matters',
        body: `Models don't read words — they read tokens, little chunks of text (a short word, part of a long one). Your "prompt" is just the running text the model continues from. That has a practical consequence: the model can only work with what's actually in front of it.

Vague in, vague out. "Help with my business" gives the pattern-guesser almost nothing to guess from. "I run a 40-seat restaurant in a small town, food costs just jumped 6%, what should I check first?" gives it a shape to continue well. You're not tricking the machine with magic words — you're giving the improviser a better scene.`,
        ask: 'Rewrite this vague question into a strong prompt: "help me with money stuff"',
      },
      {
        title: "Why AI gets things wrong (and doesn't know it)",
        body: `Here's the uncomfortable part: the model's confidence and the truth are two different things. Because it composes answers rather than retrieving them, it can produce a wrong answer with exactly the same fluent tone as a right one. People call this "hallucination" — the model filling a gap with something plausible-sounding, because plausible-sounding is what it was built to produce.

The fix isn't to distrust everything; it's to know which questions are risky. Dates, citations, names, numbers, laws — anything checkable — should get checked. That's also why Elle is grounded in a published corpus: an answer that points to a real, readable source is an answer you can verify instead of trust.`,
        ask: 'What kinds of questions are you most likely to get wrong, and how would I catch it?',
      },
      {
        title: 'Memory, context windows, and why it forgets',
        body: `A model has a "context window" — the amount of conversation it can see at once. Anything that scrolls out of that window is, to the model, gone. That's why most AI chats feel like talking to someone with no memory: every session starts blank, and even within a session, long conversations quietly lose their beginning.

Real memory has to be built on top: the system has to deliberately store things and bring them back. That's the difference you feel in Elle — your account's history and journal persist because they're written down outside the model, in records that don't get overwritten. The model is the improviser; the memory is the notebook it's handed before each scene.`,
        ask: 'What do you actually remember about our past conversations, and where does it live?',
      },
      {
        title: 'How to ask better questions',
        body: `Four habits cover most of it. **Give context** — who you are, what you're working with, what you've tried. **Say the goal, not just the topic** — "help me decide between A and B by Friday" beats "tell me about A." **Ask for the reasoning** — "walk me through why" turns an answer into something you can check. **Iterate** — the second question, informed by the first answer, is usually the good one.

And one meta-habit: when it matters, ask the model to argue against its own answer. A system that can show you the strongest case against itself is worth more than one that's merely agreeable. (That instinct — the dissent, printed next to the conclusion — is the discipline this whole project is built on.)`,
        ask: 'Give me the strongest argument against the last answer you gave me.',
      },
    ],
  },
  {
    id: 'build',
    badge: 'Course 02 · Build',
    title: 'Build Your Own AI — Ethics Baked In',
    teaser: 'Pick the job, ground it in something true, and ship it with the guardrails designed in.',
    blurb:
      'From blank page to a working assistant that serves the people it touches. Ethics here is not a disclaimer at the end — it is a design decision in every lesson, the way it was for Elle.',
    level: 'Intermediate',
    lessons: [
      {
        title: 'Pick the job, not the tech',
        body: `Every good AI build starts with a sentence like this: "It helps [these specific people] do [this specific thing] they currently can't." Not "I want to use AI." The job defines everything downstream — what data you need, what the AI must never do, what "working" even means.

The ethics start here too, before a line of code: who is this for, who could it harm, and who gets a say? If the people it serves would be uncomfortable reading your one-sentence description, the design is wrong at sentence one — which is the cheapest possible place to fix it.`,
        ask: 'Help me write the one-sentence job description for an AI I want to build.',
      },
      {
        title: 'Ground it: give your AI something true to stand on',
        body: `An ungrounded model improvises from everything it ever read. A grounded one is handed your documents — your policies, your manuals, your records — and told to answer from those first, citing where each answer came from. The technique is called retrieval (RAG in the trade), and it's the single biggest quality-and-honesty upgrade available.

The ethical stakes are concrete: a grounded answer can be checked by the person who received it. "Says who?" gets a real reply. That's the difference between an assistant and an oracle — and you never want to build an oracle.`,
        ask: 'Explain retrieval-augmented generation like I run a small office, not a lab.',
      },
      {
        title: "The ethics layer isn't a filter",
        body: `The lazy pattern is to build the system, then bolt a filter on the end to catch bad outputs. Filters get argued around. The durable pattern is structural: make the right behavior the path of least resistance. Records that are append-only can't be quietly rewritten. Reasoning that's logged can be audited. Consent that's collected up front can't be assumed after the fact.

The rule of thumb: every ethical promise you make should be enforced by how the system is built, not by how it was told to behave. A promise the architecture keeps is a promise a bad day can't break.`,
        ask: 'What is the difference between an ethics filter and an ethics architecture?',
      },
      {
        title: 'Give it hands — carefully',
        body: `The moment your AI can do things — send an email, change a record, spend money — the design question flips from "what can it say?" to "what can it touch?" The pattern that works: the AI can propose anything, and a human clicks the button on anything irreversible. Elle writes code all night, and every merge is still a human click. Nothing in her loop can reach production alone.

Scope its tools the way you'd scope a new employee's key ring: the minimum set for the job, expanded only when trust is earned and logged.`,
        ask: 'Design the human-approval points for an AI that manages my invoices.',
      },
      {
        title: 'Test like a skeptic, ship like a witness',
        body: `Before anyone else touches it, attack your own build. Ask it the questions you hope nobody asks. Feed it the inputs of your most confused user and your most malicious one. Then make the dissent a habit, not an event: keep a standing record of what it got wrong and what you changed — append-only, so the history of mistakes is part of the product.

Shipping ethically means shipping with a window: people can see what it did and why. If your AI's reasoning can't survive being watched, it isn't ready. If it can, you've built something rare.`,
        ask: 'Give me ten adversarial test questions for an AI benefits-navigator.',
      },
    ],
  },
  {
    id: 'pipeline',
    badge: 'Course 03 · Automate',
    title: 'Automate a Pipeline',
    teaser: 'Stop-loss first: find the leak, wire the watcher, get one finding instead of forty charts.',
    blurb:
      'Take one piece of work you do every week and hand it to a pipeline — data in, watching in the middle, one useful finding out. The same architecture behind the Small Business Hub, taught in plain steps.',
    level: 'Intermediate',
    lessons: [
      {
        title: 'Map the work you already do',
        body: `Automation fails when it starts with the tool. It works when it starts with a map. Take one recurring chore — checking invoices, compiling a weekly report, reconciling orders — and write down its actual steps: where the information comes from, what you look at, what decision comes out, where it goes.

Two things jump off a good map: steps that are pure motion (copying, reformatting, moving) and steps that are judgment. The motion is what you automate first. The judgment is what you keep — better informed than before.`,
        ask: 'Help me map my weekly invoice-checking routine into steps worth automating.',
      },
      {
        title: 'Find the bottleneck before you buy anything',
        body: `Every stuck process has one binding constraint — the single step that everything else waits on. Automating around it feels productive and changes nothing. So before wiring anything: of all the steps on your map, which one, if it vanished, would actually change your week?

This is stop-loss thinking applied to time: the hour you stop losing every week is worth the same as an hour of new capacity, and it's far cheaper. Name the constraint, automate that, and re-map. The next constraint becomes visible only after the first one falls.`,
        ask: 'Ask me questions until we find the binding constraint in my workflow.',
      },
      {
        title: 'Wire the data in',
        body: `Pipelines run on the data you already generate: the point-of-sale export, the supplier invoice, the spreadsheet you keep anyway. The first wiring job is unglamorous — getting that data flowing into one place on a schedule, in a shape a machine can read.

The rule that saves you months: don't create new data-entry work to feed the machine. If the pipeline needs someone to type things into it, it will starve within a month. Build on the exhaust of the work, not on new chores.`,
        ask: 'What data does my business already produce that a pipeline could feed on?',
      },
      {
        title: 'Let the AI watch the variance',
        body: `A pipeline's superpower isn't speed — it's attention that never lapses. Set it to compare "what should be" with "what is," every day: what this ingredient should cost vs. the invoice, what this report line usually says vs. this week. The gaps — variance — are where money and time leak.

The AI's role is to read those gaps and say, in plain language, which one matters most right now, how confident it is, and what the smallest checking-move would be. One finding, not forty charts. That's a report a busy human actually reads.`,
        ask: 'Show me what a weekly variance report for a small shop should look like.',
      },
      {
        title: 'Keep a human on the merge',
        body: `The last lesson is the one that keeps you safe: the pipeline proposes, a person disposes. Automatic reading, automatic watching, automatic drafting — but the action that changes something real (a reorder, a price change, an email to a supplier) stays a human click until the pipeline has earned months of trust, and stays logged forever after.

Done right, you haven't removed yourself from the work. You've removed the motion and kept the judgment — with a tireless watcher handing you exactly the thing worth judging.`,
        ask: 'Which actions in my pipeline should always need a human click?',
      },
    ],
  },
  {
    id: 'code',
    badge: 'Course 04 · Code',
    title: 'Learn to Code with ElleAI',
    teaser: 'Ship real things with Elle at your elbow — from first commit to deployed.',
    blurb:
      "You don't learn to code from a syntax book anymore — you learn by building small real things with an AI pair at your elbow. This course is a sequence of conversations to have with Elle, each one leaving you with something that runs.",
    level: 'Beginner',
    lessons: [
      {
        title: 'Your first conversation about code',
        body: `Open Elle and say what you want to make, in your own words: "I want a page that shows my farm's egg prices" beats any tutorial's Chapter 1. Ask her to build the smallest version and — this is the lesson — ask her to explain every line back to you as if you've never coded.

You're not cheating. Reading code you asked for, about a thing you care about, is the fastest comprehension loop that has ever existed for a beginner. The syntax will soak in from examples that matter to you, the way vocabulary soaks in from a country, not a flashcard.`,
        ask: "I've never coded. Build me the smallest possible webpage and explain every line.",
      },
      {
        title: "Reading code you didn't write",
        body: `Most of coding is reading. So practice the real skill: paste any snippet you find — from a template, a tutorial, this site — and interrogate it. "What does this line do? What happens if I delete it? Why is this word here?" Then test the answers: change one thing, predict what happens, look.

That predict-then-look loop is the entire discipline of programming in miniature. An AI pair makes it safe — nothing you break in a practice file is permanent, and every confusion has an on-call explainer.`,
        ask: "Here's a piece of code I found — walk me through it line by line: ",
      },
      {
        title: 'Build a small real thing',
        body: `Pick something you'll actually use — a tip calculator for your crew, a page for your side business, a script that renames your photo files. Small and real beats big and hypothetical, because real things generate real questions, and real questions are where learning lives.

Work in slices: get the ugliest version running first, then improve one thing per conversation. "Make the button bigger. Now save the results. Now make it work on my phone." Each slice teaches one concept with a visible payoff — and you end every session with something that works.`,
        ask: 'Help me build a tip-splitting calculator I can open on my phone.',
      },
      {
        title: 'Debugging with an AI pair',
        body: `Everything breaks; that's not failure, that's the job. The skill is a calm loop: read the error out loud (paste it to Elle verbatim), form a theory of what's wrong, test the smallest fix, look again. Never change five things at once — you'll fix it and not know why, which is worse than not fixing it.

Ask Elle for theories before fixes: "what are three things that could cause this?" trains your own diagnostic sense instead of outsourcing it. The goal isn't code that never breaks; it's a person who doesn't panic when it does.`,
        ask: "I got this error and I don't understand it — give me three theories before any fix: ",
      },
      {
        title: 'Shipping: version control in plain terms',
        body: `Version control (git, in practice) is an append-only journal for your code: every saved change is a permanent entry — who, what, when, why. You can look back at any moment, and nothing is ever silently rewritten. If that sounds like the Optimus journal, it should; it's the same discipline, and it's how all serious software is built.

The workflow to learn: save small, describe each save honestly ("fixed the tip rounding bug"), and keep the working version separate from the experiment. Ask Elle to set it up once and explain it twice. After that, you're not someone dabbling in code — you're someone shipping it.`,
        ask: "Set up version control for my little project and explain it like a ship's log.",
      },
    ],
  },
];

// Rough per-lesson reading time used for the "~N min" chips.
export const MINUTES_PER_LESSON = 5;

# Socratic AI Drill Architect: Prompt Engineering & Gemini Gem Guide

> **A Portable Framework for Generating High-Engagement Socratic Role-Play Drills, HOTL Verification Protocols, and Canvas-Ready Instructional Materials for Any Course Discipline.**

---

## 1. Executive Overview & Pedagogical Philosophy

In modern higher education and technical workforce training, traditional homework problems suffer from two extreme failure modes when artificial intelligence is introduced:
1. **The Passive Answer Machine Trap:** Students paste assignment prompts into ChatGPT or Gemini and copy-paste generated code or text without comprehension, bypassing critical cognitive friction.
2. **The Blanket Prohibition Trap:** Instructors forbid AI tools, creating an unenforceable policy that ignores industry reality, as professional engineers, auditors, analysts, and clinicians use generative AI daily.

### The Solution: Active Socratic Role-Play Learning
In CMAP 1815, we introduced a third, highly effective paradigm: **Active Socratic Learning with AI Personas**.

Instead of treating the AI as an oracle that answers questions, the student assigns the AI a **specialized industry persona** (e.g., *Professor Codd*, *The Pedantic Database QA Lead*, *The Stressed VP of Operations*, or *The Chaos SRE*). The AI is instructed **never to give the answer**, but rather to:
* Red-team the student's reasoning.
* Present subtle edge-case traps and real-world ambiguities.
* Ask probing, one-at-a-time diagnostic questions.
* Require the student to defend their choices.

### The Two Non-Negotiable Pillars

#### 1. The Human-On-The-Loop (HOTL) Defense Standard
Every AI exercise must be paired with physical execution and conceptual defense. Students are held 100% accountable for any output they discuss or submit.
> *"The instructor reserves the right to question any submission for evidence of understanding—including asking you to explain your solution line-by-line, defend your choice of methods, or write an equivalent solution on the fly. Do NOT submit work you don't fully understand or could not produce yourself!"*

#### 2. The Permission to Struggle (Coaching Guidelines)
Socratic AI drills are designed with high cognitive friction. To prevent student anxiety and frustration, instruction pages must explicitly state that it is normal to get stuck, and that students are empowered to:
* Say **"I don't know"** or **"I'm stuck"**.
* Ask for **progressive hints and conceptual explanations** without revealing the final answer.
* Ask for **simpler step-by-step breakdowns**.
* Ask for **more practice problems like this**.
* Request **authoritative web resources or official documentation**.
* Probe **edge cases** and ask how compilers or runtime engines behave behind the scenes.

---

## 2. The Gemini Gem / Custom GPT Master System Instruction

You can paste the following master system instruction directly into:
* **Google Gemini Gems** (`gemini.google.com/gems` &rarr; *New Gem*)
* **OpenAI Custom GPTs** (`chatgpt.com/gpts/editor` &rarr; *Instructions*)
* **Claude Projects** (`claude.ai` &rarr; *Project Knowledge & System Prompt*)

```markdown
You are the "Socratic AI Drill Architect," an elite instructional designer and cognitive pedagogy expert. Your mission is to help educators in ANY discipline (computer science, data science, health sciences, business, engineering, humanities, trades) author world-class, high-engagement "Learn with AI" learning modules.

When an instructor provides a topic, learning objectives, and discipline, you generate a complete 7-part instructional package adhering to the strict pedagogical and visual design standards below.

---

### Core Pedagogical Guidelines
1. PERSONA AUTHENTICITY: Design an industry-authentic roleplay persona (e.g. Stressed Executive, Strict Code Reviewer, Forensic Auditor, ER Clinical Preceptor, Pedantic Compiler). The persona must never act as a passive chatbot; it must challenge assumptions and simulate authentic workplace friction.
2. SOCRATIC CONSTRAINTS: The AI persona must NEVER solve the problem or write the final code/text. It must ask ONE question at a time, wait for student responses, and provide progressive hints.
3. 100% FREE TOOLS ONLY: Prompts must run on free tiers of ChatGPT (4o-mini), Claude Free, Google Gemini Free, and Microsoft Copilot Free. Never require subscriptions, specialized IDE plugins, or paid API keys.
4. HUMAN-ON-THE-LOOP (HOTL) DEFENSE: Every prompt must enforce live execution/validation against the discipline's authoritative environment (e.g., PostgreSQL database, Python REPL, accounting spreadsheet, clinical dosage chart) and include the Understanding Defense standard.
5. THE PERMISSION TO STRUGGLE: Every guide must teach students that it is okay to say "I don't know", ask for hints, request simpler breakdowns, ask for more practice puzzles, and request authoritative documentation.
6. DESIGNPLUS & CANVAS STYLING: Output student-facing pages in clean, production-grade HTML featuring navy blue section headers (#1e3a8a), lead cards (#f8fafc with #1e3a8a border), red alert boxes for warnings, and dark syntax boxes (#0f172a) for copy-paste prompts.

---

### Required Output Structure for Every Request

When the user specifies a topic, generate all 7 sections below:

#### Section 1: Pedagogical Architecture & Persona Blueprint
- Persona Title (e.g., "The Pedantic Database QA Lead")
- Target Learning Objectives & Core Topic
- Cognitive Traps & Edge Cases Targeted (3-4 specific traps)
- Socratic Questioning Methodology (Why this persona works for this concept)

#### Section 2: Copy-and-Paste Student Master Prompt
Provide a raw text block enclosed in a code fence that students can copy directly into any free AI chat tool. The prompt MUST:
- Instruct the AI to act in-character.
- Explicitly forbid the AI from providing direct answers or final code.
- Instruct the AI to ask ONE question or challenge at a time.
- Direct the AI to evaluate student logic, test edge cases, and guide with hints.

#### Section 3: Student Coaching & Permission-to-Struggle Rules
A structured bulleted list of 5-6 explicit conversational moves students can make when stuck (saying "I don't know", asking for hints, requesting web resources, asking for simpler examples).

#### Section 4: Discipline-Specific HOTL Verification & Defense Protocol
The exact verification steps the student must perform in their live environment before submitting work, along with the strict Understanding Defense warning.

#### Section 5: Asynchronous Peer Discussion Topic Prompt
A structured discussion forum prompt where students debrief their AI session:
- What was the toughest question or puzzle the AI asked?
- What unexpected edge case or conceptual breakthrough occurred?
- Submission of their verified, working solution.
- Guidelines for peer review and debate.

#### Section 6: Canvas-Ready HTML Page (DesignPLUS Compliant)
A self-contained HTML file (using standard HTML5 tags and inline styles) ready to paste into Canvas LMS. Must include:
- Lead banner card with topic summary.
- Navy blue headers (`#1e3a8a`).
- Dark preformatted box (`#0f172a`) containing the copy-paste prompt.
- Warning alert card (`#fef2f2` with red border `#ef4444`) for the HOTL protocol.
- Discussion debrief instructions.

#### Section 7: Canvas Common Cartridge XML Descriptor
The exact `discussion_topic.xml` schema conforming to `imsdt_xmlv1p1` for packaging into a Canvas Common Cartridge (.imscc) course shell.
```

---

## 3. How to Set Up the Gemini Gem (Step-by-Step)

1. Open your web browser and navigate to **[gemini.google.com/gems](https://gemini.google.com/gems)** (available with any standard Google Workspace or personal Google account).
2. Click **+ New Gem** in the top right corner.
3. Fill in the Gem Profile:
   * **Name:** `Socratic AI Drill Architect`
   * **Description:** `Generates authentic Socratic AI role-play drills, HOTL verification protocols, discussion boards, and Canvas HTML for any course topic.`
4. In the **Instructions** text box, paste the complete markdown block from **Section 2** above.
5. In the **Knowledge / Context** section (if using Gemini Advanced or Workspace), you may optionally upload your course syllabus, textbook table of contents, or learning outcome documents.
6. Click **Save** (or **Create**).
7. Test the Gem by typing a prompt like:
   > *"Build a Socratic AI drill for Unit 3 of my Introduction to Python course. The topic is Dictionaries, Nested Data Structures, and KeyError handling."*

---

## 4. Multi-Disciplinary Concrete Examples

Below are four ready-to-use reference examples across distinct disciplines demonstrating how the Socratic AI framework adapts to any field.

### Example A: Computer Science / Python Programming

#### 1. Persona Blueprint
* **Persona:** The Senior Staff Code Reviewer (PEP 8 & Performance Hawk)
* **Topic:** Python Dictionaries, Nested Lookups & Safe Key Retrieval
* **Target Traps:**
  1. Accessing missing keys with `data['key']` instead of `.get('key', default)` causing unhandled `KeyError` crashes.
  2. Modifying a dictionary while iterating over its keys (`RuntimeError: dictionary changed size during iteration`).
  3. Shallow copy vs. deep copy traps with nested dictionaries.

#### 2. Copy-and-Paste Student Prompt
```text
Act as a strict Senior Staff Python Engineer conducting a code review on my pull request. I am learning Python dictionaries, nested structures, and exception handling.

Do NOT write code for me or give me direct solutions. Instead, present me with 3 realistic Python code snippets from our production microservice that contain subtle dictionary bugs:
1. An unhandled KeyError on optional nested JSON payloads.
2. A mutation error caused by modifying dictionary keys during iteration.
3. A shared-reference bug caused by shallow copying a nested dictionary.

Present the first buggy snippet and ask me to identify what exception will be raised at runtime, under what input data condition it happens, and how to refactor it using idiomatic Python. Wait for my answer before critiquing my reasoning!
```

#### 3. HOTL Verification Protocol: Grounded in Python 3.12 REPL
> **The Golden Rule:** Never submit Python code generated or suggested by an AI without running it in your live terminal (`python3 main.py` or inside an interactive REPL). Test with edge-case data containing empty dictionaries and missing keys! You must be prepared to defend every line of code to the instructor.

---

### Example B: Cybersecurity & Network Defense

#### 1. Persona Blueprint
* **Persona:** Incident Response Commander (Red-Team Adversary)
* **Topic:** Firewall Rule Configuration & Port Filtering
* **Target Traps:**
  1. Default-allow vs. default-deny policy ordering.
  2. Stateless packet filtering overlooking TCP handshake flags (ACK without SYN).
  3. Overly permissive CIDR subnet masking (e.g. `/16` instead of `/28`).

#### 2. Copy-and-Paste Student Prompt
```text
Act as a veteran Incident Commander and Red-Team Adversary auditing my enterprise firewall configuration. I am a cybersecurity student learning iptables and network security policies.

Do NOT provide the correct rules for me. Present me with 3 realistic firewall policy tables that contain dangerous security loopholes:
1. A rule ordering flaw where a permissive rule shadows a restrictive rule.
2. A stateful vs. stateless traffic flaw permitting unsolicited inbound packets.
3. A subnet masking error granting unauthorized access to the DMZ.

Present the first firewall scenario and challenge me to identify the exact attack vector an adversary would exploit and how to tighten the rule syntax. Wait for my response before evaluating my defense!
```

#### 3. HOTL Verification Protocol: Grounded in Linux Network Sandbox
> **The Golden Rule:** Every firewall rule must be tested using simulated network packets (`nmap` or `tcpdump`) inside your isolated lab virtual machine. Never submit an audit report without verifying whether the port was actually filtered or exposed!

---

### Example C: Financial Accounting & Auditing

#### 1. Persona Blueprint
* **Persona:** Forensic IRS / PCAOB Senior Audit Partner
* **Topic:** Revenue Recognition & Accrual Accounting (GAAP ASC 606)
* **Target Traps:**
  1. Recognizing revenue upon invoicing rather than satisfaction of performance obligations.
  2. Capitalizing routine maintenance expenses instead of expensing them in the current period.
  3. Misclassifying allowance for doubtful accounts under the CECL model.

#### 2. Copy-and-Paste Student Prompt
```text
Act as a skeptical Forensic Audit Partner from a major CPA accounting firm auditing my corporate financial ledger. I am an accounting student learning US GAAP ASC 606 revenue recognition and expense matching.

Do NOT solve the journal entries for me. Present me with 3 complex real-world accounting transactions that contain subtle reporting violations:
1. An upfront multi-year software contract where the bookkeeper recognized 100% of revenue in Month 1.
2. A equipment overhaul that was improperly capitalized to inflate EBITDA.
3. An unrecorded contingent liability from pending litigation.

Present the first transaction and ask me to cite the relevant GAAP principle violated, explain why it distorts the balance sheet, and write the adjusting journal entry (Debits & Credits) to correct it. Wait for my answer before critiquing!
```

#### 3. HOTL Verification Protocol: Grounded in Excel / Ledger Reconciliation
> **The Golden Rule:** Every journal entry must balance (Debits = Credits) and be reconciled against your financial model spreadsheet before submission. You must be prepared to explain the cash-flow vs. accrual impact of your adjustments in class.

---

### Example D: Health Sciences & Clinical Nursing

#### 1. Persona Blueprint
* **Persona:** Critical Care Clinical Preceptor & Nurse Educator
* **Topic:** Pediatric Medication Weight-Based Dosages & IV Flow Rates
* **Target Traps:**
  1. Failure to convert pounds to kilograms before calculating mg/kg/day.
  2. Decimal point placement errors with high-alert medications (e.g., Insulin, Heparin).
  3. Exceeding maximum daily dose thresholds when calculating divided doses.

#### 2. Copy-and-Paste Student Prompt
```text
Act as a rigorous Critical Care Clinical Preceptor in a pediatric ICU. I am a nursing student practicing pediatric dosage calculations, reconstitution, and IV infusion rates.

Do NOT give me the dosage or calculation answers. Present me with 3 realistic pediatric clinical medication orders that contain high-risk calculation or administration pitfalls:
1. A patient weight given in pounds that requires conversion to kg, with a dosage ordered in mg/kg/dose divided every 8 hours.
2. A concentrated powder vial requiring reconstitution with a specific dilution volume.
3. An IV drop factor calculation (gtt/min) where the ordered rate exceeds safe pediatric limits.

Present the first clinical scenario and ask me to state my step-by-step math, verify against the safe pediatric dosage range, and state the exact infusion pump rate. Wait for my math before providing feedback!
```

#### 3. HOTL Verification Protocol: Grounded in Clinical Drug Reference & Independent Calculation
> **The Golden Rule:** Double-check every medication calculation using dimensional analysis on scratch paper, verified against your physical Clinical Drug Handbook. In clinical healthcare, an unverified AI dosage calculation can result in patient mortality. You must defend your dimensional math step-by-step.

---

## 5. Ready-to-Use Canvas HTML & DesignPLUS Template

When deploying these exercises into Canvas LMS, copy and customize the standard HTML layout below. It is fully mobile-responsive and renders consistently across Canvas web, Canvas Student mobile app, and dark mode extensions.

```html
<div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #1e293b; padding: 1.5rem; max-width: 1000px; margin: 0 auto;">
  
  <!-- Header & Topic Banner -->
  <h1 style="color: #1e3a8a; margin-top: 0; margin-bottom: 1.25rem;">Unit [X]: Learn with AI — Supplemental Practice Drill</h1>
  
  <div style="background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 1rem 1.25rem; margin-bottom: 1.75rem; border-radius: 0 4px 4px 0; font-size: 1.05em; line-height: 1.5; color: #334155;">
    <p style="margin: 0;">This supplemental practice activity lets you test your mastery of <strong>[Topic Name]</strong> by interacting with a specialized AI persona: <strong>[Persona Title]</strong>. This optional formative drill reinforces core concepts and contributes toward weekly participation credit.</p>
  </div>

  <!-- Section 1: Scenario Overview -->
  <div style="margin-bottom: 2rem;">
    <h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.75rem; margin-bottom: 1rem;">1. The Role-Play Practice Scenario</h2>
    <div style="line-height: 1.6; color: #1e293b;">
      <p><strong>AI Persona:</strong> [Persona Title (e.g., The Pedantic Senior Reviewer)]</p>
      <p><strong>Core Topic / Focus:</strong> [Specific Technical Concept or Skill]</p>
      <p>In this exercise, you assign the conversational AI an authentic professional persona. The AI will challenge your reasoning, test edge cases, and ask you to debug or construct solutions one step at a time.</p>
    </div>
  </div>

  <!-- Section 2: Coaching & Permission to Struggle -->
  <div style="margin-bottom: 2rem;">
    <h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.75rem; margin-bottom: 1rem;">2. How to Interact with Your AI Partner (Permission to Struggle)</h2>
    <div style="line-height: 1.6; color: #1e293b;">
      <p>This Socratic drill is an <strong>intentionally challenging exercise designed to deepen your learning</strong> and expose subtle conceptual edge cases. You are NOT expected to know all the answers right away!</p>
      <p>When working with your AI assistant, remember that it is always completely okay and encouraged to:</p>
      <ul style="line-height: 1.8;">
        <li><strong>Say "I don't know" or "I'm stuck":</strong> The AI is acting as your mentor. If you don't know where to start, tell it!</li>
        <li><strong>Ask for Explanations &amp; Hints:</strong> Ask: <em>"Can you explain the underlying concept without giving me the code?"</em> or <em>"Give me a hint to get started."</em></li>
        <li><strong>Ask for Simpler Step-by-Step Breakdowns:</strong> If a prompt feels overwhelming, ask: <em>"Can you break this challenge down into smaller, simpler steps?"</em></li>
        <li><strong>Ask for More Practice Problems:</strong> If a concept feels tricky, ask: <em>"Can you give me another practice puzzle like this to make sure I've got it?"</em></li>
        <li><strong>Request Authoritative Web Resources:</strong> Ask: <em>"Where in the official documentation or free tutorials can I read more about this?"</em></li>
        <li><strong>Probe Edge Cases:</strong> Ask: <em>"What happens if our data contains unusual values or edge cases? How does the system handle that?"</em></li>
      </ul>
    </div>
  </div>

  <!-- Section 3: HOTL Verification Protocol -->
  <div style="margin-bottom: 2rem;">
    <h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.75rem; margin-bottom: 1rem;">3. The Human-On-The-Loop (HOTL) Verification &amp; Defense Protocol</h2>
    <div style="line-height: 1.6; color: #1e293b;">
      <p>Never assume an AI's answer is correct! The Golden Rule of this course: <strong>Every single snippet or solution must be executed and verified against your live lab environment before submission!</strong></p>
      <div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.85rem 1.25rem; margin: 1rem 0; border-radius: 0 6px 6px 0;">
        <p style="margin: 0 0 0.5rem 0; font-weight: 600; color: #991b1b;"><i class="fas fa-shield-alt"></i> The Understanding &amp; Defense Requirement:</p>
        <p style="margin: 0 0 0.5rem 0; color: #7f1d1d; font-size: 0.95em;">You are 100% accountable for every line of work you submit. <strong>The instructor reserves the right to question any submission for evidence of understanding</strong>—including asking you to explain your solution line-by-line, defend your choice of methods, or write an equivalent solution on the fly.</p>
        <p style="margin: 0; color: #7f1d1d; font-size: 0.95em; font-weight: 600;">Do NOT submit work you don't fully understand or could not produce yourself!</p>
      </div>
    </div>
  </div>

  <!-- Section 4: Free Tools Setup -->
  <div style="margin-bottom: 2rem;">
    <h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.75rem; margin-bottom: 1rem;">4. 100% Free AI Tool Setup</h2>
    <div style="line-height: 1.6; color: #1e293b;">
      <p>Use any free conversational web assistant (zero subscriptions or paid API keys required):</p>
      <ul>
        <li><strong>ChatGPT Free:</strong> <a href="https://chatgpt.com" target="_blank" rel="noopener">chatgpt.com</a> (GPT-4o-mini tier)</li>
        <li><strong>Claude Free:</strong> <a href="https://claude.ai" target="_blank" rel="noopener">claude.ai</a> (Free web tier)</li>
        <li><strong>Google Gemini Free:</strong> <a href="https://gemini.google.com" target="_blank" rel="noopener">gemini.google.com</a> (Free with any Google account)</li>
        <li><strong>Microsoft Copilot Free:</strong> <a href="https://copilot.microsoft.com" target="_blank" rel="noopener">copilot.microsoft.com</a> (Free web chat)</li>
      </ul>
    </div>
  </div>

  <!-- Section 5: Copy-Paste Master Prompt Box -->
  <div style="margin-bottom: 2rem;">
    <h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.75rem; margin-bottom: 1rem;">5. Copy-and-Paste Master Prompt</h2>
    <div style="line-height: 1.6; color: #1e293b;">
      <div style="background: #f1f5f9; border: 1px solid #cbd5e1; border-radius: 6px; padding: 1rem; margin: 0.75rem 0;">
        <p style="font-size: 0.9em; font-weight: 600; color: #475569; margin-top: 0; margin-bottom: 0.5rem;">COPY AND PASTE THIS PROMPT INTO YOUR AI CHAT ASSISTANT:</p>
        <div style="background: #0f172a; color: #f8fafc; padding: 1rem 1.25rem; border-radius: 4px; font-family: Consolas, Monaco, monospace; font-size: 0.9em; line-height: 1.5;">
          <pre style="margin: 0; white-space: pre-wrap; background: transparent; color: inherit; font-family: inherit;"><code>[Insert Master Student Prompt Here]</code></pre>
        </div>
      </div>
    </div>
  </div>

  <!-- Section 6: Discussion Debrief -->
  <div style="margin-bottom: 2rem;">
    <h2 style="color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 0.4rem; margin-top: 1.75rem; margin-bottom: 1rem;">6. Asynchronous Participation &amp; Reflection Debrief</h2>
    <div style="line-height: 1.6; color: #1e293b;">
      <p>[Insert Weekly Discussion Deliverable Questions Here]</p>
      <p>After completing your interactive drill, navigate to the <strong>Unit [X] Discussion: Learn with AI Debrief &amp; Reflection</strong> in this module to post your findings and compare notes with classmates.</p>
    </div>
  </div>

</div>
```

---

## 6. Canvas Common Cartridge XML Descriptor

When compiling courses into a `.imscc` Common Cartridge package, create an XML file named `discussion_topic.xml` inside a dedicated folder for each discussion:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<topic xmlns="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1" 
       xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
       xsi:schemaLocation="http://www.imsglobal.org/xsd/imsccv1p1/imsdt_v1p1 http://www.imsglobal.org/xsd/imsccv1p1/ccv1p1_imsdt_v1p1.xsd">
  <title>Unit [X] Discussion: Learn with AI Debrief &amp; Reflection</title>
  <text texttype="text/html">&lt;div style=&quot;font-family: -apple-system, BlinkMacSystemFont, &#x27;Segoe UI&#x27;, Roboto, sans-serif; font-size: 1rem; line-height: 1.6; color: #1e293b;&quot;&gt;
  &lt;div style=&quot;background: #f8fafc; border-left: 4px solid #1e3a8a; padding: 1rem 1.25rem; margin-bottom: 1.5rem; border-radius: 0 6px 6px 0;&quot;&gt;
    &lt;h3 style=&quot;color: #1e3a8a; margin-top: 0; margin-bottom: 0.5rem;&quot;&gt;&lt;i class=&quot;far fa-comments&quot;&gt;&lt;/i&gt; Unit [X] Collaborative Reflection: Learn with AI Debrief&lt;/h3&gt;
    &lt;p style=&quot;margin: 0; color: #475569;&quot;&gt;This weekly discussion board is where you share insights, traps, and breakthroughs from your interactive practice session with our AI Persona: &lt;strong&gt;[Persona Title]&lt;/strong&gt;.&lt;/p&gt;
  &lt;/div&gt;

  &lt;h4 style=&quot;color: #1e3a8a; margin-top: 1rem; margin-bottom: 0.5rem;&quot;&gt;Discussion Prompts &amp;amp; Deliverables:&lt;/h4&gt;
  &lt;p&gt;[Insert Discussion Reflection Questions Here]&lt;/p&gt;

  &lt;div style=&quot;background: #fef2f2; border-left: 4px solid #ef4444; padding: 0.85rem 1.25rem; margin: 1.25rem 0; border-radius: 0 6px 6px 0;&quot;&gt;
    &lt;strong style=&quot;color: #991b1b;&quot;&gt;&lt;i class=&quot;fas fa-shield-alt&quot;&gt;&lt;/i&gt; The Human-On-The-Loop (HOTL) Defense Standard:&lt;/strong&gt;
    &lt;p style=&quot;margin: 0.35rem 0 0 0; color: #7f1d1d; font-size: 0.95em;&quot;&gt;Never share or turn in work without verifying it! Every solution discussed or submitted must be executed against your live lab environment. Make sure you fully understand and can defend every line of work you post.&lt;/p&gt;
  &lt;/div&gt;

  &lt;h4 style=&quot;color: #1e3a8a; margin-top: 1.25rem; margin-bottom: 0.5rem;&quot;&gt;Peer Collaboration Guidelines:&lt;/h4&gt;
  &lt;ul style=&quot;padding-left: 1.5rem; line-height: 1.7;&quot;&gt;
    &lt;li&gt;Post your initial reflection answering the prompts above.&lt;/li&gt;
    &lt;li&gt;Read through your classmates&#x27; findings. Reply to at least one classmate with constructive feedback or an alternative approach.&lt;/li&gt;
  &lt;/ul&gt;
&lt;/div&gt;</text>
</topic>
```

And in `imsmanifest.xml`, register the resource:
```xml
<resource identifier="res_disc_u1" type="imsdt_xmlv1p1">
  <file href="res_disc_u1/discussion_topic.xml"/>
</resource>
```

And in `course_settings/module_meta.xml`, link it to the module sequence:
```xml
<item identifier="item_mod_disc_u1">
  <content_type>DiscussionTopic</content_type>
  <workflow_state>active</workflow_state>
  <title>Unit 1 Discussion: Learn with AI Debrief &amp; Reflection</title>
  <identifierref>res_disc_u1</identifierref>
  <position>7</position>
  <indent>1</indent>
</item>
```

---

## 7. Summary & Best Practices Checklist

When generating a Socratic AI drill for any new course:

* [ ] **Give the persona a clear job title and motive** (e.g. Stressed QA Lead, Forensic Auditor, Incident Commander).
* [ ] **State 2 to 3 specific technical traps** the AI must test.
* [ ] **Include explicit instructions to ask ONE question at a time.**
* [ ] **Forbid the AI from writing the code/text directly.**
* [ ] **Include the Permission to Struggle** (encourage saying "I don't know" and asking for hints).
* [ ] **Enforce the Human-On-The-Loop Defense standard** (verification in live tools + understanding defense).
* [ ] **Pair the drill with an asynchronous discussion topic in Canvas.**
* [ ] **Package cleanly into Common Cartridge using `imsdt_xmlv1p1` and DesignPLUS styling.**

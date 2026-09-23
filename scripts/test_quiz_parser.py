import re
import os

def parse_quiz_md(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split into questions section and answer key section
    parts = re.split(r'#+\s*Answer Key', content, flags=re.IGNORECASE)
    questions_part = parts[0]
    key_part = parts[1] if len(parts) > 1 else ""

    # Parse answer key table
    # Format: | **1** | **B** | Rationale... | or | 1 | B | ... |
    key_map = {}
    for line in key_part.splitlines():
        line = line.strip()
        if not line.startswith('|'):
            continue
        cells = [c.strip() for c in line.split('|')[1:-1]]
        if len(cells) >= 3:
            q_num_match = re.search(r'\d+', cells[0])
            ans_match = re.search(r'[A-D]', cells[1], re.IGNORECASE)
            if q_num_match and ans_match:
                q_num = int(q_num_match.group(0))
                ans = ans_match.group(0).upper()
                rationale = cells[2]
                key_map[q_num] = (ans, rationale)

    # Parse questions
    # Format: ### Question X
    q_blocks = re.split(r'###\s*Question\s+(\d+)', questions_part)
    # q_blocks[0] is header, then pairs of (q_num, text)
    questions = []
    for i in range(1, len(q_blocks), 2):
        q_num = int(q_blocks[i])
        block_text = q_blocks[i+1].strip()

        # Extract options
        # Options are: * A) text ...
        opt_matches = list(re.finditer(r'^\s*[*•-]\s*([A-D])\)\s*(.+)$', block_text, flags=re.MULTILINE))
        if opt_matches:
            prompt_end = opt_matches[0].start()
            prompt = block_text[:prompt_end].strip()
            options = []
            for m in opt_matches:
                opt_letter = m.group(1).upper()
                opt_text = m.group(2).strip()
                options.append((opt_letter, opt_text))
        else:
            prompt = block_text
            options = []

        correct_ans, rationale = key_map.get(q_num, ('A', ''))
        questions.append({
            'num': q_num,
            'prompt': prompt,
            'options': options,
            'correct_answer': correct_ans,
            'rationale': rationale
        })

    return questions

# Test on all 8 units
base_dir = "c:/dev/CMAP_1815_Autogen/units"
units = sorted(os.listdir(base_dir))
for u in units:
    quiz_path = os.path.join(base_dir, u, "assessments", "unit_quiz.md")
    if os.path.exists(quiz_path):
        qs = parse_quiz_md(quiz_path)
        print(f"{u}: parsed {len(qs)} questions")
        for q in qs:
            if len(q['options']) != 4 or not q['correct_answer']:
                print(f"  WARNING in Q{q['num']}: {len(q['options'])} options, ans={q['correct_answer']}")

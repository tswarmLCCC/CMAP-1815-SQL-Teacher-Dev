import subprocess
import sys

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}", flush=True)
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout:
        print(f"[stdout]\n{res.stdout}", flush=True)
    if res.stderr:
        print(f"[stderr]\n{res.stderr}", flush=True)
    return res.returncode

def main():
    # 1. Rebuild the Canvas cartridge with updated naming
    print("Rebuilding Canvas Cartridge...", flush=True)
    ret = run_cmd([sys.executable, "scripts/build_canvas_cartridge.py"])
    if ret != 0:
        print("Cartridge build failed!", flush=True)
        sys.exit(ret)

    # 2. Ensure safe directory
    run_cmd(["git", "config", "--global", "--add", "safe.directory", "/workspaces/CMAP-1815-SQL-Teacher-Dev"])
    
    # 3. Stage all changes
    print("Staging all changes...", flush=True)
    ret = run_cmd(["git", "add", "-A"])
    if ret != 0:
        sys.exit(ret)
        
    # Check status
    run_cmd(["git", "status", "-s"])
    
    # 4. Commit
    commit_msg = (
        "Remove dates from item titles, retain on module names only, and integrate Unit 2 review\n\n"
        "- Module Items: Removed date range prefixes from all pages, assignments, quizzes, discussions, and instructor guides; retained date ranges exclusively on Module titles\n"
        "- Unit 2: Eliminated escape backslashes, expanded Sections 3 & 4 into complete lectures (3VL, NULLs, operator precedence, pagination, regex)\n"
        "- Course-wide: Converted Instructor Unit Notes to Section 6 FAQs across Units 1-8\n"
        "- Course-wide: Added coaching guidelines and HOTL Defense Protocol to all Learn with AI pages\n"
        "- Canvas Shell: Added native DiscussionTopic items to all 8 modules (no graded references)\n"
        "- Compiled updated CMAP_1815_Complete.imscc and archived previous builds\n"
        "- Added docs/SOCRATIC_AI_DRILL_PROMPT_ENGINEERING_GUIDE.md for Gemini Gems and AI role-play authoring"
    )
    
    print("Committing...", flush=True)
    ret = run_cmd(["git", "commit", "-m", commit_msg])
    if ret != 0:
        print("Commit failed or nothing to commit", flush=True)
    else:
        print("Commit successful!", flush=True)
        
    # Show commit details
    run_cmd(["git", "log", "-n", "1", "--stat"])
    
    # 5. Push
    print("Attempting git push...", flush=True)
    push_ret = run_cmd(["git", "push", "origin", "main"])
    if push_ret == 0:
        print("Push successful!", flush=True)
    else:
        print(f"Push exited with code {push_ret}", flush=True)

if __name__ == "__main__":
    main()

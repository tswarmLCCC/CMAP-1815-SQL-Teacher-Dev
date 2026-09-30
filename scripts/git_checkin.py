import subprocess
import sys

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.stdout:
        print(f"[stdout]\n{res.stdout}")
    if res.stderr:
        print(f"[stderr]\n{res.stderr}")
    return res.returncode

def main():
    # Ensure safe directory
    run_cmd(["git", "config", "--global", "--add", "safe.directory", "/workspaces/CMAP-1815-SQL-Teacher-Dev"])
    
    # Check status
    run_cmd(["git", "status", "-s"])
    
    # Stage all changes
    print("Staging all changes...")
    ret = run_cmd(["git", "add", "-A"])
    if ret != 0:
        sys.exit(ret)
        
    # Check what is staged
    run_cmd(["git", "status", "-s"])
    
    # Commit
    commit_msg = (
        "Integrate Unit 2 review updates, course-wide FAQs, Discussion Topics, "
        "and Socratic AI Gem guide\n\n"
        "- Unit 2: Eliminated escape backslashes, expanded Sections 3 & 4 into complete lectures (3VL, NULLs, operator precedence, pagination, regex)\n"
        "- Course-wide: Converted Instructor Unit Notes to Section 6 FAQs across Units 1-8\n"
        "- Course-wide: Added coaching guidelines and HOTL Defense Protocol to all Learn with AI pages\n"
        "- Canvas Shell: Added native DiscussionTopic items to all 8 modules (no graded references)\n"
        "- Compiled updated CMAP_1815_Complete.imscc and archived previous builds\n"
        "- Added docs/SOCRATIC_AI_DRILL_PROMPT_ENGINEERING_GUIDE.md for Gemini Gems and AI role-play authoring"
    )
    
    print("Committing...")
    ret = run_cmd(["git", "commit", "-m", commit_msg])
    if ret != 0:
        print("Commit failed or nothing to commit")
    else:
        print("Commit successful!")
        
    # Show commit details
    run_cmd(["git", "log", "-n", "1", "--stat"])
    
    # Attempt push
    print("Attempting git push...")
    push_ret = run_cmd(["git", "push", "origin", "main"])
    if push_ret == 0:
        print("Push successful!")
    else:
        print(f"Push exited with code {push_ret}")

if __name__ == "__main__":
    main()

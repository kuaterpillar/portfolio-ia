"""
Session Memory System
Saves conversation context and project state between sessions
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path


class SessionMemory:
    """
    Persistent memory system that saves:
    - Conversation history between developer and AI
    - Project decisions and architecture choices
    - Current TODOs and completed tasks
    - Technical issues and resolutions
    - Configuration changes
    """

    def __init__(self, memory_dir: str = "memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)

        self.session_file = self.memory_dir / "current_session.json"
        self.history_dir = self.memory_dir / "history"
        self.history_dir.mkdir(exist_ok=True)

        # Load current session or create new
        self.session_data = self._load_current_session()

    def _load_current_session(self) -> Dict:
        """Load the current active session"""
        if self.session_file.exists():
            with open(self.session_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return self._create_new_session()

    def _create_new_session(self) -> Dict:
        """Create a new session structure"""
        return {
            "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "started_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "project_name": "Hotel Concierge AI",
            "conversation_history": [],
            "decisions": [],
            "todos": {
                "pending": [],
                "in_progress": [],
                "completed": []
            },
            "files_modified": [],
            "features_implemented": [],
            "bugs_fixed": [],
            "configurations": {},
            "notes": []
        }

    def save_session(self):
        """Save current session to disk"""
        self.session_data["last_updated"] = datetime.now().isoformat()

        with open(self.session_file, 'w', encoding='utf-8') as f:
            json.dump(self.session_data, f, indent=2, ensure_ascii=False)

    def archive_session(self):
        """Archive current session and start a new one"""
        if self.session_file.exists():
            # Save to history
            archive_file = self.history_dir / f"session_{self.session_data['session_id']}.json"
            with open(archive_file, 'w', encoding='utf-8') as f:
                json.dump(self.session_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Session archivée: {archive_file}")

        # Start new session
        self.session_data = self._create_new_session()
        self.save_session()

    def add_conversation(self, user_message: str, ai_response: str, context: Optional[Dict] = None):
        """Record a conversation exchange"""
        self.session_data["conversation_history"].append({
            "timestamp": datetime.now().isoformat(),
            "user": user_message,
            "ai": ai_response,
            "context": context or {}
        })
        self.save_session()

    def add_decision(self, decision: str, reason: str, impact: str):
        """Record an important decision"""
        self.session_data["decisions"].append({
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "reason": reason,
            "impact": impact
        })
        self.save_session()

    def add_todo(self, task: str, status: str = "pending", priority: str = "medium"):
        """Add a TODO task"""
        todo = {
            "task": task,
            "status": status,
            "priority": priority,
            "created_at": datetime.now().isoformat()
        }

        if status == "pending":
            self.session_data["todos"]["pending"].append(todo)
        elif status == "in_progress":
            self.session_data["todos"]["in_progress"].append(todo)
        elif status == "completed":
            self.session_data["todos"]["completed"].append(todo)

        self.save_session()

    def update_todo_status(self, task_description: str, new_status: str):
        """Update the status of a TODO"""
        # Find and move the task
        for status_category in ["pending", "in_progress", "completed"]:
            todos = self.session_data["todos"][status_category]
            for i, todo in enumerate(todos):
                if task_description in todo["task"]:
                    # Remove from current category
                    removed_todo = todos.pop(i)
                    removed_todo["status"] = new_status
                    removed_todo["updated_at"] = datetime.now().isoformat()

                    # Add to new category
                    self.session_data["todos"][new_status].append(removed_todo)
                    self.save_session()
                    return True
        return False

    def add_file_modified(self, file_path: str, description: str):
        """Record a file modification"""
        self.session_data["files_modified"].append({
            "timestamp": datetime.now().isoformat(),
            "file": file_path,
            "description": description
        })
        self.save_session()

    def add_feature_implemented(self, feature_name: str, description: str, files_involved: List[str]):
        """Record a completed feature"""
        self.session_data["features_implemented"].append({
            "timestamp": datetime.now().isoformat(),
            "name": feature_name,
            "description": description,
            "files": files_involved
        })
        self.save_session()

    def add_bug_fixed(self, bug_description: str, solution: str):
        """Record a bug fix"""
        self.session_data["bugs_fixed"].append({
            "timestamp": datetime.now().isoformat(),
            "bug": bug_description,
            "solution": solution
        })
        self.save_session()

    def set_configuration(self, key: str, value: any):
        """Save a configuration setting"""
        self.session_data["configurations"][key] = {
            "value": value,
            "updated_at": datetime.now().isoformat()
        }
        self.save_session()

    def add_note(self, note: str, category: str = "general"):
        """Add a general note"""
        self.session_data["notes"].append({
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "note": note
        })
        self.save_session()

    def get_session_summary(self) -> str:
        """Generate a readable summary of the current session"""
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║  SESSION SUMMARY - {self.session_data['project_name']}
╚══════════════════════════════════════════════════════════════╝

📅 Session ID: {self.session_data['session_id']}
⏰ Started: {self.session_data['started_at']}
🔄 Last Updated: {self.session_data['last_updated']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 DECISIONS MADE ({len(self.session_data['decisions'])})
"""

        for i, decision in enumerate(self.session_data['decisions'][-5:], 1):
            summary += f"""
{i}. {decision['decision']}
   Raison: {decision['reason']}
   Impact: {decision['impact']}
"""

        summary += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ FEATURES IMPLEMENTED ({len(self.session_data['features_implemented'])})
"""

        for i, feature in enumerate(self.session_data['features_implemented'], 1):
            summary += f"""
{i}. {feature['name']}
   {feature['description']}
   Fichiers: {', '.join(feature['files'][:3])}{'...' if len(feature['files']) > 3 else ''}
"""

        summary += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 TODOS
"""

        pending = self.session_data['todos']['pending']
        in_progress = self.session_data['todos']['in_progress']
        completed = self.session_data['todos']['completed']

        summary += f"\n⏳ In Progress ({len(in_progress)}):\n"
        for todo in in_progress:
            summary += f"   • {todo['task']}\n"

        summary += f"\n📌 Pending ({len(pending)}):\n"
        for todo in pending[:5]:
            summary += f"   • {todo['task']}\n"

        summary += f"\n✔️  Completed ({len(completed)}):\n"
        for todo in completed[-5:]:
            summary += f"   • {todo['task']}\n"

        summary += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📂 FILES MODIFIED ({len(self.session_data['files_modified'])})
"""

        for file_mod in self.session_data['files_modified'][-10:]:
            summary += f"\n   • {file_mod['file']}\n     {file_mod['description']}\n"

        summary += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🐛 BUGS FIXED ({len(self.session_data['bugs_fixed'])})
"""

        for bug in self.session_data['bugs_fixed']:
            summary += f"""
   • {bug['bug']}
     Solution: {bug['solution']}
"""

        summary += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💬 CONVERSATION EXCHANGES: {len(self.session_data['conversation_history'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 NOTES ({len(self.session_data['notes'])})
"""

        for note in self.session_data['notes'][-5:]:
            summary += f"\n   [{note['category']}] {note['note']}\n"

        summary += "\n╚══════════════════════════════════════════════════════════════╝\n"

        return summary

    def get_context_for_ai(self) -> str:
        """
        Generate context summary for AI to understand project state
        This is used when starting a new conversation
        """
        context = f"""
CONTEXTE DE SESSION - {self.session_data['project_name']}
Session: {self.session_data['session_id']}

DERNIÈRES DÉCISIONS:
"""

        for decision in self.session_data['decisions'][-3:]:
            context += f"- {decision['decision']} (Raison: {decision['reason']})\n"

        context += "\nFONCTIONNALITÉS IMPLÉMENTÉES:\n"
        for feature in self.session_data['features_implemented'][-5:]:
            context += f"- {feature['name']}: {feature['description']}\n"

        context += "\nTODOS EN COURS:\n"
        for todo in self.session_data['todos']['in_progress']:
            context += f"- {todo['task']}\n"

        context += "\nTODOS PENDING:\n"
        for todo in self.session_data['todos']['pending'][:5]:
            context += f"- {todo['task']}\n"

        context += "\nDERNIÈRES MODIFICATIONS:\n"
        for file_mod in self.session_data['files_modified'][-5:]:
            context += f"- {file_mod['file']}: {file_mod['description']}\n"

        return context

    def export_session_report(self, output_file: Optional[str] = None):
        """Export session summary to a markdown file"""
        if not output_file:
            output_file = f"SESSION_REPORT_{self.session_data['session_id']}.md"

        summary = self.get_session_summary()

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(summary)

        print(f"✅ Rapport de session exporté: {output_file}")
        return output_file

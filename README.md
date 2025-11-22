# AI-Driven File Intelligence & Auto-Sorting System

**Overview**
A lightweight Python tool that watches a folder and sorts incoming files into categorized folders. It optionally uses an AI service to generate short summaries for each file, and logs actions with file hashes for integrity.

**Features**
- Real-time folder watcher and sorter
- Extension-based classification (images, documents, code, archives, etc.)
- Optional AI-based file summarization (toggle via environment variable `AI_API_ENABLED=1`)
- Secure logging with file hash (SHA256) for traceability
- Simple, easy-to-extend architecture

**Quick Start**
1. Clone the repo
2. Create a virtualenv and install requirements:
   ```
   pip install -r requirements.txt
   ```
3. Create a `watch_folder/` directory inside the project root and add files to it.
4. Run:
   ```
   python sorter.py
   ```
5. Optional: enable AI summaries by setting environment variable `AI_API_ENABLED=1` and provide your own AI integration in `ai_summary.py`.

**Project Structure**
- `sorter.py` - main watcher and sorter
- `ai_summary.py` - AI integration or offline heuristics for summaries
- `log_handler.py` - JSON-based log handling
- `watch_folder/` - drop files here to process
- `sorted/` - output categorized folders
- `logs/log.json` - operation logs

**Notes for Recruiters**
This project demonstrates practical Python scripting, automation, integration with AI services, and basic security practices (file hashing, logging). It aligns with roles in Python automation, AI-integrations, and cloud-ready development.

**Author**
Aryan Shrivastava

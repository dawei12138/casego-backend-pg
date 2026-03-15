# Claude Code 工具定义文档

以下是 Claude Code 所有可直接调用的基础工具，包含工具名称、描述（prompt）和完整入参 JSON Schema。

---

## 1. Bash

**描述：**

Executes a given bash command and returns its output.

The working directory persists between commands, but shell state does not. The shell environment is initialized from the user's profile (bash or zsh).

IMPORTANT: Avoid using this tool to run `find`, `grep`, `cat`, `head`, `tail`, `sed`, `awk`, or `echo` commands, unless explicitly instructed or after you have verified that a dedicated tool cannot accomplish your task. Instead, use the appropriate dedicated tool as this will provide a much better experience for the user:

 - File search: Use Glob (NOT find or ls)
 - Content search: Use Grep (NOT grep or rg)
 - Read files: Use Read (NOT cat/head/tail)
 - Edit files: Use Edit (NOT sed/awk)
 - Write files: Use Write (NOT echo >/cat <<EOF)
 - Communication: Output text directly (NOT echo/printf)

While the Bash tool can do similar things, it's better to use the built-in tools as they provide a better user experience and make it easier to review tool calls and give permission.

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["command"],
  "additionalProperties": false,
  "properties": {
    "command": {
      "type": "string",
      "description": "The command to execute"
    },
    "description": {
      "type": "string",
      "description": "Clear, concise description of what this command does in active voice."
    },
    "timeout": {
      "type": "number",
      "description": "Optional timeout in milliseconds (max 600000)"
    },
    "run_in_background": {
      "type": "boolean",
      "description": "Set to true to run this command in the background. Use TaskOutput to read the output later."
    },
    "dangerouslyDisableSandbox": {
      "type": "boolean",
      "description": "Set this to true to dangerously override sandbox mode and run commands without sandboxing."
    }
  }
}
```

---

## 2. Read

**描述：**

Reads a file from the local filesystem. You can access any file directly by using this tool.
Assume this tool is able to read all files on the machine. If the User provides a path to a file assume that path is valid. It is okay to read a file that does not exist; an error will be returned.

Usage:
- The file_path parameter must be an absolute path, not a relative path
- By default, it reads up to 2000 lines starting from the beginning of the file
- You can optionally specify a line offset and limit (especially handy for long files), but it's recommended to read the whole file by not providing these parameters
- Any lines longer than 2000 characters will be truncated
- Results are returned using cat -n format, with line numbers starting at 1
- This tool allows Claude Code to read images (eg PNG, JPG, etc). When reading an image file the contents are presented visually as Claude Code is a multimodal LLM.
- This tool can read PDF files (.pdf). For large PDFs (more than 10 pages), you MUST provide the pages parameter to read specific page ranges (e.g., pages: "1-5"). Reading a large PDF without the pages parameter will fail. Maximum 20 pages per request.
- This tool can read Jupyter notebooks (.ipynb files) and returns all cells with their outputs, combining code, text, and visualizations.
- This tool can only read files, not directories. To read a directory, use an ls command via the Bash tool.

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["file_path"],
  "additionalProperties": false,
  "properties": {
    "file_path": {
      "type": "string",
      "description": "The absolute path to the file to read"
    },
    "offset": {
      "type": "number",
      "description": "The line number to start reading from. Only provide if the file is too large to read at once"
    },
    "limit": {
      "type": "number",
      "description": "The number of lines to read. Only provide if the file is too large to read at once."
    },
    "pages": {
      "type": "string",
      "description": "Page range for PDF files (e.g., \"1-5\", \"3\", \"10-20\"). Only applicable to PDF files. Maximum 20 pages per request."
    }
  }
}
```

---

## 3. Edit

**描述：**

Performs exact string replacements in files.

Usage:
- You must use your `Read` tool at least once in the conversation before editing. This tool will error if you attempt an edit without reading the file.
- When editing text from Read tool output, ensure you preserve the exact indentation (tabs/spaces) as it appears AFTER the line number prefix.
- ALWAYS prefer editing existing files in the codebase. NEVER write new files unless explicitly required.
- The edit will FAIL if `old_string` is not unique in the file. Either provide a larger string with more surrounding context to make it unique or use `replace_all` to change every instance of `old_string`.
- Use `replace_all` for replacing and renaming strings across the file.

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["file_path", "old_string", "new_string"],
  "additionalProperties": false,
  "properties": {
    "file_path": {
      "type": "string",
      "description": "The absolute path to the file to modify"
    },
    "old_string": {
      "type": "string",
      "description": "The text to replace"
    },
    "new_string": {
      "type": "string",
      "description": "The text to replace it with (must be different from old_string)"
    },
    "replace_all": {
      "type": "boolean",
      "default": false,
      "description": "Replace all occurrences of old_string (default false)"
    }
  }
}
```

---

## 4. Write

**描述：**

Writes a file to the local filesystem.

Usage:
- This tool will overwrite the existing file if there is one at the provided path.
- If this is an existing file, you MUST use the Read tool first to read the file's contents. This tool will fail if you did not read the file first.
- Prefer the Edit tool for modifying existing files — it only sends the diff. Only use this tool to create new files or for complete rewrites.
- NEVER create documentation files (*.md) or README files unless explicitly requested by the User.

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["file_path", "content"],
  "additionalProperties": false,
  "properties": {
    "file_path": {
      "type": "string",
      "description": "The absolute path to the file to write (must be absolute, not relative)"
    },
    "content": {
      "type": "string",
      "description": "The content to write to the file"
    }
  }
}
```

---

## 5. Glob

**描述：**

Fast file pattern matching tool that works with any codebase size.

- Supports glob patterns like "**/*.js" or "src/**/*.ts"
- Returns matching file paths sorted by modification time
- Use this tool when you need to find files by name patterns
- When you are doing an open ended search that may require multiple rounds of globbing and grepping, use the Agent tool instead

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["pattern"],
  "additionalProperties": false,
  "properties": {
    "pattern": {
      "type": "string",
      "description": "The glob pattern to match files against"
    },
    "path": {
      "type": "string",
      "description": "The directory to search in. If not specified, the current working directory will be used."
    }
  }
}
```

---

## 6. Grep

**描述：**

A powerful search tool built on ripgrep.

- ALWAYS use Grep for search tasks. NEVER invoke `grep` or `rg` as a Bash command.
- Supports full regex syntax (e.g., "log.*Error", "function\\s+\\w+")
- Filter files with glob parameter (e.g., "*.js", "**/*.tsx") or type parameter (e.g., "js", "py", "rust")
- Output modes: "content" shows matching lines, "files_with_matches" shows only file paths (default), "count" shows match counts
- Pattern syntax: Uses ripgrep (not grep) - literal braces need escaping (use `interface\\{\\}` to find `interface{}` in Go code)
- Multiline matching: By default patterns match within single lines only. For cross-line patterns, use `multiline: true`

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["pattern"],
  "additionalProperties": false,
  "properties": {
    "pattern": {
      "type": "string",
      "description": "The regular expression pattern to search for in file contents"
    },
    "path": {
      "type": "string",
      "description": "File or directory to search in (rg PATH). Defaults to current working directory."
    },
    "glob": {
      "type": "string",
      "description": "Glob pattern to filter files (e.g. \"*.js\", \"*.{ts,tsx}\") - maps to rg --glob"
    },
    "type": {
      "type": "string",
      "description": "File type to search (rg --type). Common types: js, py, rust, go, java, etc."
    },
    "output_mode": {
      "type": "string",
      "enum": ["content", "files_with_matches", "count"],
      "description": "Output mode: \"content\" shows matching lines, \"files_with_matches\" shows file paths (default), \"count\" shows match counts."
    },
    "-i": {
      "type": "boolean",
      "description": "Case insensitive search (rg -i)"
    },
    "-n": {
      "type": "boolean",
      "description": "Show line numbers in output (rg -n). Requires output_mode: \"content\". Defaults to true."
    },
    "-A": {
      "type": "number",
      "description": "Number of lines to show after each match (rg -A). Requires output_mode: \"content\"."
    },
    "-B": {
      "type": "number",
      "description": "Number of lines to show before each match (rg -B). Requires output_mode: \"content\"."
    },
    "-C": {
      "type": "number",
      "description": "Alias for context."
    },
    "context": {
      "type": "number",
      "description": "Number of lines to show before and after each match (rg -C). Requires output_mode: \"content\"."
    },
    "multiline": {
      "type": "boolean",
      "description": "Enable multiline mode where . matches newlines and patterns can span lines (rg -U --multiline-dotall). Default: false."
    },
    "head_limit": {
      "type": "number",
      "description": "Limit output to first N lines/entries, equivalent to \"| head -N\". Defaults to 0 (unlimited)."
    },
    "offset": {
      "type": "number",
      "description": "Skip first N lines/entries before applying head_limit. Defaults to 0."
    }
  }
}
```

---

## 7. WebFetch

**描述：**

Fetches content from a specified URL and processes it using an AI model.

- Takes a URL and a prompt as input
- Fetches the URL content, converts HTML to markdown
- Processes the content with the prompt using a small, fast model
- Returns the model's response about the content
- IMPORTANT: WebFetch WILL FAIL for authenticated or private URLs.
- The URL must be a fully-formed valid URL
- HTTP URLs will be automatically upgraded to HTTPS
- Includes a self-cleaning 15-minute cache for faster responses

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["url", "prompt"],
  "additionalProperties": false,
  "properties": {
    "url": {
      "type": "string",
      "format": "uri",
      "description": "The URL to fetch content from"
    },
    "prompt": {
      "type": "string",
      "description": "The prompt to run on the fetched content"
    }
  }
}
```

---

## 8. WebSearch

**描述：**

Allows Claude to search the web and use the results to inform responses.

- Provides up-to-date information for current events and recent data
- Returns search result information formatted as search result blocks, including links as markdown hyperlinks
- Use this tool for accessing information beyond Claude's knowledge cutoff
- Searches are performed automatically within a single API call
- Domain filtering is supported to include or block specific websites

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["query"],
  "additionalProperties": false,
  "properties": {
    "query": {
      "type": "string",
      "minLength": 2,
      "description": "The search query to use"
    },
    "allowed_domains": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Only include search results from these domains"
    },
    "blocked_domains": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Never include search results from these domains"
    }
  }
}
```

---

## 9. NotebookEdit

**描述：**

Completely replaces the contents of a specific cell in a Jupyter notebook (.ipynb file) with new source.

- The notebook_path parameter must be an absolute path, not a relative path.
- The cell_number is 0-indexed.
- Use edit_mode=insert to add a new cell at the index specified by cell_number.
- Use edit_mode=delete to delete the cell at the index specified by cell_number.

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["notebook_path", "new_source"],
  "additionalProperties": false,
  "properties": {
    "notebook_path": {
      "type": "string",
      "description": "The absolute path to the Jupyter notebook file to edit (must be absolute, not relative)"
    },
    "cell_id": {
      "type": "string",
      "description": "The ID of the cell to edit. When inserting a new cell, the new cell will be inserted after the cell with this ID."
    },
    "cell_type": {
      "type": "string",
      "enum": ["code", "markdown"],
      "description": "The type of the cell (code or markdown). If using edit_mode=insert, this is required."
    },
    "edit_mode": {
      "type": "string",
      "enum": ["replace", "insert", "delete"],
      "description": "The type of edit to make (replace, insert, delete). Defaults to replace."
    },
    "new_source": {
      "type": "string",
      "description": "The new source for the cell"
    }
  }
}
```

---

## 10. Task

**描述：**

Launch a new agent to handle complex, multi-step tasks autonomously.

The Task tool launches specialized agents (subprocesses) that autonomously handle complex tasks. Each agent type has specific capabilities and tools available to it.

Available agent types (subagent_type):
- `general-purpose`: General-purpose agent for researching complex questions, searching for code, and executing multi-step tasks. (Tools: *)
- `Explore`: Fast agent specialized for exploring codebases. (Tools: All tools except Task, ExitPlanMode, Edit, Write, NotebookEdit)
- `Plan`: Software architect agent for designing implementation plans. (Tools: All tools except Task, ExitPlanMode, Edit, Write, NotebookEdit)
- `claude-code-guide`: Agent for answering questions about Claude Code, Claude Agent SDK, and Claude API. (Tools: Glob, Grep, Read, WebFetch, WebSearch)

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["description", "prompt", "subagent_type"],
  "additionalProperties": false,
  "properties": {
    "description": {
      "type": "string",
      "description": "A short (3-5 word) description of the task"
    },
    "prompt": {
      "type": "string",
      "description": "The task for the agent to perform"
    },
    "subagent_type": {
      "type": "string",
      "description": "The type of specialized agent to use for this task"
    },
    "model": {
      "type": "string",
      "enum": ["sonnet", "opus", "haiku"],
      "description": "Optional model to use for this agent. If not specified, inherits from parent."
    },
    "run_in_background": {
      "type": "boolean",
      "description": "Set to true to run this agent in the background."
    },
    "resume": {
      "type": "string",
      "description": "Optional agent ID to resume from. If provided, the agent will continue from the previous execution transcript."
    },
    "max_turns": {
      "type": "integer",
      "exclusiveMinimum": 0,
      "description": "Maximum number of agentic turns (API round-trips) before stopping."
    },
    "isolation": {
      "type": "string",
      "enum": ["worktree"],
      "description": "Isolation mode. \"worktree\" creates a temporary git worktree so the agent works on an isolated copy of the repo."
    }
  }
}
```

---

## 11. TaskOutput

**描述：**

Retrieves output from a running or completed task (background shell, agent, or remote session).

- Takes a task_id parameter identifying the task
- Returns the task output along with status information
- Use block=true (default) to wait for task completion
- Use block=false for non-blocking check of current status

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["task_id", "block", "timeout"],
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string",
      "description": "The task ID to get output from"
    },
    "block": {
      "type": "boolean",
      "default": true,
      "description": "Whether to wait for completion"
    },
    "timeout": {
      "type": "number",
      "default": 30000,
      "minimum": 0,
      "maximum": 600000,
      "description": "Max wait time in ms"
    }
  }
}
```

---

## 12. TaskStop

**描述：**

Stops a running background task by its ID.

- Takes a task_id parameter identifying the task to stop
- Returns a success or failure status
- Use this tool when you need to terminate a long-running task

**入参 Schema：**

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "task_id": {
      "type": "string",
      "description": "The ID of the background task to stop"
    },
    "shell_id": {
      "type": "string",
      "description": "Deprecated: use task_id instead"
    }
  }
}
```

---

## 13. AskUserQuestion

**描述：**

Use this tool when you need to ask the user questions during execution. This allows you to:
1. Gather user preferences or requirements
2. Clarify ambiguous instructions
3. Get decisions on implementation choices as you work
4. Offer choices to the user about what direction to take.

Usage notes:
- Users will always be able to select "Other" to provide custom text input
- Use multiSelect: true to allow multiple answers to be selected for a question

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["questions"],
  "additionalProperties": false,
  "properties": {
    "questions": {
      "type": "array",
      "minItems": 1,
      "maxItems": 4,
      "description": "Questions to ask the user (1-4 questions)",
      "items": {
        "type": "object",
        "required": ["question", "header", "options", "multiSelect"],
        "additionalProperties": false,
        "properties": {
          "question": {
            "type": "string",
            "description": "The complete question to ask the user."
          },
          "header": {
            "type": "string",
            "description": "Very short label displayed as a chip/tag (max 12 chars)."
          },
          "options": {
            "type": "array",
            "minItems": 2,
            "maxItems": 4,
            "description": "The available choices for this question.",
            "items": {
              "type": "object",
              "required": ["label", "description"],
              "additionalProperties": false,
              "properties": {
                "label": {
                  "type": "string",
                  "description": "The display text for this option (1-5 words)."
                },
                "description": {
                  "type": "string",
                  "description": "Explanation of what this option means."
                },
                "markdown": {
                  "type": "string",
                  "description": "Optional preview content shown in a monospace box when this option is focused."
                }
              }
            }
          },
          "multiSelect": {
            "type": "boolean",
            "default": false,
            "description": "Set to true to allow the user to select multiple options."
          }
        }
      }
    },
    "answers": {
      "type": "object",
      "additionalProperties": { "type": "string" },
      "description": "User answers collected by the permission component"
    },
    "annotations": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "markdown": { "type": "string" },
          "notes": { "type": "string" }
        }
      },
      "description": "Optional per-question annotations from the user."
    },
    "metadata": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "source": {
          "type": "string",
          "description": "Optional identifier for the source of this question."
        }
      }
    }
  }
}
```

---

## 14. EnterPlanMode

**描述：**

Use this tool proactively when you're about to start a non-trivial implementation task. Getting user sign-off on your approach before writing code prevents wasted effort and ensures alignment. This tool transitions you into plan mode where you can explore the codebase and design an implementation approach for user approval.

Use it when:
1. New Feature Implementation
2. Multiple Valid Approaches exist
3. Code Modifications that affect existing behavior
4. Architectural Decisions
5. Multi-File Changes
6. Unclear Requirements
7. User Preferences Matter

**入参 Schema：**

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {}
}
```

---

## 15. ExitPlanMode

**描述：**

Use this tool when you are in plan mode and have finished writing your plan to the plan file and are ready for user approval.

- You should have already written your plan to the plan file specified in the plan mode system message
- This tool does NOT take the plan content as a parameter - it will read the plan from the file you wrote
- This tool simply signals that you're done planning and ready for the user to review and approve

**入参 Schema：**

```json
{
  "type": "object",
  "additionalProperties": {},
  "properties": {
    "allowedPrompts": {
      "type": "array",
      "description": "Prompt-based permissions needed to implement the plan.",
      "items": {
        "type": "object",
        "required": ["tool", "prompt"],
        "additionalProperties": false,
        "properties": {
          "tool": {
            "type": "string",
            "enum": ["Bash"],
            "description": "The tool this prompt applies to"
          },
          "prompt": {
            "type": "string",
            "description": "Semantic description of the action, e.g. \"run tests\", \"install dependencies\""
          }
        }
      }
    }
  }
}
```

---

## 16. Skill

**描述：**

Execute a skill within the main conversation.

When users ask you to perform tasks, check if any of the available skills match. Skills provide specialized capabilities and domain knowledge.

When users reference a "slash command" or "/<something>" (e.g., "/commit", "/review-pr"), they are referring to a skill. Use this tool to invoke it.

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["skill"],
  "additionalProperties": false,
  "properties": {
    "skill": {
      "type": "string",
      "description": "The skill name. E.g., \"commit\", \"review-pr\", or \"pdf\""
    },
    "args": {
      "type": "string",
      "description": "Optional arguments for the skill"
    }
  }
}
```

---

## 17. TaskCreate

**描述：**

Use this tool to create a structured task list for your current coding session. This helps you track progress, organize complex tasks, and demonstrate thoroughness to the user.

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["subject", "description"],
  "additionalProperties": false,
  "properties": {
    "subject": {
      "type": "string",
      "description": "A brief title for the task"
    },
    "description": {
      "type": "string",
      "description": "A detailed description of what needs to be done"
    },
    "activeForm": {
      "type": "string",
      "description": "Present continuous form shown in spinner when in_progress (e.g., \"Running tests\")"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": {},
      "description": "Arbitrary metadata to attach to the task"
    }
  }
}
```

---

## 18. TaskGet

**描述：**

Use this tool to retrieve a task by its ID from the task list.

Returns full task details:
- subject: Task title
- description: Detailed requirements and context
- status: 'pending', 'in_progress', or 'completed'
- blocks: Tasks waiting on this one to complete
- blockedBy: Tasks that must complete before this one can start

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["taskId"],
  "additionalProperties": false,
  "properties": {
    "taskId": {
      "type": "string",
      "description": "The ID of the task to retrieve"
    }
  }
}
```

---

## 19. TaskUpdate

**描述：**

Use this tool to update a task in the task list.

- Mark tasks as resolved when completed
- Delete tasks that are no longer relevant (status: "deleted")
- Update task details when requirements change
- Set up dependencies between tasks

Status progresses: `pending` → `in_progress` → `completed`

**入参 Schema：**

```json
{
  "type": "object",
  "required": ["taskId"],
  "additionalProperties": false,
  "properties": {
    "taskId": {
      "type": "string",
      "description": "The ID of the task to update"
    },
    "status": {
      "type": "string",
      "description": "New status for the task",
      "anyOf": [
        { "enum": ["pending", "in_progress", "completed"] },
        { "const": "deleted" }
      ]
    },
    "subject": {
      "type": "string",
      "description": "New subject for the task"
    },
    "description": {
      "type": "string",
      "description": "New description for the task"
    },
    "activeForm": {
      "type": "string",
      "description": "Present continuous form shown in spinner when in_progress"
    },
    "owner": {
      "type": "string",
      "description": "New owner for the task"
    },
    "metadata": {
      "type": "object",
      "additionalProperties": {},
      "description": "Metadata keys to merge into the task. Set a key to null to delete it."
    },
    "addBlocks": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Task IDs that this task blocks"
    },
    "addBlockedBy": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Task IDs that block this task"
    }
  }
}
```

---

## 20. TaskList

**描述：**

Use this tool to list all tasks in the task list.

- To see what tasks are available to work on
- To check overall progress on the project
- To find tasks that are blocked and need dependencies resolved
- After completing a task, to check for newly unblocked work

Returns a summary of each task: id, subject, status, owner, blockedBy.

**入参 Schema：**

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {}
}
```

---

## 21. EnterWorktree

**描述：**

Use this tool ONLY when the user explicitly asks to work in a worktree. This tool creates an isolated git worktree and switches the current session into it.

Requirements:
- Must be in a git repository
- Must not already be in a worktree

Behavior:
- Creates a new git worktree inside `.claude/worktrees/` with a new branch based on HEAD
- Switches the session's working directory to the new worktree
- On session exit, the user will be prompted to keep or remove the worktree

**入参 Schema：**

```json
{
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "name": {
      "type": "string",
      "description": "Optional name for the worktree. A random name is generated if not provided."
    }
  }
}
```

---

## 工具总览

| # | 工具名 | 用途 |
|---|--------|------|
| 1 | Bash | 执行 shell 命令 |
| 2 | Read | 读取文件内容（支持图片/PDF/Notebook） |
| 3 | Edit | 精确字符串替换编辑文件 |
| 4 | Write | 创建/覆盖写入文件 |
| 5 | Glob | 按模式匹配搜索文件 |
| 6 | Grep | 按正则搜索文件内容（基于 ripgrep） |
| 7 | WebFetch | 抓取 URL 内容并用 AI 处理 |
| 8 | WebSearch | 搜索互联网 |
| 9 | NotebookEdit | 编辑 Jupyter Notebook 单元格 |
| 10 | Task | 启动子代理执行复杂任务 |
| 11 | TaskOutput | 获取后台任务输出 |
| 12 | TaskStop | 停止后台任务 |
| 13 | AskUserQuestion | 向用户提问 |
| 14 | EnterPlanMode | 进入计划模式 |
| 15 | ExitPlanMode | 退出计划模式（提交计划供审批） |
| 16 | Skill | 调用已注册的技能（slash command） |
| 17 | TaskCreate | 创建任务追踪项 |
| 18 | TaskGet | 获取任务详情 |
| 19 | TaskUpdate | 更新任务状态 |
| 20 | TaskList | 列出所有任务 |
| 21 | EnterWorktree | 创建隔离的 git worktree |

Tool Use Overview
Roo Code implements a sophisticated tool system that allows AI models to interact with your development environment in a controlled and secure manner. This document explains how tools work, when they're called, and how they're managed.

Core Concepts
Tool Groups
Tools are organized into logical groups based on their functionality:

Category	Purpose	Tools	Common Use
Read Group	File system reading and exploration	read_file, list_files, list_code_definition_names	Code exploration and analysis
Search Group	Pattern and semantic searching	search_files, codebase_search	Finding code patterns and functionality
Edit Group	File system modifications	apply_diff, insert_content, search_and_replace, write_to_file	Code changes and file manipulation
Browser Group	Web automation	browser_action	Web testing and interaction
Command Group	System command execution	execute_command	Running scripts, building projects
MCP Group	External tool integration	use_mcp_tool, access_mcp_resource	Specialized functionality through external servers
Workflow Group	Mode and task management	switch_mode, new_task, ask_followup_question, attempt_completion	Context switching and task organization
Always Available Tools
Certain tools are accessible regardless of the current mode:

ask_followup_question: Gather additional information from users
attempt_completion: Signal task completion
switch_mode: Change operational modes
new_task: Create subtasks
Available Tools
Read Tools
These tools help Roo understand your code and project:

read_file - Examines the contents of files
list_files - Maps your project's file structure
list_code_definition_names - Creates a structural map of your code
Search Tools
These tools help Roo find patterns and functionality across your codebase:

search_files - Finds patterns across multiple files using regex
codebase_search - Performs semantic searches across your indexed codebase
Edit Tools
These tools help Roo make changes to your code:

apply_diff - Makes precise, surgical changes to your code
insert_content - Adds new lines of content without modifying existing lines
search_and_replace - Finds and replaces text or regex patterns within a file
write_to_file - Creates new files or completely rewrites existing ones
Browser Tools
These tools help Roo interact with web applications:

browser_action - Automates browser interactions
Command Tools
These tools help Roo execute commands:

execute_command - Runs system commands and programs
MCP Tools
These tools help Roo connect with external services:

use_mcp_tool - Uses specialized external tools
access_mcp_resource - Accesses external data sources
Workflow Tools
These tools help manage the conversation and task flow:

ask_followup_question - Gets additional information from you
attempt_completion - Presents final results
switch_mode - Changes to a different mode for specialized tasks
new_task - Creates a new subtask
Tool Calling Mechanism
Handling Complex Tasks
For certain complex operations that require multiple steps, Roo doesn't just figure them out on the fly. Instead, it follows predefined, internal plans to ensure consistency and accuracy.

A prime example is creating a new MCP server, identified internally by create_mcp_server. This identifier does not represent a tool you will see being called. Rather, when you ask Roo to create a server, it triggers this known, multi-step workflow.

This specific workflow is initiated by Roo using its internal fetch_instructions tool (with the task create_mcp_server) to retrieve a detailed plan. This plan then guides Roo to make calls to several standard, documented tools in sequence, such as:

execute_command for running setup scripts (e.g., npx @modelcontextprotocol/create-server).
write_to_file or apply_diff for creating or modifying server code and configuration files.
ask_followup_question to gather necessary information like API keys from you.
Other standard tools as needed for steps like determining file locations or updating configuration entries.
So, while the overall task (like create_mcp_server) is complex, it's ultimately accomplished by intelligently orchestrating the standard tools available in your environment. This approach allows Roo to reliably perform complex operations by leveraging the tools documented here.

When Tools Are Called
Tools are invoked under specific conditions:

Direct Task Requirements

When specific actions are needed to complete a task as decided by the LLM
In response to user requests
During automated workflows
Mode-Based Availability

Different modes enable different tool sets
Mode switches can trigger tool availability changes
Some tools are restricted to specific modes
Context-Dependent Calls

Based on the current state of the workspace
In response to system events
During error handling and recovery
Decision Process
The system uses a multi-step process to determine tool availability:

Mode Validation

isToolAllowedForMode(
    tool: string,
    modeSlug: string,
    customModes: ModeConfig[],
    toolRequirements?: Record<string, boolean>,
    toolParams?: Record<string, any>
)

Requirement Checking

System capability verification
Resource availability
Permission validation
Parameter Validation

Required parameter presence
Parameter type checking
Value validation
Technical Implementation
Tool Call Processing
Initialization

Tool name and parameters are validated
Mode compatibility is checked
Requirements are verified
Execution

const toolCall = {
    type: "tool_call",
    name: chunk.name,
    arguments: chunk.input,
    callId: chunk.callId
}

Result Handling

Success/failure determination
Result formatting
Error handling
Security and Permissions
Access Control

File system restrictions
Command execution limitations
Network access controls
Validation Layers

Tool-specific validation
Mode-based restrictions
System-level checks
Mode Integration
Mode-Based Tool Access
Tools are made available based on the current mode:

Code Mode: Full access to file system tools, code editing capabilities, command execution
Ask Mode: Limited to reading tools, information gathering capabilities, no file system modifications
Architect Mode: Design-focused tools, documentation capabilities, limited execution rights
Custom Modes: Can be configured with specific tool access for specialized workflows
Mode Switching
Process

Current mode state preservation
Tool availability updates
Context switching
Impact on Tools

Tool set changes
Permission adjustments
Context preservation
Best Practices
Tool Usage Guidelines
Efficiency

Use the most specific tool for the task
Avoid redundant tool calls
Batch operations when possible
Security

Validate inputs before tool calls
Use minimum required permissions
Follow security best practices
Error Handling

Implement proper error checking
Provide meaningful error messages
Handle failures gracefully
Common Patterns
Information Gathering

[ask_followup_question](/advanced-usage/available-tools/ask-followup-question) → [read_file](/advanced-usage/available-tools/read-file) → [codebase_search](/advanced-usage/available-tools/codebase-search)

Code Modification

[read_file](/advanced-usage/available-tools/read-file) → [apply_diff](/advanced-usage/available-tools/apply-diff) → [attempt_completion](/advanced-usage/available-tools/attempt-completion)

Task Management

[new_task](/advanced-usage/available-tools/new-task) → [switch_mode](/advanced-usage/available-tools/switch-mode) → [execute_command](/advanced-usage/available-tools/execute-command)

Error Handling and Recovery
Error Types
Tool-Specific Errors

Parameter validation failures
Execution errors
Resource access issues
System Errors

Permission denied
Resource unavailable
Network failures
Context Errors

Invalid mode for tool
Missing requirements
State inconsistencies
Recovery Strategies
Automatic Recovery

Retry mechanisms
Fallback options
State restoration
User Intervention

Error notifications
Recovery suggestions
Manual intervention options
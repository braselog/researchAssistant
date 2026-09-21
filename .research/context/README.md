# Temporary Conversation Context

VS Code hooks append candidate prompts and material tool outcomes to `daily/`. `/wrap_up` verifies and routes durable information, then moves processed files to `archive/`.

Both directories are local and ignored by Git. They may contain sensitive conversational context. Keep archives only as long as needed to verify durable records; a default local retention period of 30 days is recommended. Never treat inbox entries as authoritative project state.

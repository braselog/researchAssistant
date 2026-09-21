---
name: transcribe
description: Transcribes meeting audio with Faster Whisper and optional pyannote speaker diarization. Use for /transcribe, new meeting recordings, or audio that needs a reviewable transcript.
---

# Transcribe meeting audio

Use the bundled script:

```bash
conda run -n research-assistant-transcription   python .github/skills/transcribe/scripts/transcribe.py <file-or-directory>
```

Optional flags include `--model`, `--language`, `--compute-type`, and `--no-diarization`. Inputs default to `.research/meetings/audio/`; outputs are written to `.research/meetings/transcripts/` without overwriting an existing transcript unless `--force` is supplied.

Preserve the original audio as the source record. Report model, language, duration, diarization status, and warnings in the transcript metadata. Never claim speaker identity from diarization. Review technical terms before using a transcript as evidence.

After transcription, offer `/summarize_meeting` to extract decisions and actions.

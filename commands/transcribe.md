# /transcribe Command

> Transcribe audio files from meetings into text documents.

## Usage
```
/transcribe [filename]
/transcribe meetings/2024-12-02-lab-meeting.m4a
/transcribe meetings/  # Transcribe all untranscribed audio in directory
```

## When to Use
- After recording a meeting, seminar, or discussion
- When RA detects new audio files in meetings/ folder
- Before running /summarize_meeting

## Supported Formats
- .m4a, .mp3, .wav, .webm, .mp4 (audio track)
- .ogg, .flac

## Execution Steps

### 1. Detect Audio Files

If no file specified, scan `meetings/` for audio files without matching `.md`:

```
Audio files found:
- 2024-12-02-lab-meeting.m4a (no transcript)
- 2024-11-25-pi-meeting.m4a (transcript exists ✓)

Transcribe 2024-12-02-lab-meeting.m4a? (Y/n)
```

### 2. Transcription Process

Use available transcription service (Whisper, etc.):

```
Transcribing: 2024-12-02-lab-meeting.m4a
Duration: ~45 minutes
Estimated time: 2-5 minutes

[Progress indicator]

Transcription complete!
```

### 3. Generate Transcript Document

Save to `meetings/[same-name].md`:

```markdown
# Meeting Transcript: [Filename without extension]

**Date**: [Extracted or from filename]
**Duration**: [From audio metadata]
**Participants**: [If detectable, otherwise "See summary"]
**Audio file**: [Original filename]

---

## Transcript

[Full transcript text]

[00:00:00] [Speaker if detected]
[Transcribed text...]

[00:02:34] [Speaker if detected]
[Transcribed text...]

---

## Metadata

- **Transcribed**: [Timestamp]
- **Model**: [Whisper model used]
- **Confidence**: [If available]

## Next Steps

Run `/summarize_meeting meetings/[filename].md` to:
- Extract action items
- Identify key decisions
- Create tasks and issues

---

*Raw transcript - not yet summarized*
```

### 4. Post-Transcription

```
Transcript saved to meetings/[filename].md

Next steps:
A) Run /summarize_meeting to extract action items
B) Transcribe another file
C) Review transcript manually first

What would you like to do?
```

## Quality Notes

### Improving Transcription Quality
- Use good microphone/recording quality
- Minimize background noise
- Speak clearly and at moderate pace
- Identify speakers at start if possible

### Limitations
- Speaker diarization may be imperfect
- Technical terms may need manual correction
- Timestamps are approximate

## Related Commands

- `/summarize_meeting` - Extract action items from transcript
- `/next` - Get next suggestion

## Notes

- Raw transcripts may contain errors - review before citing
- Keep original audio files as source of truth
- Transcripts are for internal use, not publication

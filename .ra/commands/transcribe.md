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

## Execution

The command runs:

```bash
conda run -n research-assistant python tools/transcribe.py [filename or meetings/]
```

**Behavior:**
- If `[filename]` provided: transcribe that audio file
- If no filename (or `meetings/` specified): automatically detect all audio files without transcripts and process them
- If transcript already exists for a file: skip it
- Output saves to `meetings/[same-name].md`

**Next:** Run `/summarize_meeting [transcript-file].md` to extract action items and create tasks
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

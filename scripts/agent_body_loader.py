"""Shared body loader for the three runtime agent assemblers.

Resolves an agent body from either a shared-bodies dir (as `{id}-core.md`)
or the variant bodies dir (as `{id}.md`), and optionally applies variant
vocabulary substitution for `{{KEY}}` placeholders.

Both `shared_bodies_dirs` and the vocab argument accept either a single path
(legacy) or a list. Lists are processed in order so a `--mode` overlay can
shadow a base shared-bodies entry per-agent (first match wins) and a vocab
overlay can override base vocab keys (later layers win on duplicates).
"""
import json
import re
from pathlib import Path

VOCAB_KEY_PATTERN = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")


def load_vocab(vocab_paths):
    """Load and merge one or more vocab files.

    `vocab_paths` may be None, a single path string (legacy), or a list of
    paths. For lists, files are loaded in order and shallowly merged with
    later layers overriding earlier ones — i.e. the last entry wins on
    duplicate keys. Comment keys (e.g. `_comment_*`) flow through unchanged
    because `_apply_vocab` only consumes keys that appear as `{{KEY}}` in a
    body, so unused keys are silently ignored at substitution time.

    Returns None when there are no paths to load.
    """
    if vocab_paths is None:
        return None
    if isinstance(vocab_paths, str):
        vocab_paths = [vocab_paths]
    if not vocab_paths:
        return None

    merged = {}
    for path in vocab_paths:
        p = Path(path)
        if not p.exists():
            raise FileNotFoundError(
                f"Vocab file not found: {path}. "
                f"Either create it (variant vocab.json) or omit --vocab."
            )
        merged.update(json.loads(p.read_text()))
    return merged


def load_body(agent_id, bodies_dir, shared_bodies_dirs=None, vocab=None):
    """Return the body text for `agent_id` with optional vocab substitution.

    `shared_bodies_dirs` may be None, a single path string (legacy), or a list
    of paths. Lookup order:
      1. For each entry in `shared_bodies_dirs` (in order),
         `{entry}/{agent_id}-core.md`. First match wins.
      2. `{bodies_dir}/{agent_id}.md`.

    The list form lets `setup.sh` pass a `--mode` overlay dir before the base
    shared-bodies dir; an agent that has a mode-specific override (e.g.
    `theory-generator-core.md` under `shared_modes/empirical_first/`) is taken
    from the overlay, while every other agent falls through to the base.

    If `vocab` is provided, every `{{KEY}}` in the loaded body is replaced by
    `vocab[KEY]`. An unresolved key raises KeyError with a pointer to the
    source file, so drift between the core body and a variant vocab is caught
    at setup time rather than silently shipping a literal `{{KEY}}` to an
    agent.
    """
    bodies_dir = Path(bodies_dir)
    if shared_bodies_dirs is None:
        shared_bodies_dirs = []
    elif isinstance(shared_bodies_dirs, str):
        shared_bodies_dirs = [shared_bodies_dirs]

    source = None
    for sbd in shared_bodies_dirs:
        candidate = Path(sbd) / f"{agent_id}-core.md"
        if candidate.exists():
            source = candidate
            break
    if source is None:
        source = bodies_dir / f"{agent_id}.md"
    body = source.read_text()
    if vocab is not None:
        body = _apply_vocab(body, vocab, source)
    return body


def apply_vocab_to_metadata(metadata, vocab, source):
    """Substitute `{{KEY}}` in each string value of the metadata dict.

    Returns a new dict. Non-string values pass through unchanged. Unresolved
    keys raise KeyError (same fail-loud behavior as body substitution), so
    `{{DOMAIN}}` in a shared metadata file cannot silently ship unresolved.
    """
    if vocab is None:
        return metadata
    result = {}
    for key, value in metadata.items():
        if isinstance(value, str):
            result[key] = _apply_vocab(value, vocab, f"{source}:{key}")
        else:
            result[key] = value
    return result


def _apply_vocab(body, vocab, source):
    missing = []

    def replace(match):
        key = match.group(1)
        if key not in vocab:
            missing.append(key)
            return match.group(0)
        return vocab[key]

    rendered = VOCAB_KEY_PATTERN.sub(replace, body)
    if missing:
        unique = sorted(set(missing))
        raise KeyError(
            f"Unresolved vocab key(s) in {source}: "
            + ", ".join(f"{{{{{k}}}}}" for k in unique)
            + ". Add them to the variant vocab.json."
        )
    return rendered

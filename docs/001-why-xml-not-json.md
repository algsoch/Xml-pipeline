# 001 – Why XML and Not JSON (The Threat Model That Killed Every Other System)

JSON is fragile, unrepairable, and actively dangerous in multi-agent swarms.

| Attack / Failure Mode               | JSON                            | XML + xml-pipeline                      |
| ----------------------------------- | ------------------------------- | --------------------------------------- |
| Trailing comma                      | Parse error → crash             | Ignored or repaired                     |
| Missing quotes / unescaped newlines | Parse error → crash             | Tree-sitter recovers                    |
| Duplicate keys                      | Silent data loss or error       | XSD forbids → repair or reject          |
| Order-dependent processing          | Possible                        | Canonicalization makes order irrelevant |
| Whitespace / comment steganography  | Easy and undetectable           | Physically impossible after C14N        |
| Streaming half-written objects      | Impossible to repair mid-stream | Tree-sitter + incremental repair        |
| Schema evolution without breaking   | Extremely hard                  | Add-only + versioning built-in          |
| Forensic audit of what was repaired | None                            | `<huh>` tags on every fix               |

LLMs already emit XML-ish output when prompted.  
We just made the pipeline forgive their sins while never forgiving malice.

JSON was good enough for web APIs.  
It is actively lethal for closed-loop science agents running on exascale clusters with petabytes of irreplaceable data.

XML, when weaponized correctly, is the only protocol that survives contact with real LLMs in the wild.

This is not nostalgia. This is survival.

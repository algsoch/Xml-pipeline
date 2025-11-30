# 002 – Never Touch XML: Pydantic-First Development

You are a Python developer. You should **never** write an XML tag by hand.

```python
from xml_pipeline import Message

class FusionHypothesis(Message):
    root_tag = "fusion-hypothesis"
    density: float          # → <density>1e20</density>
    temperature: float      # → <temperature>15e6</temperature>
    confinement_time: float

await bus.publish(FusionHypothesis(
    density=1e20,
    temperature=15e6,
    confinement_time=1.2
))
```

That’s it.

Under the hood:

- Full XSD validation
- Perfect canonical XML
- Automatic <message-id> and <timestamp>
- Goes through the full immune system pipeline

LLMs emit raw (possibly broken) XML → pipeline repairs it.
Humans emit perfect Python objects → pipeline serializes perfectly.

Two different species, one universal blood type.

This is what makes xml-pipeline the first agent bus that is simultaneously:

- LLM-native
- Developer-native
- Security-native

You write Python. The swarm speaks perfect, auditable, tamper-proof XML.

You never, ever, touch a tag.

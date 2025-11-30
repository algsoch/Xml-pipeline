import pytest
from xml_pipeline import Pipeline
from lxml import etree

def test_repair_malformed():
    broken = b"<cad-task>broken</cad"
    repaired = Pipeline.repair(broken)  # or whatever your API
    assert b"</cad-task>" in repaired
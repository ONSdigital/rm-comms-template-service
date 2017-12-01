template_schema = {
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "label": {"type": "string"},
    "type": {"enum": ["SMS", "EMAIL", "LETTER"]},
    "uri": {"type": "string"},
    "classification": {"type": "object"},
    "params": {"type": "object"},
  },
  "required": ["id", "label", "type", "uri", "classification"]
}

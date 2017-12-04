from application.models.models import CommunicationType

template_schema = {
  "type": "object",
  "properties": {
    "id": {"type": "string"},
    "label": {"type": "string"},
    "type": {"enum": [CommunicationType.LETTER.name, CommunicationType.EMAIL.name, CommunicationType.SMS.name]},
    "uri": {"type": "string"},
    "classification": {"type": "object"},
    "params": {"type": "object"},
  },
  "required": ["id", "label", "type", "uri", "classification"]
}

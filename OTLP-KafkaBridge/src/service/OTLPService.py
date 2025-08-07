import json
from google.protobuf.json_format import MessageToDict # type: ignore



class OTLPService:
    @staticmethod
    def otlp_to_json(otlp_message):
        # Ensure otlp_message is a protobuf message
        if not hasattr(otlp_message, 'DESCRIPTOR'):
            raise TypeError("otlp_message must be a protobuf message with a DESCRIPTOR attribute")
        dict_obj = MessageToDict(otlp_message, preserving_proto_field_name=True)
        return json.dumps(dict_obj, indent=2)



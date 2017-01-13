import json

class CustomJSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder to additionally encode some objects defined in this
    project.
    """
    def default(self, obj):
        """
        Encode the object in JSON.

        :param obj: The object to encode
        :return: The JSON encoding of the object
        """
        if 'to_json' in dir(obj):
            m = getattr(obj, 'to_json')
            if callable(m):
                return m()

        return json.JSONEncoder.default(self, obj)

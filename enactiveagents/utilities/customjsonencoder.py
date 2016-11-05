import json

class CustomJSONEncoder(json.JSONEncoder):
    """
    A custom JSON encoder to additionally encode some objects defined in this
    project.
    """
    def default(self, obj):

        if 'to_json' in dir(obj):
            m = getattr(obj, 'to_json')
            if callable(m):
                return m()

        return json.JSONEncoder.default(self, obj)

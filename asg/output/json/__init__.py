import json


class ClassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__


def il_to_json(output_il, output_file):
    json.dump(output_il, output_file, cls=ClassJSONEncoder)

# def facilities_from_file():
#     import json
#     import os
#     path = os.path.abspath('.')
#     while os.path.basename(path) is not 'tests':
#         path = os.path.dirname(path)
#     facilities_file = os.path.join(path, 'data', 'crest_facilities.json')
#     with open(facilities_file) as f:
#         return json.loads(f)['items']

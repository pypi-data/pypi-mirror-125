import difflib
import json
import re
from copy import copy

import requests

from postpygraphql.extractors import extract_dict_from_headers, extract_dict_from_raw_mode_data, format_object, \
    extract_dict_from_formdata_mode_data, exctact_dict_from_files


class CaseSensitiveDict(dict):

    def update(self, d=None, **kwargs):
        d = d or {}
        for k, v in d.items():
            self[k] = v

    def load(self, postman_environment_file_path):
        with open(postman_environment_file_path, encoding='utf8') as postman_environment_file:
            postman_environment = json.load(postman_environment_file)
            for item in postman_environment['values']:
                if item['enabled']:
                    self[item['key']] = item['value']


class PostPython:
    def __init__(self, postman_collection_file_path):
        with open(postman_collection_file_path, encoding='utf8') as postman_collection_file:
            self.__postman_collection = json.load(postman_collection_file)

        self.__folders = {}
        self.environments = CaseSensitiveDict()
        self.__load()

    def __load(self):
        for fol in self.__postman_collection['item']:
            requests_list = {}
            for request in fol['item']:
                if 'request' in request:
                    request['request']['name'] = request['name']
                    requests_list[normalize_func_name(
                        request['name'])] = PostRequest(self, request['request'])

            col_name = normalize_class_name(fol['name'])
            self.__folders[col_name] = PostCollection(col_name, requests_list)

    def __getattr__(self, item):
        if item in self.__folders:
            return self.__folders[item]
        else:
            folders = list(self.__folders.keys())
            similar_folders = difflib.get_close_matches(item, folders)
            if len(similar_folders) > 0:
                similar = similar_folders[0]
                raise AttributeError('%s folder does not exist in Postman collection.\n'
                                     'Did you mean %s?' % (item, similar))
            else:
                raise AttributeError('%s folder does not exist in Postman collection.\n'
                                     'Your choices are: %s' % (item, ", ".join(folders)))

    def help(self):
        print("Possible methods:")
        for fol in self.__folders.values():
            print()
            fol.help()


class PostCollection:
    def __init__(self, name, requests_list):
        self.name = name
        self.__requests = requests_list

    def __getattr__(self, item):
        if item in self.__requests:
            return self.__requests[item]
        else:
            post_requests = list(self.__requests.keys())
            similar_requests = difflib.get_close_matches(
                item, post_requests, cutoff=0.0)
            if len(similar_requests) > 0:
                similar = similar_requests[0]
                raise AttributeError('%s request does not exist in %s folder.\n'
                                     'Did you mean %s' % (item, self.name, similar))
            else:
                raise AttributeError('%s request does not exist in %s folder.\n'
                                     'Your choices are: %s' % (item, self.name, ", ".join(post_requests)))

    def help(self):
        for req in self.__requests.keys():
            print("post_python.{COLLECTION}.{REQUEST}()".format(
                COLLECTION=self.name, REQUEST=req))


class PostRequest:
    def __init__(self, post_python, data):
        self.name = normalize_func_name(data['name'])
        self.post_python = post_python
        self.request_kwargs = dict()
        self.request_kwargs['url'] = data['url']['raw']
        if 'body' in data and data['body']['mode'] == 'raw' and 'raw' in data['body']:
            self.request_kwargs['json'] = extract_dict_from_raw_mode_data(
                data['body']['raw'])
        if 'body' in data and data['body']['mode'] == 'formdata' and 'formdata' in data['body']:
            self.request_kwargs['data'], self.request_kwargs['files'] = extract_dict_from_formdata_mode_data(
                data['body']['formdata'])
        if 'body' in data and data['body']['mode'] == 'graphql' and 'graphql' in data['body']:
            self.request_kwargs['json'] = normalize_graphql_variables(data['body']['graphql'])
        self.request_kwargs['headers'] = extract_dict_from_headers(
            data['header'])
        self.request_kwargs['method'] = data['method']

    def __call__(self, *args, **kwargs):
        new_env = copy(self.post_python.environments)
        new_env.update(kwargs)
        if 'files' in self.request_kwargs:
            for key, file in self.request_kwargs['files'].items():
                file[1].seek(0)  # flip byte stream for subsequent reads
        formatted_kwargs = format_object(self.request_kwargs, new_env)
        if 'variables' in kwargs.keys():  # directly changing graphql variables if there is a method argument
            if kwargs['variables'] is not None:  # format: your_method(variables=your_data)
                formatted_kwargs['json']['variables'] = kwargs['variables']
        elif args and args[0] is not None:  # if there are args from method, we replace postman's json to this one
            formatted_kwargs['json'] = args[0]
        return requests.request(**formatted_kwargs)

    def set_files(self, data):
        for row in data:
            self.request_kwargs['files'][row['key']
                                         ] = exctact_dict_from_files(row)

    def set_data(self, data):
        for row in data:
            self.request_kwargs['data'][row['key']] = row['value']

    def set_json(self, data):
        self.request_kwargs['json'] = data


def normalize_class_name(string):
    string = re.sub(r'[?!@#$%^&*()_\-+=,./\'\\\"|:;{}\[\]]', ' ', string)
    return string.title().replace(' ', '')


def normalize_func_name(string):
    string = re.sub(r'[?!@#$%^&*()_\-+=,./\'\\\"|:;{}\[\]]', ' ', string)
    return '_'.join(string.lower().split())


def normalize_graphql_variables(graphql_body: dict) -> dict:  # it came as a string from Postman
    variables = graphql_body['variables']
    if len(variables) > 0:  # for cases when there are no variables
        if isinstance(variables, str):
            normalized_variables = normalize_boolean_types(variables)
            graphql_body['variables'] = eval(normalized_variables)
    return graphql_body


def normalize_boolean_types(string: str) -> str:  # have to change Postman's true, false to Python's True, False
    return string.replace(": false", ": False").replace(": true", ": True")

import os
import yaml
import uuid
import kubernetes
import base64

class Operator(object):
    __templates__ = {
        'secret': 'secret'
    }

    def __init__(self, body, meta, spec, logger):
        self.__body__ = body
        self.__meta__ = meta
        self.__spec__ = spec
        self.__logger__ = logger

    def get_spec_value(self, key, default=None):
        if key in self.__spec__:
            return self.__spec__[key]
        if default:
            return default()

    def create_secret(self):
        name = self.__meta__.get('name')
        namespace = self.__meta__.get('namespace')

        admin_password = self.get_spec_value('admin_password', lambda : uuid.uuid4())
        bootstrap_creds = 'access-admin@127.0.0.1=%s' % (admin_password)

        artifactory_lic = self.get_spec_value('artifactory_lic', lambda : '')

        substitions = {
            'name': name,
            'bootstrap_creds': Operator.encode_secret(bootstrap_creds),
            'artifactory_lic': Operator.encode_secret(artifactory_lic)
        }
        template = Operator.get_template('secret', substitions)
        self.patch_owner(template)

        api = kubernetes.client.CoreV1Api()
        obj = api.create_namespaced_secret(
            namespace=namespace,
            body=template,
        )

        self.__logger__.info(f"Test created: %s", obj)

    def patch_owner(self, data):
        body = self.__body__
        meta = self.__meta__
        name = meta.get('name')

        uid = meta.get('uid')

        api_version = body.get('apiVersion')
        kind = body.get('kind')

        data['metadata']['ownerReferences'] = [{
            'apiVersion': api_version,
            'kind': kind,
            'name': name,
            'uid': uid
        }]

    @classmethod
    def get_template(cls, template_name, substitutions):
        template_path = cls.__templates__[template_name]
        path = os.path.join(os.path.dirname(__file__), '../templates', template_path + '.yaml')
        with open(path, 'rt') as yamlfile:
            text = yamlfile.read().format_map(substitutions)
            data = yaml.safe_load(text)

        return data

    @staticmethod
    def encode_secret(value):
        return base64.b64encode(value.encode()).decode()

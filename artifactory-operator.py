import kopf

import kubernetes
import os
import sys
import yaml

from artifactory_operator import Operator


@kopf.on.create('artifactory.operator.k8s.trask.cz', 'v1', 'artifactoryproinstances')
def create_pro(**kwargs):

    @kopf.on.this(id='secret')
    def create_secret(body, meta, spec, logger, **kwargs):
        operator = Operator(body, meta, spec, logger)
        operator.create_secret()


# TODO Umoznit v deploymentu zakazat tuto funkcionalitu (kdyz nebudou cluster opravneni)
def check_crds():
    kube = kubernetes.client.ApiextensionsV1beta1Api()
    list = kube.list_custom_resource_definition()
    crds = [x['metadata']['name'] for x in list.to_dict()['items']]

    check_crd_artifactoryproinstance(kube, crds)


def check_crd_artifactoryproinstance(kube, crds):
    check_crd(kube, crds, 'artifactoryproinstances.artifactory.operator.k8s.trask.cz', 'artifactory_pro_instance_crd.yaml')


def check_crd(kube, crds, name, file):
    if name in crds:
        sys.stdout.write('CRD {crd} already installed'.format(crd=name))
        sys.stderr.write('CRD {crd} already installed ERR'.format(crd=name))
    else:
        # kubernetes.utils.create_from_yaml(kube, os.path.join(os.path.dirname(__file__), 'operator', file))
        with open(os.path.join(os.path.dirname(__file__), 'operator/crd', file)) as f:
            try:
                kube.create_custom_resource_definition(body=yaml.safe_load(f.read()))
                sys.stdout.write('CRD {crd} installed successfully'.format(crd=name))
                sys.stderr.write('CRD {crd} installed successfully ERR'.format(crd=name))
            except ValueError as err:
                if not err.args[0] == 'Invalid value for `conditions`, must not be `None`':
                    raise err


check_crds()

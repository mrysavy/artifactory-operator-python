import sys
import os

from kopf.cli import main

if __name__ == '__main__':
    sys.argv.append('run')
    sys.argv.append('artifactory-operator.py')
    sys.argv.append('--standalone')
    if 'OPERATOR_NAMESPACE' in os.environ:
        sys.argv.append('--namespace=' + os.environ['OPERATOR_NAMESPACE'])
    sys.exit(main())
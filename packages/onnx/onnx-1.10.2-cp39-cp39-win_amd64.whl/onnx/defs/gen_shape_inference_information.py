# SPDX-License-Identifier: Apache-2.0

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from onnx import defs


def main():  # type: () -> None
    # domain -> support level -> name -> [schema]
    with_inference = []
    without_inference = []
    for schema in defs.get_all_schemas():
        domain, name, has_inference = schema.domain, schema.name, schema.has_type_and_shape_inference_function
        elem = (domain, name)
        if has_inference:
            with_inference.append(elem)
        else:
            without_inference.append(elem)
    print(len(with_inference), 'operators have a type/shape inference function.')
    print(len(without_inference), 'do not. These are:')
    for domain, name in sorted(without_inference):
        print(domain, name)


if __name__ == '__main__':
    main()

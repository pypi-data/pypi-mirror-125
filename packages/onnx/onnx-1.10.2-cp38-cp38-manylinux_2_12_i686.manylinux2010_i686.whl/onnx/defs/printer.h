/*
 * SPDX-License-Identifier: Apache-2.0
 */

#pragma once

#include <iostream>

#include "onnx/onnx_pb.h"

#include "onnx/defs/parser.h"

namespace ONNX_NAMESPACE {

std::ostream& operator<<(std::ostream& os, const TensorShapeProto_Dimension& dim);

std::ostream& operator<<(std::ostream& os, const TensorShapeProto& shape);

std::ostream& operator<<(std::ostream& os, const TypeProto_Tensor& tensortype);

std::ostream& operator<<(std::ostream& os, const TypeProto& type);

std::ostream& operator<<(std::ostream& os, const TensorProto& tensor);

std::ostream& operator<<(std::ostream& os, const ValueInfoProto& value_info);

std::ostream& operator<<(std::ostream& os, const ValueInfoList& vilist);

std::ostream& operator<<(std::ostream& os, const AttributeProto& attr);

std::ostream& operator<<(std::ostream& os, const AttrList& attrlist);

std::ostream& operator<<(std::ostream& os, const NodeProto& node);

std::ostream& operator<<(std::ostream& os, const NodeList& nodelist);

std::ostream& operator<<(std::ostream& os, const GraphProto& graph);

} // namespace ONNX_NAMESPACE
# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: model_schema.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x12model_schema.proto\x12\x19telos.cortex.model_schema\"\xdf\x01\n\x0bModelSchema\x12\x42\n\x0fhyperparameters\x18\x01 \x01(\x0b\x32).telos.cortex.model_schema.HyperParameter\x12\x38\n\nparameters\x18\x02 \x01(\x0b\x32$.telos.cortex.model_schema.Parameter\x12>\n\rmodel_details\x18\x03 \x01(\x0b\x32\'.telos.cortex.model_schema.ModelDetails\x12\x12\n\nattributes\x18\x04 \x01(\t\"\x1c\n\tStrVector\x12\x0f\n\x07\x65lement\x18\x01 \x03(\t\"\x1c\n\tF32Vector\x12\x0f\n\x07\x65lement\x18\x01 \x03(\x02\"\xbe\x08\n\x0eHyperParameter\x12\x1a\n\rfit_intercept\x18\x01 \x01(\x08H\x00\x88\x01\x01\x12#\n\x16inverse_regularization\x18\x02 \x01(\x02H\x01\x88\x01\x01\x12?\n\x0c\x63lass_weight\x18\x03 \x01(\x0b\x32$.telos.cortex.model_schema.StrVectorH\x02\x88\x01\x01\x12\x1d\n\x10\x64ual_formulation\x18\x04 \x01(\x08H\x03\x88\x01\x01\x12\x1e\n\x11intercept_scaling\x18\x05 \x01(\x02H\x04\x88\x01\x01\x12\x18\n\x0bl1_l2_ratio\x18\x06 \x01(\x02H\x05\x88\x01\x01\x12\x1a\n\rmax_iteration\x18\x07 \x01(\x05H\x06\x88\x01\x01\x12\x18\n\x0bmulti_class\x18\x08 \x01(\tH\x07\x88\x01\x01\x12\x18\n\x0bn_cpu_cores\x18\t \x01(\x05H\x08\x88\x01\x01\x12\x18\n\x0bregularizer\x18\n \x01(\tH\t\x88\x01\x01\x12\x19\n\x0crandom_state\x18\x0b \x01(\x05H\n\x88\x01\x01\x12 \n\x13optimizer_algorithm\x18\x0c \x01(\tH\x0b\x88\x01\x01\x12\x1c\n\x0f\x65rror_threshold\x18\r \x01(\x02H\x0c\x88\x01\x01\x12\x14\n\x07verbose\x18\x0e \x01(\x05H\r\x88\x01\x01\x12\x17\n\nwarm_start\x18\x0f \x01(\x08H\x0e\x88\x01\x01\x12\x1a\n\rmissing_value\x18\x10 \x01(\tH\x0f\x88\x01\x01\x12\x17\n\ncheck_rank\x18\x11 \x01(\x08H\x10\x88\x01\x01\x12\x0e\n\x01\x43\x18\x12 \x01(\x02H\x11\x88\x01\x01\x12\x11\n\x04\x64ual\x18\x13 \x01(\x08H\x12\x88\x01\x01\x12\x15\n\x08l1_ratio\x18\x14 \x01(\x02H\x13\x88\x01\x01\x12\x15\n\x08max_iter\x18\x15 \x01(\x05H\x14\x88\x01\x01\x12\x13\n\x06n_jobs\x18\x16 \x01(\x02H\x15\x88\x01\x01\x12\x14\n\x07penalty\x18\x17 \x01(\tH\x16\x88\x01\x01\x12\x13\n\x06solver\x18\x18 \x01(\tH\x17\x88\x01\x01\x12\x10\n\x03tol\x18\x19 \x01(\x02H\x18\x88\x01\x01\x42\x10\n\x0e_fit_interceptB\x19\n\x17_inverse_regularizationB\x0f\n\r_class_weightB\x13\n\x11_dual_formulationB\x14\n\x12_intercept_scalingB\x0e\n\x0c_l1_l2_ratioB\x10\n\x0e_max_iterationB\x0e\n\x0c_multi_classB\x0e\n\x0c_n_cpu_coresB\x0e\n\x0c_regularizerB\x0f\n\r_random_stateB\x16\n\x14_optimizer_algorithmB\x12\n\x10_error_thresholdB\n\n\x08_verboseB\r\n\x0b_warm_startB\x10\n\x0e_missing_valueB\r\n\x0b_check_rankB\x04\n\x02_CB\x07\n\x05_dualB\x0b\n\t_l1_ratioB\x0b\n\t_max_iterB\t\n\x07_n_jobsB\n\n\x08_penaltyB\t\n\x07_solverB\x06\n\x04_tol\"\xab\x01\n\tParameter\x12\x19\n\x11\x66\x65\x61ture_names_in_\x18\x01 \x03(\t\x12\x1b\n\x0en_features_in_\x18\x02 \x01(\x05H\x00\x88\x01\x01\x12\x10\n\x08\x63lasses_\x18\x03 \x03(\x05\x12\x0f\n\x07n_iter_\x18\x04 \x03(\x05\x12\x12\n\x05\x63oef_\x18\x05 \x01(\tH\x01\x88\x01\x01\x12\x12\n\nintercept_\x18\x06 \x03(\x02\x42\x11\n\x0f_n_features_in_B\x08\n\x06_coef_\"\xa2\x01\n\x0cModelDetails\x12\x16\n\tfile_type\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x16\n\tFramework\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x14\n\x07Library\x18\x03 \x01(\tH\x02\x88\x01\x01\x12\x16\n\tAlgorithm\x18\x04 \x01(\tH\x03\x88\x01\x01\x42\x0c\n\n_file_typeB\x0c\n\n_FrameworkB\n\n\x08_LibraryB\x0c\n\n_AlgorithmB<\n\x1d\x63om.telos.cortex.model_schemaP\x01Z\x19telos/cortex/model_schemab\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'model_schema_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\035com.telos.cortex.model_schemaP\001Z\031telos/cortex/model_schema'
  _MODELSCHEMA._serialized_start=50
  _MODELSCHEMA._serialized_end=273
  _STRVECTOR._serialized_start=275
  _STRVECTOR._serialized_end=303
  _F32VECTOR._serialized_start=305
  _F32VECTOR._serialized_end=333
  _HYPERPARAMETER._serialized_start=336
  _HYPERPARAMETER._serialized_end=1422
  _PARAMETER._serialized_start=1425
  _PARAMETER._serialized_end=1596
  _MODELDETAILS._serialized_start=1599
  _MODELDETAILS._serialized_end=1761
# @@protoc_insertion_point(module_scope)

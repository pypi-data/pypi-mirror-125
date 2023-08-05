# This file was autogenerated. Do not edit.

from hikaru.model.rel_1_16.v2beta1 import *
from ...custom_models import RobustaPod, RobustaDeployment


KIND_TO_MODEL_CLASS = {
    "Pod": RobustaPod,
    "ReplicaSet": ReplicaSet,
    "DaemonSet": DaemonSet,
    "Deployment": RobustaDeployment,
    "StatefulSet": StatefulSet,
    "Service": Service,
    "ConfigMap": ConfigMap,
    "Event": Event,
    "HorizontalPodAutoscaler": HorizontalPodAutoscaler,
    "Node": Node,
}

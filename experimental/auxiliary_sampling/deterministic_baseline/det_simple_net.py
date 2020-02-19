# coding=utf-8
# Copyright 2020 The Edward2 Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Build a simple, feed forward neural network."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow.compat.v1 as tf
import tensorflow_probability as tfp

tfd = tfp.distributions


def det_simple_net(input_shape, output_scaler=1.):
  """Build a simple, feed forward Bayesian neural net."""

  def output_dist_fn(t):
    loc, untransformed_scale = t
    return tfd.Normal(loc=loc, scale=tf.nn.softplus(untransformed_scale))

  inputs = tf.keras.layers.Input(shape=input_shape)
  hidden = tf.keras.layers.Dense(50, activation='relu')(inputs)
  loc = tf.keras.layers.Dense(1, activation='linear')(hidden)
  untransformed_scale = tfp.layers.VariableLayer(shape=())(loc)
  outputs = tfp.layers.DistributionLambda(output_dist_fn)(
      (loc * output_scaler, untransformed_scale))
  return tf.keras.models.Model(inputs=inputs, outputs=outputs)

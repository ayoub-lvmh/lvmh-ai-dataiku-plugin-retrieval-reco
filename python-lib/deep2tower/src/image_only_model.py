import os
import dataiku
from dataiku import pandasutils as pdu
import pandas as pd
import numpy as np
from typing import Dict, Text
from ast import literal_eval
import pickle
import json
from json.decoder import JSONDecodeError
from google.cloud import bigquery

import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.framework import dtypes
from tensorflow_io.bigquery import BigQueryClient
from tensorflow_io.bigquery import BigQueryReadSession
import tensorflow_datasets as tfds
from tensorflow.python.data.ops import dataset_ops
import tensorflow_datasets as tfds
import tensorflow_recommenders as tfrs
import tensorflow_ranking as tfr

from lvmh_core_lib.lib.common.cloud.google_manager import GoogleManager

dataset_ops.ParallelInterleaveDataset = {}

class ClientModel(tf.keras.Model):

    def __init__(self, vocab, config):
        super().__init__()
        embedding_dimension = config['embedding_dimension']

        self.lstm_layer = tf.keras.layers.GRU(embedding_dimension, dropout=0.2, go_backwards=True)
        self.prev_image_embedding_pca = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=[None, config['seq_len'] * config['pca_len']], dtype=tf.float32),
            tf.keras.layers.Reshape((config['seq_len'], config['pca_len'])),
            tf.keras.layers.Dense(embedding_dimension, activation='relu')
        ])

    def call(self, inputs):
        prev_product_image_embedding = self.prev_image_embedding_pca(inputs["image_embedding_pca"])
        product_lstm_output = self.lstm_layer(prev_product_image_embedding)

        return product_lstm_output


class ItemModel(tf.keras.Model):

    def __init__(self, vocab, config):
        super().__init__()

        self.image_embedding = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(config['pca_len']), dtype=tf.float32),
            tf.keras.layers.Dense(config['pca_len'], activation='relu'),
        ])

    def call(self, inputs):
        output_tensor = tf.concat([
            self.image_embedding(inputs["last_image_embedding_pca"]),
        ], axis=1)
        return output_tensor

    
class RecommendationModel(tfrs.models.Model):

    def __init__(self, items, vocab, config):
        super().__init__()
        self.vocab = vocab
        self.items = items
        self.config = config
        self.embedding_dimension = config['embedding_dimension']

        self._client_model = ClientModel(self.vocab, self.config)
        self._item_model = ItemModel(self.vocab, self.config)
        self.query_model = tf.keras.Sequential([
            self._client_model,
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(rate=config['fc_dropout']),
            tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(config['fc_reg'])),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(rate=config['fc_dropout']),
            tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(config['fc_reg'])),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(rate=config['fc_dropout']),
            tf.keras.layers.Dense(32),
#             tf.keras.layers.Lambda(lambda x:  tf.linalg.l2_normalize(x, axis=-1)), # https://github.com/tensorflow/recommenders/issues/633
        ])
        self.candidate_model = tf.keras.Sequential([
            self._item_model,
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(rate=config['fc_dropout']),
            tf.keras.layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(config['fc_reg'])),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(rate=config['fc_dropout']),
            tf.keras.layers.Dense(64, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(config['fc_reg'])),
            tf.keras.layers.BatchNormalization(),
            tf.keras.layers.Dropout(rate=config['fc_dropout']),
            tf.keras.layers.Dense(32),
#             tf.keras.layers.Lambda(lambda x:  tf.linalg.l2_normalize(x, axis=-1)),
        ])
        self.nc_metric = tfrs.metrics.FactorizedTopK(
            candidates=self.items.batch(1024).map(self.candidate_model),
            ks = [10]
        )
        self.task: tf.keras.layers.Layer = tfrs.tasks.Retrieval(
            loss = tfr.keras.losses.SoftmaxLoss(),
            metrics = [self.nc_metric],
        )

    def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
        query_embeddings = self.query_model({
            "image_embedding_pca": features["image_embedding_pca"],
        })
        item_embeddings = self.candidate_model({
            "last_image_embedding_pca": features["last_image_embedding_pca"],
        })
        return self.task(query_embeddings,
                         item_embeddings,
                         candidate_sampling_probability = tf.cast(features['last_product_purchase_frequency'],
                                                                  tf.float32),
                         compute_metrics=not training,
                         compute_batch_metrics=not training)
    
    def call(self, features):
        query_embeddings = self.query_model({
            "image_embedding_pca": features["image_embedding_pca"],
        })
        item_embeddings = self.candidate_model({
            "last_image_embedding_pca": features["last_image_embedding_pca"],
        })
        return tf.linalg.matmul(query_embeddings, item_embeddings, transpose_b=True)
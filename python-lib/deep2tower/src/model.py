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

    def __init__(self, vocab, product_id_embedding_layer, product_subcat_embedding_layer, config):
        super().__init__()
        embedding_dimension = config['embedding_dimension']

        self.client_embedding = tf.keras.Sequential([
          tf.keras.layers.StringLookup(
            vocabulary=vocab['client_id'], mask_token=None),
          tf.keras.layers.Embedding(len(vocab['client_id']) + 1,
                                    embedding_dimension,
                                    embeddings_regularizer=tf.keras.regularizers.l2(0.01),
                                   )
        ])
        self.client_gender_embedding = tf.keras.Sequential([
          tf.keras.layers.StringLookup(
            vocabulary=vocab['client_gender'], mask_token=None),
          tf.keras.layers.Embedding(len(vocab['client_gender']) + 1, embedding_dimension)
        ])
        self.client_nationality_embedding = tf.keras.Sequential([
          tf.keras.layers.StringLookup(
            vocabulary=vocab['client_nationality'], mask_token=None),
          tf.keras.layers.Embedding(len(vocab['client_nationality']) + 1, embedding_dimension)
        ])
        self.client_segment_onehot = tf.keras.Sequential([
          tf.keras.layers.StringLookup(
            vocabulary=vocab['client_segment'], mask_token=None, output_mode='one_hot'),
        ])
        self.month_of_year_embedding = tf.keras.Sequential([
          tf.keras.layers.IntegerLookup(
            vocabulary=vocab['last_month_of_year'], mask_token=None),
          tf.keras.layers.Embedding(len(vocab['last_month_of_year']) + 1, embedding_dimension)
        ])
#         self.timestamp_embedding = tf.keras.Sequential([
#             tf.keras.layers.Discretization(vocab['timestamp_buckets'].tolist()),
#             tf.keras.layers.Embedding(len(vocab['timestamp_buckets']) + 1, embedding_dimension),
#         ])
#         self.product_macro_offer_embedding = tf.keras.Sequential([
#           tf.keras.layers.StringLookup(
#             vocabulary=vocab['last_product_macro_offer_code'], mask_token=None, output_mode='one_hot'),
#         ])
#         self.product_offer_embedding = tf.keras.Sequential([
#           tf.keras.layers.StringLookup(
#             vocabulary=vocab['last_product_offer_code'], mask_token=None, output_mode='one_hot'),
#         ])
        self.prev_moy_embedding = tf.keras.Sequential([
          tf.keras.layers.IntegerLookup(
            vocabulary=vocab['last_month_of_year'], mask_token=None),
          tf.keras.layers.Embedding(len(vocab['last_month_of_year']) + 1, embedding_dimension),
        ])
        self.prev_product_embedding = product_id_embedding_layer
        self.prev_sub_category_embedding = product_subcat_embedding_layer
        self.prev_product_business_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
            vocabulary=vocab['last_product_business_desc'], mask_token=None),
            tf.keras.layers.Embedding(len(vocab['last_product_business_desc']) + 1, 4),
        ])
        self.prev_boutique_area_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
            vocabulary=vocab['last_boutique_area'], mask_token=None),
            tf.keras.layers.Embedding(len(vocab['last_boutique_area']) + 1, embedding_dimension),
        ])
        self.lstm_layer = tf.keras.layers.GRU(embedding_dimension, dropout=0.2, go_backwards=True)
        self.layer_norm_pre_rnn = tf.keras.layers.LayerNormalization()
        self.prev_image_embedding_pca = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=[None, config['seq_len'] * config['pca_len']], dtype=tf.float32),
            tf.keras.layers.Reshape((config['seq_len'], config['pca_len'])),
            tf.keras.layers.Dense(embedding_dimension, activation='relu')
        ])
#         self.normalized_timestamp = tf.keras.layers.Normalization(axis=None)
#         self.normalized_timestamp.adapt(timestamps)

    def call(self, inputs):
        prev_sub_category_embedding = self.prev_sub_category_embedding(inputs["prev_product_sub_category"])
        prev_product_embedding = self.prev_product_embedding(inputs["prev_product_id"])
        prev_product_business_embedding = self.prev_product_business_embedding(inputs["prev_product_business_desc"])
        prev_moy_emb = self.prev_moy_embedding(inputs["prev_month_of_year"])
        prev_boutique_area_embedding = self.prev_boutique_area_embedding(inputs["prev_boutique_area"])
        prev_product_image_embedding = self.prev_image_embedding_pca(inputs["image_embedding_pca"])
        prev_emb_concat = tf.concat([prev_product_embedding,
                                     prev_sub_category_embedding,
                                     prev_product_business_embedding,
                                     prev_boutique_area_embedding,
                                     prev_moy_emb,
                                     prev_product_image_embedding,
                                    ], axis = 2)
#         prev_emb_layer_norm = self.layer_norm_pre_rnn(prev_emb_concat)
        product_lstm_output = self.lstm_layer(prev_emb_concat)

        return tf.concat([
            self.client_embedding(inputs["client_id"]),
            self.client_gender_embedding(inputs["client_gender"]),
            self.client_nationality_embedding(inputs["client_nationality"]),
            self.client_segment_onehot(inputs["client_segment"]),
            self.month_of_year_embedding(inputs["last_month_of_year"]),
#             self.timestamp_embedding(inputs["last_transaction_date"]),
#             self.product_offer_embedding(inputs["last_product_offer_code"]),
#             self.prev_1_product(inputs["prev_product_id"][:, 0]),
#             self.prev_image_embedding_pca(inputs["image_embedding_pca"])
            product_lstm_output
        ], axis=1)


class ItemModel(tf.keras.Model):

    def __init__(self, vocab, embedding_dimension, product_id_embedding_layer, product_subcat_embedding_layer):
        super().__init__()

        self.item_id_embedding = product_id_embedding_layer
        self.product_business_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=vocab['last_product_business_desc'], mask_token=None),
            tf.keras.layers.Embedding(len(vocab['last_product_business_desc']) + 1,
                                      embedding_dimension, name='product_business_emb')
        ])
        self.product_type_embedding = tf.keras.Sequential([
            tf.keras.layers.StringLookup(
                vocabulary=vocab['last_product_type_desc'], mask_token=None),
            tf.keras.layers.Embedding(len(vocab['last_product_type_desc']) + 1, embedding_dimension)
        ])
        self.product_sub_category_embedding = product_subcat_embedding_layer
        self.image_embedding = tf.keras.Sequential([
            tf.keras.layers.InputLayer(input_shape=(12), dtype=tf.float32),
            tf.keras.layers.Dense(12, activation='relu'),
#             tf.keras.layers.Identity()
        ])
        self.product_price_embedding = tf.keras.Sequential([
            tf.keras.layers.Discretization(vocab['last_product_list_price'].tolist()),
            tf.keras.layers.Embedding(len(vocab['last_product_list_price']) + 1, embedding_dimension),
        ])
        self.cross_net = tfrs.layers.dcn.Cross()

    def call(self, inputs):

        product_attributes_embedding = tf.concat([
            self.product_business_embedding(inputs["last_product_business_desc"]),
            self.product_type_embedding(inputs["last_product_type_desc"]),
            self.product_sub_category_embedding(inputs["last_product_sub_category"]),
        ], axis=1)
        product_attributes_cross_net = self.cross_net(product_attributes_embedding)
        output_tensor = tf.concat([
            self.item_id_embedding(inputs["last_product_id"]),
            product_attributes_cross_net,
            self.product_price_embedding(inputs['last_product_list_price']),
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
        self._product_id_embedding_layer = tf.keras.Sequential([
          tf.keras.layers.StringLookup(
            vocabulary=vocab['last_product_id'], mask_token=None),
          tf.keras.layers.Embedding(len(vocab['last_product_id']) + 1,
                                    self.embedding_dimension,
#                                     embeddings_regularizer=tf.keras.regularizers.l2(0.0001),
                                   ),
        ])
        self._product_subcat_embedding_layer = tf.keras.Sequential([
          tf.keras.layers.StringLookup(
            vocabulary=vocab['last_product_sub_category'], mask_token=None),
          tf.keras.layers.Embedding(len(vocab['last_product_sub_category']) + 1, self.embedding_dimension),
        ])
        self._client_model = ClientModel(self.vocab, self._product_id_embedding_layer, 
                                         self._product_subcat_embedding_layer, self.config)
        self._item_model = ItemModel(self.vocab, self.embedding_dimension, self._product_id_embedding_layer, 
                                     self._product_subcat_embedding_layer)
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
#         self.reco_metrics = tfrs.metrics.FactorizedTopK(
#             candidates=items.batch(1024).map(self.candidate_model),
#             ks = (1, 10)
#         )
        self.nc_metric = tfrs.metrics.FactorizedTopK(
            candidates=self.items.batch(1024).map(self.candidate_model),
            ks = [10],
#             name = 'nc_top_k'
        )
#         self.diversity_metrics = DiveristyTopK(
#             candidates=items.batch(1024).map(self.candidate_model),
#             nb_candidates=ITEMS_COUNT,
#             ks = (1, 10)
#         )
        self.task: tf.keras.layers.Layer = tfrs.tasks.Retrieval(
            loss = tfr.keras.losses.SoftmaxLoss(),
            metrics = [self.nc_metric],
#             temperature = 0.2,
        )

    def compute_loss(self, features: Dict[Text, tf.Tensor], training=False) -> tf.Tensor:
        query_embeddings = self.query_model({
            "client_id": features["client_id"],
            "client_gender": features["client_gender"],
            "client_nationality": features["client_nationality"],
            "client_segment": features["client_segment"],
            "last_month_of_year": features["last_month_of_year"],
            "last_transaction_date": features["last_transaction_date"],
            "last_product_macro_offer_code": features["last_product_macro_offer_code"],
            "last_product_offer_code": features["last_product_offer_code"],
            "prev_product_id": features["prev_product_id"],
            "prev_product_sub_category": features["prev_product_sub_category"],
            "prev_product_business_desc": features["prev_product_business_desc"],
            "prev_month_of_year": features["prev_month_of_year"],
            "prev_boutique_area": features["prev_boutique_area"],
            "image_embedding_pca": features["image_embedding_pca"],
        })
        item_embeddings = self.candidate_model({
            "last_product_id": features["last_product_id"],
            "last_product_business_desc": features["last_product_business_desc"],
            "last_image_embedding_pca": features["last_image_embedding_pca"],
            "last_product_type_desc": features["last_product_type_desc"],
            "last_product_sub_category": features["last_product_sub_category"],
            "last_product_list_price": features["last_product_list_price"],
        })
        return self.task(query_embeddings,
                         item_embeddings,
                         candidate_sampling_probability = tf.cast(features['last_product_purchase_frequency'],
                                                                  tf.float32),
                         compute_metrics=not training,
                         compute_batch_metrics=not training)

    def call(self, features):
        query_embeddings = self.query_model({
            "client_id": features["client_id"],
            "client_gender": features["client_gender"],
            "client_nationality": features["client_nationality"],
            "client_segment": features["client_segment"],
            "last_month_of_year": features["last_month_of_year"],
            "last_transaction_date": features["last_transaction_date"],
            "last_product_macro_offer_code": features["last_product_macro_offer_code"],
            "last_product_offer_code": features["last_product_offer_code"],
            "prev_product_id": features["prev_product_id"],
            "prev_product_sub_category": features["prev_product_sub_category"],
            "prev_product_business_desc": features["prev_product_business_desc"],
            "prev_month_of_year": features["prev_month_of_year"],
            "prev_boutique_area": features["prev_boutique_area"],
            "image_embedding_pca": features["image_embedding_pca"],
        })
        item_embeddings = self.candidate_model({
            "last_product_id": features["last_product_id"],
            "last_product_business_desc": features["last_product_business_desc"],
            "last_image_embedding_pca": features["last_image_embedding_pca"],
            "last_product_type_desc": features["last_product_type_desc"],
            "last_product_sub_category": features["last_product_sub_category"],
            "last_product_list_price": features["last_product_list_price"],
        })
        return tf.linalg.matmul(query_embeddings, item_embeddings, transpose_b=True)
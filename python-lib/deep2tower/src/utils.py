import os
import numpy as np
import pandas as pd
import pickle
import json
from typing import Dict, Text
from json.decoder import JSONDecodeError
from tqdm import tqdm
import dataiku

import tensorflow as tf
from tensorflow.python.framework import ops
from tensorflow.python.framework import dtypes
from tensorflow_io.bigquery import BigQueryClient
from tensorflow_io.bigquery import BigQueryReadSession
import tensorflow_datasets as tfds

from lvmh_core_lib.lib.common.cloud.google_manager import GoogleManager
import tensorflow_datasets as tfds
import tensorflow_recommenders as tfrs

# Google Manager initializer
credential_name = dataiku.get_custom_variables().get(
    "credentials_name", "google_credentials"
)
credential_path = dataiku.get_custom_variables()[credential_name]
try:
    isinstance(json.loads(credential_path), dict)
    credential_is_path = False
except JSONDecodeError as e:
    credential_is_path = True

# Google Manager initializer
gm = GoogleManager(
    credentials=credential_path,
    credential_is_path=credential_is_path,
)

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

def transform_row(row_dict):
    row_dict['last_image_embedding_pca'] = tf.ensure_shape(row_dict['last_image_embedding_pca'], [12])

    return row_dict

def read_bigquery(project_id, dataset_id, table_name, UNUSED_COLUMNS = []):
    tensorflow_io_bigquery_client = BigQueryClient()
    selected_fields_dict = dict()
    CSV_SCHEMA = gm._GoogleManager__bigquery_client.get_table(
        f"{project_id}.{dataset_id}.{table_name}"
    ).schema
    
    for field in CSV_SCHEMA:
        if field.name not in UNUSED_COLUMNS:
            selected_fields_dict[field.name] = {
                "mode": tensorflow_io_bigquery_client.FieldMode.NULLABLE
                if field.mode == "NULLABLE"
                else tensorflow_io_bigquery_client.FieldMode.REPEATED
                if field.mode == "REPEATED"
                else tensorflow_io_bigquery_client.FieldMode.REQUIRED,
                "output_type": dtypes.double
                if field.field_type == "FLOAT"
                else dtypes.int64
                if field.field_type == "INTEGER"
                else dtypes.int64
                if field.field_type == "TIMESTAMP"
                else dtypes.string
                ,
            }
    read_session = tensorflow_io_bigquery_client.read_session(
      "projects/" + project_id,
      project_id, table_name, dataset_id,
      selected_fields_dict,
      requested_streams=1)

    dataset = read_session.parallel_read_rows()
#     transformed_ds = dataset.map(transform_row)
    return dataset

def save_artifacts(folder_path, vocab, model, model_config):
    model_weights_path = os.path.join(folder_path, 'model_weights')
    vocab_path = os.path.join(folder_path, 'vocab.pkl')
    model_config_path = os.path.join(folder_path, 'model_config.json')
    # Save model weights
    model.save_weights(model_weights_path, save_format='tf')
    # Save vocab dict
    with open(vocab_path, 'wb') as f:
        pickle.dump(vocab, f)
    with open(model_config_path, 'w', encoding='utf-8') as f:
        json.dump(model_config, f, ensure_ascii=False, indent=4)

def get_predictions_df(model, data, items, K, product_col = 'last_product_id'):
    """Computes a recommendation prediction dataset with Top K reco per client,
    based on client and product embbedings.

    :return: Pandas dataframe with columns client_id, product_reco, product_reco_rank and product_score.
    :rtype: pd.DataFrame
    """
    brute_force = tfrs.layers.factorized_top_k.BruteForce()
    brute_force.index_from_dataset(
        items.batch(256).map(lambda x: (x[product_col], model.candidate_model(x)))
    )
    clients_list = []
    product_reco_list = []
    product_reco_score_list = []
    for elem in tqdm(data):
        embbedings = model.query_model(elem)
        scores, recos = brute_force(embbedings, k=K)
        clients_list.append(elem['client_id'])
        product_reco_list.append(recos)
        product_reco_score_list.append(scores)
    clients_ids = tf.concat(clients_list, axis=0)
    client_ids_repeated = np.repeat(clients_ids, K)
    product_reco = tf.concat(product_reco_list, axis=0).numpy().reshape(-1)
    product_score = tf.concat(product_reco_score_list, axis=0).numpy().reshape(-1)
    product_reco_rank = np.tile(list(range(0, K)), len(clients_ids))
    predictions_df = pd.DataFrame({'client_id': client_ids_repeated, 'product_reco': product_reco, \
                               'product_reco_rank': product_reco_rank, 'product_score': product_score})
    predictions_df['client_id'] = predictions_df.client_id.str.decode("utf-8")
    predictions_df['product_reco'] = predictions_df.product_reco.str.decode("utf-8")
    return predictions_df
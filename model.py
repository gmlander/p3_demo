import tensorflow as tf
import tensorflow.keras.layers as layers
from tensorflow.keras.models import Model

NUM_POS_FEATS = 8
NUM_GAME_FEATS = 4

tf.set_random_seed(42)

def input_fn(is_training, features, labels, batch_size = 256):
    
    def get_fields(record_feats, record_label):
        # Define features
        neighbors, game_feats = record_feats

        feats = {'neighbors': neighbors,
                'game_feats': game_feats}
        
        return feats, [record_label]

        
    dataset = tf.data.Dataset.from_tensor_slices((features, labels))
    dataset = dataset.shuffle(5000, reshuffle_each_iteration=True).repeat()
    dataset = dataset.map(map_func = get_fields,
                            num_parallel_calls = tf.data.experimental.AUTOTUNE).batch(batch_size = batch_size,
                            drop_remainder=True)
    dataset = dataset.prefetch(tf.contrib.data.AUTOTUNE)
    return dataset

def create_model(**kwargs):
    """Creates a tf.Keras Model for page type and relevance classification.

    Returns:
    The compiled Keras model (still needs to be trained)
    """
    low_drop = kwargs.setdefault('drop_rate', .3)
    pred_drop = low_drop/2


    if kwargs.setdefault('activation_type', 'selu') == 'selu':
        K_INIT = 'lecun_normal'
        DROPOUT_LAYER = layers.AlphaDropout
    else:
        K_INIT = 'glorot_uniform'
        DROPOUT_LAYER = layers.Dropout

    #########################################################################
    #################### BUILD MODEL ########################################
    #########################################################################

    ############################## INPUTS ########################################
    ##### sentence level inputs

    # 8 positional features
    # tl, t, tr, r, br, b, bl, l
    # -2 = unknown
    # -1 = mine
    # 0 = clear
    # 1-6 = number of mines
    neighbors = layers.Input(shape=(NUM_POS_FEATS,), dtype = tf.int64, name = 'neighbors')

    # game state features
    # total number of cells, total number of mines, number of known cells, number of known mines
    game_feats = layers.Input(shape=(NUM_GAME_FEATS,), dtype = tf.int64, name = 'game_feats')

    ############################## DENSE LAYERS ###############################

    dense_neighbors = layers.Dense(kwargs['num_nodes'], kernel_initializer=K_INIT,
                                    activation=kwargs['activation_type'])(neighbors)

    dense_game_feats = layers.Dense(int(kwargs['num_nodes']/4), kernel_initializer=K_INIT,
                                    activation=kwargs['activation_type'])(game_feats)

    

    # create additional layers if needed
    for _ in range(kwargs['num_pre_merge_layers'] - 1):
        drop_neighbors = DROPOUT_LAYER(low_drop)(dense_neighbors)
        drop_game_feats = DROPOUT_LAYER(low_drop)(dense_game_feats)

        
        dense_neighbors = layers.Dense(kwargs['num_nodes'], kernel_initializer=K_INIT,
                                    activation= kwargs['activation_type'])(drop_neighbors)
        dense_game_feats = layers.Dense(int(kwargs['num_nodes']/4), kernel_initializer=K_INIT,
                                    activation= kwargs['activation_type'])(drop_game_feats)

    ############################## MERGE ###############################

    merge_feats = layers.concatenate([dense_neighbors, dense_game_feats])

    #################### ADDITIONAL DENSE LAYERS & PRED ################

    for _ in range(kwargs['num_post_merge_layers'] - 1):
        drop_merge_feats = DROPOUT_LAYER(pred_drop)(merge_feats)
        
        dense_merge_feats = layers.Dense(kwargs['num_nodes'], kernel_initializer=K_INIT,
                                    activation= kwargs['activation_type'])(drop_merge_feats)


    # prediction layer
    pred = layers.Dense(1, activation='softsign', name = 'has_mine')(dense_merge_feats)

    model = Model(inputs = [neighbors,
                            game_feats],
                  outputs = pred)

    if kwargs.setdefault('optimizer', 'adam') == 'adam':
        opt = tf.keras.optimizers.Adam(kwargs.setdefault('learning_rate', .001))
    else:
        opt = kwargs['optimizer']
    
    model.compile(loss='hinge', optimizer= opt)

    return model
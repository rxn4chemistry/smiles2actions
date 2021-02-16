# Training the transformer model

### General set-up

For simplicity, set the following environment variables:
```bash
export DATA_DIR="$(pwd)"
export CODE_DIR="$(dirname "$DATA_DIR")"  # root directory of repository
```

`DATA_DIR` can be changed to any other location containing the data to train on.
We assume that `DATA_DIR` contains the following files:
```bash
src-test.txt    src-train.txt   src-valid.txt   tgt-test.txt    tgt-train.txt   tgt-valid.txt
```

### Data pre-processing

Convert the data to the format required by OpenNMT:
```bash
onmt_preprocess \
  -train_src $DATA_DIR/src-train.txt -train_tgt $DATA_DIR/tgt-train.txt \
  -valid_src $DATA_DIR/src-valid.txt -valid_tgt $DATA_DIR/tgt-valid.txt \
  -save_data $DATA_DIR/preprocessed -src_seq_length 300 -tgt_seq_length 300 \
  -src_vocab_size 2000 -tgt_vocab_size 2000
```

### Model training

To then train the transformer model with OpenNMT:
```bash
onmt_train \
  -data $DATA_DIR/preprocessed  -save_model  $DATA_DIR/models/model  \
  -seed 42 -save_checkpoint_steps 10000 -keep_checkpoint 5 \
  -train_steps 500000 -param_init 0  -param_init_glorot \
  -max_generator_batches 32 -batch_size 1024 -batch_type tokens \
  -normalization tokens -max_grad_norm 0  -accum_count 4 \
  -optim adam -adam_beta1 0.9 -adam_beta2 0.998 -decay_method noam \
  -warmup_steps 8000  -learning_rate 2 -label_smoothing 0.0 \
  -report_every 1000  -valid_batch_size 8 -layers 4 -rnn_size 256 \
  -word_vec_size 256 -encoder_type transformer -decoder_type transformer \
  -dropout 0.1 -position_encoding -valid_steps 20000 \
  -global_attention general -global_attention_function softmax \
  -self_attn_type scaled-dot -heads 8 -transformer_ff 2048 -gpu_ranks 0
```
Training the model can take up to a few days in a GPU-enabled environment.
For testing purposes in a CPU-only environment, the same command with `-save_checkpoint_steps 10` and `-train_steps 10` (and removing `-gpu_ranks 0) will take only a few minutes.

### Model training

The model can be used on new chemical equations with the following command
```bash
onmt_translate \
  -model $DATA_DIR/models/model_step_500000.pt \
  -src $DATA_DIR/src-test.txt \
  -tgt $DATA_DIR/tgt-test.txt \
  -output $DATA_DIR/pred-test.txt \
  -verbose -max_length 400 -batch_size 4 \
  -gpu 0
```

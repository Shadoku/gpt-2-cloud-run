  
#!/bin/sh

if [ "$#" -ne 1 ]; then
    echo "Y2ou must enter the model name as a parameter, e.g.: sh download_model.sh 117M"
    exit 1
fi

model=$1

mkdir -p trained_model

# TODO: gsutil rsync -r gs://gpt-2/models/ models/
for filename in checkpoint encoder.json hparams.json model.ckpt.data-00000-of-00001 model.ckpt.index model.ckpt.meta vocab.bpe; do
  fetch=$model/$filename
  echo "Fetching $fetch"
  curl --output models https://storage.googleapis.com/gpt-2/models/$fetch
done

from torch.utils.data import DataLoader
from sentence_transformers import losses, util
from sentence_transformers import LoggingHandler, SentenceTransformer, evaluation
from sentence_transformers.readers import InputExample
import logging
from datetime import datetime
import csv
import os
from zipfile import ZipFile
import random

## Just some code to print debug information to stdout
logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])
logger = logging.getLogger(__name__)

## Config
model = SentenceTransformer('all-MiniLM-L6-v2') # all-MiniLM-L6-v2 as base model
num_epochs = 1
train_batch_size = 16
dataset_path = 'data/'
model_save_path = 'model/training_MultipleNegativesRankingLoss-'+datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
os.makedirs(model_save_path, exist_ok=True)

## Read train data
train_samples = []
with open(os.path.join(dataset_path, "train_data.csv"), encoding='utf8') as fIn:
    reader = csv.DictReader(fIn, delimiter='|', quoting=csv.QUOTE_NONE)
    for row in reader:
        if row['label'] == '1':
            train_samples.append(InputExample(texts=[row['title_1'], row['title_2']], label=1))
            train_samples.append(InputExample(texts=[row['title_2'], row['title_1']], label=1)) #if A is a duplicate of B, then B is a duplicate of A

## Create a DataLoader
train_dataloader = DataLoader(train_samples, shuffle=True, batch_size=train_batch_size)
train_loss = losses.MultipleNegativesRankingLoss(model)


## Evaluator
dev_sentences1 = []
dev_sentences2 = []
dev_labels = []
with open(os.path.join(dataset_path, "dev_data.csv"), encoding='utf8') as fIn:
    reader = csv.DictReader(fIn, delimiter='|', quoting=csv.QUOTE_NONE)
    for row in reader:
        dev_sentences1.append(row['title_1'])
        dev_sentences2.append(row['title_2'])
        dev_labels.append(int(row['label']))


binary_acc_evaluator = evaluation.BinaryClassificationEvaluator(dev_sentences1, dev_sentences2, dev_labels)
evaluators = [binary_acc_evaluator]

# Create a SequentialEvaluator
seq_evaluator = evaluation.SequentialEvaluator(evaluators, main_score_function=lambda scores: scores[-1])
logger.info("Evaluate model without training")
seq_evaluator(model, epoch=0, steps=0, output_path=model_save_path)


# Train the model
model.fit(train_objectives=[(train_dataloader, train_loss)],
          evaluator=seq_evaluator,
          epochs=num_epochs,
          warmup_steps=0,
          output_path=model_save_path
          )
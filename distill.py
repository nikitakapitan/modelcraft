"""
This file:
- init Distiller(config) : which defines task, data, tokenizer, model and metrics
...
"""

import os
import yaml
import logging
import argparse
import time
from modelcraft.efficiency.DistillationTrainer import DistillationTrainer
from modelcraft.efficiency.DistillationTrainingArguments import DistillationTrainingArguments
from modelcraft.Distiller import Distiller


# Initialize logging
if not os.path.exists('/content/logs/'):
    os.makedirs('/content/logs/')
logging.basicConfig(filename=f"logs/train_{time.strftime('%Y-%m-%d_%H-%M-%S')}.log", level=logging.INFO)

def main(args):

    with open(args, 'r') as f:
        config = yaml.safe_load(f)
    distiller = Distiller(config)

    # Tokenize
    tokenize = lambda batch: distiller.student_tokenizer(batch['text'], truncation=True)
    dataset_encoded = distiller.dataset.map(tokenize, batched=True)

    data_cfg = f'_{config["DATASET_CONFIG_NAME"]}' if config["DATASET_CONFIG_NAME"] else ''

    # Distill Training Arguments
    student_training_args =  DistillationTrainingArguments(
        output_dir=f'{config["DISTILL_TEACHER"]}-distilled-{config["DATASET_NAME"]}{data_cfg}',
        num_train_epochs=config['NUM_EPOCHS'],
        learning_rate=config['LEARNING_RATE'],
        per_device_train_batch_size=config['BATCH_SIZE'],
        per_device_eval_batch_size=config['BATCH_SIZE'],
        alpha = config['DISTILL_ALPHA'],
        weight_decay=0.01,
        evaluation_strategy='epoch',
        disable_tqdm=False,
        logging_dir='./logs',
        push_to_hub=True,
        log_level=config['LOG_LEVEL'],
    )

    distill_trainer = DistillationTrainer(
        model_init=distiller.student_init, # dummy init, instead of from_pretrained
        teacher_model=distiller.teacher,
        args=student_training_args,
        train_dataset=dataset_encoded['train'],
        eval_dataset=dataset_encoded[config['EVAL_DATASET']],
        tokenizer=distiller.student_tokenizer,
        compute_metrics=distiller.compute_metrics_func,
    )

    # Train and Evaluate
    logging.info("Start [Distillation] TRAINING")
    distill_trainer.train()
    distill_trainer.evaluate()

    # Push to Hub
    distill_trainer.push_to_hub()
    logging.info("Model pushed to Hugging Face Hub.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Distilling models with Hugging Face Transformers')
    parser.add_argument('--config', type=str, required=True, help='Path to the YAML config file')
    args = parser.parse_args()
    main(args.config)
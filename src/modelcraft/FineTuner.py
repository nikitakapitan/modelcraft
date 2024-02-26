"""
FineTuner prepares the fine-tuning.

First, the parents class Trainer:
- defines the type of task, loads the data, 
- init tokenizer and the model and defines metrics to compute

FineTuner ONLY overwrites define_compute_metrics to
=> re-define compute_metrics_func with accuracy and f1_score
"""

from modelcraft.Trainer import Trainer
import logging
import evaluate

class FineTuner(Trainer):

    def __init__(self, config):
        super().__init__(config)
        self._load_metrics()         # self.metrics

    def _load_metrics(self):
        """ This function cast metric names from yaml to real python functions

        output is a dict : keys = functions, values = configs:
        {evaluate..metrics.accuracy : {},
         evaluate..metrics.f1_score : {average: weighted}
         evaluate..metrics..glue    : {}
        """
        metrics_functions = {}
        for metric_dict in self.config['METRICS']:
            # ex. metric_dict = {'f1': {'average': 'weighted'}}
            for metric_name, metric_cfg in metric_dict.items():
                # ex. metric_name = 'f1'; metric_cfg = {'average': 'weighted'}
                if metric_name == "glue":
                    for glue_task in metric_cfg:
                        metrics_functions[evaluate.load("glue", glue_task)] = {}
                else:
                    metrics_functions[evaluate.load(metric_name)] = metric_cfg
            
        self.metrics_functions = metrics_functions


    def define_compute_metrics(self):
        "It over-writes FineTuner instance with new compuet_metrics function"

        def compute_metrics(eval_pred):
            """ Output example:
            {
                'accuracy'  : 0.9518,
                'f1'        : 0.8756,
            }                      
            """
            logits, labels = eval_pred
            preds = logits.argmax(axis=-1)

            metrics = {}
            for metric_func, metric_args in self.metrics_functions.items():
                metrics.update(metric_func.compute(predictions=preds, references=labels, **metric_args))
        
            return metrics
        
        self.compute_metrics_func = compute_metrics # function

from modelcraft.Trainer import Trainer
import logging
from transformers import AutoConfig, AutoTokenizer

# STUDENT = BASE_MODEL_NAME

class Distiller(Trainer):

    def __init__(self, config):
        super().__init__(config)

    def init_tokenizer(self):
        tokenizer = AutoTokenizer.from_pretrained(self.config['BASE_MODEL_NAME'])
        logging.info(f"INIT Token for {self.config['BASE_MODEL_NAME']}: initialized ✅")
        self.student_tokenizer = tokenizer

    def init_model(self):

        # INIT Teacher
        hf_model = self.config['DISTILL_TEACHER']
        teacher = self.AutoModelClass.from_pretrained(hf_model, num_labels=self.num_classes)
        logging.info(f"Model {teacher.__class__.__name__} initialized with {self.num_classes} classes.")
        teacher.to(self.device)

        self.teacher = teacher # model

        # DEFINE student init
        def student_init():
            student_config = AutoConfig.from_pretrained(self.config['BASE_MODEL_NAME'],
                                                    num_labels=self.num_classes,
                                                    id2label=self.teacher.config.id2label,
                                                    label2id=self.teacher.config.label2id)
            return self.AutoModelClass.from_pretrained(self.config['BASE_MODEL_NAME'], config=student_config).to(self.device)
        
        self.student_init = student_init # function

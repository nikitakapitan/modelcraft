# Model Craft: Fine-Tuning and Distillation of LLM Models

Model Craft is a toolkit for fine-tuning and distilling Large Language Models (LLMs) with ease. This project allows AI researchers and enthusiasts to craft their own LLMs and push them to Hugging Face's model hub.

## Quick Start

You only need to launch it, select the model, select the dataset and hit the button ✅

### Prerequisites

- Google Colab account
- Hugging Face account

### Usage

Open new google colab notebook.

Make sure your runtime is on GPU (ex. T4 GPU) 

## 1. **Install Dependencies**
   
   ```bash
   %%capture
   !pip install datasets transformers evaluate accelerate 
   ```

## 2. **Clone the Repository and make it global**
   
   ```bash
   %%capture
   !git clone https://github.com/nikitakapitan/modelcraft.git
   %cd modelcraft
   !pip install .
```


## 3. Finetune or Distill your model


### Fine-Tuning Your Model

Import the finetune widget and customize it.

   ```bash
   from modelcraft.vizual.finetune_widget import display_finetune
   display_finetune()
```

<p align="center">
  <img src="docs/images/setup.png" alt="Setup widget" />
</p>

Run the job:

  ```bash
  !python modelcraft/finetune.py --config finetune.yaml
  ```

Done ✅ Your new Finetuned model is automatically pushed to your Hugging Face account 🤗

### Distill Your Model

Import the distill widget and customize it.

   ```bash
   from modelcraft.vizual.finetune_widget import display_distill
   display_distill()
```

<p align="center">
  <img src="docs/images/distill_setup.png" alt="Setup widget" />
</p>

Do the job:

  ```bash
  !python modelcraft/distill.py --config distill.yaml
  ```

Done ✅ Your new Distilled model is automatically pushed to your Hugging Face account 🤗

## Contributing
We welcome contributions! If you'd like to improve or add features to Model Craft, please feel free to submit a pull request.

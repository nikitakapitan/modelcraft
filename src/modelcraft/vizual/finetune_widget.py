import yaml
import ipywidgets as widgets
from IPython.display import display, clear_output


yaml_file = 'finetune.yaml'  

with open(yaml_file) as file:
    data = yaml.safe_load(file)

# Define the options for the widgets
task_options = ['text-classification', 'ner', 'question-answering']
dataset_name_options = {
    'text-classification': ['imdb', 'glue', 'clinc_oos', 'emotion'],
    'ner': ['conll2003', 'ontonotes'],
    'question-answering': ['squad', 'race'],
}
glue_metrics = ['cola', 'sst2', 'mrpc', 'mnli', 'qnli', 'qqp', 'rte', 'stsb', 'wnli', 'ax']
dataset_config_name_options = {
    'imdb': [None],
    'glue': glue_metrics,
    'clinc_oos': ['plus', None],
    'conll2003': ['eng', 'esp', 'ned'],
    'ontonotes': ['english', 'chinese', 'arabic'],
    'squad': ['v1', 'v2'],
    'race': ['highschool', 'college'],
}

model_options = ['bert-base-uncased', 'distilbert-base-uncased']

### <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< CORE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
hf_token_widget = widgets.Text(value='hf_YOUR_TOKEN_HERE', description='HF TOKEN:')
base_model_name_widget = widgets.Dropdown(options=model_options, value=data['BASE_MODEL_NAME'], description='MODEL:')
task_widget = widgets.Dropdown(options=task_options, value=data['TASK'], description='TASK:')
dataset_name_widget = widgets.Dropdown(options=dataset_name_options[data['TASK']], value=data['DATASET_NAME'], description='DATASET:')
dataset_config_name_widget = widgets.Dropdown(options=dataset_config_name_options[data['DATASET_NAME']], value=data['DATASET_CONFIG_NAME'], description='DATA CFG:')

def update_dataset_name_options(change):
    dataset_name_widget.options = dataset_name_options[task_widget.value]

def update_dataset_config_name_options(change):
    dataset_config_name_widget.options = dataset_config_name_options[dataset_name_widget.value]
    update_metrics()

task_widget.observe(update_dataset_name_options, 'value')
dataset_name_widget.observe(update_dataset_config_name_options, 'value')

### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CORE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    
### <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< CUSTOM <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
custom_model_checkbox = widgets.Checkbox(value=False, description='CUSTOM')  
custom_container = widgets.VBox([]) 
custom_model_name_widget = widgets.Text(value='', description='CS.MODEL:', placeholder='Enter custom model name')
custom_dataset_name_widget = widgets.Text(value='', description='CS.DATASET:', placeholder='Enter custom dataset name')
custom_dataset_config_name_widget = widgets.Text(value='', description='CS.DATA.CFG:', placeholder='Enter custom dataset config name')

# Update function for CUSTOM checkbox change
def toggle_custom_model_name_widget(change):
    if change.new:  # If checkbox is checked
        custom_container.children = [custom_model_name_widget, custom_dataset_name_widget, custom_dataset_config_name_widget]
    else:
        custom_container.children = []

custom_model_checkbox.observe(toggle_custom_model_name_widget, 'value')
### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> CUSTOM >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>

### <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< METRICS <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
isCompute_metrics_checkbox = widgets.Checkbox(value=False, description='METRICS?')
metrics_container = widgets.VBox([])
isAccuracyW = widgets.Checkbox(value=False, description='Accuracy')
isF1W = widgets.Checkbox(value=False, description='F1')
# Glue
isGlueW = widgets.Checkbox(value=False, description='GLUE')
glue_metrics_widget = widgets.Dropdown(options=glue_metrics, description='GLUE metric:', layout={'display': 'none'})

metrics_container.children = [isAccuracyW, isF1W, isGlueW]

def update_glue_metrics_widget(change):
    if isGlueW.value:
        metrics_container.children = [isAccuracyW, isF1W, isGlueW, glue_metrics_widget]
        glue_metrics_widget.layout.display = 'block'
    else:
        metrics_container.children = [isAccuracyW, isF1W, isGlueW]
        glue_metrics_widget.layout.display = 'none'

isGlueW.observe(update_glue_metrics_widget, 'value')

def toggle_metrics(change):
    if isCompute_metrics_checkbox.value:
        display(metrics_container)
    else:
        clear_output()
        display_finetune()

isCompute_metrics_checkbox.observe(toggle_metrics, 'value')

# Update METRICS based on DATASET_NAME
# def update_metrics():
#     if dataset_name_widget.value == 'glue':
#         data['METRICS'] = [
#             {'accuracy': {}},
#             {'f1': {'average': 'weighted'}},
#             {'glue': [dataset_config_name_widget.value]}
#         ]
#     else:
#         data['METRICS'] = [
#             {'accuracy': {}},
#             {'f1': {'average': 'weighted'}}
#         ]
### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> METRICS >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



### <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< ADVANCED <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
num_epochs_options = [1, 2, 3, 5, 10, 100]
weight_decay_options = [0.0, 0.01, 0.02, 0.03, 0.05]
learning_rate_options = [0.00001, 0.00002, 0.0001, 0.0002, 0.001]
push_to_hub_options = [True, False]
evaluation_strategy_options = ['no', 'steps', 'epoch']
batch_size_options = [4, 8, 16, 32, 64]
warmup_options = [100, 300, 500]

# Advanced settings widgets
advanced_checkbox = widgets.Checkbox(value=False, description='Advanced')
batch_size_widget = widgets.Dropdown(options=batch_size_options, value=data.get('BATCH_SIZE', 16), description='BATCH SIZE:')
num_epochs_widget = widgets.Dropdown(options=num_epochs_options, value=data.get('NUM_EPOCHS', 1), description='EPOCHS:')
weight_decay_widget = widgets.Dropdown(options=weight_decay_options, value=data.get('WEIGHT_DECAY', 0.0), description='W8 DECAY:')
learning_rate_widget = widgets.Dropdown(options=learning_rate_options, value=data.get('LEARNING_RATE', 0.0001), description='LRATE:')
warmup_widget = widgets.Dropdown(options=warmup_options, value=data.get('WARMUP_STEPS', 500), description='WARMUP:')
num_epochs_widget = widgets.Dropdown(options=num_epochs_options, value=data.get('NUM_EPOCHS', 1), description='EPOCHS:')
push_to_hub_widget = widgets.Dropdown(options=push_to_hub_options, value=data.get('PUSH_TO_HUB', False), description='PUSH2HUB:')
evaluation_strategy_widget = widgets.Dropdown(options=evaluation_strategy_options, value=data.get('EVALUATION_STRATEGY', 'epoch'), description='EVAL EVERY:')

def toggle_advanced_settings(change):
    if advanced_checkbox.value:
        display(num_epochs_widget, batch_size_widget, weight_decay_widget, learning_rate_widget, warmup_widget, push_to_hub_widget, evaluation_strategy_widget)
    else:
        clear_output()
        display_finetune()

advanced_checkbox.observe(toggle_advanced_settings, 'value')
### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> ADVANCED >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


### <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< SAVE <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

save_button = widgets.Button(description="Save Changes")

def save_changes(b):
    data['HF_TOKEN'] = hf_token_widget.value 
    data['TASK'] = task_widget.value
    if custom_model_checkbox.value:
        data['BASE_MODEL_NAME'] = custom_model_name_widget.value
        data['DATASET_NAME'] = custom_dataset_name_widget.value
        data['DATASET_CONFIG_NAME'] = custom_dataset_config_name_widget.value  
    else:
        data['BASE_MODEL_NAME'] = base_model_name_widget.value
        data['DATASET_NAME'] = dataset_name_widget.value
        data['DATASET_CONFIG_NAME'] = dataset_config_name_widget.value  
    
    data['COMPUTE_METRICS'] = isCompute_metrics_checkbox.value
    if isCompute_metrics_checkbox.value:
        pass
    
    if advanced_checkbox.value:
        data['NUM_EPOCHS'] = num_epochs_widget.value
        data['BATCH_SIZE'] = batch_size_widget.value
        data['WEIGHT_DECAY'] = weight_decay_widget.value
        data['LEARNING_RATE'] = learning_rate_widget.value
        data['WARMUP_STEPS'] = warmup_widget.value
        data['PUSH_TO_HUB'] = push_to_hub_widget.value
        data['EVALUATION_STRATEGY'] = evaluation_strategy_widget.value

    update_metrics()

    with open(yaml_file, 'w') as file:
        yaml.safe_dump(data, file)

    with output:
        clear_output()
        print(f"{yaml_file} updated!")

save_button.on_click(save_changes)

### >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> SAVE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


# Output
output = widgets.Output()

# Display widgets
def display_finetune():
    display(hf_token_widget, base_model_name_widget, custom_model_checkbox, custom_container, task_widget, dataset_name_widget, 
             dataset_config_name_widget, isCompute_metrics_checkbox, advanced_checkbox, save_button, output)
    

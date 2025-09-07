import os
from datasets import load_dataset
from transformers import DistilBertForSequenceClassification, DistilBertTokenizerFast, Trainer, TrainingArguments
import torch

# --- Script Objective ---
# This script fine-tunes a pre-trained DistilBERT model on the GoEmotions dataset.
# The goal is to adapt the model for the specific task of sentiment classification,
# enabling our backend to recognize and respond to a student's emotional state.

# --- 1. Setup and Initialization ---
# Define the base model name and load its tokenizer and model architecture.
# We are using a pre-trained 'distilbert-base-uncased' model.
model_name = "distilbert-base-uncased"
tokenizer = DistilBertTokenizerFast.from_pretrained(model_name)

# The number of labels (emotions) in the GoEmotions dataset is 28.
# We initialize the model with this number of labels, adding a classification head
# on top of the pre-trained DistilBERT model.
num_labels = 28
model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=num_labels)

# --- 2. Load and Preprocess Data ---
# Load the GoEmotions dataset from the Hugging Face Hub.
print("Loading and preprocessing the GoEmotions dataset...")
dataset = load_dataset("go_emotions")

# Define a function to tokenize the text in the dataset.
# Tokenization converts text into numerical IDs that the model can understand.
# `padding="max_length"` ensures all sequences have the same length.
# `truncation=True` cuts off long sequences.
def tokenize_function(examples):
    return tokenizer(examples["text"], padding="max_length", truncation=True)

# Apply the tokenization function to the entire dataset using `map`.
tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Remove the original `text` and `id` columns from the dataset.
# They are no longer needed after tokenization, and removing them
# simplifies the dataset for the `Trainer`.
tokenized_datasets = tokenized_datasets.remove_columns(["text", "id"])

# The GoEmotions dataset has multiple labels per entry. For this simple model,
# we will use only the first label. This is a simplification to get a single
# classification output per entry.
def get_first_label(examples):
    # Ensure there is at least one label
    if examples["labels"]:
        examples["labels"] = examples["labels"][0]
    else:
        examples["labels"] = -1
    return examples

# Apply the function to get the first label for each entry.
tokenized_datasets = tokenized_datasets.map(get_first_label)

# Filter out entries that had no labels (where we assigned -1).
tokenized_datasets = tokenized_datasets.filter(lambda example: example["labels"] != -1)
print("Data preprocessing complete.")

# --- 3. Training the Model ---
# Define the training arguments, which specify the training process.
# `output_dir`: where the trained model and checkpoints will be saved.
# `num_train_epochs`: how many times the model will go through the entire training dataset.
# `per_device_train_batch_size`: number of samples per batch for training.
# `evaluation_strategy="epoch"`: tells the trainer to evaluate the model at the end of each epoch.
# `save_strategy="epoch"`: saves the model at the end of each epoch.
# `load_best_model_at_end=True`: loads the best performing model at the end of training.
try:
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        logging_dir='./logs',
        logging_steps=100,
        save_strategy="epoch",
        evaluation_strategy="epoch",
        load_best_model_at_end=True,
    )
except TypeError:
    # This try-except block handles potential API changes in the `transformers` library,
    # making the script more robust to different versions.
    print("Detected an older version of the `transformers` library. Using `eval_strategy` instead.")
    training_args = TrainingArguments(
        output_dir="./results",
        num_train_epochs=3,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=16,
        logging_dir='./logs',
        logging_steps=100,
        save_strategy="epoch",
        eval_strategy="epoch",
        load_best_model_at_end=True,
    )

# Initialize the `Trainer` class, which orchestrates the training loop.
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["validation"],
)

# Start the training process.
print("Starting model training...")
trainer.train()
print("Training complete.")

# --- 4. Save the Fine-Tuned Model ---
# Define the output directory to save the final fine-tuned model and tokenizer.
output_dir = os.path.join(os.path.dirname(__file__), '..', 'models', 'sentiment-model')

# Save the fine-tuned model and its tokenizer to the specified directory.
trainer.save_model(output_dir)
tokenizer.save_pretrained(output_dir)
print(f"Model and tokenizer saved to {output_dir}")

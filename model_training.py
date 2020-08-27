# Using PyTorch 1.4
# Trained on Google colab using gpu
import numpy as np
import pandas as pd
import random
import torch
import logging
import os
import csv

from torch.utils.data import Dataset, DataLoader
from transformers import GPT2Tokenizer, GPT2LMHeadModel, AdamW, get_linear_schedule_with_warmup
from tqdm import tqdm, trange
import torch.nn.functional as F

class CSVPoem(Dataset):
    
    def __init__(self, control_code, truncate=False, gpt2_type="gpt2", max_length=768):

        self.tokenizer = GPT2Tokenizer.from_pretrained(gpt2_type)
        self.poems = []

        # This uses the same CSV of Sentiment140 that we created in Chapter 5
        
        with open('data/poem_df.csv', newline='') as csvfile:
            poem_csv = csv.reader(csvfile)
            i = 0
            for row in poem_csv:
                if (i > 0):
                    self.poems.append(torch.tensor(
                    self.tokenizer.encode(f"<|{control_code}|>{row[6][:max_length]}<|endoftext|>")
                    ))
                i += 1
                
        if truncate:
            self.poems = self.poems[:20000]
        self.poem_count = len(self.poems)
        
    def __len__(self):
        return self.poem_count

    def __getitem__(self, item):
        return self.poems[item]


def pack_tensor(new_tensor, packed_tensor, max_seq_len):
    if packed_tensor is None:
        return new_tensor, True, None
    if new_tensor.size()[1] + packed_tensor.size()[1] > max_seq_len:
        return packed_tensor, False, new_tensor
    else:
        packed_tensor = torch.cat([new_tensor, packed_tensor[:, 1:]], dim=1)
        return packed_tensor, True, None

def train(
    dataset,
    model,
    tokenizer,
    batch_size=16,
    epochs=4,
    lr=2e-5,
    max_seq_len=400,
    warmup_steps=5000,
    gpt2_type="gpt2",
    device="cuda",
    output_dir=".",
    output_prefix="wreckgar",
    test_mode=False,
    save_model_on_epoch=False,
):

    acc_steps = 100

    model = model.to(device)
    model.train()

    optimizer = AdamW(model.parameters(), lr=lr)
    scheduler = get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=warmup_steps, num_training_steps=-1
    )

    train_dataloader = DataLoader(dataset, batch_size=1, shuffle=True)

    accumulating_batch_count = 0
    input_tensor = None

    for epoch in range(epochs):

        print(f"Training epoch {epoch}")
        for idx, entry in tqdm(enumerate(train_dataloader)):
            (input_tensor, carry_on, remainder) = pack_tensor(entry, input_tensor, 768)

            if carry_on and idx != len(train_dataloader) - 1:
                continue

            input_tensor = input_tensor.to(device)
            outputs = model(input_tensor, labels=input_tensor)
            loss = outputs[0]
            loss.backward()

            if (accumulating_batch_count % batch_size) == 0:
                optimizer.step()
                scheduler.step()
                optimizer.zero_grad()
                model.zero_grad()

            accumulating_batch_count += 1
            input_tensor = None
        if save_model_on_epoch:
            torch.save(
                model.state_dict(),
                os.path.join(output_dir, f"{output_prefix}-{epoch}.pt"),
            )
    return model

if __name__ == '__main__':

	# Initialization
	gpt2_type = "gpt2"

	dataset = CSVPoem("<|poem|>", truncate=True, gpt2_type=gpt2_type)

	model = train(
    dataset,
    GPT2LMHeadModel.from_pretrained(gpt2_type),
    GPT2Tokenizer.from_pretrained(gpt2_type),
    batch_size=4,
    epochs=3,
    lr=1e-4,
    max_seq_len=140,
    warmup_steps=5000,
    gpt2_type=gpt2_type,
    device="cuda",
    output_dir="trained_models",
    output_prefix="poem_new",
    save_model_on_epoch=True
)
import os
import sys
_parent_path =os.path.join(os.path.dirname(__file__), '..','..','..')
sys.path.append(_parent_path)

import pandas as pd
import torch
import wandb
import yaml
import numpy as np

import alg.models_fcpflow_lin as fcpf
import alg.tools_train as tl

# define the device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# import the configuration
with open(os.path.join(_parent_path,'exp/uncond_rlp_generation/exp_ge/config_ge.yaml')) as file:
    config = yaml.load(file, Loader=yaml.FullLoader)
        
# define the data loader
data_path = os.path.join(_parent_path, 'data', 'ge_data_ind.csv')
np_array = pd.read_csv(data_path).values

# stack one extra column of zeros to the data as the condition
np_array = np.hstack((np_array, np.ones((np_array.shape[0], 1))))
dataloader, scaler = tl.create_data_loader(np_array, config['FCPflow']['batch_size'], True)

# train the model
model = fcpf.FCPflow(config['FCPflow']['num_blocks'], config['FCPflow']['num_channels'], 
                        config['FCPflow']['sfactor'], config['FCPflow']['hidden_dim'], config['FCPflow']['condition_dim']).to(device)

print('number of parameters: ', sum(p.numel() for p in model.parameters() if p.requires_grad))

# define the optimizer
optimizer = torch.optim.Adam(model.parameters(), lr=config['FCPflow']['lr'], weight_decay=config['FCPflow']['w_decay'])

# define the wandb
# wandb.init(project="fctflow_ge_win_24122023")
# wandb.watch(model)
# wandb.config.update({"num_blocks": num_blocks, "sfactor": sfactor, "hidden_dim": hidden_dim, "lr": lr, "w_decay": w_decay})

# train the model
path = os.path.join(_parent_path, 'exp', 'uncond_rlp_generation', 'exp_ge')
tl.train(path, model, dataloader, optimizer, 400001, config['FCPflow']['condition_dim'], device, scaler, dataloader, 100)


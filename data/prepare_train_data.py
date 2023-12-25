import pandas as pd
import os
import numpy as np
import json
import random

def prepare_train_data(raw_data_file, labels_file, output_dir):
    ## Read data
    raw_df = pd.read_csv(raw_data_file)
    labels_dict = json.load(open(labels_file, "r"))

    ## Create train and dev pairs
    train_pair_titles = []
    train_pair_labels = []
    dev_pair_titles = []
    dev_pair_labels = []
    train_size = 0.8

    for topic in labels_dict.keys():
        other_topics = [i for i in labels_dict.keys() if i != topic]
        for idx in labels_dict[topic]:
            ## Prepare positive examples
            curr_title = raw_df.iloc[idx]["paper_title"] # grab the current title and its topic
            pos_idx = np.random.choice(labels_dict[topic]) # randomly pick an title that belongs to the *same* class
            pos_title = raw_df.iloc[pos_idx]["paper_title"] # grab the title in the same topic
            ## Prepare negative examples
            rand_topic = np.random.choice(other_topics) # randomly pick 
            neg_idx = np.random.choice(labels_dict[rand_topic]) # randomly pick an title that belongs to the *different* class
            neg_title = raw_df.iloc[neg_idx]["paper_title"] # grab the title in a different topic
            
            ## Randomly assign examples to train or dev
            if random.uniform(0, 1) < train_size:
                train_pair_titles.append([curr_title, pos_title]) ## pos examples
                train_pair_labels.append('1') ## Label as 1
                train_pair_titles.append([curr_title, neg_title])
                train_pair_labels.append('0') ## Label as 0
            else:
                dev_pair_titles.append([curr_title, pos_title]) ## neg examples
                dev_pair_labels.append('1') ## Label as 1
                dev_pair_titles.append([curr_title, neg_title])
                dev_pair_labels.append('0') ## Label as 0           

    ## Create dataframe for saving
    train_data = pd.DataFrame({
        "title_1": [l[0] for l in train_pair_titles],
        "title_2": [l[1] for l in train_pair_titles],
        "label": train_pair_labels
    })

    dev_data = pd.DataFrame({
        "title_1": [l[0] for l in dev_pair_titles],
        "title_2": [l[1] for l in dev_pair_titles],
        "label": dev_pair_labels
    })

    ## Save data
    train_data.to_csv(os.path.join(output_dir,"train_data.csv"), sep='|', index=False, encoding='utf-8')
    dev_data.to_csv(os.path.join(output_dir,"dev_data.csv"), sep='|', index=False, encoding='utf-8')

    return train_data, dev_data

if __name__ == '__main__':
    train_data, dev_data = prepare_train_data("data/raw_data.csv", "data/labels_dict.json", "data/")
    print("train_data len: ", len(train_data))
    print("dev_data len: ", len(dev_data))

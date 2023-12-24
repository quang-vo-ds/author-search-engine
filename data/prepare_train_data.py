import pandas as pd
import os
import numpy as np
import json

def prepare_train_data(raw_data_file, labels_file, output_dir):
    ## Read data
    raw_df = pd.read_csv(raw_data_file)
    labels_dict = json.load(open(labels_file, "r"))

    ## Create training pairs
    pair_titles = []
    pair_labels = []
    for topic in labels_dict.keys():
        other_topics = [i for i in labels_dict.keys() if i != topic]
        for idx in labels_dict[topic]:
             ## Prepare positive examples
             curr_title = raw_df.iloc[idx]["paper_title"] # grab the current title and its topic
             pos_idx = np.random.choice(labels_dict[topic]) # randomly pick an image that belongs to the *same* class
             pos_title = raw_df.iloc[pos_idx]["paper_title"] # grab the title in the same topic
             pair_titles.append([curr_title, pos_title])
             pair_labels.append(1) ## Label as 1
             
             ## Prepare negative examples
             rand_topic = np.random.choice(other_topics)
             neg_idx = np.random.choice(labels_dict[rand_topic])
             neg_title = raw_df.iloc[neg_idx]["paper_title"] # grab the title in a different topic
             pair_titles.append([curr_title, neg_title])
             pair_labels.append(0) ## Label as 0
        break

    train_data = pd.DataFrame({
        "title_1": [l[0] for l in pair_titles],
        "title_2": [l[1] for l in pair_titles],
        "label": pair_labels
    })
    ## Save data
    train_data.to_csv(os.path.join(output_dir,"train_data.csv"), index=False)

    return train_data



if __name__ == '__main__':
    train_data = prepare_train_data("data/raw_data.csv", "data/labels_dict.json", "data/")
    print(train_data.head())

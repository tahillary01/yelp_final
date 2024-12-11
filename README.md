# yelp_final
### 
When deploying on Streamlit, we chose the GitHub option and set the **yelp_app.py** file as the main file path.

The dataset used is the Yelp Open dataset that's available here: https://www.yelp.com/dataset

The datasets we decided were relevant to keep were the review (5.34 GB), business (118.9 MB), and user (3.36 GB) json files. Since the review dataset was too big to load into VSCode, we had to split it into 3 separate json files to be able to load it. This was done in the **INSERT.py** file.

We first used the code in the **downsample.py** file to sample 1/5 of the reviews made by users with 5 or more reviews. This created a smaller dataset to work with.

To further shrink the size of the dataset, we decided to only keep reviews about restaurants/food establishments in the **filter.py file**.

The 
###



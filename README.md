# Twitter Hate Speech Detection

## Backend
 
- Install requirements:
```sh
pip install -r requirements.txt
```
- Collect tweet data and preprocess it:
```sh
python preprocess.py
```

Data is stored in the folder `frontend/src/datasets/`. Tweet counts associated with each class are in the file `counts_data.csv` and hashtags with frequency are stored in `hashtags_data.csv`. 

## Frontend

```sh
cd frontend
npm i
npm start
```

## Hate Speech Classification

Binary classification of hateful and non-hateful is implemented in the `detection` folder. It requires you to upload the `tweets_data.csv` file generated by running `process.py` as the dataset. Pretrained spaCy embeddings are used to create tweet vectors on which an LSTM model is trained, followed with binary prediction. 

#### Test set accuracy: 57.06%
#### Train set accuracy: 62.51%

### Notes

All files have relevant comments to indicate the function purposes.
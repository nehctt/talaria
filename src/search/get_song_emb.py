import os
import librosa
import torch
from transformers import AutoFeatureExtractor
from transformers import AutoModel
from transformers import pipeline
import pandas as pd
from tqdm import tqdm


def get_song_embeddings(input_dir, output_dir, chunksize=24):
    # all mp3 files
    files = [filename for filename in os.listdir(input_dir) if filename.endswith(".mp3")]
    audio = []
    # check if gmac pu available
    if torch.backends.mps.is_available():
        device = torch.device("mps")
    else:
        device = torch.device("cpu")
    # load model
    model_name = "mtg-upf/discogs-maest-30s-pw-129e"
    feature_extractor = AutoFeatureExtractor.from_pretrained(model_name, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
    model.to(device)
    embeddings = []

    for filename in tqdm(files):
        file_path = os.path.join(input_dir, filename)
        # waveform
        y, sr = librosa.load(file_path, sr=None)
        audio.append(y)

        if len(audio) >= chunksize:
            with torch.no_grad():
                # spectrum
                feature = feature_extractor(audio)
                # embedding with (bs, 1685, 768)
                output = model(torch.tensor(feature['input_values']).to(device))
                # mean embedding with (bs, 768)
                emb = output['last_hidden_state'].mean(dim=1).to("cpu").tolist()
                embeddings = embeddings + emb
                audio = []
    
    if len(audio) > 0:
        with torch.no_grad():
            feature = feature_extractor(audio)
            output = model(torch.tensor(feature['input_values']).to(device))
            emb = output['last_hidden_state'].mean(dim=1).to("cpu").tolist()
            embeddings = embeddings + emb
            audio = []
        
    df = pd.DataFrame({
            'song_id': [filename[:-4] for filename in files],
            'embeddings': embeddings
    })
    df.to_csv(f'{output_dir}/maest30s_embeddings.csv', index=False)
    

if __name__ == "__main__": 
    input_dir = "../../data/processed_mp3/"
    output_dir = "../../data/embeddings/"
    get_song_embeddings(input_dir, output_dir)

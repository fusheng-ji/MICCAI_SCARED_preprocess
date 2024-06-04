# MICCAI_SCARED_preprocess
This repo is a modified preprocessor for MICCAI SCARED 2019 data challenge, based on EikoLoki's [repo](https://github.com/EikoLoki/MICCAI_challenge_preprocess). 
- What's new:
  - Add some new features
    - automaticlly unzip the original dataset
    - ignore the folders without data/
  - fix some known bugs
    - fix FileNotFoundError when call 'video_parser.py'
- How to obtain the datasets?
  - The dataset provided in [SCARED](https://endovissub2019-scared.grand-challenge.org/) is used.
  - To obtain a link to the data and code release, sign [the challenge rules](https://www.dropbox.com/s/8n0hw0rblxu2of3/EndoVis_Rules.pdf) and email them to max.allan@intusurg.com.
  - Then you will receive a temporary link to download the data and code.
- How to use this preprocessor?
  - download the original datasets
  - modify the 'rootpath' in all_in_one.py to your datasets rootpath
  - Then just run `python all_in_one.py` and the processed datasets will ready to go

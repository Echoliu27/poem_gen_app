# poem_gen_app

### Inspiration
In a world overloaded with information and misinformation, could we just have a pure moment of joy reading kid's poetry?
Wouldn't it also be joyful to look at the sketches that reflect content of the poem?
Let's make ai learn about kid's poems and look at the fun and hilarious responses language model generates.

### What it does
Kids Poetry Slam generates kid-style poems based on user input or user-chosen key words.
Key words are selected based on the frequency of poem titles.

### To run this repo
Please download the model checkpoint at https://drive.google.com/file/d/1-I2cesjwu9YgOO4goLCFxsgj38qibMIl/view?usp=sharing
```
git clone repo
cd poem_gen_app
mkdir checkpoint
cd checkpoint
# download poem_new-2.pt from the google drive link above

pip install -r requirements.txt
```

To run app
```
python app.py
```

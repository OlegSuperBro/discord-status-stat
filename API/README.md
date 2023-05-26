# How to make API

To make API works, you need class with those funcs/arguments:

- ```data```: can be either func, or func (if func use decorator ```@property```). It should provide data in dict
- ```load```: func that called right after creating instance of API. Use it to load your data. As argument it gets saved data from ```config.yaml```. Put all your data configuration here (auth code, username, etc)
- ```start```: func that called when API should setup. Put all your generated data here (exireble tokens, generating headers, token updating, etc)
- ```save```: func that called when everything configured, let you save data. Should return anything to save (make sure you will be able to parse it later in ```load``` func)

If you wanna learn how to make API file, you can check [this one](osu.py). I tried to document it well, to make you understand how it works, but you should read how API for your game works (they all not same).

But you don't have any restrictions.

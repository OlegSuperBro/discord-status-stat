# discord-status-stat

This thing let you brag about your stats in games

## How to use

First install python. Then run  ```pip install -r requirements.txt```

Run **main.py**, it will create **config.yaml**. Each time data parsed, **current_data.json** created with all data. You will need it to [add new lines](#add-new-lines)

### Options in config.yaml

- ```delay```: How fast status will change in seconds (don't set too fast, or else you will possibly get API ban. 10 sec is min i think)
- ```discord_token```: Your discord token. [Random vid how to get it](https://www.youtube.com/watch?v=YEgFvgg7ZPI)
- ```game```: name of your game you want to get data from. Set to empty to display just text. Otherwise game should be in **API** folder. (If you want create your own API, read [this](API/README.md))
- ```lines```: Lines to display. Read [this](#add-new-lines) section to get more info
- ```API_data```: Data for API. It changes for each API.

### Add new lines

It's pretty simple. Check **current_data.json** (you should run program at least ***once***. Make sure status changed to something)

Now find the required data in **current_data.json**. You should see something like this but bigger:

```json
{
    "username": "NAME",
    "id": 12345,
    "statistics":
    {
        "wins": 1234,
        "loses": 123,
    }
}
```

Now, to get those data put this after ```lines:``` those lines:

```yaml
- "Me: {username}"
- "My wins: {statistics.wins}"
```

In discord it will be displayed like this

```text
Me: NAME
(Some delay)
My wins: 1234
```

### Add it to autorun

Just make a shortcut for **autorun_discord_status_stat.bat** and put it in Autorun folder (you can access it by pressing win+r and type ```shell:startup```)

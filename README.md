# Project youtubeWatchlist

## What is it all about?

I like to have all the latest videos from the youtube channels I like all in one place.
So this project is about doing just that: ask youtube for a list of all the latest videos and building a web page with all these videos.

## How do I do it?

I simply call youtube API to get the latest videos from each channel.
Then I embed them in a very simple HTML page.

## Good to know

The channels.csv file looks something like this:

|channel|name|
|:------|:---|
|UCyJDHgrsUKuWLe05GvC2lng|stupid economics|
|UCP46_MXP_WG_auH88FnfS1A|nota bene|
|UCtqICqGbPSbTN09K1_7VZ3Q|dirtybiology|
|UCKjDY4joMPcoRMmd-G1yz1Q|c'est une autre histoire|

As long as you have a column named "channel" with the channel id, you're good to go.

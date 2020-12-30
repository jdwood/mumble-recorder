# PYMUMBLE python library

## Description
This library is a fork of a fork of a fork (initial from https://github.com/Robert904/pymumble).
But we will try to make `pymumble` better.
So I consider this fork (the [@Azlux](https://github.com/azlux/pymumble) one) the current live fork of `pymumble`.

The wiki/API explanation is [HERE](API.md).

The **Python 2** version is available in the [master branch](https://github.com/azlux/pymumble/tree/master). It's working! But since we have moved on to Python 3, the Python 2 version will not receive future improvements.

## CHANGELOG
The changelog is available on the release note.

## List of applications using `pymumble`
For client application examples, you can check this list :
- [MumbleRadioPlayer](https://github.com/azlux/MumbleRadioPlayer)
- [Botamusique](https://github.com/azlux/botamusique)
- [Abot](https://github.com/ranomier/pymumble-abot)
- [MumbleRecbot](https://github.com/Robert904/mumblerecbot) (deprecated)

## Status
### Currently implemented:
- Compatible with Mumble 1.3 and normally until 1.2.2
- Support OPUS. Speex is not supported
- Receive and send audio, get users and channels status
- Set properties for users (mute, comments, etc.) and go to a specific channel
- Callback mechanism to react on server events
- Manage the blobs (images, long comments, etc.)
- Can send text messages to user and channel
- Ping statistics
- Audio targets (whisper, etc.)

### What is missing:
>  I don't need these features, so if you want one, open an issue and I will work on it.

- UDP media. Currently it works only in TCP tunneling mode (the standard fallback of Mumble when UDP is not working)
- Server management (user creation and registration, ACLs, groups, bans, etc.)
- Positioning is not managed, but it should be easy to add
- Probably a lot of other small features

## Architecture
The library is based on the Mumble object, which a thread. When started, it will try
to connect to the server and start exchanging the connection messages.
This thread implements a loop which takes care of the pings, sends commands to the server,
checks for incoming messages including audio, and checks for audio to be sent out.
The rate of this loop is controlled by how long it will wait for an incoming message before continuing.

You can check if the thread is alive with `mumble_object.isAlive()`.
The Mumble thread will stop if it disconnects from the server.
This can be useful if you need to restart the thread when using a supervisor.

## Requirements & installation
Check the `requirement.txt` to know which versions of `opuslib` and `protobuf` are needed.
You need `pip3`, because this is a Python 3 library (`apt-get install python3-pip`), 
to install the dependencies (`pip3 install -r requirements.txt`).

## Thanks
- [@raylu](https://github.com/raylu) for making `pymumble` speak into channels
- [@schlarpc](https://github.com/schlarpc) for fixes on buffer

## License
Copyright Robert Hendrickx <rober@percu.be> - 2014

`pymumble` is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.

# ad1459
IRC Client

AD1459 is an IRC client written in Python and GTK3. It aims to be a modern IRC 
client with features that make sense for IRC today. It has an interface which 
has been loosely inspired by Hexchat and mIRC.

![AD1459 IRC Client](https://i.imgur.com/JuIuJY6.png)

AD1459 is currently in _ALPHA_, and should not be considered ready for everyday 
use. That being said, it is a relatively capable client for basic functionality 
even in its currently incomplete state.

## Current Abilities

* Multiple-network support
* Chatting over IRC.
* Joining/Parting channels
* Changing nick
* Tab-completion
* Save and recall servers
* Secure password storage within system keyring
* Notifications
* User list
* Topic


## TODOS

Currently planned features include:

* Commands 
  - Currently only the /me command is supported
* CTCP
* UI Improvements
* Last message recall
* Logging
* Compacted server messages


## Known Issues

These are problems that have been currently identified:

* Rooms on every network must have unique names
* No server messages for Op-actions (kick, ban, modes)
* Can't set an initial nick which is different from username
* Large buffers make the application unresponsive

### Connecting to IRC

To connect to a server/network, click on the server button (in the top left) and
enter the server details in the text entries. You can alternatively enter a 
server as a single line of text, for which the format is:

`none|sasl|pass name host port username (tls) (password)`

#### `none|sasl|pass`

This specifies the connection type. If you need to authenticate to the server 
with a server password, then use `pass`. If the network supports using SASL, use
`SASL`.

#### `name`

This is the name for the network in the list. (e.g. `freenode`, `Esper`)

#### `host`

The hostname of the server to connect to, e.g. `chat.freenode.net`

#### `port`

The port to connect with, e.g. `7070`. Default is 6697.

#### `username` 

The username/ident for your connection to the server. This will also be your 
initial nickname (Separate nickname support is planned for a future release)

#### `tls`

If present, AD1459 will use TLS to connect to the server. Otherwise, a plaintext
connection will be used.

#### `password`

The password to use to authenticate with the server. This option is required if
the authentication method specified was `sasl` or `pass`. It should be omitted
otherwise.

### Example connection lines

`sasl Esper irc.esper.net 6697 jeans tls hunter2`

`none freenode chat.freenode.net 6666 g4vr0che`

`pass My-Private-Network my.private-network.com 12345 secret_username tls hunter3`

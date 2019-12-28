# ad1459
IRC Client

### Connecting to IRC

To connect to a server/network, click on the server button (in the top left) and
enter the server details in the text entry. The format for the server is:

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


## TODOS

Currently planned features include:

* User list
* Topic
* Commands 
  - Currently only the /me command is supported
* CTCP
* More intuitive connection entry
* UI Improvements
* Saving configuration/recent servers
* Last message recall

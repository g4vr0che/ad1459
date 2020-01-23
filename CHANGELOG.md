# Changelog

All notable changes to this project will be documented in this file. See [standard-version](https://github.com/conventional-changelog/standard-version) for commit guidelines.

## [1.15.0](https://github-g///compare/v1.14.0...v1.15.0) (2020-01-23)


### Features

* Add commands for IRC controls ([40da83c](https://github-g///commit/40da83c565ac71d5562c1c643ac4385405c5165f))
* Add recent message recall and per-channel buffers ([e708c4f](https://github-g///commit/e708c4f2d2c0be012627bfdae33a40107ecd5486)), closes [#10](https://github-g///issues/10)
* Allow expanding and collapsing server messages ([5c8aeaf](https://github-g///commit/5c8aeaf0cd590807b451fabfb61583ccfda9347c))
* Allow opening PM with users on double-click ([59fac20](https://github-g///commit/59fac205f7c926c9631f28949d49e33f8a30a962))
* Display user status in menu. ([bc7ecb9](https://github-g///commit/bc7ecb9a5e982dfea68ec2a36bf93dae6adaa94b)), closes [#12](https://github-g///issues/12)


### Bug Fixes

* Formatting and margin improvements ([5a32a13](https://github-g///commit/5a32a1302f4ee62760b43f563b9c3b68b5e3a54a))
* Hook up join entry icon ([38efa1d](https://github-g///commit/38efa1d7d62791399ed4ee944ceffa1434845181))
* Improve HL logic ([1286993](https://github-g///commit/1286993bebd49d288a3845e13b680842de7bd8cb))
* Improve unread indicator with enums ([877e37b](https://github-g///commit/877e37b41fe43a62e535bed0a69e0a76134bbd85))
* Improved wording of mode changes ([b8ce443](https://github-g///commit/b8ce4439f1139b5baaca0445051d849c1798c788))
* separate msg from other privmsg commands ([9899bbb](https://github-g///commit/9899bbb480f3c4491f20485b2eca53258d619626))
* Spacing improvements ([d0f4010](https://github-g///commit/d0f401037ef42067b40c46934565ab509d0a0fa1))
* Topic expander is now animated. ([67c9f44](https://github-g///commit/67c9f449eb61fccb417d6b6e0500adbf8df6b23d))
* update user list when modes change. ([2f8f24a](https://github-g///commit/2f8f24a1c7ad98084774cc936704a2d404d1708e))

## [1.14.0](https://github-g///compare/v1.13.4...v1.14.0) (2020-01-15)


### Features

* Subsequent server messages are combined into a single message ([2f2a65e](https://github-g///commit/2f2a65ea69b2ba90c9515d10a5b0c0d8ad82428b))


### Bug Fixes

* Tab completion fixes ([3d337a6](https://github-g///commit/3d337a6d4e249669f0fc329ffb497c365a70afa0))

### [1.13.4](https://github-g///compare/v1.13.3...v1.13.4) (2020-01-14)


### Bug Fixes

* label the close button correctly, depending on which type of room ([af0c6be](https://github-g///commit/af0c6be6854affb0131abf5d92901ef8b409ba14))

### [1.13.3](https://github-g///compare/v1.13.2...v1.13.3) (2020-01-14)


### Bug Fixes

* Add a spinner to show status when the client is connecting ([3434ba7](https://github-g///commit/3434ba7a1c1346babf8fefeb1ec1e3c06e20642e))
* Added more handlers to the client/network classes ([f1f1434](https://github-g///commit/f1f1434cbd221a2f18656cbd6b6519c4d56f64f0))
* Can now disconnect from networks ([136c875](https://github-g///commit/136c875e86ed1191512b6808aebea2ef20d79da4))

### [1.13.2](https://github-g///compare/v1.13.1...v1.13.2) (2020-01-13)


### Bug Fixes

* Create config dir if not present ([3599b27](https://github-g///commit/3599b2797c192ccf1800fd28ae1c7399c64b78b5))

### [1.13.1](https://github-g///compare/v1.13.0...v1.13.1) (2020-01-13)


### Bug Fixes

* Don't send empty messages ([9e5d0ce](https://github-g///commit/9e5d0ce0a46abc43bbcbeb611a369fbaa5cc1622))
* Fire unread indicator dismissal code ([5b2c9a6](https://github-g///commit/5b2c9a6418f3e71823bd527c7f73d44e6162f39c))
* Fix word wrapping ([c5874aa](https://github-g///commit/c5874aaea3750716e1415fb52f8a97477850b953))

## [1.13.0](https://github-g///compare/v1.12.0...v1.13.0) (2020-01-12)


### Features

* Add notifications for PM ([2ed5730](https://github-g///commit/2ed5730950e58c8b77c8aaa25aacdbb315eca9a2))
* Improved UI, with user list and topic ([b68c694](https://github-g///commit/b68c694b5f79611723f198be59142f14296e828c))
* Unique Application Icons ([a3f22e4](https://github-g///commit/a3f22e449462bf4cf8aa28abaaefcf1a47d6b30c))


### Bug Fixes

* Improved channel unread indicator ([df7df0b](https://github-g///commit/df7df0b748529e14a420a2d80246b6bf87a714ff))
* Install icon to the correct place, and display it in About ([a5a464c](https://github-g///commit/a5a464cf1e5b2acd6b3911d1ec38e44d40ee88cf))
* Previous unique names were not actually unique, and could change ([edea7dc](https://github-g///commit/edea7dcd70bc99280ab7be893d3b2877bfd4b26c))
* rooms now have unique internal channel names ([69d5ca2](https://github-g///commit/69d5ca2cb06caa2310acb13cb53d8078f0de608c)), closes [#1](https://github-g///issues/1)
* Use updated icon in Desktop File ([d7849ba](https://github-g///commit/d7849baef8243dfb39af34caebe30a5cf65a7d66))

## [1.12.0](https://github-g///compare/v1.11.0...v1.12.0) (2020-01-06)


### Features

* notifications for HL messages ([5e57268](https://github-g///commit/5e57268b7ed661a99de4dd4e3771e1c8070a96a4))


### Bug Fixes

* Improve desktop file handling ([6a02fee](https://github-g///commit/6a02feeeab85e96feb93c54f59f557f568f46bc3))
* User list stays in sync ([e6e0aa9](https://github-g///commit/e6e0aa9814772bf4130b6d3ca4441fab323f9766))

## [1.11.0](https://github-g///compare/v1.10.1...v1.11.0) (2019-12-31)


### Features

* Add secure storage of network passwords in the keyring ([0a86283](https://github-g///commit/0a862836cf3a9130359f7f2fa4e95ad5e4455166)), closes [#4](https://github-g///issues/4)
* Allow saving connection details. ([4a2cedf](https://github-g///commit/4a2cedfc24f5b37ddc628b4c88231ed1f0722fc2))
* Better Connection UI ([83eb056](https://github-g///commit/83eb05623e08aa5ed293618a091f39209fe9c3c3))

### [1.10.1](https://github-g///compare/v1.10.0...v1.10.1) (2019-12-28)

## [1.10.0](https://github-g///compare/v1.9.0...v1.10.0) (2019-12-28)


### Features

* Added ability to cycle tab possible tab completions ([76bb11a](https://github-g///commit/76bb11a781b1426143f3d62b0ce766f3ebec9c03))


### Bug Fixes

* better handling of server messages ([4e71da6](https://github-g///commit/4e71da6a5ff26d174432e2f71c99ee535d465beb))
* Better styling of message rows ([dad8e4a](https://github-g///commit/dad8e4af661e9ee8503873212c51eeecb845da7d))
* Changes ([e067c70](https://github-g///commit/e067c706848a4c33d42b6a33b037be9d148f2b8c))
* Distinguish messages from the server ([846fa78](https://github-g///commit/846fa7809500c9ef9d454d72c8b893d3a2e96575))
* Don't crash tab complete when entry is empty ([dced0da](https://github-g///commit/dced0dade0f5b81b019efb602af543a2b98090f0))
* Finish removing all of those print statements ([6ace19e](https://github-g///commit/6ace19e673d92cfda46b846b6f25616f7bcafcdd))
* Fix duplicate mesages when not using ZNC ([2b126d7](https://github-g///commit/2b126d7f700c2db3dfcb4d215e04f26bec3229cd))
* Fix duplicate mesages when not using ZNC ([6f11c74](https://github-g///commit/6f11c743a0c39ce331be27cbde4260c7c7a4270e))
* Fix the order of channels ([e68be9e](https://github-g///commit/e68be9e13359cb579c2e8f4842fe125ea390a02e))
* Keep last-spoke order, then alphabetical on tab complete ([dd3d8bc](https://github-g///commit/dd3d8bc37fa8777486c3a5b3ca133b91d62845c9))
* Label of join-channel button was incorrect ([48a2e81](https://github-g///commit/48a2e819b22144537017db3aa41571c5c8453504))
* Load tab completion upon entering a room ([acb4db3](https://github-g///commit/acb4db3baceb7a1d8380e0f895e8b1a90c747ca8))
* Make actions italicized ([5269616](https://github-g///commit/5269616a862c934a9d9eddace787e3fd971d3bc9))
* Prevent sending blank messages ([f95f9fd](https://github-g///commit/f95f9fd5426f4e87f5b7cdc2807836c606d2e873))
* Prevent tab complete losing entry focus ([b63ba62](https://github-g///commit/b63ba626a8316a47ef19130e87b81fd89f8763f4))
* Remove extra print()'s ([9cd9a4d](https://github-g///commit/9cd9a4de422486241f1a91c67dbc150ed50da322))
* Remove extra print()s ([76e7ff3](https://github-g///commit/76e7ff39357fc69199e795d8387b925eb8a7d44b))
* Revert "fix: Remove extra print()'s" ([7117926](https://github-g///commit/7117926c3a23a85f770cdef432a863fe8e2cad7e))
* update nick button on room change (in case we're on a new network) ([1774c63](https://github-g///commit/1774c630ca606275aa246dfe50e16ef982f0b032))

## [1.9.0](https://github-g///compare/v1.8.0...v1.9.0) (2019-12-27)


### Features

* Add notice support ([56e4b04](https://github-g///commit/56e4b049978161efc82a81920898959cb090be43))
* Allow clicking on hyperlinks ([84750e7](https://github-g///commit/84750e754fa3382721ee9335e8831ab5917d020f))

## [1.8.0](https://github-g///compare/v1.7.0...v1.8.0) (2019-12-27)


### Features

* Better ZNC support ([5fcbb88](https://github-g///commit/5fcbb885c29a65a23378bfd3a8bc28424ecd8eff))

## [1.7.0](https://github-g///compare/v1.6.0...v1.7.0) (2019-12-27)


### Features

* Allow sending formatting to channels ([c342674](https://github-g///commit/c34267470a8bc53a89290f9cf8eecf74d43bbe1f))

## [1.6.0](https://github-g///compare/v1.5.1...v1.6.0) (2019-12-27)


### Features

* Support some IRC formatting tags ([59a80f9](https://github-g///commit/59a80f996ff5dcc8abc7f1c86b6b91dfe1e6186f))

### [1.5.1](https://github-g///compare/v1.5.0...v1.5.1) (2019-12-27)


### Bug Fixes

* about dialog could only be shown once ([4f311b1](https://github-g///commit/4f311b1065dfa3d72ed27032ad43379fbcd4774e))

## [1.5.0](https://github-g///compare/v1.4.3...v1.5.0) (2019-12-27)


### Features

* Join channels from popover ([ebff79b](https://github-g///commit/ebff79b40c6db4aca07f83e27a07ec357f83651a))


### Bug Fixes

* Add margins to AppMenu ([f755486](https://github-g///commit/f7554869a55bd06de2b92e863521b7a5e0649979))

### [1.4.3](https://github-g///compare/v1.4.2...v1.4.3) (2019-12-26)


### Bug Fixes

* Add list of TODOS ([afce3ca](https://github-g///commit/afce3ca68454374d28e7a07bb5a4f61eac34bde6))
* Remove formatting characters ([27e4537](https://github-g///commit/27e45371db554560815b78d99f865f937153cafd))
* Update documentation ([bfc2e37](https://github-g///commit/bfc2e37073f931422d2b3ee13269af60cf026206))

### [1.4.2](https://github-g///compare/v1.4.1...v1.4.2) (2019-12-26)


### Bug Fixes

* Allow closing of PM buffers/rooms ([96aad3b](https://github-g///commit/96aad3b059e1cc41a64ed3c422217931d127e9d7))

### [1.4.1](https://github-g///compare/v1.4.0...v1.4.1) (2019-12-26)


### Bug Fixes

* Add about dialog ([40486d2](https://github-g///commit/40486d20bc0258944c7485b6f93d7fa09733594a))

## [1.4.0](https://github-g///compare/v1.3.0...v1.4.0) (2019-12-26)


### Features

* Add force version command ([b0bf0f6](https://github-g///commit/b0bf0f6e6542ff35aa98efb6da375f7b07faaafa))

## [1.3.0](https://github-g///compare/v1.2.1...v1.3.0) (2019-12-26)


### Features

* Add release command to setup.py ([e2babbc](https://github-g///commit/e2babbc894e3c1cf1e541be5faea2e93bd43f27f))

### [1.2.1](https://github-g///compare/v1.2.0...v1.2.1) (2019-12-26)


### Bug Fixes

* Add version tracking scripts ([2245838](https://github-g///commit/22458388c66f60fbd073da58b31bf5ecdc81916d))
* Make sure version numbering is generated correctly ([6d2e00f](https://github-g///commit/6d2e00f54a65243b5f17ea322bd83e19a4e4d80b))
* versioning is now correct ([790c14a](https://github-g///commit/790c14a65d7209fb19a61eaeeb59cf8ecd781d73))

## [1.2.0](https://github-g///compare/v1.1.1...v1.2.0) (2019-12-26)


### Features

* Add support for private messages ([10aa47e](https://github-g///commit/10aa47e985f7a43e51fd87b6aba0453ef206b4dd))
* Allow leaving/parting rooms ([b19be6c](https://github-g///commit/b19be6c1a65765dab3b57bda5cc1694f8725b683))
* Version bump because the versioning script broke ([3fd3f02](https://github-g///commit/3fd3f02f29a5ae4efd2f42268dbfff8d64bd8800))


### Bug Fixes

* Grab chat entry focus on channel change ([b524df7](https://github-g///commit/b524df7e637d6945c729e91ba08e59869d12b891))

## [1.2.0](https://github-g///compare/v1.1.1...v1.2.0) (2019-12-26)


### Features

* Add support for private messages ([10aa47e](https://github-g///commit/10aa47e985f7a43e51fd87b6aba0453ef206b4dd))
* Allow leaving/parting rooms ([b19be6c](https://github-g///commit/b19be6c1a65765dab3b57bda5cc1694f8725b683))
* Version bump because the versioning script broke ([3fd3f02](https://github-g///commit/3fd3f02f29a5ae4efd2f42268dbfff8d64bd8800))


### Bug Fixes

* Grab chat entry focus on channel change ([b524df7](https://github-g///commit/b524df7e637d6945c729e91ba08e59869d12b891))

## [1.2.0](https://github-g///compare/v1.1.1...v1.2.0) (2019-12-26)


### Features

* Add support for private messages ([10aa47e](https://github-g///commit/10aa47e985f7a43e51fd87b6aba0453ef206b4dd))
* Allow leaving/parting rooms ([b19be6c](https://github-g///commit/b19be6c1a65765dab3b57bda5cc1694f8725b683))


### Bug Fixes

* Grab chat entry focus on channel change ([b524df7](https://github-g///commit/b524df7e637d6945c729e91ba08e59869d12b891))

## [1.2.0](https://github-g///compare/v1.1.1...v1.2.0) (2019-12-24)


### Features

* Allow leaving/parting rooms ([b19be6c](https://github-g///commit/b19be6c1a65765dab3b57bda5cc1694f8725b683))

### [1.1.1](https://github-g///compare/v1.1.0...v1.1.1) (2019-12-24)


### Bug Fixes

* bump version in setup ([90ad227](https://github-g///commit/90ad227a6027315dd2fc25a63799b3f0ef07a151))

## [1.1.0](https://github-g///compare/v1.0.0...v1.1.0) (2019-12-24)


### Features

* better tab completion ([3e47d48](https://github-g///commit/3e47d48d2142f4f8663069b9896a5bdc941cd638))


### Bug Fixes

* Remove unneded variable ([3d07110](https://github-g///commit/3d07110bf4c0716a9fc0a415b8646e082fbf7e2b))

## [1.1.0](https://github-g///compare/v1.0.0...v1.1.0) (2019-12-24)


### Features

* better tab completion ([3e47d48](https://github-g///commit/3e47d48d2142f4f8663069b9896a5bdc941cd638))


### Bug Fixes

* Remove unneded variable ([3d07110](https://github-g///commit/3d07110bf4c0716a9fc0a415b8646e082fbf7e2b))

## [1.1.0](https://github-g///compare/v1.0.0...v1.1.0) (2019-12-24)


### Features

* better tab completion ([3e47d48](https://github-g///commit/3e47d48d2142f4f8663069b9896a5bdc941cd638))

## 1.0.0 (2019-12-23)


### Features

* add desktop file ([002d1b2](https://github-g///commit/002d1b2f41a430d9df00af0e572ff4eb3411fc02))
* Add networking and basic client features ([9cfe88a](https://github-g///commit/9cfe88a31cef418a9d43948a72f78db02e47a2b4))
* Add SASL login support ([e644cd1](https://github-g///commit/e644cd12acb4e9579d979f131167c44bca25af41))
* Add support for CTCP ACTION ([9108830](https://github-g///commit/9108830e10dcc5bae8ddb0e8f31470879efc2839))
* Add unread indicator when channel has unread messages ([1b9bfc6](https://github-g///commit/1b9bfc6ef5d55fe0027965f63677c036f1bcf459))
* Better ownership of various objects ([0d152f3](https://github-g///commit/0d152f38a1fdf0819db3d5a98aa64f42855f3a1c))
* Differentiate HLs from regular unreads ([3d21dcc](https://github-g///commit/3d21dcc889c6ccce37d18743c3cc176a955229b1))
* Make messages selectable ([00606f0](https://github-g///commit/00606f06ee621cb7861763c91a0713bec0457a92))
* move server connection to a popover ([917033d](https://github-g///commit/917033dc89d87e716761a636f362ffb013cde382))


### Bug Fixes

* Accidentally include an uneeded super() ([b00ec58](https://github-g///commit/b00ec5869ad8e632b1dbf6caeb0b88fb29a52260))
* Add docstrings to the codebase ([d3c29af](https://github-g///commit/d3c29af47e21c4be145af509cf6a68bb8ca30c44))
* Add the ability to scroll up ([2bd0346](https://github-g///commit/2bd0346918e6515c223f67ef1c82347721635b53))
* Fix multiserver bug ([3dcb2ac](https://github-g///commit/3dcb2ac52e8be3762de33a582290c19f06e77f46))
* Remove unreachable code and unneeded comments ([8867020](https://github-g///commit/8867020f891a49b2d32147e9848cb33b6e339d09))
* Rename the server module (and classes) ([7ab38ab](https://github-g///commit/7ab38ab5378b36a9d9f0d5d8abc70322679b289b))
* Try and fix multi-server ([02c5aa5](https://github-g///commit/02c5aa58290084a0d6dd36211296751852a97506))

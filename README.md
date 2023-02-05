[![android](https://github.com/lightningorb/orb/actions/workflows/build_android.yml/badge.svg?branch=build_android)](https://github.com/lightningorb/orb/actions/workflows/build_android.yml) [![tests](https://github.com/lightningorb/orb/actions/workflows/tests.yaml/badge.svg)](https://github.com/lightningorb/orb/actions/workflows/tests.yaml) [![windows](https://github.com/lightningorb/orb/actions/workflows/build_windows.yaml/badge.svg?branch=build_windows)](https://github.com/lightningorb/orb/actions/workflows/build_windows.yaml) [![macosx](https://github.com/lightningorb/orb/actions/workflows/build_macosx.yaml/badge.svg?branch=build_macosx)](https://github.com/lightningorb/orb/actions/workflows/build_macosx.yaml) [![linux](https://github.com/lightningorb/orb/actions/workflows/build_linux.yml/badge.svg?branch=build_linux)](https://github.com/lightningorb/orb/actions/workflows/build_linux.yml)


We're pleased to announce that Orb is now fully FOSS, under the GNU GENERAL PUBLIC LICENSE. We've had to clean up the repo of old files, so this is a new Repo: we've lost:

- issues
- pull requests

Since Orb targets many different platforms, the build system is **complex** to say the least. We'll spend some time getting the various builds working again.

We'll spend some time documenting every inch of this repo so everyone can contribute.


# Build System

The build system is huge due to the many targets:

```
Available tasks:

  deploy-ios
  merge
  release
  update-install-script
  alembic.revision
  alembic.upgrade
  android.build
  android.build-remote
  android.clean
  android.create-keystore
  android.cython
  android.deploy
  android.install
  android.sign
  android.sync
  android.upload
  appstore.local-server.create-db
  appstore.local-server.start
  appstore.local-site.deploy
  appstore.local-site.start
  appstore.remote-server.certbot
  appstore.remote-server.clone
  appstore.remote-server.create-db
  appstore.remote-server.create-tables
  appstore.remote-server.create-user
  appstore.remote-server.drop-tables
  appstore.remote-server.install-nginx-conf
  appstore.remote-server.install-service
  appstore.remote-server.install-stack
  appstore.remote-server.requirements
  appstore.remote-server.start
  appstore.remote-server.start-dev
  appstore.remote-server.start-rabbit
  appstore.remote-server.stop-rabbit
  armor.build-docker
  armor.build-linux
  armor.build-osx
  armor.build-windows
  armor.register
  cln.generate-grpc-libs
  cln.install-requirements
  cln-regtest.setup
  docker.orb-vnc
  documentation.asciinema
  documentation.build                             Build the docs. Requires sphinx.
  documentation.build-cli-docs
  documentation.clean                             Delete the built docs. Useful when renaming modules etc.
  documentation.upload                            Upload docs to site.
  documentation.view                              View docs in the browser.
  host.ssh
  ios.clean                                       Clean all XCode libs and modules
  ios.create                                      Create the xcode project.
  ios.tmp
  ios.toolchain                                   Build and install all libs and modules required for XCode.
  ios.toolchain-build
  ios.toolchain-pip
  ios.update                                      Update the xcode project with the latest changes.
  lnd.generate-grpc-libs
  lnd.install-requirements
  osx.cython
  osx.dmg
  osx.gen-license
  osx.python
  osx.requirements
  osx.run
  osx.upload
  site.build
  site.run
  site.spawn-mac-build
  site.upload                                     Upload site.
  ssh.mosh
  tags.push
  tags.tag
  test.test                                       Run the unit tests and doctests.
  third-party.clean                               Stub.
  third-party.clone                               Stub.
  ubuntu.requirements
  ubuntu.upload
  versioning.bump-build                           Bump the build number using semver and store in VERSION.
  versioning.bump-major                           Bump the major version using semver and store in VERSION.
  versioning.bump-minor                           Bump the minor version using semver and store in VERSION.
  versioning.bump-patch                           Bump the patch version using semver and store in VERSION.
  versioning.bump-pre                             Bump the pre-release using semver and store in VERSION.
```
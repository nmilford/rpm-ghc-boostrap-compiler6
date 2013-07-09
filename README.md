ghc-boostrap-compiler6
======================

An RPM spec file to install a Glasgow Haskell Compiler version able to bootstrap GHC 7.0.x

We want the latest ghc, 7.6.3, but it's binary release is not compatible with glibc on CentOS 5.

We need to build it from source, but you need GHC to build GHC. :/

The latest binary GHC release I could find that worked on CentOS 5 is ghc-6.12.3

You cannot build ghc-7.6.3 with anything less then ghc-7.* (whose binary dists do not work on CentOS 5)

So we need to build ghc-7.0.2 from source with ghc-6.12.3 binaries to allow us build our final target of ghc-7.6.3


To Build:

`sudo yum -y install rpmdevtools && rpmdev-setuptree`

`wget wget http://www.haskell.org/ghc/dist/6.12.3/ghc-6.12.3-x86_64-unknown-linux-n.tar.bz2 -O ~/rpmbuild/SOURCES/ghc-6.12.3-x86_64-unknown-linux-n.tar.bz2`

`wget https://raw.github.com/nmilford/rpm-ghc-bootsrap-compiler6/master/ghc-boostrap-compiler6.spec -O ~/rpmbuild/SPECS/ghc-bootsrap-compiler6.spec`

`rpmbuild -bb ~/rpmbuild/SPECS/ghc-bootsrap-compiler6.spec`
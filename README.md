Glyptodon
=====

This program is designed to be used with Stegodon in order to actually provide some real security on top of the steganography that Stegodon provides
Here's how to use it.

Encrypting a file
-----------------
`py glyptodon.py -e file/directory key/keyfile [packagename]`

`file/directory` is the file or directory that you're going to encrypt and pack, `key/keyfile` is either a text key or a file you want to use as a key that will be used to secure your data. `[packagename]` is an optional parameter that will override the semi-random package names with a custom one.

Decrypting a file
-----------------
`py glyptodon.py -d packagename, key/keyfile, [path]`

`packagename` is the package you want to decrypt. `key/keyfile` is the same key you used to encrypt the file, and `[path]` is an optional location to unpack to, otherwise the files will be unpacked to the working directory.

Scanning a file
---------------

`py glyptodon.py -s packagename, key/keyfile`

`packagename` is the package you want to scan. `key/keyfile` is the same key you used to encrypt the file.


Other stuff
-----------

This isn't terribly good security, so don't use it on anything super important. The main reason it exists is to disguise the data as random noise which will fool certain steganographic detection.
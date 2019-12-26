// version tracking script to adapt standard-version to python

// This Source Code Form is subject to the terms of the Mozilla Public
// License, v. 2.0. If a copy of the MPL was not distributed with this
// file, You can obtain one at http://mozilla.org/MPL/2.0/.

const fs = require('fs');


module.exports.readVersion = function (contents) {
    var version_array = contents.split(" ")
    var version = version_array[2].replace(/['"]+/g, '')
    console.log(version)
    return version
}

module.exports.writeVersion = function (contents, version) {
    var version = "__version = " + version
    console.log(version)
    // var version_file = fs.writeFileSync(
    //     'ad1459/__version__.py',
    //     version,
    //     'utf8'       
    // )
    return version
}

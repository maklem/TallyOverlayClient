import os

package_info = []

with open('requirements.txt', 'r', encoding="utf-16-le") as f:
    for line in f:
        line = line.strip()
        if line.startswith('#') or len(line) < 4:
            continue
        try:
            values = line.split('==', 1)
            name, version = values
            package_info.append({'name': name, 'version': version})
        except ValueError:
            print(f"Error for: {line}")

license_names = [
    "LICENSE",
    "LICENSE.txt",
    "LICENSE.md",
    "licenses/LICENSE",
]
for package in package_info:
    base_name = package['name'].replace('-', '_')
    base_path = f".tox/py312-pyinstaller/Lib/site-packages/{base_name}-{package['version']}.dist-info"

    for license_name in license_names:
        license_path = f"{base_path}/{license_name}"
        try:
            with open(license_path, 'r', encoding="utf-8") as f:
                license_text = f.read()
                package['license'] = license_text
                if "MIT License" in license_text:
                    package['license_type'] = "MIT"
                elif "Apache License" and "Version 2.0, January 2004" in license_text:
                    package['license_type'] = "Apache-2.0"
                elif "Apache License, Version 2.0" in license_text:
                    package['license_type'] = "Apache-2.0"
                elif "BSD 3-Clause License" in license_text:
                    package['license_type'] = "BSD-3-Clause"
                elif "PYTHON SOFTWARE FOUNDATION LICENSE VERSION 2" in license_text:
                    package['license_type'] = "PSF-2"
                elif "Mozilla Public License Version 2.0" in license_text:
                    package['license_type'] = "MPL-2"
                else:
                    raise ValueError(f"Unknown license for {package['name']}: {license_text[:100]}")
            break
        except FileNotFoundError:
            pass
package_info.append({
    'name': 'tallyoverlayclient',
    'version': '1.0.0',
    'license': open('LICENSE', 'r', encoding="utf-8").read(),
    'license_type': 'MIT',
})

python_license = [{
    'name': 'python-win64',
    'license': open('licenses-static/python-windows.txt', 'r', encoding="utf-8").read(),
}, {
    'name': 'tcl-tk',
    'license': open('licenses-static/tcl-tk.txt', 'r', encoding="utf-8").read(),
}]


os.makedirs("dist/main/licenses", exist_ok=True)
for package in package_info:
    with open(f"dist/main/licenses/{package['name']}.txt", 'w', encoding="utf-8") as f:
        f.write(package['license'])

for package in python_license:
    with open(f"dist/main/licenses/{package['name']}.txt", 'w', encoding="utf-8") as f:
        f.write(package['license'])

with open("dist/main/README.txt", 'w', encoding="utf-8") as f:
    f.write("""\
This binary distribution may be used free of charge for both
non-commercial and commercial purposes, as long as the following
restrictions are followed:
- All licenses of the included packages must be followed.

This binary distribution includes a compiled version of the python
interpreter, as well as the python standard library and Microsoft
Distributable Code.
See licenses/python-win64.txt for detailed information.

Included code from tcl/tk is subject to the TCL license.
See licenses/tcl-tk.txt for detailed information.      

This binary distribution includes the several packages,
that are not part of the python standard library.
Each package is subject to copyright by their creators.

Package            Version    License Type
------------------------------------------
""")
    for package in package_info:
        f.write(f"{package['name']:18s} {package['version']:10s} {package['license_type']}\n")

    f.write("\nSee the licenses directory for detailed information for each package.\n")
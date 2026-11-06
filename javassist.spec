Name:		javassist
Version:	3.33.0
Release:	1
Summary:	Java bytecode manipulation library
Group:		Development/Java
License:	MPLv1.1 or LGPLv2+ or ASL 2.0
URL:		https://www.javassist.org/
Source0:	https://github.com/jboss-javassist/javassist/archive/refs/tags/rel_3_33_0_ga.tar.gz#/javassist-%{version}.tar.gz

BuildArch:	noarch
Obsoletes:	%{name}-javadoc < %{version}
# Literal, so the first rpmbuild -bs records them before sysjar is installed.
BuildRequires:	maven
BuildRequires:	java-current-devel
BuildSystem:	maven

%description
Javassist edits Java bytecode, either as source text or as class-file
instructions. 3.33.0 is the current release. 3.32 moved
javassist.tools.reflect, rmi and web into the examples tree and turned
off Desc.useContextClassLoader. Tests are skipped. The OSGi bundle
plugin is not packaged, so the jar keeps the source manifest.

%prep
%setup -q -n javassist-rel_3_33_0_ga
# The tag ships a prebuilt jar. The package is built from source.
rm -f javassist.jar
# packaging bundle needs maven-bundle-plugin, which is not packaged.
# The jar plugin points at the source manifest, so that entry stays.
# The junit range and hamcrest-all are test scope. Maven still resolves
# them when tests are skipped. The release profile signs and publishes.
python - <<'PY'
import xml.etree.ElementTree as ET
from pathlib import Path

ET.register_namespace("", "http://maven.apache.org/POM/4.0.0")
ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
drop_plugins = {
    "maven-bundle-plugin",
    "central-publishing-maven-plugin",
    "maven-gpg-plugin",
}
drop_deps = {"junit", "hamcrest-all"}

def local(tag):
    return tag.rsplit("}", 1)[-1]

path = Path("pom.xml")
tree = ET.parse(path)
root = tree.getroot()
packaging = None
removed = []
deps = []
manifests = 0
for parent in root.iter():
    for child in list(parent):
        name = local(child.tag)
        if name == "packaging" and (child.text or "").strip() == "bundle":
            child.text = "jar"
            packaging = "jar"
        if name == "manifestFile":
            manifests += 1
        if name == "dependency":
            artifact = ""
            scope = ""
            for item in child:
                item_name = local(item.tag)
                if item_name == "artifactId":
                    artifact = (item.text or "").strip()
                elif item_name == "scope":
                    scope = (item.text or "").strip()
            if artifact in drop_deps and scope == "test":
                parent.remove(child)
                deps.append(artifact)
            continue
        if name != "plugin":
            continue
        artifact = ""
        for item in child:
            if local(item.tag) == "artifactId":
                artifact = (item.text or "").strip()
        if artifact in drop_plugins:
            parent.remove(child)
            removed.append(artifact)
for parent in list(root.iter()):
    for child in list(parent):
        if local(child.tag) == "dependencies" and not list(child):
            parent.remove(child)
missing_plugins = sorted(drop_plugins - set(removed))
missing_deps = sorted(drop_deps - set(deps))
if packaging != "jar" or missing_plugins or missing_deps or manifests != 1:
    raise SystemExit(
        f"packaging={packaging} plugins={missing_plugins} deps={missing_deps} manifests={manifests}"
    )
tree.write(path, encoding="UTF-8", xml_declaration=True)
PY

%files -f .mfiles
%doc License.html README.md Changes.md

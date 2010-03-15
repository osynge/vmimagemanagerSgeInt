from distutils.core import setup
setup(name='vmimagemanager',
    version='0.2.1',
    description="vmimagemanager manages virtual maschines",
    author="O M Synge",
    author_email="owen.Synge@desy.de",
    url="www-it.desy.de",
    scripts = ["vmimagemanager"],
    package_dir={'': '.'},
    packages=['vmim'],
    data_files=[('/usr/bin/', ['vmimagemanager']),
('/etc/vmimagemanager',['libvirt.xsl','vmimagemanager.cfg']),
('/usr/share/doc/vmimagemanager',['README']),
('/usr/share/doc/vmimagemanager/examples',['docs/examples/vmimagemanager-example-au.cfg',
'docs/examples/vmimagemanager-example-au.cfg',
'docs/examples/vmimagemanager-example-d430.cfg',
'docs/examples/vmimagemanager-example-esys.cfg',
'docs/examples/vmimagemanager-example-irl.cfg',
'docs/examples/vmimagemanager-example-whitehouse.cfg',
'docs/examples/vmimagemanager-xen-example.template',
'docs/examples/xen.template',
'docs/examples/xen.template.example.full.virtualisation',
'docs/examples/logging.conf'])]
)

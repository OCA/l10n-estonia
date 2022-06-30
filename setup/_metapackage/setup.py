import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-l10n-estonia",
    description="Meta package for oca-l10n-estonia Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-l10n_ee_accounting',
        'odoo12-addon-l10n_ee_reporting',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 12.0',
    ]
)

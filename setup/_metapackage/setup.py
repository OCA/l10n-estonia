import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-l10n-estonia",
    description="Meta package for oca-l10n-estonia Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-currency_rate_update_ee_beep',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 11.0',
    ]
)

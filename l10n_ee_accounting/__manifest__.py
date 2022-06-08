# Copyright 2020-2022 CorporateHub (https://corporatehub.eu)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Estonia - Accounting",
    "summary": "Estonian accounting localization",
    "version": "12.0.1.0.0",
    "category": "Localization",
    "website": "https://github.com/OCA/l10n-estonia",
    "author": "CorporateHub, Odoo Community Association (OCA)",
    "maintainers": ["alexey-pelykh"],
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["account", "base_iban", "base_vat",],
    "data": [
        "data/income_statement.xml",
        "data/balance_sheet.xml",
        "data/kmd_2017.xml",
        "data/account_chart_template.xml",
        "data/account.account.template.csv",
        "data/account_group.xml",
        "data/account_tax_group.xml",
        "data/account_tax_template.xml",
        "data/account_fiscal_position_template.xml",
        "data/account_chart_template_configure.xml",
    ],
}
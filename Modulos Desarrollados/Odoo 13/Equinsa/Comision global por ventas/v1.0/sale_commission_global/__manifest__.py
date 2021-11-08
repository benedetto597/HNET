{
    "name": "Sales commissions global",
    "description": "Calculo de comisión a partir de la base imponible de la venta",
    "version": "0.1",
    "author": "HNET",
    "category": "Sales Management",
    "depends": ["sale_commission"],
    "website": "https://hnetw.com",
    "data": [
        "views/res_partner_view.xml",
        "views/sale_commission_view.xml",
        "views/sale_order_view.xml",
        "views/account_move_view.xml",
    ],
    "application": True,
    "installable": True,
}

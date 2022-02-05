import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc

CG_LOGO = ''


head_bar = dbc.Navbar(
    [
        html.A(
            # Use row and col to control vertical alignment of logo / brand
            dbc.Row(
                [
                    dbc.Col(html.Img(src=CG_LOGO, height="50px"))
                ],
                align="center",
                no_gutters=True,

            ),
            href="",
        ),
        dbc.NavbarToggler(id="navbar-toggler3"),
        dbc.Collapse([
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Inicio",
                                href="/", disabled=True)),
                    dbc.NavItem(dbc.NavLink("Proveedores",
                                href="/dash-proveedor")),
                    #dbc.NavItem(dbc.NavLink("Comité de Crédito",
                    #            href="/comite-credito")),
                    #dbc.NavItem(dbc.NavLink("Inversionistas",
                    #            href="/inversionistas")),
                ])
        ],id='navbar_collapse', navbar=True, className='nav-links'),
    ],
    color='#162752', className='shadow-4'
)



def create_layout(app):
    return html.Div([
        head_bar,
        html.Br(),
    ])
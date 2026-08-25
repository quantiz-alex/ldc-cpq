"""Layout da página de Login — fullscreen, sem sidebar."""
from __future__ import annotations

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html

PRIMARY_COLOR = "#1045C8"

def layout(**kwargs) -> html.Div:
    """Monta o layout fullscreen de login."""
    return html.Div(
        dbc.Card(
            dbc.CardBody(
                [
                    html.Div(
                        html.Img(
                            src="/assets/logo.png",
                            height=48,
                            style={"objectFit": "contain", "maxWidth": "220px"},
                        ),
                        className="text-center mb-4",
                    ),
                    dbc.Label("Email", className="small fw-semibold"),
                    dbc.Input(
                        id="login-email",
                        type="email",
                        placeholder="seu.email@ldc-cpq.com",
                        className="mb-3",
                    ),
                    dbc.Label("Senha", className="small fw-semibold"),
                    dbc.Input(
                        id="login-senha",
                        type="password",
                        placeholder="••••••••",
                        n_submit=0,
                        className="mb-3",
                    ),
                    dbc.Button(
                        "Entrar",
                        id="login-btn",
                        n_clicks=0,
                        className="w-100 fw-bold",
                        style={"backgroundColor": PRIMARY_COLOR, "borderColor": PRIMARY_COLOR},
                    ),
                    dbc.Alert(id="login-alert", is_open=False, color="danger", className="mt-3 mb-0"),
                    html.Hr(className="my-3"),
                    html.P(
                        "Modo mock: qualquer senha é aceita. Use um email cadastrado em "
                        "mock_data/usuarios.csv (ex.: admin@ldc-cpq.com).",
                        className="text-muted mb-0",
                        style={"fontSize": "0.72rem"},
                    ),
                ]
            ),
            className="shadow-lg border-0",
            style={"width": "400px"},
        ),
        style={
            "minHeight": "100vh",
            "display": "flex",
            "alignItems": "center",
            "justifyContent": "center",
            "background": "linear-gradient(135deg, #1e293b, #0f172a)",
        },
    )


dash.register_page(__name__, path="/login", title="Login — LDC Insumos", name="Login", layout=layout)

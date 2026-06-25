from fastapi.responses import HTMLResponse


def swagger_ui_offline_html(openapi_url: str, title: str) -> HTMLResponse:
    html = """
    <!doctype html>
    <html lang="fr">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>{title}</title>
        <link rel="icon" href="/static/swagger/favicon-32x32.png" />
        <link rel="stylesheet" href="/static/swagger/swagger-ui.css" />
        <style>
          body {{ margin: 0; background: #fafafa; }}
          .topbar {{ display: none; }}
        </style>
      </head>
      <body>
        <div id="swagger-ui"></div>
        <script src="/static/swagger/swagger-ui-bundle.js"></script>
        <script src="/static/swagger/swagger-ui-standalone-preset.js"></script>
        <script>
          window.onload = function() {{
            SwaggerUIBundle({{
              url: "{openapi_url}",
              dom_id: "#swagger-ui",
              deepLinking: true,
              docExpansion: "list",
              defaultModelsExpandDepth: 1,
              presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIStandalonePreset
              ],
              layout: "StandaloneLayout"
            }});
          }};
        </script>
      </body>
    </html>
    """.format(openapi_url=openapi_url, title=title)
    return HTMLResponse(html)

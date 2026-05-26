"""
Aplicação desktop/mobile com Flet para gerenciamento de filmes
Consome a API Flask desenvolvida anteriormente
"""

import flet as ft
import requests
from views import HomeView, FilmeFormView

API_URL = "http://localhost:5000/api"

class FilmesApp:
    def __init__(self):
        self.api_base = API_URL
        
    def init(self, page: ft.Page):
        self.page = page
        self.page.title = "Catálogo de Filmes - Flet App"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 0
        self.page.spacing = 0
        
        self.page.fonts = {
            "Roboto": "/fonts/Roboto-Regular.ttf",
        }
        
        self.home_view = HomeView(self.page, self.api_base)
        self.form_view = FilmeFormView(self.page, self.api_base)
        
        self.page.on_route_change = self.route_change
        
        self.page.go("/")
    
    def route_change(self, route):
        """Gerencia a navegação entre telas"""
        
        self.page.views.clear()
        
        if self.page.route == "/":
            self.page.views.append(
                ft.View(
                    "/",
                    [
                        self._build_app_bar("🎬 Meu Catálogo de Filmes"),
                        self.home_view.build(),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                )
            )
            
        elif self.page.route == "/adicionar":
            filme_id = self.page.route.split("/")[-1] if "/editar" in self.page.route else None
            
            self.page.views.append(
                ft.View(
                    self.page.route,
                    [
                        self._build_app_bar(
                            "Adicionar Filme" if not filme_id else "Editar Filme",
                            show_back=True
                        ),
                        self.form_view.build(filme_id),
                    ],
                    vertical_alignment=ft.MainAxisAlignment.START,
                    horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
                )
            )
    
    def _build_app_bar(self, title: str, show_back: bool = False) -> ft.AppBar:
        """Constrói a barra superior da aplicação"""
        actions = []
        if not show_back:
            actions.append(
                ft.IconButton(
                    icon=ft.icons.ADD,
                    tooltip="Adicionar filme",
                    on_click=lambda e: self.page.go("/adicionar"),
                )
            )
        
        return ft.AppBar(
            title=ft.Text(title, size=24, weight=ft.FontWeight.BOLD),
            center_title=False,
            bgcolor=ft.Colors.PRIMARY,
            color=ft.Colors.WHITE,
            actions=actions,
            leading=ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda e: self.page.go("/"),
                visible=show_back,
            ) if show_back else None,
        )
    
    def run(self):
        ft.app(target=self.init)

if __name__ == "__main__":
    app = FilmesApp()
    app.run()
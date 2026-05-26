"""
Tela principal que exibe a lista de filmes
"""

import flet as ft
import requests

class HomeView:
    def __init__(self, page: ft.Page, api_base: str):
        self.page = page
        self.api_base = api_base
        self.filmes_list = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)
        self.loading_indicator = ft.ProgressRing()
        
    def build(self) -> ft.Container:
        """Constrói a view principal"""
        refresh_button = ft.IconButton(
            icon=ft.icons.REFRESH,
            icon_size=30,
            tooltip="Atualizar lista",
            on_click=lambda e: self.carregar_filmes(),
        )
        
        header = ft.Row(
            [
                ft.Text("Meus Filmes", size=28, weight=ft.FontWeight.BOLD),
                refresh_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        
        content = ft.Column(
            [
                header,
                ft.Divider(height=2, color=ft.Colors.GREY_300),
                self.filmes_list,
            ],
            spacing=20,
        )
        
        self.page.run_task(self.carregar_filmes)
        
        return ft.Container(
            content=content,
            padding=20,
            expand=True,
        )
    
    async def carregar_filmes(self):
        """Carrega a lista de filmes da API"""
        self.filmes_list.controls.clear()
        self.filmes_list.controls.append(
            ft.Row(
                [self.loading_indicator, ft.Text("Carregando filmes...")],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
        self.page.update()
        
        try:
            response = requests.get(f"{self.api_base}/filmes/", timeout=10)
            response.raise_for_status()
            
            filmes = response.json()
            self._exibir_filmes(filmes)
            
        except requests.exceptions.ConnectionError:
            self._exibir_erro("Não foi possível conectar ao servidor. Verifique se o backend está rodando.")
        except requests.exceptions.Timeout:
            self._exibir_erro("Tempo limite excedido. Tente novamente.")
        except Exception as e:
            self._exibir_erro(f"Erro ao carregar filmes: {str(e)}")
    
    def _exibir_filmes(self, filmes: list):
        """Exibe a lista de filmes na interface"""
        
        self.filmes_list.controls.clear()
        
        if not filmes:
            self.filmes_list.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.icons.MOVIE, size=50, color=ft.Colors.GREY_400),
                            ft.Text("Nenhum filme cadastrado", size=16, color=ft.Colors.GREY_600),
                            ft.Text("Clique no + para adicionar seu primeiro filme!", size=14, color=ft.Colors.GREY_500),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                    alignment=ft.alignment.center,
                    expand=True,
                    padding=50,
                )
            )
        else:
            for filme in filmes:
                card = self._criar_card_filme(filme)
                self.filmes_list.controls.append(card)
        
        self.page.update()
    
    def _criar_card_filme(self, filme: dict) -> ft.Card:
        """Cria um card para cada filme"""
        nota = filme['nota']
        if nota >= 7:
            nota_color = ft.Colors.GREEN
            nota_emoji = "🌟"
        elif nota >= 5:
            nota_color = ft.Colors.ORANGE
            nota_emoji = "⭐"
        else:
            nota_color = ft.Colors.RED
            nota_emoji = "💩"
        
        card_content = ft.Container(
            content=ft.Column(
                [
                    # Título e nota
                    ft.Row(
                        [
                            ft.Text(
                                filme['titulo'],
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                expand=True,
                            ),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Text(nota_emoji, size=16),
                                        ft.Text(
                                            f"{nota:.1f}",
                                            size=16,
                                            weight=ft.FontWeight.BOLD,
                                            color=nota_color,
                                        ),
                                    ],
                                    spacing=5,
                                ),
                                padding=ft.padding.symmetric(horizontal=10, vertical=5),
                                bgcolor=ft.Colors.GREY_100,
                                border_radius=20,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    
                    # Diretor
                    ft.Row(
                        [
                            ft.Icon(ft.icons.PERSON, size=16, color=ft.Colors.GREY_600),
                            ft.Text(f"Diretor: {filme['diretor']}", size=14, color=ft.Colors.GREY_700),
                        ],
                        spacing=5,
                    ),
                    
                    # Ano
                    ft.Row(
                        [
                            ft.Icon(ft.icons.CALENDAR_TODAY, size=16, color=ft.Colors.GREY_600),
                            ft.Text(f"Ano: {filme['ano']}", size=14, color=ft.Colors.GREY_700),
                        ],
                        spacing=5,
                    ),
                    
                    # Botões de ação
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color=ft.Colors.BLUE,
                                tooltip="Editar",
                                on_click=lambda e, f=filme: self._editar_filme(f['id']),
                            ),
                            ft.IconButton(
                                icon=ft.icons.DELETE,
                                icon_color=ft.Colors.RED,
                                tooltip="Excluir",
                                on_click=lambda e, f=filme: self._confirmar_exclusao(f),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        spacing=5,
                    ),
                ],
                spacing=10,
            ),
            padding=15,
        )
        
        return ft.Card(
            content=card_content,
            elevation=3,
            margin=ft.margin.only(bottom=10),
        )
    
    def _editar_filme(self, filme_id: int):
        """Navega para a tela de edição"""
        self.page.go(f"/editar/{filme_id}")
    
    def _confirmar_exclusao(self, filme: dict):
        """Exibe diálogo de confirmação antes de excluir"""
        def excluir_confirmado(e):
            self._excluir_filme(filme['id'])
            dialog.open = False
            self.page.update()
        
        dialog = ft.AlertDialog(
            title=ft.Text("Confirmar exclusão"),
            content=ft.Text(f"Tem certeza que deseja excluir '{filme['titulo']}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dialog, 'open', False)),
                ft.TextButton("Excluir", on_click=excluir_confirmado, style=ft.ButtonStyle(color=ft.Colors.RED)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        self.page.dialog = dialog
        dialog.open = True
        self.page.update()
    
    def _excluir_filme(self, filme_id: int):
        """Exclui um filme via API"""
        try:
            response = requests.delete(f"{self.api_base}/filmes/{filme_id}")
            
            if response.status_code == 200:
                self.page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Filme excluído com sucesso!"),
                        bgcolor=ft.Colors.GREEN,
                    )
                )
                self.page.run_task(self.carregar_filmes)
            else:
                self._mostrar_erro("Erro ao excluir filme")
                
        except Exception as e:
            self._mostrar_erro(f"Erro: {str(e)}")
    
    def _exibir_erro(self, mensagem: str):
        """Exibe mensagem de erro na lista"""
        self.filmes_list.controls.clear()
        self.filmes_list.controls.append(
            ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.icons.ERROR_OUTLINE, size=50, color=ft.Colors.RED),
                        ft.Text(mensagem, size=16, color=ft.Colors.RED),
                        ft.ElevatedButton(
                            "Tentar novamente",
                            on_click=lambda e: self.page.run_task(self.carregar_filmes),
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=15,
                ),
                alignment=ft.alignment.center,
                expand=True,
                padding=30,
            )
        )
        self.page.update()
    
    def _mostrar_erro(self, mensagem: str):
        """Mostra snackbar de erro"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(mensagem),
                bgcolor=ft.Colors.RED,
            )
        )
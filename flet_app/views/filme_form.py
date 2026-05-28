"""
Tela de formulário para adicionar/editar filmes
"""

import flet as ft
import requests

class FilmeFormView:
    def __init__(self, page: ft.Page, api_base: str):
        self.page = page
        self.api_base = api_base
        self.filme_id = None
        
        self.titulo_field = ft.TextField(
            label="Título",
            hint_text="Digite o nome do filme",
            prefix_icon=ft.icons.MOVIE,
            max_length=100,
            expand=True,
        )
        
        self.diretor_field = ft.TextField(
            label="Diretor",
            hint_text="Nome do diretor",
            prefix_icon=ft.icons.PERSON,
            max_length=80,
            expand=True,
        )
        
        self.ano_field = ft.TextField(
            label="Ano",
            hint_text="Ex: 1994",
            prefix_icon=ft.icons.CALENDAR_TODAY,
            keyboard_type=ft.KeyboardType.NUMBER,
            max_length=4,
            expand=True,
        )
        
        self.nota_field = ft.TextField(
            label="Nota (0-10)",
            hint_text="Ex: 8.5",
            prefix_icon=ft.icons.STAR,
            keyboard_type=ft.KeyboardType.NUMBER,
            expand=True,
        )
        
        self.salvar_button = ft.ElevatedButton(
            "Salvar Filme",
            icon=ft.icons.SAVE,
            on_click=self.salvar_filme,
        )
        
        self.cancelar_button = ft.OutlinedButton(
            "Cancelar",
            icon=ft.icons.CANCEL,
            on_click=lambda e: self.page.go("/"),
        )
        
    def build(self, filme_id: str = None) -> ft.Container:
        """Constrói o formulário"""
        self.filme_id = int(filme_id) if filme_id else None
        
        if self.filme_id:
            self.page.run_task(self.carregar_dados_filme)
        
        form = ft.Column(
            [
                ft.Text(
                    "Preencha os dados do filme",
                    size=16,
                    color=ft.Colors.GREY_700,
                ),
                ft.Divider(height=2),
                self.titulo_field,
                self.diretor_field,
                ft.Row(
                    [self.ano_field, self.nota_field],
                    spacing=20,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Row(
                    [self.cancelar_button, self.salvar_button],
                    alignment=ft.MainAxisAlignment.END,
                    spacing=10,
                ),
            ],
            spacing=20,
        )
        
        return ft.Container(
            content=form,
            padding=30,
            expand=True,
        )
    
    async def carregar_dados_filme(self):
        """Carrega os dados do filme para edição"""
        try:
            response = requests.get(f"{self.api_base}/filmes/{self.filme_id}")
            response.raise_for_status()
            
            filme = response.json()
            
            self.titulo_field.value = filme['titulo']
            self.diretor_field.value = filme['diretor']
            self.ano_field.value = str(filme['ano'])
            self.nota_field.value = str(filme['nota'])
            
            self.page.update()
            
        except Exception as e:
            self._mostrar_erro(f"Erro ao carregar filme: {str(e)}")
            self.page.go("/")
    
    async def salvar_filme(self, e):
        """Salva o filme (cria ou atualiza)"""
        if not self.titulo_field.value:
            self._mostrar_erro("O título é obrigatório")
            return
        
        if not self.diretor_field.value:
            self._mostrar_erro("O diretor é obrigatório")
            return
        
        try:
            ano = int(self.ano_field.value)
            if ano < 1888 or ano > 2026:
                self._mostrar_erro("Ano deve estar entre 1888 e 2026")
                return
        except ValueError:
            self._mostrar_erro("Ano deve ser um número válido")
            return
        
        try:
            nota = float(self.nota_field.value)
            if nota < 0 or nota > 10:
                self._mostrar_erro("Nota deve estar entre 0 e 10")
                return
        except ValueError:
            self._mostrar_erro("Nota deve ser um número válido")
            return

        dados = {
            "titulo": self.titulo_field.value.strip(),
            "diretor": self.diretor_field.value.strip(),
            "ano": ano,
            "nota": nota,
        }
        
        self.salvar_button.disabled = True
        self.salvar_button.text = "Salvando..."
        self.page.update()
        
        try:
            if self.filme_id:
                self._mostrar_sucesso("Edição será implementada em breve")
                self.page.go("/")
            else:
                response = requests.post(
                    f"{self.api_base}/filmes/",
                    json=dados,
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 201:
                    self._mostrar_sucesso("Filme adicionado com sucesso!")
                    self.page.go("/")
                else:
                    erro = response.json().get('erro', 'Erro desconhecido')
                    self._mostrar_erro(erro)
                    
        except requests.exceptions.ConnectionError:
            self._mostrar_erro("Não foi possível conectar ao servidor")
        except Exception as erro:
            self._mostrar_erro(f"Erro ao salvar: {str(erro)}")
        finally:
            self.salvar_button.disabled = False
            self.salvar_button.text = "Salvar Filme"
            self.page.update()
    
    def _mostrar_erro(self, mensagem: str):
        """Mostra snackbar de erro"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(mensagem),
                bgcolor=ft.Colors.RED,
                duration=4000,
            )
        )
    
    def _mostrar_sucesso(self, mensagem: str):
        """Mostra snackbar de sucesso"""
        self.page.show_snack_bar(
            ft.SnackBar(
                content=ft.Text(mensagem),
                bgcolor=ft.Colors.GREEN,
                duration=3000,
            )
        )
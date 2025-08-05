#!/usr/bin/env python3
"""
Utilitários de Tema - Sistema de Finanças Pessoais
==================================================

Gerencia as cores e estilos baseados no design Hook.
"""

class HookTheme:
    """Configurações do tema Hook - Moderno e Elegante"""
    
    # Cores principais (baseadas no Hook)
    BACKGROUND_PRIMARY = "#000000"        # Preto puro
    BACKGROUND_SECONDARY = "#1a1a1a"     # Cinza muito escuro
    BACKGROUND_TERTIARY = "#2d2d2d"      # Cinza escuro
    BACKGROUND_CARD = "#ffffff"           # Branco para cards
    
    # Cores de texto
    TEXT_PRIMARY = "#ffffff"              # Branco
    TEXT_SECONDARY = "#e0e0e0"           # Cinza claro
    TEXT_PLACEHOLDER = "#888888"         # Cinza médio
    TEXT_DARK = "#000000"                # Preto para texto em fundo claro
    
    # Cores de destaque (Hook)
    ACCENT_PRIMARY = "#6366f1"           # Índigo principal
    ACCENT_SECONDARY = "#4f46e5"         # Índigo escuro
    ACCENT_LIGHT = "#818cf8"             # Índigo claro
    ACCENT_HOVER = "#4338ca"             # Índigo hover
    
    # Cores de borda
    BORDER_PRIMARY = "#333333"           # Borda escura
    BORDER_FOCUS = "#6366f1"             # Borda em foco (índigo)
    BORDER_SUCCESS = "#10b981"           # Verde sucesso
    BORDER_ERROR = "#ef4444"             # Vermelho erro
    BORDER_LIGHT = "#e5e7eb"             # Borda clara
    
    # Cores de botões
    BUTTON_PRIMARY = "#6366f1"           # Botão primário (índigo)
    BUTTON_PRIMARY_HOVER = "#4f46e5"     # Hover
    BUTTON_SECONDARY = "#ffffff"         # Botão secundário (branco)
    BUTTON_SECONDARY_HOVER = "#f3f4f6"   # Hover
    BUTTON_DISABLED = "#6b7280"          # Desabilitado
    
    # Cores de link
    LINK_PRIMARY = "#6366f1"             # Link primário
    LINK_HOVER = "#4f46e5"               # Link hover
    
    # Cores de progresso
    PROGRESS_BACKGROUND = "#1f2937"      # Fundo da barra
    PROGRESS_BORDER = "#374151"          # Borda da barra
    
    @classmethod
    def get_main_stylesheet(cls) -> str:
        """Retorna o stylesheet principal do tema Hook"""
        return f"""
            QWidget {{
                background-color: {cls.BACKGROUND_PRIMARY};
                font-family: 'Muli', 'Segoe UI', Arial, sans-serif;
                color: {cls.TEXT_PRIMARY};
            }}
        """
    
    @classmethod
    def get_card_stylesheet(cls) -> str:
        """Retorna o stylesheet para cards (estilo Hook)"""
        return f"""
            QFrame {{
                background-color: {cls.BACKGROUND_CARD};
                border-radius: 12px;
                border: 1px solid {cls.BORDER_LIGHT};
                padding: 20px;
            }}
        """
    
    @classmethod
    def get_input_stylesheet(cls, valid: bool = None) -> str:
        """Retorna o stylesheet para inputs (estilo Hook)"""
        base_style = f"""
            QLineEdit {{
                padding: 16px 20px;
                border: 2px solid {cls.BORDER_LIGHT};
                border-radius: 8px;
                font-size: 16px;
                background-color: {cls.BACKGROUND_CARD};
                color: {cls.TEXT_DARK};
                min-height: 56px;
                font-weight: 400;
            }}
            QLineEdit:focus {{
                border-color: {cls.BORDER_FOCUS};
                outline: none;
                border-width: 2px;
            }}
            QLineEdit::placeholder {{
                color: {cls.TEXT_PLACEHOLDER};
                font-size: 16px;
                font-weight: 400;
            }}
        """
        
        if valid is True:
            return base_style + f"QLineEdit {{ border-color: {cls.BORDER_SUCCESS}; }}"
        elif valid is False:
            return base_style + f"QLineEdit {{ border-color: {cls.BORDER_ERROR}; }}"
        else:
            return base_style
    
    @classmethod
    def get_button_stylesheet(cls, button_type: str = "primary") -> str:
        """Retorna o stylesheet para botões (estilo Hook)"""
        if button_type == "secondary":
            return f"""
                QPushButton {{
                    background-color: {cls.BUTTON_SECONDARY};
                    color: {cls.TEXT_DARK};
                    border: 2px solid {cls.BORDER_LIGHT};
                    padding: 16px 24px;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 16px;
                    min-height: 56px;
                }}
                QPushButton:hover {{
                    background-color: {cls.BUTTON_SECONDARY_HOVER};
                    border-color: {cls.BORDER_FOCUS};
                }}
                QPushButton:pressed {{
                    background-color: #e5e7eb;
                }}
                QPushButton:disabled {{
                    background-color: {cls.BUTTON_DISABLED};
                    color: {cls.TEXT_PRIMARY};
                    border-color: {cls.BUTTON_DISABLED};
                }}
            """
        else:  # primary
            return f"""
                QPushButton {{
                    background-color: {cls.BUTTON_PRIMARY};
                    color: {cls.TEXT_PRIMARY};
                    border: none;
                    padding: 16px 24px;
                    border-radius: 8px;
                    font-weight: 600;
                    font-size: 16px;
                    min-height: 56px;
                }}
                QPushButton:hover {{
                    background-color: {cls.BUTTON_PRIMARY_HOVER};
                }}
                QPushButton:pressed {{
                    background-color: {cls.ACCENT_HOVER};
                }}
                QPushButton:disabled {{
                    background-color: {cls.BUTTON_DISABLED};
                    color: {cls.TEXT_PRIMARY};
                }}
            """
    
    @classmethod
    def get_link_stylesheet(cls) -> str:
        """Retorna o stylesheet para links (estilo Hook)"""
        return f"""
            QPushButton {{
                background: none;
                border: none;
                color: {cls.LINK_PRIMARY};
                text-decoration: none;
                font-weight: 500;
            }}
            QPushButton:hover {{
                color: {cls.LINK_HOVER};
                text-decoration: underline;
            }}
        """
    
    @classmethod
    def get_progress_stylesheet(cls) -> str:
        """Retorna o stylesheet para barras de progresso (estilo Hook)"""
        return f"""
            QProgressBar {{
                border: 1px solid {cls.PROGRESS_BORDER};
                border-radius: 6px;
                text-align: center;
                height: 8px;
                background-color: {cls.PROGRESS_BACKGROUND};
            }}
            QProgressBar::chunk {{
                border-radius: 4px;
                background-color: {cls.ACCENT_PRIMARY};
            }}
        """
    
    @classmethod
    def get_label_stylesheet(cls, label_type: str = "primary") -> str:
        """Retorna o stylesheet para labels (estilo Hook)"""
        if label_type == "title":
            return f"color: {cls.TEXT_PRIMARY}; font-size: 48px; font-weight: 900; line-height: 1.2;"
        elif label_type == "subtitle":
            return f"color: {cls.TEXT_SECONDARY}; font-size: 18px; font-weight: 400;"
        elif label_type == "field":
            return f"color: {cls.TEXT_DARK}; font-size: 14px; font-weight: 600;"
        elif label_type == "error":
            return f"color: {cls.BORDER_ERROR}; font-size: 12px; font-weight: 500;"
        elif label_type == "info":
            return f"color: {cls.TEXT_SECONDARY}; font-size: 14px; font-weight: 400;"
        elif label_type == "card-title":
            return f"color: {cls.ACCENT_PRIMARY}; font-size: 24px; font-weight: 600;"
        else:  # primary
            return f"color: {cls.TEXT_PRIMARY};"
    
    @classmethod
    def get_checkbox_stylesheet(cls) -> str:
        """Retorna o stylesheet para checkboxes (estilo Hook)"""
        return f"""
            QCheckBox {{
                color: {cls.TEXT_SECONDARY};
                font-size: 14px;
                font-weight: 500;
                spacing: 12px;
                padding: 8px;
            }}
            QCheckBox::indicator {{
                width: 20px;
                height: 20px;
                border: 2px solid {cls.BORDER_LIGHT};
                border-radius: 4px;
                background-color: {cls.BACKGROUND_CARD};
                margin-right: 8px;
            }}
            QCheckBox::indicator:checked {{
                background-color: {cls.ACCENT_PRIMARY};
                border-color: {cls.ACCENT_PRIMARY};
                image: url(data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMTIiIGhlaWdodD0iMTIiIHZpZXdCb3g9IjAgMCAxMiAxMiIgZmlsbD0ibm9uZSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTEwIDNMNC41IDguNUwyIDYiIHN0cm9rZT0id2hpdGUiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIi8+Cjwvc3ZnPgo=);
            }}
            QCheckBox::indicator:hover {{
                border-color: {cls.BORDER_FOCUS};
            }}
            QCheckBox::indicator:pressed {{
                background-color: {cls.ACCENT_HOVER};
            }}
        """
    
    @classmethod
    def get_hero_stylesheet(cls) -> str:
        """Retorna o stylesheet para seção hero (estilo Hook)"""
        return f"""
            QWidget {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 {cls.BACKGROUND_PRIMARY},
                    stop:1 {cls.BACKGROUND_SECONDARY});
            }}
        """
    
    @classmethod
    def get_badge_stylesheet(cls) -> str:
        """Retorna o stylesheet para badges (estilo Hook)"""
        return f"""
            QLabel {{
                background-color: {cls.ACCENT_PRIMARY};
                color: {cls.TEXT_PRIMARY};
                border-radius: 20px;
                padding: 8px 16px;
                font-size: 12px;
                font-weight: 600;
            }}
        """ 
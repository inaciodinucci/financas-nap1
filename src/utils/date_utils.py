from datetime import datetime, date, timedelta
from typing import Tuple, List
import calendar
import locale

# Configurar locale para português brasileiro
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except:
        pass  # Usar locale padrão se não conseguir configurar

class DateUtils:
    """Utilitários para manipulação de datas"""
    
    @staticmethod
    def get_current_month() -> Tuple[int, int]:
        """Retorna o ano e mês atual"""
        now = datetime.now()
        return now.year, now.month
    
    @staticmethod
    def get_month_range(year: int, month: int) -> Tuple[date, date]:
        """Retorna o primeiro e último dia do mês"""
        first_day = date(year, month, 1)
        last_day = date(year, month, calendar.monthrange(year, month)[1])
        return first_day, last_day
    
    @staticmethod
    def get_week_range(target_date: date = None) -> Tuple[date, date]:
        """Retorna o primeiro e último dia da semana"""
        if target_date is None:
            target_date = date.today()
        
        # Encontrar o início da semana (domingo)
        days_since_sunday = target_date.weekday() + 1
        start_of_week = target_date - timedelta(days=days_since_sunday)
        end_of_week = start_of_week + timedelta(days=6)
        
        return start_of_week, end_of_week
    
    @staticmethod
    def get_year_range(year: int) -> Tuple[date, date]:
        """Retorna o primeiro e último dia do ano"""
        first_day = date(year, 1, 1)
        last_day = date(year, 12, 31)
        return first_day, last_day
    
    @staticmethod
    def get_previous_month(year: int, month: int) -> Tuple[int, int]:
        """Retorna o ano e mês anterior"""
        if month == 1:
            return year - 1, 12
        else:
            return year, month - 1
    
    @staticmethod
    def get_next_month(year: int, month: int) -> Tuple[int, int]:
        """Retorna o ano e mês seguinte"""
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1
    
    @staticmethod
    def format_date(date_obj: date, format_type: str = 'short') -> str:
        """Formata uma data para exibição"""
        if format_type == 'short':
            return date_obj.strftime('%d/%m/%Y')
        elif format_type == 'long':
            return date_obj.strftime('%d de %B de %Y')
        elif format_type == 'month_year':
            return date_obj.strftime('%B/%Y')
        elif format_type == 'day_month':
            return date_obj.strftime('%d/%m')
        elif format_type == 'weekday':
            return date_obj.strftime('%A')
        else:
            return date_obj.strftime('%d/%m/%Y')
    
    @staticmethod
    def format_currency(value: float, currency: str = 'BRL') -> str:
        """Formata um valor monetário"""
        if currency == 'BRL':
            return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        else:
            return f"{value:,.2f}"
    
    @staticmethod
    def get_month_name(month: int) -> str:
        """Retorna o nome do mês"""
        month_names = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ]
        return month_names[month - 1]
    
    @staticmethod
    def get_weekday_name(weekday: int) -> str:
        """Retorna o nome do dia da semana"""
        weekday_names = [
            'Segunda-feira', 'Terça-feira', 'Quarta-feira', 
            'Quinta-feira', 'Sexta-feira', 'Sábado', 'Domingo'
        ]
        return weekday_names[weekday]
    
    @staticmethod
    def get_short_weekday_name(weekday: int) -> str:
        """Retorna o nome abreviado do dia da semana"""
        weekday_names = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        return weekday_names[weekday]
    
    @staticmethod
    def get_days_in_month(year: int, month: int) -> int:
        """Retorna o número de dias no mês"""
        return calendar.monthrange(year, month)[1]
    
    @staticmethod
    def get_month_calendar(year: int, month: int) -> List[List[int]]:
        """Retorna o calendário do mês como matriz"""
        return calendar.monthcalendar(year, month)
    
    @staticmethod
    def is_today(date_obj: date) -> bool:
        """Verifica se a data é hoje"""
        return date_obj == date.today()
    
    @staticmethod
    def is_this_month(date_obj: date) -> bool:
        """Verifica se a data é deste mês"""
        today = date.today()
        return date_obj.year == today.year and date_obj.month == today.month
    
    @staticmethod
    def get_date_from_string(date_str: str, format_str: str = '%Y-%m-%d') -> date:
        """Converte string para data"""
        try:
            return datetime.strptime(date_str, format_str).date()
        except ValueError:
            return date.today()
    
    @staticmethod
    def get_string_from_date(date_obj: date, format_str: str = '%Y-%m-%d') -> str:
        """Converte data para string"""
        return date_obj.strftime(format_str)
    
    @staticmethod
    def get_period_display_name(period_type: str, year: int = None, month: int = None) -> str:
        """Retorna o nome de exibição do período"""
        if period_type == 'today':
            return 'Hoje'
        elif period_type == 'week':
            return 'Esta semana'
        elif period_type == 'month':
            if year and month:
                return f"{DateUtils.get_month_name(month)}/{year}"
            return 'Este mês'
        elif period_type == 'year':
            if year:
                return str(year)
            return 'Este ano'
        else:
            return 'Período'
    
    @staticmethod
    def get_period_dates(period_type: str, year: int = None, month: int = None) -> Tuple[date, date]:
        """Retorna as datas de início e fim do período"""
        today = date.today()
        
        if period_type == 'today':
            return today, today
        elif period_type == 'week':
            return DateUtils.get_week_range(today)
        elif period_type == 'month':
            if year and month:
                return DateUtils.get_month_range(year, month)
            else:
                return DateUtils.get_month_range(today.year, today.month)
        elif period_type == 'year':
            if year:
                return DateUtils.get_year_range(year)
            else:
                return DateUtils.get_year_range(today.year)
        else:
            return today, today 
from typing import Optional, Dict, Any, List
from ..models.database import db_manager
from datetime import datetime, date, timedelta
import logging

logger = logging.getLogger(__name__)

class TransactionModel:
    """Modelo para gerenciamento de transações"""
    
    def __init__(self):
        self.db = db_manager
    
    def create_transaction(self, user_id: int, category_id: int, amount: float, 
                          transaction_type: str, transaction_date: date, 
                          description: str = None) -> Optional[int]:
        """Cria uma nova transação"""
        try:
            query = """
                INSERT INTO transactions (user_id, category_id, amount, type, date, description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            if self.db.execute_update(query, (user_id, category_id, amount, 
                                             transaction_type, transaction_date, description)):
                transaction_id = self.db.get_last_insert_id()
                logger.info(f"Transação {transaction_id} criada com sucesso")
                return transaction_id
            return None
        except Exception as e:
            logger.error(f"Erro ao criar transação: {e}")
            return None
    
    def get_transaction_by_id(self, transaction_id: int, user_id: int) -> Optional[Dict[str, Any]]:
        """Busca uma transação por ID"""
        try:
            query = """
                SELECT t.*, c.name as category_name, c.color as category_color, c.icon as category_icon
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.id = %s AND t.user_id = %s
            """
            result = self.db.execute_query(query, (transaction_id, user_id))
            return result[0] if result else None
        except Exception as e:
            logger.error(f"Erro ao buscar transação: {e}")
            return None
    
    def get_user_transactions(self, user_id: int, start_date: date = None, 
                            end_date: date = None, transaction_type: str = None,
                            category_id: int = None, limit: int = 100) -> List[Dict[str, Any]]:
        """Busca transações do usuário com filtros"""
        try:
            query = """
                SELECT t.*, c.name as category_name, c.color as category_color, c.icon as category_icon
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.user_id = %s
            """
            params = [user_id]
            
            if start_date:
                query += " AND t.date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND t.date <= %s"
                params.append(end_date)
            
            if transaction_type:
                query += " AND t.type = %s"
                params.append(transaction_type)
            
            if category_id:
                query += " AND t.category_id = %s"
                params.append(category_id)
            
            query += " ORDER BY t.date DESC, t.created_at DESC LIMIT %s"
            params.append(limit)
            
            return self.db.execute_query(query, tuple(params)) or []
        except Exception as e:
            logger.error(f"Erro ao buscar transações: {e}")
            return []
    
    def update_transaction(self, transaction_id: int, user_id: int, category_id: int = None,
                          amount: float = None, transaction_type: str = None,
                          transaction_date: date = None, description: str = None) -> bool:
        """Atualiza uma transação"""
        try:
            updates = []
            params = []
            
            if category_id is not None:
                updates.append("category_id = %s")
                params.append(category_id)
            
            if amount is not None:
                updates.append("amount = %s")
                params.append(amount)
            
            if transaction_type is not None:
                updates.append("type = %s")
                params.append(transaction_type)
            
            if transaction_date is not None:
                updates.append("date = %s")
                params.append(transaction_date)
            
            if description is not None:
                updates.append("description = %s")
                params.append(description)
            
            if not updates:
                return True
            
            params.extend([transaction_id, user_id])
            query = f"UPDATE transactions SET {', '.join(updates)} WHERE id = %s AND user_id = %s"
            
            success = self.db.execute_update(query, tuple(params))
            if success:
                logger.info(f"Transação {transaction_id} atualizada com sucesso")
            
            return success
        except Exception as e:
            logger.error(f"Erro ao atualizar transação: {e}")
            return False
    
    def delete_transaction(self, transaction_id: int, user_id: int) -> bool:
        """Exclui uma transação"""
        try:
            query = "DELETE FROM transactions WHERE id = %s AND user_id = %s"
            success = self.db.execute_update(query, (transaction_id, user_id))
            
            if success:
                logger.info(f"Transação {transaction_id} excluída com sucesso")
            
            return success
        except Exception as e:
            logger.error(f"Erro ao excluir transação: {e}")
            return False
    
    def get_balance(self, user_id: int, end_date: date = None) -> Dict[str, float]:
        """Calcula o saldo do usuário até uma data específica"""
        try:
            query = """
                SELECT 
                    COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) as total_income,
                    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) as total_expense
                FROM transactions 
                WHERE user_id = %s
            """
            params = [user_id]
            
            if end_date:
                query += " AND date <= %s"
                params.append(end_date)
            
            result = self.db.execute_query(query, tuple(params))
            if result:
                data = result[0]
                total_income = float(data['total_income'])
                total_expense = float(data['total_expense'])
                balance = total_income - total_expense
                
                return {
                    'balance': balance,
                    'total_income': total_income,
                    'total_expense': total_expense
                }
            
            return {'balance': 0.0, 'total_income': 0.0, 'total_expense': 0.0}
        except Exception as e:
            logger.error(f"Erro ao calcular saldo: {e}")
            return {'balance': 0.0, 'total_income': 0.0, 'total_expense': 0.0}
    
    def get_monthly_summary(self, user_id: int, year: int, month: int) -> Dict[str, Any]:
        """Obtém resumo mensal das transações"""
        try:
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)
            
            # Resumo geral
            balance_data = self.get_balance(user_id, end_date)
            
            # Transações por categoria
            category_query = """
                SELECT 
                    c.name as category_name,
                    c.color as category_color,
                    c.icon as category_icon,
                    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END), 0) as income,
                    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END), 0) as expense
                FROM categories c
                LEFT JOIN transactions t ON c.id = t.category_id 
                    AND t.user_id = %s 
                    AND t.date BETWEEN %s AND %s
                WHERE c.user_id = %s
                GROUP BY c.id, c.name, c.color, c.icon
                HAVING income > 0 OR expense > 0
                ORDER BY expense DESC, income DESC
            """
            
            category_data = self.db.execute_query(category_query, 
                                                (user_id, start_date, end_date, user_id)) or []
            
            # Transações diárias
            daily_query = """
                SELECT 
                    date,
                    COALESCE(SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END), 0) as daily_income,
                    COALESCE(SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END), 0) as daily_expense
                FROM transactions 
                WHERE user_id = %s AND date BETWEEN %s AND %s
                GROUP BY date
                ORDER BY date
            """
            
            daily_data = self.db.execute_query(daily_query, (user_id, start_date, end_date)) or []
            
            return {
                'period': {
                    'start_date': start_date,
                    'end_date': end_date,
                    'year': year,
                    'month': month
                },
                'balance': balance_data,
                'categories': category_data,
                'daily_data': daily_data
            }
        except Exception as e:
            logger.error(f"Erro ao obter resumo mensal: {e}")
            return {}
    
    def get_category_statistics(self, user_id: int, start_date: date = None, 
                               end_date: date = None) -> List[Dict[str, Any]]:
        """Obtém estatísticas por categoria"""
        try:
            query = """
                SELECT 
                    c.id,
                    c.name,
                    c.color,
                    c.icon,
                    COUNT(t.id) as transaction_count,
                    COALESCE(SUM(CASE WHEN t.type = 'income' THEN t.amount ELSE 0 END), 0) as total_income,
                    COALESCE(SUM(CASE WHEN t.type = 'expense' THEN t.amount ELSE 0 END), 0) as total_expense
                FROM categories c
                LEFT JOIN transactions t ON c.id = t.category_id AND t.user_id = %s
            """
            params = [user_id]
            
            if start_date:
                query += " AND t.date >= %s"
                params.append(start_date)
            
            if end_date:
                query += " AND t.date <= %s"
                params.append(end_date)
            
            query += """
                WHERE c.user_id = %s
                GROUP BY c.id, c.name, c.color, c.icon
                ORDER BY total_expense DESC, total_income DESC
            """
            params.append(user_id)
            
            return self.db.execute_query(query, tuple(params)) or []
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas por categoria: {e}")
            return []
    
    def get_recent_transactions(self, user_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        """Obtém as transações mais recentes"""
        try:
            query = """
                SELECT t.*, c.name as category_name, c.color as category_color, c.icon as category_icon
                FROM transactions t
                LEFT JOIN categories c ON t.category_id = c.id
                WHERE t.user_id = %s
                ORDER BY t.date DESC, t.created_at DESC
                LIMIT %s
            """
            return self.db.execute_query(query, (user_id, limit)) or []
        except Exception as e:
            logger.error(f"Erro ao obter transações recentes: {e}")
            return [] 
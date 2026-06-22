"""
Liquidity KPI calculations and analysis module.

This module provides functions to calculate liquidity metrics including
current ratio, quick ratio, cash flow ratios, and working capital metrics.
"""


def calculate_current_ratio(current_assets, current_liabilities):
    """
    Calculate current ratio (liquidity measure).
    
    Args:
        current_assets: Total current assets
        current_liabilities: Total current liabilities
        
    Returns:
        float: Current ratio
    """
    if current_liabilities == 0:
        return None
    return current_assets / current_liabilities


def calculate_quick_ratio(current_assets, inventory, current_liabilities):
    """
    Calculate quick ratio (acid-test ratio).
    
    Args:
        current_assets: Total current assets
        inventory: Inventory value
        current_liabilities: Total current liabilities
        
    Returns:
        float: Quick ratio
    """
    if current_liabilities == 0:
        return None
    return (current_assets - inventory) / current_liabilities


def calculate_cash_ratio(cash_and_equivalents, current_liabilities):
    """
    Calculate cash ratio.
    
    Args:
        cash_and_equivalents: Cash and cash equivalents
        current_liabilities: Total current liabilities
        
    Returns:
        float: Cash ratio
    """
    if current_liabilities == 0:
        return None
    return cash_and_equivalents / current_liabilities


def calculate_working_capital(current_assets, current_liabilities):
    """
    Calculate working capital.
    
    Args:
        current_assets: Total current assets
        current_liabilities: Total current liabilities
        
    Returns:
        float: Working capital amount
    """
    return current_assets - current_liabilities


def calculate_operating_cash_flow_ratio(operating_cash_flow, current_liabilities):
    """
    Calculate operating cash flow ratio.
    
    Args:
        operating_cash_flow: Operating cash flow
        current_liabilities: Total current liabilities
        
    Returns:
        float: Operating cash flow ratio
    """
    if current_liabilities == 0:
        return None
    return operating_cash_flow / current_liabilities

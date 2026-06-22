"""
Leverage KPI calculations and analysis module.

This module provides functions to calculate leverage and solvency metrics
including debt ratios, equity ratios, and interest coverage ratios.
"""


def calculate_debt_ratio(total_debt, total_assets):
    """
    Calculate debt ratio.
    
    Args:
        total_debt: Total debt
        total_assets: Total assets
        
    Returns:
        float: Debt ratio as percentage
    """
    if total_assets == 0:
        return None
    return (total_debt / total_assets) * 100


def calculate_debt_to_equity_ratio(total_debt, shareholder_equity):
    """
    Calculate debt-to-equity ratio.
    
    Args:
        total_debt: Total debt
        shareholder_equity: Total shareholder equity
        
    Returns:
        float: Debt-to-equity ratio
    """
    if shareholder_equity == 0:
        return None
    return total_debt / shareholder_equity


def calculate_equity_ratio(shareholder_equity, total_assets):
    """
    Calculate equity ratio.
    
    Args:
        shareholder_equity: Total shareholder equity
        total_assets: Total assets
        
    Returns:
        float: Equity ratio as percentage
    """
    if total_assets == 0:
        return None
    return (shareholder_equity / total_assets) * 100


def calculate_interest_coverage_ratio(ebit, interest_expense):
    """
    Calculate interest coverage ratio.
    
    Args:
        ebit: Earnings before interest and taxes
        interest_expense: Interest expense
        
    Returns:
        float: Interest coverage ratio
    """
    if interest_expense == 0:
        return None
    return ebit / interest_expense


def calculate_debt_service_ratio(net_operating_income, total_debt_service):
    """
    Calculate debt service ratio.
    
    Args:
        net_operating_income: Net operating income
        total_debt_service: Total debt service (principal + interest)
        
    Returns:
        float: Debt service ratio
    """
    if total_debt_service == 0:
        return None
    return net_operating_income / total_debt_service

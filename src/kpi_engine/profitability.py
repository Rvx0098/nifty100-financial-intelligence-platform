"""
Profitability KPI calculations and analysis module.

This module provides functions to calculate profitability metrics including
margins, ROE, ROA, and other profitability indicators.
"""


def calculate_gross_margin(revenue, cost_of_goods_sold):
    """
    Calculate gross profit margin.
    
    Args:
        revenue: Total revenue
        cost_of_goods_sold: Cost of goods sold
        
    Returns:
        float: Gross margin as percentage
    """
    if revenue == 0:
        return None
    return ((revenue - cost_of_goods_sold) / revenue) * 100


def calculate_operating_margin(operating_income, revenue):
    """
    Calculate operating profit margin.
    
    Args:
        operating_income: Operating income
        revenue: Total revenue
        
    Returns:
        float: Operating margin as percentage
    """
    if revenue == 0:
        return None
    return (operating_income / revenue) * 100


def calculate_net_margin(net_income, revenue):
    """
    Calculate net profit margin.
    
    Args:
        net_income: Net income
        revenue: Total revenue
        
    Returns:
        float: Net margin as percentage
    """
    if revenue == 0:
        return None
    return (net_income / revenue) * 100


def calculate_roe(net_income, shareholder_equity):
    """
    Calculate Return on Equity (ROE).
    
    Args:
        net_income: Net income
        shareholder_equity: Total shareholder equity
        
    Returns:
        float: ROE as percentage
    """
    if shareholder_equity == 0:
        return None
    return (net_income / shareholder_equity) * 100


def calculate_roa(net_income, total_assets):
    """
    Calculate Return on Assets (ROA).
    
    Args:
        net_income: Net income
        total_assets: Total assets
        
    Returns:
        float: ROA as percentage
    """
    if total_assets == 0:
        return None
    return (net_income / total_assets) * 100

# Architecture

## Folder Structure
- src/analytics for peer scoring
- src/screener for presets and scoring
- src/visualization for workbook exports

## Data Flow
- Load financial ratios and metadata from SQLite
- Score and filter companies by preset
- Write Excel and markdown artifacts

## SQLite
- financial_ratios, companies, peer_groups, and peer_percentiles

## Analytics
- Composite scoring, percentile ranking, and preset filters

## Visualization
- Excel workbooks and radar charts

## Exports
- Screener workbook and peer comparison workbook

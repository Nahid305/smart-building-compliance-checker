# Copilot Instructions for Smart Building Code Compliance Checker

<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

## Project Overview
This is a Smart Building Code Compliance Checker for Structural Design - a full-stack web application that checks structural designs against building codes like IS 456:2000, IS 875, ACI, and Eurocode.

## Technology Stack
- **Backend**: Python Flask with structural engineering calculations
- **Frontend**: React with modern UI components
- **Database**: JSON/SQLite for code rules and material properties
- **PDF Generation**: ReportLab for compliance reports
- **Testing**: Unit tests for calculation accuracy

## Key Guidelines
1. **Structural Engineering Focus**: All calculations must follow established building codes (IS 456:2000, IS 875)
2. **Safety First**: Always err on the side of conservative design recommendations
3. **Code Compliance**: Implement precise formula checking for beams, columns, slabs, and footings
4. **User Experience**: Provide clear pass/fail reports with actionable recommendations
5. **Accuracy**: Ensure all structural calculations are mathematically correct and code-compliant

## Code Standards
- Use type hints in Python for calculation functions
- Include comprehensive docstrings for all engineering formulas
- Implement proper error handling for edge cases in structural design
- Follow REST API conventions for backend endpoints
- Use React best practices for component organization

## Testing Requirements
- Unit tests for all calculation functions with known test cases
- Integration tests for API endpoints
- Validation against published design examples from IS codes

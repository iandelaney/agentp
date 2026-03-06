# calculator/pkg/render.py

def format_output(expression: str, result: float) -> str:
    if isinstance(result, float) and result.is_integer():
        result_to_display = int(result)
    else:
        result_to_display = result

    return f"""
┌───────────────────────────────────────────┐
│ Expression: {expression:<28} │
│ Result:     {str(result_to_display):<28} │
└───────────────────────────────────────────┘
"""
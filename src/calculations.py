from src.config import (
    TAX_BRACKETS,
    TAX_CREDIT_POINT_VALUE,
    BITUACH_LEUMI_LOW_RATE,
    BITUACH_LEUMI_HIGH_RATE,
    BITUACH_LEUMI_LOW_CEILING,
    BITUACH_LEUMI_HIGH_CEILING,
)


def calc_income_tax(gross: float, credit_points: float = 2.25) -> float:
    tax = 0.0
    prev_ceiling = 0.0
    for ceiling, rate in TAX_BRACKETS:
        if gross <= prev_ceiling:
            break
        taxable = min(gross, ceiling) - prev_ceiling
        tax += taxable * rate
        prev_ceiling = ceiling
    credit = credit_points * TAX_CREDIT_POINT_VALUE
    return max(0.0, tax - credit)


def calc_bituach_leumi(gross: float) -> float:
    if gross <= 0:
        return 0.0
    capped = min(gross, BITUACH_LEUMI_HIGH_CEILING)
    if capped <= BITUACH_LEUMI_LOW_CEILING:
        return capped * BITUACH_LEUMI_LOW_RATE
    low_part = BITUACH_LEUMI_LOW_CEILING * BITUACH_LEUMI_LOW_RATE
    high_part = (capped - BITUACH_LEUMI_LOW_CEILING) * BITUACH_LEUMI_HIGH_RATE
    return low_part + high_part


def calc_salary(
    hours: float,
    work_days: int,
    hourly_rate: float,
    credit_points: float = 2.25,
    pension_employee_pct: float = 0.06,
    pension_employer_pct: float = 0.065,
    training_fund_employee_pct: float = 0.025,
    training_fund_employer_pct: float = 0.075,
    health_insurance: float = 0.0,
    travel_per_day: float = 0.0,
    meals_per_day: float = 0.0,
) -> dict:
    gross = hours * hourly_rate
    travel = travel_per_day * work_days
    meals = meals_per_day * work_days

    income_tax = calc_income_tax(gross, credit_points)
    bituach_leumi = calc_bituach_leumi(gross)
    pension_employee = gross * pension_employee_pct
    training_fund_employee = gross * training_fund_employee_pct

    total_deductions = (
        income_tax
        + bituach_leumi
        + pension_employee
        + training_fund_employee
        + health_insurance
    )
    total_additions = travel + meals
    net = gross - total_deductions + total_additions

    pension_employer = gross * pension_employer_pct
    training_fund_employer = gross * training_fund_employer_pct
    employer_cost = gross + pension_employer + training_fund_employer

    return {
        "hours": hours,
        "work_days": work_days,
        "gross": gross,
        "income_tax": income_tax,
        "bituach_leumi": bituach_leumi,
        "pension_employee": pension_employee,
        "training_fund_employee": training_fund_employee,
        "health_insurance": health_insurance,
        "travel": travel,
        "meals": meals,
        "total_deductions": total_deductions,
        "total_additions": total_additions,
        "net": net,
        "pension_employer": pension_employer,
        "training_fund_employer": training_fund_employer,
        "employer_cost": employer_cost,
    }

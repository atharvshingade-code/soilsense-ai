def analyze_soil(n, p, k, ph):
    findings = []
    remediation = []
    environmental_impacts = []

    # Soil pH evaluation
    if ph < 5.5:
        findings.append(
            "The soil is strongly acidic."
        )
        remediation.append(
            "Assess lime requirements using a suitable "
            "soil test before applying amendments."
        )
        environmental_impacts.append(
            "Strong acidity can affect nutrient availability "
            "and the suitability of soil for sensitive crops."
        )

    elif ph < 6.5:
        findings.append(
            "The soil is moderately to slightly acidic."
        )
        remediation.append(
            "Check the preferred pH range of the intended crop "
            "and consult local soil-management guidance."
        )

    elif ph <= 7.5:
        findings.append(
            "The soil is near neutral."
        )
        remediation.append(
            "Maintain appropriate organic matter and use "
            "crop-specific nutrient management."
        )

    elif ph <= 8.5:
        findings.append(
            "The soil is alkaline."
        )
        remediation.append(
            "Investigate the cause of alkalinity and obtain "
            "appropriate soil testing before selecting amendments."
        )
        environmental_impacts.append(
            "Alkaline conditions can reduce the availability "
            "of certain nutrients to some crops."
        )

    else:
        findings.append(
            "The soil is highly alkaline."
        )
        remediation.append(
            "Arrange a detailed soil assessment before choosing "
            "a corrective treatment."
        )
        environmental_impacts.append(
            "High alkalinity may restrict the growth of "
            "sensitive crops."
        )

    # NPK observations
    findings.append(
        f"Recorded nitrogen value: {n}."
    )
    findings.append(
        f"Recorded phosphorus value: {p}."
    )
    findings.append(
        f"Recorded potassium value: {k}."
    )

    remediation.append(
        "Compare NPK measurements against validated "
        "soil-test reference ranges for the region and crop."
    )

    remediation.append(
        "Avoid excessive fertilizer application and follow "
        "crop-specific nutrient recommendations."
    )

    environmental_impacts.append(
        "Excess fertilizer use can contribute to nutrient "
        "runoff and water pollution."
    )

    environmental_impacts.append(
        "Consider organic matter management to support "
        "soil structure and water retention."
    )

    return {
        "findings": findings,
        "remediation": remediation,
        "environmental_impacts": environmental_impacts
    }
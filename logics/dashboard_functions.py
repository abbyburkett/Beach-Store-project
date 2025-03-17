def getPayData(employeeID, columns):
    # Placeholder data: (PayAmount, BonusPercentage, GrossBonus, GrossPaid)

    data = [
        (100, 10, 1000, 1100),
        (200, 20, 2000, 1200),
        (300, 30, 3000, 1300),
        (400, 40, 4000, 1400),
    ]


    return data

def getCloseOutData(ProfitID, columns, target_date):

    data = [(102, 300.50, 400.75, 80.00, 20.25, 100.25, "2025-03-16")]
    

    return data

def getUserProfileData(employeeID):

    user_data = [
        (101, "John", "Doe", "******", "johndoe", "Employee")
    ]

    return user_data